#!/usr/bin/env python3
"""Create and validate Super Survey directories and round templates."""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import json
import re
import sys
from pathlib import Path

LANGUAGES = ("en", "zh", "ja")
MODES = ("quick", "standard", "deep")
REPORT_SCHEMA_VERSION = 2
MIN_REPORT_SUBSTANTIVE_LINES = 20
REPORT_PASS_SCORE = 90
REPORT_CONDITIONAL_SCORE = 80
REGISTRY_FILES = ("sources.jsonl", "claims.jsonl", "evidence.jsonl")

MODE_CONFIG = {
    "quick": {
        "min_sources": 1,
        "min_claims": 1,
        "min_evidence": 1,
        "min_report_lines": 12,
        "pass_score": 80,
        "target_report_length": "800-1,500 words",
        "quality_gate": "quick directional memo; continue if the decision still turns on public facts",
    },
    "standard": {
        "min_sources": 3,
        "min_claims": 3,
        "min_evidence": 3,
        "min_report_lines": 20,
        "pass_score": 90,
        "target_report_length": "1,500-3,500 words",
        "quality_gate": "standard standalone report; continue while desk-researchable unknowns remain",
    },
    "deep": {
        "min_sources": 8,
        "min_claims": 6,
        "min_evidence": 8,
        "min_report_lines": 35,
        "pass_score": 95,
        "target_report_length": "3,500+ words, or route long-form packaging to deep-research",
        "quality_gate": "deep report; use strict source triangulation and companion routing when useful",
    },
}

LABELS = {
    "en": {
        "brief_title": "Survey Brief",
        "index_title": "Survey Index",
        "round": "Round",
        "research": "Research",
        "brainstorm": "Brainstorming Checkpoint",
        "redteam": "Red-Team Challenge",
        "synthesis": "Synthesis",
        "evolver": "Lightweight Evolver",
        "empty": "- ",
        "confidence": "Low / Medium / High",
        "decision": "Keep / Narrow / Pivot / Kill",
        "strength": "strong / weak / unknown",
        "verdict": "support / concern / reject",
        "brief_headings": [
            "User Question",
            "Superpowers Brainstorming Gate",
            "Decision To Make",
            "Research Lens",
            "Decision Evidence Standard",
            "Decision Frame Integrity",
            "Target Customer",
            "Success Criteria",
            "Disqualifying Conditions",
            "Initial Assumptions",
            "Continuation Policy",
        ],
        "index_headings": [
            "Current Thesis",
            "Current Evidence-Bound Conclusion",
            "Round Ledger",
            "Continuation Status",
            "Next Research Target",
            "Why Not Final Yet",
            "Open Questions",
            "Source Inventory",
            "Wiki / Graph Index Status",
            "Decision Log",
        ],
        "wiki_status_notes": [
            "Wiki Tool Attempted: karpathy-llm-wiki / llm-wiki / pin-llm-wiki / other / none",
            "Wiki Ingest Result: ingested / initialized then ingested / failed / not built",
            "Wiki Fallback Reason: none / unavailable / not initialized / command failed / user skipped",
            "Wiki Artifact Path: path to wiki page, raw file, log entry, or index.md-only fallback",
        ],
        "report_headings": [
            "Executive Summary",
            "Reader's Path",
            "Main Narrative",
            "Decision Logic",
            "Final Recommendation",
            "What Could Change This Conclusion",
            "Next Actions",
            "Limits Of This Report",
            "Appendix: Evidence Register",
            "Appendix: Method And Source Quality",
            "Appendix: Red-Team Notes",
            "Appendix: Options Or Scenarios",
            "Report Quality Score",
            "Appendix: Source Notes",
        ],
        "legacy_report_headings": [
            "Executive Summary",
            "Key Findings",
            "Comparison Or Analysis",
            "Recommendation",
            "Limitations",
            "Source Notes",
        ],
        "report_quality_heading": "Report Quality Score",
        "appendix_start_heading": "Appendix: Evidence Register",
        "research_headings": [
            "Research Question",
            "Source List",
            "Evidence Table",
            "Findings",
            "Data Quality Notes",
        ],
        "brainstorm_headings": [
            "Brainstorming Status",
            "Current Framing",
            "Clarifying Questions",
            "Alternative Next Moves",
            "Chosen Direction",
            "Design Notes For Next Round",
        ],
        "redteam_headings": [
            "Strongest Objections",
            "Incumbent Response",
            "Alternative Explanations Or Substitutes",
            "Data And Access Risks",
            "Legal, ToS, Privacy, Or Compliance Risks",
            "Monetization And Distribution Risks",
            "Kill Criteria Checked",
            "Falsification Tests",
        ],
        "synthesis_headings": [
            "Updated Conclusion",
            "Confidence",
            "Decision Rationale",
            "What Changed",
            "Remaining Unknowns",
            "Evolved Next Research Target",
            "Recommended Next Action",
        ],
        "evolver_headings": [
            "Current Thesis",
            "Probe Results",
            "Persona Judgments",
            "Decision",
            "Round Evidence Quality Gate",
            "Next Research Target",
            "Evidence Needed Next",
        ],
        "source_cols": "Source | URL | Date Checked | Notes",
        "evidence_cols": "Claim | Evidence | Source | Source Type | Freshness | Confidence | Contradictions",
        "probe_cols": "Probe | Answer | Strength",
        "persona_cols": "Persona | Verdict | Reason",
        "search_tool_notes": [
            "Search Tool Used: tavily-search / fallback web search / other",
            "Tavily Fallback Reason: none / not installed / not authenticated / failed / insufficient results / unsuitable source surface",
            "Query And Filter Notes: queries, domains, date filters, source-type filters",
        ],
        "decision_frame_note": (
            "- Original question preserved:\n"
            "- Decision frame supported:\n"
            "- Stronger claim not assumed:\n"
            "- Allowed narrowing:"
        ),
        "continuation_policy_note": "- Start with the next research round; decide whether to continue only after evidence, red-team critique, synthesis, and the raw evolver decision are written.\n- Do not predict the number of rounds or prewrite a stop conclusion in the brief.\n- Record actual round history and next targets in index.md, not here.",
        "report_template_notes": [
            "After the final gate passes, answer first: decision, confidence, key reason, strongest caveat, next action",
            "Tell the reader how to read the report: who it is for, what decision it supports, and what to skip if time is short",
            "Readable narrative that explains the situation, why it matters, how the evidence changes the thesis, and what judgment follows",
            "Reasoning chain from question to recommendation, including tradeoffs and why alternatives were rejected",
            "Final recommendation with conditions, who should act, who should not act, and confidence",
            "Concrete evidence or events that would upgrade, downgrade, pivot, or kill the conclusion",
            "Concrete next actions, monitoring metrics, owners/timeframes where useful, and stop/continue triggers",
            "Limits, uncertainty, missing data, freshness caveats, and external validation needs",
            "Appendix only: claim-level evidence with confidence, contradictions, source freshness, and source names",
            "Appendix only: search tools used, source freshness, source types, confidence rules, and fallback notes",
            "Appendix only: strongest objections, substitutes, kill criteria, and falsification tests",
            "Appendix only: options, scenarios, or alternatives with pros, cons, and trigger conditions",
            "Total Score, Score Breakdown, pass/continue decision, lowest-scoring areas, and next-round focus",
            "Appendix only: source inventory with URLs, dates checked, and companion/indexing notes",
        ],
        "probes": [
            "Buyer",
            "Pain",
            "Trigger",
            "Data",
            "Distribution",
            "Incumbent",
            "Compliance",
            "Alternative",
            "Falsifier",
        ],
        "personas": [
            "Skeptical buyer",
            "Incumbent strategist",
            "Distribution realist",
            "Compliance reviewer",
            "Builder/operator",
        ],
    },
    "zh": {
        "brief_title": "调研简报",
        "index_title": "调研索引",
        "round": "第",
        "research": "轮调研",
        "brainstorm": "轮 Brainstorming 检查点",
        "redteam": "轮反方挑战",
        "synthesis": "轮综合结论",
        "evolver": "轮轻量进化器",
        "empty": "- ",
        "confidence": "低 / 中 / 高",
        "decision": "保留 / 收窄 / 转向 / 放弃",
        "strength": "强 / 弱 / 未知",
        "verdict": "支持 / 担忧 / 反对",
        "brief_headings": [
            "用户问题",
            "Superpowers Brainstorming 门",
            "需要做出的决策",
            "研究镜头",
            "决策证据标准",
            "决策框架完整性",
            "目标客户",
            "成功标准",
            "放弃条件",
            "初始假设",
            "继续策略",
        ],
        "index_headings": [
            "当前论点",
            "当前证据约束结论",
            "轮次台账",
            "继续状态",
            "下一轮调研目标",
            "为何尚未最终成稿",
            "开放问题",
            "来源清单",
            "Wiki / Graph 索引状态",
            "决策日志",
        ],
        "wiki_status_notes": [
            "Wiki Tool Attempted: karpathy-llm-wiki / llm-wiki / pin-llm-wiki / other / none",
            "Wiki Ingest Result: ingested / initialized then ingested / failed / not built",
            "Wiki Fallback Reason: none / unavailable / not initialized / command failed / user skipped",
            "Wiki Artifact Path: wiki 页面、raw 文件、log 记录路径，或 index.md-only fallback",
        ],
        "report_headings": [
            "执行摘要",
            "阅读路径",
            "正文叙事",
            "决策逻辑",
            "最终建议",
            "什么会改变结论",
            "下一步行动",
            "本报告边界",
            "附录：证据登记表",
            "附录：方法与来源质量",
            "附录：反方挑战记录",
            "附录：选项或情景",
            "报告质量评分",
            "附录：来源备注",
        ],
        "legacy_report_headings": [
            "执行摘要",
            "关键发现",
            "对比或分析",
            "建议",
            "局限性",
            "来源备注",
        ],
        "report_quality_heading": "报告质量评分",
        "appendix_start_heading": "附录：证据登记表",
        "research_headings": [
            "本轮问题",
            "来源列表",
            "证据表",
            "发现",
            "数据质量备注",
        ],
        "brainstorm_headings": [
            "Brainstorming 状态",
            "当前问题框定",
            "澄清问题",
            "可选下一步",
            "选定方向",
            "下一轮设计备注",
        ],
        "redteam_headings": [
            "最强反对意见",
            "头部竞品反应",
            "替代解释或替代方案",
            "数据与访问风险",
            "法律、平台条款、隐私或合规风险",
            "变现与分发风险",
            "已检查的放弃条件",
            "证伪测试",
        ],
        "synthesis_headings": [
            "更新后的结论",
            "置信度",
            "决策依据",
            "本轮变化",
            "剩余未知",
            "进化后的下一轮目标",
            "建议的下一步",
        ],
        "evolver_headings": [
            "当前论点",
            "探针结果",
            "角色判断",
            "决策",
            "轮次证据质量门",
            "下一轮调研目标",
            "下一轮所需证据",
        ],
        "source_cols": "来源 | URL | 检查日期 | 备注",
        "evidence_cols": "主张 | 证据 | 来源 | 来源类型 | 新鲜度 | 置信度 | 矛盾证据",
        "probe_cols": "探针 | 回答 | 强度",
        "persona_cols": "角色 | 判断 | 理由",
        "search_tool_notes": [
            "使用的搜索工具：tavily-search / fallback web search / other",
            "Tavily fallback 原因：无 / 未安装 / 未认证 / 失败 / 结果不足 / 不适合所需来源",
            "查询与过滤备注：查询词、域名、日期过滤、来源类型过滤",
        ],
        "decision_frame_note": (
            "- 原始问题已保留：\n"
            "- 支持的决策框架：\n"
            "- 未预设更强命题：\n"
            "- 允许收窄的依据："
        ),
        "continuation_policy_note": "- 从下一轮调研开始；只有在证据、反方挑战、综合结论和原始进化器决策写入后，才能决定是否继续。\n- 不要在 brief 中预测轮数，也不要预写停止结论。\n- 实际轮次历史和下一轮目标记录在 index.md，而不是这里。",
        "report_template_notes": [
            "最终门通过后，先给答案：决策、置信度、核心理由、最大保留意见和下一步",
            "告诉读者如何阅读：适合谁、支持什么决策、时间有限先看哪里",
            "用连贯正文解释背景、为什么重要、证据如何改变判断、最终判断为何成立",
            "从问题到建议的推理链，包括取舍和为什么排除其他选择",
            "最终建议、适合行动的人、不适合行动的人、条件和置信度",
            "哪些证据或事件会让结论升级、降级、转向或放弃",
            "具体下一步、监控指标、责任/时间框架（如适用）和停止/继续触发条件",
            "本报告的边界、未知、缺失数据、时效性和外部验证需求",
            "仅作附录：claim-level 证据，包含置信度、矛盾证据、来源新鲜度和来源名",
            "仅作附录：使用的搜索工具、来源新鲜度、来源类型、置信规则和 fallback 记录",
            "仅作附录：最强反对意见、替代方案、放弃条件和证伪测试",
            "仅作附录：选项、情景或替代路径，并写明优缺点和触发条件",
            "总分、分项得分、通过/继续决策、最低分维度和下一轮重点",
            "仅作附录：来源清单、URL、检查日期和 companion/indexing 备注",
        ],
        "probes": ["买方", "痛点", "触发事件", "数据", "分发", "既有玩家", "合规", "替代解释", "证伪条件"],
        "personas": ["怀疑的买方", "头部竞品策略负责人", "分发现实主义者", "合规审查者", "构建/运营负责人"],
    },
    "ja": {
        "brief_title": "調査ブリーフ",
        "index_title": "調査インデックス",
        "round": "第",
        "research": "回調査",
        "brainstorm": "回 Brainstorming チェックポイント",
        "redteam": "回レッドチーム",
        "synthesis": "回統合結論",
        "evolver": "回軽量エボルバー",
        "empty": "- ",
        "confidence": "低 / 中 / 高",
        "decision": "維持 / 絞り込み / ピボット / 中止",
        "strength": "強い / 弱い / 不明",
        "verdict": "支持 / 懸念 / 反対",
        "brief_headings": [
            "ユーザーの問い",
            "Superpowers Brainstorming ゲート",
            "判断すべきこと",
            "調査レンズ",
            "判断に必要な証拠基準",
            "判断枠の整合性",
            "対象顧客",
            "成功基準",
            "中止条件",
            "初期仮説",
            "継続ポリシー",
        ],
        "index_headings": [
            "現在の仮説",
            "現在の証拠制約付き結論",
            "ラウンド台帳",
            "継続状態",
            "次回調査目標",
            "まだ最終化しない理由",
            "未解決の問い",
            "情報源一覧",
            "Wiki / Graph インデックス状態",
            "意思決定ログ",
        ],
        "wiki_status_notes": [
            "Wiki Tool Attempted: karpathy-llm-wiki / llm-wiki / pin-llm-wiki / other / none",
            "Wiki Ingest Result: ingested / initialized then ingested / failed / not built",
            "Wiki Fallback Reason: none / unavailable / not initialized / command failed / user skipped",
            "Wiki Artifact Path: wiki ページ、raw ファイル、log エントリ、または index.md-only fallback",
        ],
        "report_headings": [
            "エグゼクティブサマリー",
            "読み方",
            "本文",
            "判断ロジック",
            "最終推奨",
            "結論を変える条件",
            "次の行動",
            "本レポートの範囲",
            "付録: 証拠レジスター",
            "付録: 方法と情報源品質",
            "付録: レッドチームメモ",
            "付録: 選択肢またはシナリオ",
            "レポート品質スコア",
            "付録: 情報源メモ",
        ],
        "legacy_report_headings": [
            "エグゼクティブサマリー",
            "主要な発見",
            "比較または分析",
            "推奨事項",
            "制約",
            "情報源メモ",
        ],
        "report_quality_heading": "レポート品質スコア",
        "appendix_start_heading": "付録: 証拠レジスター",
        "research_headings": [
            "今回の調査問い",
            "情報源リスト",
            "証拠テーブル",
            "発見",
            "データ品質メモ",
        ],
        "brainstorm_headings": [
            "Brainstorming 状態",
            "現在の問いの定義",
            "確認すべき問い",
            "次の選択肢",
            "選んだ方向",
            "次回ラウンドの設計メモ",
        ],
        "redteam_headings": [
            "最も強い反論",
            "既存大手の反応",
            "代替説明または代替手段",
            "データとアクセスのリスク",
            "法律、規約、プライバシー、コンプライアンスのリスク",
            "収益化と流通のリスク",
            "確認済みの中止条件",
            "反証テスト",
        ],
        "synthesis_headings": [
            "更新された結論",
            "信頼度",
            "判断根拠",
            "今回変わったこと",
            "残る不明点",
            "進化した次回調査目標",
            "推奨される次の行動",
        ],
        "evolver_headings": [
            "現在の仮説",
            "プローブ結果",
            "ペルソナ判断",
            "判断",
            "ラウンド証拠品質ゲート",
            "次回調査目標",
            "次に必要な証拠",
        ],
        "source_cols": "情報源 | URL | 確認日 | メモ",
        "evidence_cols": "主張 | 証拠 | 情報源 | 情報源タイプ | 鮮度 | 信頼度 | 矛盾する証拠",
        "probe_cols": "プローブ | 回答 | 強度",
        "persona_cols": "ペルソナ | 判断 | 理由",
        "search_tool_notes": [
            "使用した検索ツール: tavily-search / fallback web search / other",
            "Tavily fallback 理由: なし / 未インストール / 未認証 / 失敗 / 結果不足 / 必要な情報源に不向き",
            "クエリとフィルタのメモ: クエリ、ドメイン、日付フィルタ、情報源タイプ",
        ],
        "decision_frame_note": (
            "- 元の問いを保持:\n"
            "- 支援する判断枠:\n"
            "- より強い主張を仮定しない:\n"
            "- 絞り込みを許す根拠:"
        ),
        "continuation_policy_note": "- 次の調査ラウンドから始める。証拠、レッドチーム、統合結論、生のエボルバー判断を書いた後にだけ継続可否を決める。\n- brief でラウンド数を予測したり、停止結論を先に書いたりしない。\n- 実際のラウンド履歴と次回目標はここではなく index.md に記録する。",
        "report_template_notes": [
            "最終ゲート通過後に結論を先に示す: 判断、信頼度、主要理由、最大の留保、次の行動",
            "読者向けの読み方: 対象読者、支援する判断、時間がない場合に読む箇所",
            "背景、重要性、証拠が仮説をどう変えたか、判断がなぜ成立するかを読みやすく説明する",
            "問いから推奨までの推論、トレードオフ、却下した代替案の理由",
            "最終推奨、行動すべき人/すべきでない人、条件、信頼度",
            "結論を上方修正、下方修正、ピボット、または中止させる証拠や事象",
            "具体的な次の行動、監視指標、担当/時期が有用な場合の記載、停止/継続トリガー",
            "本レポートの範囲、未知、欠落データ、鮮度、外部検証の必要性",
            "付録のみ: claim-level 証拠、信頼度、矛盾する証拠、鮮度、情報源名",
            "付録のみ: 使用した検索ツール、情報源の鮮度、情報源タイプ、信頼度基準、fallback 記録",
            "付録のみ: 最も強い反論、代替手段、中止条件、反証テスト",
            "付録のみ: 選択肢、シナリオ、代替案と、それぞれの長所、短所、発動条件",
            "総合スコア、内訳、合格/継続判断、最低スコア領域、次回ラウンドの焦点",
            "付録のみ: 情報源一覧、URL、確認日、companion/indexing メモ",
        ],
        "probes": [
            "買い手",
            "痛み",
            "きっかけ",
            "データ",
            "流通",
            "既存企業",
            "コンプライアンス",
            "代替説明",
            "反証条件",
        ],
        "personas": ["懐疑的な買い手", "既存大手の戦略担当", "流通の現実主義者", "コンプライアンス審査者", "構築/運用担当"],
    },
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "survey"


def labels(language: str) -> dict[str, object]:
    if language not in LANGUAGES:
        raise SystemExit(f"Unsupported language: {language}. Use one of: {', '.join(LANGUAGES)}")
    return LABELS[language]


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("round must be a positive integer")
    return number


def metadata_path(survey_dir: Path) -> Path:
    return survey_dir / ".super-survey.json"


def write_metadata(survey_dir: Path, topic: str, language: str) -> None:
    path = metadata_path(survey_dir)
    if path.exists():
        return
    path.write_text(
        json.dumps(
            {"topic": topic, "language": language, "mode": "standard", "report_schema_version": REPORT_SCHEMA_VERSION},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def read_metadata(survey_dir: Path) -> dict[str, object]:
    path = metadata_path(survey_dir)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if isinstance(data, dict):
        return data
    return {}


def metadata_warnings(survey_dir: Path) -> list[str]:
    path = metadata_path(survey_dir)
    if not path.exists():
        return ["metadata warning: .super-survey.json is missing; assuming current schema for validation"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"metadata warning: .super-survey.json could not be parsed ({exc.msg}); assuming current schema for validation"]
    if not isinstance(data, dict):
        return ["metadata warning: .super-survey.json must contain a JSON object; assuming current schema for validation"]
    if "report_schema_version" not in data:
        return ["metadata warning: .super-survey.json has no report_schema_version; assuming current schema for validation"]
    return []


def update_metadata(survey_dir: Path, **updates: object) -> None:
    data = read_metadata(survey_dir)
    data.update(updates)
    path = metadata_path(survey_dir)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_mode(survey_dir: Path, override: str | None = None) -> str:
    if override:
        return override
    data = read_metadata(survey_dir)
    mode = data.get("mode")
    if mode in MODES:
        return str(mode)
    return "standard"


def read_language(survey_dir: Path, override: str | None = None) -> str:
    if override:
        return override
    data = read_metadata(survey_dir)
    language = data.get("language")
    if language in LANGUAGES:
        return str(language)
    return "en"


def report_schema_version(survey_dir: Path) -> int:
    path = metadata_path(survey_dir)
    if not path.exists():
        return REPORT_SCHEMA_VERSION
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return REPORT_SCHEMA_VERSION
    if not isinstance(data, dict):
        return REPORT_SCHEMA_VERSION
    value = data.get("report_schema_version")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return REPORT_SCHEMA_VERSION


def table(cols: str) -> str:
    count = len([col for col in cols.split("|") if col.strip()])
    return f"| {cols} |\n|{'---|' * count}"


def write_once(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"^## {re.escape(heading)}\s*$", text, flags=re.MULTILINE) is not None


def placeholder_values(language: str) -> set[str]:
    label = labels(language)
    return {
        "",
        "-",
        label["empty"].strip(),
        str(label["confidence"]),
        str(label["decision"]),
        str(label["strength"]),
        str(label["verdict"]),
    }


@functools.lru_cache(maxsize=None)
def structural_values(language: str) -> frozenset[str]:
    label = labels(language)
    values: set[str] = set()
    for key in ("source_cols", "evidence_cols", "probe_cols", "persona_cols"):
        values.update(col.strip() for col in str(label[key]).split("|"))
    values.update(str(probe) for probe in label["probes"])
    values.update(str(persona) for persona in label["personas"])
    values.update(str(note) for note in label["search_tool_notes"])
    values.update(str(note) for note in str(label["decision_frame_note"]).splitlines())
    values.update(str(note) for note in str(label["continuation_policy_note"]).splitlines())
    values.update(str(note) for note in label["report_template_notes"])
    return frozenset(values)


def is_substantive_line(line: str, language: str) -> bool:
    stripped = line.strip()
    placeholders = placeholder_values(language)
    if not stripped or stripped.startswith("#") or stripped in placeholders:
        return False
    if stripped in structural_values(language):
        return False
    if stripped.startswith("- ") and stripped[2:].strip() in structural_values(language):
        return False
    if re.fullmatch(r"-\s*(Status|Notes|Option [A-Z]|Round \d+):\s*", stripped):
        return False
    if re.fullmatch(
        r"-\s*(Mode|Minimum Sources|Minimum Claims|Minimum Evidence Items|Target Report Length|Quality Gate|Registry):.*",
        stripped,
    ):
        return False
    if stripped.startswith("|") and stripped.endswith("|"):
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and all(re.fullmatch(r"-+", cell) for cell in cells):
            return False
        ignored = placeholders | structural_values(language)
        return any(cell not in ignored for cell in cells)
    return True


def file_has_substance(path: Path, language: str) -> bool:
    text = path.read_text(encoding="utf-8")
    return sum(1 for line in text.splitlines() if is_substantive_line(line, language)) > 1


def substantive_line_count(path: Path, language: str) -> int:
    text = path.read_text(encoding="utf-8")
    return sum(1 for line in text.splitlines() if is_substantive_line(line, language))


def section_body(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    return match.group("body")


def required_report_headings(label: dict[str, object], schema_version: int) -> list[str]:
    if schema_version >= REPORT_SCHEMA_VERSION:
        return list(label["report_headings"])
    return list(label["legacy_report_headings"])


def required_evolver_headings(label: dict[str, object], schema_version: int) -> list[str]:
    headings = list(label["evolver_headings"])
    if schema_version >= REPORT_SCHEMA_VERSION:
        return headings
    quality_heading = {
        "en": "Round Evidence Quality Gate",
        "zh": "轮次证据质量门",
        "ja": "ラウンド証拠品質ゲート",
    }
    return [heading for heading in headings if heading not in quality_heading.values()]


def has_any_heading(text: str, heading: str) -> bool:
    return has_heading(text, heading)


def report_has_v2_headings(path: Path, label: dict[str, object]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return all(has_any_heading(text, heading) for heading in label["report_headings"])


def parse_report_score(text: str, heading: str) -> int | None:
    body = section_body(text, heading)
    if body is None:
        return None
    patterns = (
        r"Total Score\s*[:：]\s*(\d{1,3})\s*/\s*100",
        r"总分\s*[:：]\s*(\d{1,3})\s*/\s*100",
        r"総合スコア\s*[:：]\s*(\d{1,3})\s*/\s*100",
        r"Score\s*[:：]\s*(\d{1,3})\s*/\s*100",
    )
    for pattern in patterns:
        match = re.search(pattern, body, flags=re.IGNORECASE)
        if match:
            score = int(match.group(1))
            if 0 <= score <= 100:
                return score
    return None


def validate_report_quality(
    errors: list[str],
    warnings: list[str],
    report_path: Path,
    label: dict[str, object],
    language: str,
    schema_version: int,
    mode: str,
) -> None:
    if not report_path.exists():
        return

    if schema_version < REPORT_SCHEMA_VERSION:
        if not report_has_v2_headings(report_path, label):
            errors.append("report.md: legacy report schema detected; run 'upgrade-report' and expand the new sections before final delivery")
            return

    mode_config = MODE_CONFIG[mode]
    min_lines = int(mode_config["min_report_lines"])
    pass_score = int(mode_config["pass_score"])

    line_count = substantive_line_count(report_path, language)
    if line_count < min_lines:
        errors.append(
            f"report.md: {mode} mode complete report must contain at least {min_lines} substantive lines"
        )

    text = report_path.read_text(encoding="utf-8")
    appendix_heading = str(label["appendix_start_heading"])
    appendix_match = re.search(rf"^## {re.escape(appendix_heading)}\s*$", text, flags=re.MULTILINE)
    if appendix_match:
        body_before_appendix = text[: appendix_match.start()]
        if any(line.strip().startswith("|") and line.strip().endswith("|") for line in body_before_appendix.splitlines()):
            errors.append("report.md: prose-first rule violated; evidence tables belong in appendices, not the report body")

    thin_sections: list[str] = []
    for heading in label["report_headings"]:
        body = section_body(text, str(heading))
        if body is None:
            continue
        section_lines = [line for line in body.splitlines() if is_substantive_line(line, language)]
        if len(section_lines) < 1:
            thin_sections.append(str(heading))
    if thin_sections:
        errors.append("report.md: sections need substantive content: " + ", ".join(thin_sections))

    score_heading = str(label["report_quality_heading"])
    score_body = section_body(text, score_heading) or ""
    score = parse_report_score(text, score_heading)
    if score is None:
        errors.append("report.md: Report Quality Score must include a parseable 'Total Score: N / 100'")
        return
    if score < pass_score:
        errors.append(f"report.md: {mode} mode requires report score >= {pass_score}")


def init_survey(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    today = args.date or dt.date.today().isoformat()
    language = args.language
    mode = args.mode
    mode_config = MODE_CONFIG[mode]
    label = labels(language)
    survey_dir = root / "surveys" / f"{today}-{slugify(args.topic)}"
    survey_dir.mkdir(parents=True, exist_ok=True)
    write_metadata(survey_dir, args.topic, language)
    update_metadata(survey_dir, mode=mode, language=language, report_schema_version=REPORT_SCHEMA_VERSION)
    create_registry_files(survey_dir)

    headings = label["brief_headings"]
    decision_frame_note = str(label["decision_frame_note"])
    continuation_policy_note = str(label["continuation_policy_note"])
    write_once(
        survey_dir / "00-brief.md",
        f"""# {label['brief_title']}: {args.topic}

## {headings[0]}

{args.topic}

## {headings[1]}

- Status:
- Notes:

## {headings[2]}

- 

## {headings[3]}

- 

## {headings[4]}

- Mode: {mode}
- Minimum Sources: {mode_config['min_sources']}
- Minimum Claims: {mode_config['min_claims']}
- Minimum Evidence Items: {mode_config['min_evidence']}
- Target Report Length: {mode_config['target_report_length']}
- Quality Gate: {mode_config['quality_gate']}

## {headings[5]}

{decision_frame_note}

## {headings[6]}

-

## {headings[7]}

-

## {headings[8]}

-

## {headings[9]}

-

## {headings[10]}

{continuation_policy_note}
""",
    )
    headings = label["index_headings"]
    wiki_status_notes = "\n".join(f"- {note}" for note in label["wiki_status_notes"])
    write_once(
        survey_dir / "index.md",
        f"""# {label['index_title']}: {args.topic}

## {headings[0]}

-

## {headings[1]}

-

## {headings[2]}

-

## {headings[3]}

-

## {headings[4]}

-

## {headings[5]}

-

## {headings[6]}

-

## {headings[7]}

-
- Registry: sources.jsonl, claims.jsonl, evidence.jsonl

## {headings[8]}

{wiki_status_notes}

## {headings[9]}

-
""",
    )
    print(survey_dir)


def round_title(label: dict[str, object], round_number: int, suffix: str) -> str:
    if label["round"] == "Round":
        return f"Round {round_number} {suffix}"
    return f"{label['round']}{round_number}{suffix}"


def create_round(args: argparse.Namespace) -> None:
    survey_dir = Path(args.survey_dir).expanduser().resolve()
    survey_dir.mkdir(parents=True, exist_ok=True)
    language = read_language(survey_dir, args.language)
    label = labels(language)
    prefix = f"{int(args.round):02d}"

    headings = label["research_headings"]
    search_tool_notes = "\n".join(f"- {note}" for note in label["search_tool_notes"])
    write_once(
        survey_dir / f"{prefix}-research.md",
        f"""# {round_title(label, int(args.round), str(label['research']))}

## {headings[0]}

- 

## {headings[1]}

{table(str(label['source_cols']))}

## {headings[2]}

{table(str(label['evidence_cols']))}

## {headings[3]}

- 

## {headings[4]}

{search_tool_notes}
""",
    )
    headings = label["brainstorm_headings"]
    write_once(
        survey_dir / f"{prefix}-brainstorm.md",
        f"""# {round_title(label, int(args.round), str(label['brainstorm']))}

## {headings[0]}

- Status:
- Notes:

## {headings[1]}

- 

## {headings[2]}

- 

## {headings[3]}

- Option A:
- Option B:
- Option C:

## {headings[4]}

- 

## {headings[5]}

- 
""",
    )
    headings = label["redteam_headings"]
    write_once(
        survey_dir / f"{prefix}-redteam.md",
        f"""# {round_title(label, int(args.round), str(label['redteam']))}

## {headings[0]}

- 

## {headings[1]}

- 

## {headings[2]}

- 

## {headings[3]}

- 

## {headings[4]}

- 

## {headings[5]}

- 

## {headings[6]}

-

## {headings[7]}

-
""",
    )
    headings = label["synthesis_headings"]
    write_once(
        survey_dir / f"{prefix}-synthesis.md",
        f"""# {round_title(label, int(args.round), str(label['synthesis']))}

## {headings[0]}

- 

## {headings[1]}

{label['confidence']}

## {headings[2]}

- 

## {headings[3]}

- 

## {headings[4]}

- 

## {headings[5]}

- 

## {headings[6]}

-
""",
    )
    headings = label["evolver_headings"]
    write_once(
        survey_dir / f"{prefix}-evolver.md",
        f"""# {round_title(label, int(args.round), str(label['evolver']))}

## {headings[0]}

- 

## {headings[1]}

{table(str(label['probe_cols']))}
"""
        + "\n".join(f"| {probe} |  | {label['strength']} |" for probe in label["probes"])
        + f"""

## {headings[2]}

{table(str(label['persona_cols']))}
"""
        + "\n".join(f"| {persona} | {label['verdict']} |  |" for persona in label["personas"])
        + f"""

## {headings[3]}

{label['decision']}

## {headings[4]}

- Evidence coverage this round:
- Weakest evidence dimensions:
- Continue / stop implication:
- Next-round focus:

## {headings[5]}

-

## {headings[6]}

-
""",
    )
    print(survey_dir)


def detect_rounds(survey_dir: Path) -> list[int]:
    rounds: set[int] = set()
    for path in survey_dir.glob("[0-9][0-9]-*.md"):
        try:
            round_number = int(path.name[:2])
        except ValueError:
            continue
        if round_number > 0:
            rounds.add(round_number)
    return sorted(rounds)


def check_required_file(errors: list[str], path: Path, headings: list[str], language: str) -> None:
    if not path.exists():
        errors.append(f"missing file: {path.name}")
        return
    text = path.read_text(encoding="utf-8")
    for heading in headings:
        if not has_heading(text, heading):
            errors.append(f"{path.name}: missing heading '## {heading}'")
            continue
        body = section_body(text, heading)
        if body is not None and not any(is_substantive_line(line, language) for line in body.splitlines()):
            errors.append(f"{path.name}: section '## {heading}' appears to be empty")
    if not file_has_substance(path, language):
        errors.append(f"{path.name}: appears to be only an empty template")


def check_research_tool_notes(
    errors: list[str],
    warnings: list[str],
    path: Path,
    label: dict[str, object],
    schema_version: int,
) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    body = section_body(text, str(label["research_headings"][-1]))
    if body is None:
        return
    expected_notes = [str(note).split(":")[0].split("：")[0] for note in label["search_tool_notes"][:2]]
    missing = [note for note in expected_notes if note and note not in body]
    if missing:
        message = f"{path.name}: Data Quality Notes must record search tool and Tavily fallback status"
        if schema_version < REPORT_SCHEMA_VERSION:
            warnings.append(message)
        else:
            errors.append(message)


def check_wiki_status_notes(
    errors: list[str],
    warnings: list[str],
    index_path: Path,
    label: dict[str, object],
    schema_version: int,
) -> None:
    if not index_path.exists():
        return
    text = index_path.read_text(encoding="utf-8")
    body = section_body(text, str(label["index_headings"][-2]))
    if body is None:
        return
    expected_notes = [str(note).split(":")[0] for note in label["wiki_status_notes"][:2]]
    missing = [note for note in expected_notes if note and note not in body]
    if missing:
        message = "index.md: Wiki / Graph Index Status must record wiki tool attempt and ingest result"
        if schema_version < REPORT_SCHEMA_VERSION:
            warnings.append(message)
        else:
            errors.append(message)


def check_continuation_policy(errors: list[str], brief_path: Path, label: dict[str, object]) -> None:
    if not brief_path.exists():
        return
    text = brief_path.read_text(encoding="utf-8")
    heading = str(label["brief_headings"][-1])
    body = section_body(text, heading) or ""
    predictive_patterns = (
        r"(?im)^\s*-?\s*round\s+\d+\s*[:：]",
        r"(?im)^\s*-?\s*第\s*\d+\s*轮\s*[:：]",
        r"(?im)^\s*-?\s*第\s*\d+\s*回\s*[:：]",
    )
    if any(re.search(pattern, body) for pattern in predictive_patterns):
        errors.append("00-brief.md: continuation policy must not predict specific round outcomes")


def parse_evolver_decision(path: Path, label: dict[str, object]) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    body = section_body(text, str(label["evolver_headings"][3])) or ""
    first_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
    token = re.sub(r"^[\-\*\d\.\)\s]+", "", first_line).strip()
    token = re.sub(r"[。.!！、,，；;：:]+$", "", token).strip()
    normalized = token.lower()
    exact_tokens = {
        "kill": "Kill",
        "放弃": "Kill",
        "中止": "Kill",
        "pivot": "Pivot",
        "转向": "Pivot",
        "ピボット": "Pivot",
        "narrow": "Narrow",
        "收窄": "Narrow",
        "絞り込み": "Narrow",
        "keep": "Keep",
        "保留": "Keep",
        "維持": "Keep",
    }
    if normalized in exact_tokens:
        return exact_tokens[normalized]
    if token in exact_tokens:
        return exact_tokens[token]
    return None


def validate_evolver_gate(
    errors: list[str],
    warnings: list[str],
    evolver_path: Path,
    label: dict[str, object],
    *,
    final: bool,
) -> None:
    if not evolver_path.exists():
        return
    decision = parse_evolver_decision(evolver_path, label)
    if decision is None:
        errors.append(
            f"{evolver_path.name}: Decision first non-empty line must be exactly one of Keep, Narrow, Pivot, or Kill"
        )
        return

    if decision == "Kill":
        return

    if decision in {"Keep", "Narrow", "Pivot"}:
        message = f"evolver decision {decision} requires another round"
        if final:
            errors.append(message)
        else:
            warnings.append(f"continuation required: {message}")


def read_jsonl(path: Path, errors: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        errors.append(f"missing file: {path.name}")
        return rows
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = json.loads(stripped)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}:{index}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path.name}:{index}: entry must be a JSON object")
            continue
        rows.append(value)
    return rows


def require_fields(
    errors: list[str],
    filename: str,
    row: dict[str, object],
    row_id: str,
    fields: tuple[str, ...],
) -> None:
    for field in fields:
        value = row.get(field)
        if value in (None, "", []):
            errors.append(f"{filename}: {row_id} missing required field '{field}'")


def validate_evidence_registry(survey_dir: Path, mode: str) -> list[str]:
    errors: list[str] = []
    mode_config = MODE_CONFIG[mode]
    sources = read_jsonl(survey_dir / "sources.jsonl", errors)
    evidence = read_jsonl(survey_dir / "evidence.jsonl", errors)
    claims = read_jsonl(survey_dir / "claims.jsonl", errors)

    minimums = {
        "sources.jsonl": int(mode_config["min_sources"]),
        "claims.jsonl": int(mode_config["min_claims"]),
        "evidence.jsonl": int(mode_config["min_evidence"]),
    }
    actuals = {
        "sources.jsonl": len(sources),
        "claims.jsonl": len(claims),
        "evidence.jsonl": len(evidence),
    }
    for filename, minimum in minimums.items():
        if actuals[filename] < minimum:
            errors.append(f"{filename}: expected at least {minimum} entries for {mode} mode, found {actuals[filename]}")

    source_ids: set[str] = set()
    for index, source in enumerate(sources, start=1):
        row_id = str(source.get("source_id") or f"row {index}")
        require_fields(
            errors,
            "sources.jsonl",
            source,
            row_id,
            ("source_id", "title", "url", "source_type", "date_checked", "credibility"),
        )
        source_id = source.get("source_id")
        if isinstance(source_id, str) and source_id:
            if source_id in source_ids:
                errors.append(f"sources.jsonl: duplicate source_id {source_id}")
            source_ids.add(source_id)

    evidence_ids: set[str] = set()
    for index, item in enumerate(evidence, start=1):
        row_id = str(item.get("evidence_id") or f"row {index}")
        require_fields(
            errors,
            "evidence.jsonl",
            item,
            row_id,
            ("evidence_id", "source_id", "quote_or_summary", "locator", "confidence"),
        )
        evidence_id = item.get("evidence_id")
        source_id = item.get("source_id")
        if isinstance(evidence_id, str) and evidence_id:
            if evidence_id in evidence_ids:
                errors.append(f"evidence.jsonl: duplicate evidence_id {evidence_id}")
            evidence_ids.add(evidence_id)
        if isinstance(source_id, str) and source_id and source_id not in source_ids:
            errors.append(f"evidence.jsonl: {row_id} references missing source_id {source_id}")

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims, start=1):
        row_id = str(claim.get("claim_id") or f"row {index}")
        require_fields(
            errors,
            "claims.jsonl",
            claim,
            row_id,
            ("claim_id", "claim", "supporting_evidence_ids", "status"),
        )
        claim_id = claim.get("claim_id")
        if isinstance(claim_id, str) and claim_id:
            if claim_id in claim_ids:
                errors.append(f"claims.jsonl: duplicate claim_id {claim_id}")
            claim_ids.add(claim_id)
        supporting_ids = claim.get("supporting_evidence_ids")
        if not isinstance(supporting_ids, list):
            errors.append(f"claims.jsonl: {row_id} supporting_evidence_ids must be a list")
            continue
        status = str(claim.get("status") or "").lower()
        if status in {"supported", "partial", "contested"} and not supporting_ids:
            errors.append(f"claims.jsonl: {row_id} needs at least one supporting evidence id")
        for evidence_id in supporting_ids:
            if not isinstance(evidence_id, str) or not evidence_id:
                errors.append(f"claims.jsonl: {row_id} has invalid evidence id {evidence_id!r}")
            elif evidence_id not in evidence_ids:
                errors.append(f"claims.jsonl: {row_id} references missing evidence_id {evidence_id}")

    return errors


def create_registry_files(survey_dir: Path) -> None:
    for filename in REGISTRY_FILES:
        write_once(survey_dir / filename, "")


def check_survey(args: argparse.Namespace, *, final: bool = False) -> None:
    survey_dir = Path(args.survey_dir).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not survey_dir.exists():
        print(f"ERROR: survey directory does not exist: {survey_dir}", file=sys.stderr)
        raise SystemExit(2)

    language = read_language(survey_dir, args.language)
    mode = read_mode(survey_dir, getattr(args, "mode", None))
    label = labels(language)
    schema_version = report_schema_version(survey_dir)
    warnings.extend(metadata_warnings(survey_dir))

    brief_path = survey_dir / "00-brief.md"
    check_required_file(errors, brief_path, list(label["brief_headings"]), language)
    check_continuation_policy(errors, brief_path, label)
    index_path = survey_dir / "index.md"
    check_required_file(errors, index_path, list(label["index_headings"]), language)
    check_wiki_status_notes(errors, warnings, index_path, label, schema_version)
    if final:
        report_path = survey_dir / "report.md"
        check_required_file(errors, report_path, required_report_headings(label, schema_version), language)
        validate_report_quality(errors, warnings, report_path, label, language, schema_version, mode)
    errors.extend(validate_evidence_registry(survey_dir, mode))

    rounds = detect_rounds(survey_dir)
    if not rounds:
        errors.append("missing round files: run the 'round' command first")

    for round_number in rounds:
        prefix = f"{round_number:02d}"
        research_path = survey_dir / f"{prefix}-research.md"
        check_required_file(errors, research_path, list(label["research_headings"]), language)
        check_research_tool_notes(errors, warnings, research_path, label, schema_version)
        check_required_file(errors, survey_dir / f"{prefix}-brainstorm.md", list(label["brainstorm_headings"]), language)
        check_required_file(errors, survey_dir / f"{prefix}-redteam.md", list(label["redteam_headings"]), language)
        check_required_file(errors, survey_dir / f"{prefix}-synthesis.md", list(label["synthesis_headings"]), language)
        evolver_path = survey_dir / f"{prefix}-evolver.md"
        check_required_file(errors, evolver_path, required_evolver_headings(label, schema_version), language)
    if rounds:
        latest_evolver_path = survey_dir / f"{rounds[-1]:02d}-evolver.md"
        validate_evolver_gate(errors, warnings, latest_evolver_path, label, final=final)

    if errors:
        label_text = "final check" if final else "check"
        print(f"Super Survey {label_text} failed:")
        if warnings:
            for warning in warnings:
                print(f"- {warning}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    if warnings:
        print("Super Survey check warnings:")
        for warning in warnings:
            print(f"- {warning}")

    label_text = "final check" if final else "check"
    print(f"Super Survey {label_text} passed: {survey_dir} ({language}, {mode})")


def check_final(args: argparse.Namespace) -> None:
    check_survey(args, final=True)


def validate_evidence_command(args: argparse.Namespace) -> None:
    survey_dir = Path(args.survey_dir).expanduser().resolve()
    if not survey_dir.exists():
        print(f"ERROR: survey directory does not exist: {survey_dir}", file=sys.stderr)
        raise SystemExit(2)
    mode = read_mode(survey_dir, args.mode)
    errors = validate_evidence_registry(survey_dir, mode)
    if errors:
        print("Super Survey evidence validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Super Survey evidence validation passed: {survey_dir} ({mode})")


def append_missing_report_sections(report_path: Path, label: dict[str, object]) -> bool:
    if not report_path.exists():
        return False
    text = report_path.read_text(encoding="utf-8")
    additions: list[str] = []
    for heading, note in zip(label["report_headings"], label["report_template_notes"], strict=True):
        if not has_heading(text, str(heading)):
            additions.append(f"## {heading}\n\n- {note}")
    if not additions:
        return False
    separator = "" if text.endswith("\n") else "\n"
    report_path.write_text(text + separator + "\n".join(additions) + "\n", encoding="utf-8")
    return True


def upgrade_report(args: argparse.Namespace) -> None:
    survey_dir = Path(args.survey_dir).expanduser().resolve()
    if not survey_dir.exists():
        print(f"ERROR: survey directory does not exist: {survey_dir}", file=sys.stderr)
        raise SystemExit(2)
    language = read_language(survey_dir, args.language)
    label = labels(language)
    report_path = survey_dir / "report.md"
    if not report_path.exists():
        print(f"ERROR: report.md does not exist: {report_path}", file=sys.stderr)
        raise SystemExit(2)
    changed = append_missing_report_sections(report_path, label)
    update_metadata(survey_dir, language=language, report_schema_version=REPORT_SCHEMA_VERSION)
    status = "updated" if changed else "already current"
    print(f"report.md {status}: {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create a survey directory")
    p_init.add_argument("topic")
    p_init.add_argument("--root", default=".")
    p_init.add_argument("--date")
    p_init.add_argument("--language", choices=LANGUAGES, default="en")
    p_init.add_argument("--mode", choices=MODES, default="standard")
    p_init.set_defaults(func=init_survey)

    p_round = sub.add_parser("round", help="create round templates")
    p_round.add_argument("survey_dir")
    p_round.add_argument("round", type=positive_int)
    p_round.add_argument("--language", choices=LANGUAGES)
    p_round.set_defaults(func=create_round)

    p_check = sub.add_parser("check", help="validate a survey directory")
    p_check.add_argument("survey_dir")
    p_check.add_argument("--language", choices=LANGUAGES)
    p_check.add_argument("--mode", choices=MODES)
    p_check.set_defaults(func=check_survey)

    p_check_final = sub.add_parser("check-final", help="validate final report delivery gate")
    p_check_final.add_argument("survey_dir")
    p_check_final.add_argument("--language", choices=LANGUAGES)
    p_check_final.add_argument("--mode", choices=MODES)
    p_check_final.set_defaults(func=check_final)

    p_validate = sub.add_parser("validate-evidence", help="validate sources, claims, and evidence registry files")
    p_validate.add_argument("survey_dir")
    p_validate.add_argument("--mode", choices=MODES)
    p_validate.set_defaults(func=validate_evidence_command)

    p_upgrade = sub.add_parser("upgrade-report", help="append missing v2 report sections")
    p_upgrade.add_argument("survey_dir")
    p_upgrade.add_argument("--language", choices=LANGUAGES)
    p_upgrade.set_defaults(func=upgrade_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
