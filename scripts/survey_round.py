#!/usr/bin/env python3
"""Create and validate Super Survey directories and round templates."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

LANGUAGES = ("en", "zh", "ja")

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
            "Target Customer",
            "Success Criteria",
            "Disqualifying Conditions",
            "Initial Assumptions",
            "Planned Rounds",
        ],
        "index_headings": [
            "Current Thesis",
            "Round Summaries",
            "Open Questions",
            "Source Inventory",
            "Wiki / Graph Index Status",
            "Decision Log",
        ],
        "report_headings": [
            "Executive Summary",
            "Key Findings",
            "Comparison Or Analysis",
            "Recommendation",
            "Limitations",
            "Source Notes",
        ],
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
        "planned_rounds_note": "- Round 1:\n- Continue with Round 2+ while unresolved unknowns are desk-researchable; there is no implicit two-round cap.",
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
            "目标客户",
            "成功标准",
            "放弃条件",
            "初始假设",
            "计划轮次",
        ],
        "index_headings": [
            "当前论点",
            "轮次摘要",
            "开放问题",
            "来源清单",
            "Wiki / Graph 索引状态",
            "决策日志",
        ],
        "report_headings": [
            "执行摘要",
            "关键发现",
            "对比或分析",
            "建议",
            "局限性",
            "来源备注",
        ],
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
        "planned_rounds_note": "- Round 1:\n- 如果剩余未知仍可通过桌面调研解决，继续 Round 2+；不存在默认两轮上限。",
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
            "対象顧客",
            "成功基準",
            "中止条件",
            "初期仮説",
            "予定ラウンド",
        ],
        "index_headings": [
            "現在の仮説",
            "ラウンド要約",
            "未解決の問い",
            "情報源一覧",
            "Wiki / Graph インデックス状態",
            "意思決定ログ",
        ],
        "report_headings": [
            "エグゼクティブサマリー",
            "主要な発見",
            "比較または分析",
            "推奨事項",
            "制約",
            "情報源メモ",
        ],
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
        "planned_rounds_note": "- Round 1:\n- 未解決事項が desk research で減らせる間は Round 2+ を続ける。暗黙の 2 ラウンド上限はない。",
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
        json.dumps({"topic": topic, "language": language}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_language(survey_dir: Path, override: str | None = None) -> str:
    if override:
        return override
    path = metadata_path(survey_dir)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            language = data.get("language")
            if language in LANGUAGES:
                return language
        except json.JSONDecodeError:
            pass
    return "en"


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


def structural_values(language: str) -> set[str]:
    label = labels(language)
    values: set[str] = set()
    for key in ("source_cols", "evidence_cols", "probe_cols", "persona_cols"):
        values.update(col.strip() for col in str(label[key]).split("|"))
    values.update(str(probe) for probe in label["probes"])
    values.update(str(persona) for persona in label["personas"])
    values.update(str(note) for note in label["search_tool_notes"])
    values.update(str(note) for note in str(label["planned_rounds_note"]).splitlines())
    return values


def is_substantive_line(line: str, language: str) -> bool:
    stripped = line.strip()
    placeholders = placeholder_values(language)
    if not stripped or stripped.startswith("#") or stripped in placeholders:
        return False
    if stripped in structural_values(language):
        return False
    if re.fullmatch(r"-\s*(Status|Notes|Option [A-Z]|Round \d+):\s*", stripped):
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


def section_body(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    return match.group("body")


def init_survey(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    today = args.date or dt.date.today().isoformat()
    language = args.language
    label = labels(language)
    survey_dir = root / "surveys" / f"{today}-{slugify(args.topic)}"
    survey_dir.mkdir(parents=True, exist_ok=True)
    write_metadata(survey_dir, args.topic, language)

    headings = label["brief_headings"]
    planned_rounds_note = str(label["planned_rounds_note"])
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

- 

## {headings[5]}

- 

## {headings[6]}

- 

## {headings[7]}

-

## {headings[8]}

-

## {headings[9]}

{planned_rounds_note}
""",
    )
    headings = label["index_headings"]
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
""",
    )
    headings = label["report_headings"]
    write_once(
        survey_dir / "report.md",
        f"""# {args.topic}

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

- 

## {headings[5]}

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


def check_survey(args: argparse.Namespace) -> None:
    survey_dir = Path(args.survey_dir).expanduser().resolve()
    errors: list[str] = []

    if not survey_dir.exists():
        print(f"ERROR: survey directory does not exist: {survey_dir}", file=sys.stderr)
        raise SystemExit(2)

    language = read_language(survey_dir, args.language)
    label = labels(language)

    check_required_file(errors, survey_dir / "00-brief.md", list(label["brief_headings"]), language)
    check_required_file(errors, survey_dir / "index.md", list(label["index_headings"]), language)
    check_required_file(errors, survey_dir / "report.md", list(label["report_headings"]), language)

    rounds = detect_rounds(survey_dir)
    if not rounds:
        errors.append("missing round files: run the 'round' command first")

    for round_number in rounds:
        prefix = f"{round_number:02d}"
        check_required_file(errors, survey_dir / f"{prefix}-research.md", list(label["research_headings"]), language)
        check_required_file(errors, survey_dir / f"{prefix}-brainstorm.md", list(label["brainstorm_headings"]), language)
        check_required_file(errors, survey_dir / f"{prefix}-redteam.md", list(label["redteam_headings"]), language)
        check_required_file(errors, survey_dir / f"{prefix}-synthesis.md", list(label["synthesis_headings"]), language)
        check_required_file(errors, survey_dir / f"{prefix}-evolver.md", list(label["evolver_headings"]), language)

    if errors:
        print("Super Survey check failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Super Survey check passed: {survey_dir} ({language})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create a survey directory")
    p_init.add_argument("topic")
    p_init.add_argument("--root", default=".")
    p_init.add_argument("--date")
    p_init.add_argument("--language", choices=LANGUAGES, default="en")
    p_init.set_defaults(func=init_survey)

    p_round = sub.add_parser("round", help="create round templates")
    p_round.add_argument("survey_dir")
    p_round.add_argument("round", type=positive_int)
    p_round.add_argument("--language", choices=LANGUAGES)
    p_round.set_defaults(func=create_round)

    p_check = sub.add_parser("check", help="validate a survey directory")
    p_check.add_argument("survey_dir")
    p_check.add_argument("--language", choices=LANGUAGES)
    p_check.set_defaults(func=check_survey)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
