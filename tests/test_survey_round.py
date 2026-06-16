from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "survey_round.py"


def load_survey_round_module():
    spec = importlib.util.spec_from_file_location("survey_round", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        text=True,
        capture_output=True,
    )


def markdown_document(title: str, sections: dict[str, str]) -> str:
    parts = [f"# {title}"]
    for heading, body in sections.items():
        parts.extend(["", f"## {heading}", "", body.strip()])
    return "\n".join(parts) + "\n"


def write_markdown(path: Path, title: str, sections: dict[str, str]) -> None:
    path.write_text(markdown_document(title, sections), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows)
    path.write_text(text + ("\n" if text else ""), encoding="utf-8")


class SurveyRoundCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def init_round(self, language: str = "en", mode: str = "standard") -> Path:
        result = run_cli(
            "init",
            "AI recruiting agent",
            "--root",
            str(self.root),
            "--date",
            "2026-06-13",
            "--language",
            language,
            "--mode",
            mode,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        survey_dir = Path(result.stdout.strip())

        result = run_cli("round", str(survey_dir), "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        return survey_dir

    def test_check_rejects_empty_brief_and_brainstorm_templates(self) -> None:
        survey_dir = self.init_round()

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("00-brief.md: appears to be only an empty template", result.stdout)
        self.assertIn("01-brainstorm.md: appears to be only an empty template", result.stdout)
        self.assertNotIn("report.md", result.stdout)

    def test_check_rejects_files_with_empty_required_sections(self) -> None:
        survey_dir = self.init_round()
        research = survey_dir / "01-research.md"
        research.write_text(
            """# Round 1 Research

## Research Question

Can this target customer pay for this workflow?

## Source Registry Updates

## Claim And Evidence Notes

## Findings

## Data Quality Notes
""",
            encoding="utf-8",
        )

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("01-research.md: section '## Source Registry Updates' appears to be empty", result.stdout)
        self.assertIn("01-research.md: section '## Claim And Evidence Notes' appears to be empty", result.stdout)

    def test_check_warns_for_missing_search_tool_notes_when_current_sources_not_required(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_report=False)
        research = survey_dir / "01-research.md"
        text = re.sub(
            r"(?ms)^## Data Quality Notes\n\n.*?(?=^## |\Z)",
            "## Data Quality Notes\n\nEvidence came from stable local/project artifacts, so current-source discovery was not required.\n",
            research.read_text(encoding="utf-8"),
        )
        research.write_text(text, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Data Quality Notes should record search tool and Tavily fallback status when current sources matter", result.stdout)

    def test_check_requires_search_tool_notes_when_current_sources_are_enabled(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_report=False)
        research = survey_dir / "01-research.md"
        text = re.sub(
            r"(?ms)^## Data Quality Notes\n\n.*?(?=^## |\Z)",
            "## Data Quality Notes\n\nCurrent Source Discovery: yes. Recent policy and pricing facts were needed.\n",
            research.read_text(encoding="utf-8"),
        )
        research.write_text(text, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Data Quality Notes must record search tool and Tavily fallback status", result.stdout)

    def test_round_number_must_be_positive(self) -> None:
        survey_dir = self.init_round()

        zero = run_cli("round", str(survey_dir), "0")
        negative = run_cli("round", str(survey_dir), "-1")

        self.assertNotEqual(zero.returncode, 0)
        self.assertNotEqual(negative.returncode, 0)
        self.assertFalse((survey_dir / "00-research.md").exists())
        self.assertFalse((survey_dir / "-1-research.md").exists())

    def test_templates_include_generic_research_framework_fields(self) -> None:
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")
        research = (survey_dir / "01-research.md").read_text(encoding="utf-8")
        brainstorm = (survey_dir / "01-brainstorm.md").read_text(encoding="utf-8")
        redteam = (survey_dir / "01-redteam.md").read_text(encoding="utf-8")
        synthesis = (survey_dir / "01-synthesis.md").read_text(encoding="utf-8")
        evolver = (survey_dir / "01-evolver.md").read_text(encoding="utf-8")
        index = (survey_dir / "index.md").read_text(encoding="utf-8")

        self.assertIn("## Research Lens", brief)
        self.assertIn("## Research Framework", brief)
        self.assertIn("## Decision Evidence Standard", brief)
        self.assertIn("## Decision Frame Integrity", brief)
        self.assertIn("Original user frame", brief)
        self.assertIn("Implicit assumptions", brief)
        self.assertIn("Reframed objective", brief)
        self.assertIn("Competing objectives", brief)
        self.assertIn("What not to optimize for", brief)
        self.assertIn("## Initial Assumptions", brief)
        self.assertIn("## Continuation Policy", brief)
        self.assertNotIn("## Planned Rounds", brief)
        self.assertNotIn("Round 1:", brief)
        self.assertIn("Keep the round count open until evidence", brief)
        self.assertIn("Source Registry Updates", research)
        self.assertIn("Claim And Evidence Notes", research)
        self.assertIn("Search Tool Used", research)
        self.assertIn("Tavily Fallback Reason", research)
        self.assertIn("## Framework Coverage", research)
        self.assertIn("## Alternative Explanations Or Substitutes", redteam)
        self.assertIn("## Kill Criteria Checked", redteam)
        self.assertIn("## Decision Rationale", synthesis)
        self.assertIn("## Framework-Based Synthesis", synthesis)
        self.assertIn("Alternative", evolver)
        self.assertIn("## Round Evidence Quality Gate", evolver)
        self.assertIn("Framework coverage this round", evolver)
        self.assertNotIn("## Report Quality Gate", evolver)
        self.assertNotIn("Current report quality score", evolver)
        self.assertFalse((survey_dir / "report.md").exists())
        self.assertIn("## Current Evidence-Bound Conclusion", index)
        self.assertNotIn("## Current Best Conclusion", index)
        self.assertIn("## Round Ledger", index)
        self.assertIn("## Continuation Status", index)
        self.assertIn("## Next Research Target", index)
        self.assertIn("## Why Not Final Yet", index)
        self.assertIn("## Framework Refinement Log", index)
        self.assertIn("Wiki Tool Attempted", index)
        self.assertIn("Wiki Ingest Result", index)
        self.assertIn("Wiki Persistence Needed", index)
        self.assertIn("Mode:", brief)
        self.assertIn("Minimum Sources:", brief)
        self.assertIn("Target Report Length:", brief)
        self.assertIn("### <framework dimension>", brief)
        self.assertIn("### <framework dimension>", research)
        self.assertIn("### <framework dimension>", brainstorm)
        self.assertIn("### <framework dimension>", redteam)
        self.assertIn("### <framework dimension>", synthesis)
        self.assertIn("### <framework dimension>", evolver)

    def test_templates_include_decision_robustness_tools(self) -> None:
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")
        synthesis = (survey_dir / "01-synthesis.md").read_text(encoding="utf-8")
        evolver = (survey_dir / "01-evolver.md").read_text(encoding="utf-8")

        self.assertIn("Object quality vs action attractiveness", brief)
        self.assertIn("Hard constraints", brief)
        self.assertIn("Soft constraints", brief)
        self.assertIn("User-specific constraints", brief)
        self.assertIn("Missing constraints", brief)
        self.assertIn("Implied expectations", brief)
        self.assertIn("Action attractiveness", synthesis)
        self.assertIn("Bayesian update", synthesis)
        self.assertIn("Decision tree", synthesis)
        self.assertIn("Implied expectation check", evolver)
        self.assertIn("Decision tree triggers", evolver)
        self.assertIn("Bayesian update needed", evolver)

    def test_templates_include_decision_optimization_contract(self) -> None:
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")

        self.assertIn("## Decision Optimization Contract", brief)
        self.assertIn("Original question", brief)
        self.assertIn("Reconstructed objective function", brief)
        self.assertIn("Candidate actions", brief)
        self.assertIn("Do nothing / wait / continue research option", brief)
        self.assertIn("Hard constraints", brief)
        self.assertIn("Soft constraints", brief)
        self.assertIn("Missing constraints", brief)
        self.assertIn("Success criteria", brief)
        self.assertIn("Failure criteria", brief)
        self.assertIn("Opportunity cost", brief)
        self.assertIn("Reversibility", brief)
        self.assertIn("Implied expectations", brief)
        self.assertIn("Decision-changing evidence", brief)

    def test_synthesis_template_includes_sensitivity_and_counterfactuals(self) -> None:
        survey_dir = self.init_round()

        synthesis = (survey_dir / "01-synthesis.md").read_text(encoding="utf-8")

        self.assertIn("## Sensitivity And Counterfactuals", synthesis)
        self.assertIn("Key variable", synthesis)
        self.assertIn("Current assumption", synthesis)
        self.assertIn("If better", synthesis)
        self.assertIn("If worse", synthesis)
        self.assertIn("Evidence needed", synthesis)
        self.assertIn("Decision impact", synthesis)

    def test_evolver_template_requires_kill_scope_and_original_question_status(self) -> None:
        survey_dir = self.init_round()

        evolver = (survey_dir / "01-evolver.md").read_text(encoding="utf-8")

        self.assertIn("Kill scope", evolver)
        self.assertIn("Original question still open", evolver)
        self.assertIn("thesis / path / candidate action / original question", evolver)
        self.assertIn("If original question remains open", evolver)

    def test_index_quality_gate_includes_anti_sycophancy_objective_integrity(self) -> None:
        survey_dir = self.init_round()

        index = (survey_dir / "index.md").read_text(encoding="utf-8")

        self.assertIn("Anti-sycophancy / objective-function integrity", index)
        self.assertIn("Objective reconstruction quality", index)
        self.assertIn("User-frame challenge quality", index)

    def test_docs_describe_anti_sycophancy_and_local_optimum_checks(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "README.zh-CN.md": (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "README.ja.md": (ROOT / "README.ja.md").read_text(encoding="utf-8"),
            "SKILL.md": (ROOT / "SKILL.md").read_text(encoding="utf-8"),
            "references/research-quality.md": (ROOT / "references" / "research-quality.md").read_text(encoding="utf-8"),
        }

        self.assertIn("The user's question is the starting point, not the objective function", docs["README.md"])
        self.assertIn("用户问题是初始点，不是目标函数", docs["README.zh-CN.md"])
        self.assertIn("ユーザーの問いは出発点であり、目的関数ではありません", docs["README.ja.md"])
        self.assertIn("Anti-Sycophancy / Anti-Local-Optimum Checks", docs["SKILL.md"])
        self.assertIn("Anti-Sycophancy / Anti-Local-Optimum Checks", docs["references/research-quality.md"])
        self.assertIn("known facts, unverified assumptions, subjective judgments, missing information, and stakeholders", docs["SKILL.md"])
        self.assertIn("decision tree", docs["references/research-quality.md"])
        self.assertIn("good object is not automatically a good action", docs["SKILL.md"])
        self.assertIn("Decision Robustness Tools", docs["references/research-quality.md"])
        self.assertIn("implied expectations", docs["references/research-quality.md"])
        self.assertIn("Decision Optimization Contract", docs["SKILL.md"])
        self.assertIn("Sensitivity And Counterfactuals", docs["SKILL.md"])
        self.assertIn("Kill scope", docs["SKILL.md"])
        self.assertIn("Anti-sycophancy / objective-function integrity", docs["README.md"])
        self.assertIn("反谄媚 / 目标函数完整性", docs["README.zh-CN.md"])
        self.assertIn("反シコファンシー / 目的関数の整合性", docs["README.ja.md"])

    def test_readmes_frame_super_survey_as_decision_optimization(self) -> None:
        readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        readme_ja = (ROOT / "README.ja.md").read_text(encoding="utf-8")

        self.assertIn("constrained decision-optimization workflow", readme_en)
        self.assertIn("rebuilds the objective function", readme_en)
        self.assertIn("带约束的决策优化工作流", readme_zh)
        self.assertIn("重建目标函数", readme_zh)
        self.assertIn("制約付き意思決定最適化ワークフロー", readme_ja)
        self.assertIn("目的関数を再構築", readme_ja)
        self.assertIn("通过多轮迭代不断逼近人类决策者需要的最终报告", readme_zh)
        self.assertIn("初始直觉很容易导致偏见或不完整信息", readme_zh)
        self.assertNotIn("调研报告是写给人类决策者看的判断报告，不是智能体的任务审计日志", readme_zh)

    def test_foundational_anti_sycophancy_paper_is_included(self) -> None:
        paper = ROOT / "如何拒绝AI谄媚人类.md"

        self.assertTrue(paper.exists())
        paper_text = paper.read_text(encoding="utf-8")
        self.assertIn("拒绝AI谄媚人类：用约束优化方法重构开放式调研", paper_text)
        self.assertIn("以“英伟达现阶段是否值得买入”为例", paper_text)
        self.assertIn("局部最优", paper_text)
        self.assertIn("贝叶斯更新", paper_text)
        self.assertIn("决策树", paper_text)

        readme = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        quality = (ROOT / "references" / "research-quality.md").read_text(encoding="utf-8")
        self.assertIn("如何拒绝AI谄媚人类.md", readme)
        self.assertIn("如何拒绝AI谄媚人类.md", skill)
        self.assertIn("如何拒绝AI谄媚人类.md", quality)

    def test_round_template_uses_registry_as_evidence_source_of_truth(self) -> None:
        survey_dir = self.init_round()
        research = (survey_dir / "01-research.md").read_text(encoding="utf-8")

        self.assertIn("## Source Registry Updates", research)
        self.assertIn("## Claim And Evidence Notes", research)
        self.assertIn("sources.jsonl", research)
        self.assertIn("claims.jsonl", research)
        self.assertIn("evidence.jsonl", research)
        self.assertNotIn("| Source | URL | Date Checked | Notes |", research)
        self.assertNotIn("| Claim | Evidence | Source | Source Type | Freshness | Confidence | Contradictions |", research)

    def test_brainstorm_template_does_not_own_continue_stop_decision(self) -> None:
        survey_dir = self.init_round()
        brainstorm = (survey_dir / "01-brainstorm.md").read_text(encoding="utf-8")

        self.assertIn("## Candidate Next Moves", brainstorm)
        self.assertIn("## Preferred Exploration Path", brainstorm)
        self.assertNotIn("## Chosen Direction", brainstorm)
        self.assertNotIn("continue / stop", brainstorm.lower())

    def test_init_creates_evidence_registry_files_and_mode_metadata(self) -> None:
        survey_dir = self.init_round(mode="deep")

        metadata = (survey_dir / ".super-survey.json").read_text(encoding="utf-8")
        self.assertIn('"mode": "deep"', metadata)
        for filename in ("sources.jsonl", "claims.jsonl", "evidence.jsonl"):
            self.assertTrue((survey_dir / filename).exists(), filename)
            self.assertEqual((survey_dir / filename).read_text(encoding="utf-8"), "")

    def test_section_schemas_are_canonical_across_languages(self) -> None:
        module = load_survey_round_module()

        for language in ("en", "zh", "ja"):
            label = module.labels(language)
            for schema_key, canonical_headings in module.SECTION_SCHEMAS.items():
                self.assertEqual(len(label[schema_key]), len(canonical_headings))
        self.assertEqual(module.labels("en")["research_headings"], list(module.SECTION_SCHEMAS["research_headings"]))
        self.assertEqual(module.labels("zh")["research_headings"][0], "本轮问题")
        self.assertEqual(module.labels("ja")["research_headings"][0], "今回の調査問い")

    def test_validate_evidence_rejects_missing_registry_entries(self) -> None:
        survey_dir = self.init_round()

        result = run_cli("validate-evidence", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("sources.jsonl: expected at least", result.stdout)
        self.assertIn("claims.jsonl: expected at least", result.stdout)
        self.assertIn("evidence.jsonl: expected at least", result.stdout)

    def test_validate_evidence_rejects_orphan_claim_support(self) -> None:
        survey_dir = self.init_round()
        (survey_dir / "sources.jsonl").write_text(
            '{"source_id":"S1","title":"Example","url":"https://example.com","source_type":"primary","date_checked":"2026-06-13","credibility":"medium"}\n',
            encoding="utf-8",
        )
        (survey_dir / "evidence.jsonl").write_text(
            '{"evidence_id":"E1","source_id":"S1","quote_or_summary":"Users repeat this workflow.","locator":"page","confidence":"medium"}\n',
            encoding="utf-8",
        )
        (survey_dir / "claims.jsonl").write_text(
            '{"claim_id":"C1","claim":"Users repeat this workflow.","supporting_evidence_ids":["E2"],"status":"supported"}\n',
            encoding="utf-8",
        )

        result = run_cli("validate-evidence", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("claims.jsonl: C1 references missing evidence_id E2", result.stdout)

    def test_check_runs_evidence_registry_validation_for_v2_surveys(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_registry=False)

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("sources.jsonl: expected at least", result.stdout)

    def test_check_rejects_predictive_round_plan_in_brief(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        brief = survey_dir / "00-brief.md"
        text = brief.read_text(encoding="utf-8").replace(
            "Start with the next research round; decide whether to continue only after evidence, red-team critique, synthesis, and the raw evolver decision are written.",
            "Round 1: collect enough sources and stop if the first pass supports a conclusion.",
        )
        brief.write_text(text, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "00-brief.md: continuation policy should keep round outcomes open until round artifacts are complete",
            result.stdout,
        )

    def test_deep_mode_requires_higher_quality_score(self) -> None:
        survey_dir = self.init_round(mode="deep")
        self._write_substantive_required_files(survey_dir, report_score=91)

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("deep mode requires report score >= 95", result.stdout)

    def test_report_body_rejects_tables_before_appendix(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)
        report_path = survey_dir / "report.md"
        report = report_path.read_text(encoding="utf-8")
        report = report.replace(
            "The opportunity is visible because job seekers repeat the same painful workflow across many applications.\n",
            "| Claim | Evidence |\n|---|---|\n| Early body claim | Early body evidence |\n",
        )
        report_path.write_text(report, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("prose-first rule violated", result.stdout)

    def test_final_report_rejects_bare_registry_citations(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        report_path = survey_dir / "report.md"
        report = report_path.read_text(encoding="utf-8")
        report = report.replace(
            "Job seekers repeat a frustrating workflow across many applications",
            "Job seekers repeat a frustrating workflow across many applications (C1/E1)",
        )
        report_path.write_text(report, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("report.md: replace registry IDs with standalone source links", result.stdout)
        self.assertIn("C1", result.stdout)
        self.assertIn("E1", result.stdout)

    def test_chinese_framework_dimensions_are_extracted_from_framework_body(self) -> None:
        module = load_survey_round_module()
        body = "核心维度包括市场环境、行业主题、公司业务结构、财务质量、估值、机构预期、资金面、技术面、催化剂和风险。"

        dimensions = module.extract_framework_dimensions_from_body(body)

        self.assertEqual(
            dimensions,
            ["市场环境", "行业主题", "公司业务结构", "财务质量", "估值", "机构预期", "资金面", "技术面", "催化剂", "风险"],
        )

    def test_report_rejects_framework_dimensions_without_body_subheadings(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        report_path = survey_dir / "report.md"
        report = report_path.read_text(encoding="utf-8")
        for heading in ("User Pain", "Workflow Frequency", "Policy Constraints"):
            report = re.sub(rf"(?ms)^## {re.escape(heading)}\n\n.*?(?=^## |\Z)", "", report)
        report = report.replace(
            "The opportunity is visible because job seekers repeat the same painful workflow across many applications.",
            "The opportunity is visible because user pain, workflow frequency, and policy constraints matter, but this paragraph does not make them report chapters.",
        )
        report_path.write_text(report, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("report.md: body must include top-level framework dimension headings", result.stdout)
        self.assertIn("user pain", result.stdout)

    def test_empty_report_section_is_reported_once(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)
        report_path = survey_dir / "report.md"
        report = report_path.read_text(encoding="utf-8")
        report = report.replace(
            "## Executive Summary\n\nContinue with a narrower policy-first validation path.\nConfidence is medium because demand is visible but policy and payment remain unresolved.",
            "## Executive Summary\n\n",
        )
        report_path.write_text(report, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.count("Executive Summary"), 1)
        self.assertNotIn("sections need substantive content", result.stdout)

    def test_check_warns_for_missing_wiki_attempt_notes_when_not_required(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_wiki_notes=False)

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Wiki / Graph Index Status should record wiki tool attempt and ingest result when persistence is needed", result.stdout)

    def test_check_requires_wiki_attempt_notes_when_persistence_enabled(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_wiki_notes=False, evolver_decision="Kill.", evolver_evidence_needed="None.")
        index_path = survey_dir / "index.md"
        index = re.sub(
            r"(?ms)^## Wiki / Graph Index Status\n\n.*?(?=^## |\Z)",
            "## Wiki / Graph Index Status\n\nWiki Persistence Needed: yes. Long-term knowledge reuse was requested.\n",
            index_path.read_text(encoding="utf-8"),
        )
        index_path.write_text(index, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Wiki / Graph Index Status must record wiki tool attempt and ingest result", result.stdout)

    def test_legacy_report_schema_fails_final_until_upgraded(self) -> None:
        survey_dir = self.init_round()
        metadata = survey_dir / ".super-survey.json"
        metadata.write_text(
            '{"topic": "AI recruiting agent", "language": "en", "report_schema_version": 1}\n',
            encoding="utf-8",
        )
        (survey_dir / "report.md").write_text(
            """# AI recruiting agent

## Executive Summary

Continue with a narrower policy-first validation path.

## Key Findings

Demand signals exist, but payment and policy evidence are incomplete.

## Comparison Or Analysis

Manual workflows and job trackers are the main substitutes.

## Recommendation

Run a policy-first round before building.

## Limitations

No direct buyer interviews were conducted.

## Source Notes

Sources were checked during this round and remain directional.
""",
            encoding="utf-8",
        )
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("legacy report schema detected", result.stdout)

    def test_upgrade_report_appends_v3_sections_and_metadata(self) -> None:
        survey_dir = self.init_round()
        metadata = survey_dir / ".super-survey.json"
        metadata.write_text(
            '{"topic": "AI recruiting agent", "language": "en", "report_schema_version": 1}\n',
            encoding="utf-8",
        )
        (survey_dir / "report.md").write_text(
            """# AI recruiting agent

## Executive Summary

Continue with a narrower policy-first validation path.

## Key Findings

Demand signals exist, but payment and policy evidence are incomplete.

## Comparison Or Analysis

Manual workflows and job trackers are the main substitutes.

## Recommendation

Run a policy-first round before building.

## Limitations

No direct buyer interviews were conducted.

## Source Notes

Sources were checked during this round and remain directional.
""",
            encoding="utf-8",
        )

        result = run_cli("upgrade-report", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = (survey_dir / "report.md").read_text(encoding="utf-8")
        self.assertNotIn("## Reader's Path", report)
        self.assertNotIn("## Research Method And Framework", report)
        self.assertNotIn("## Framework Dimension Analysis", report)
        self.assertNotIn("## Report Quality Score", report)
        self.assertIn("## Appendix: Evidence Register", report)
        self.assertIn('"report_schema_version": 3', metadata.read_text(encoding="utf-8"))

    def test_v2_report_rejects_thin_content(self) -> None:
        survey_dir = self.init_round()
        (survey_dir / "report.md").write_text(
            """# AI recruiting agent

## Executive Summary
Thin.
## User Pain
Thin.
## Main Narrative
Thin.
## Decision Logic
Thin.
## Final Recommendation
Thin.
## What Could Change This Conclusion
Thin.
## Next Actions
Thin.
## Limits Of This Report
Thin.
## Appendix: Evidence Register
Thin.
## Appendix: Method And Source Quality
Thin.
## Appendix: Red-Team Notes
Thin.
## Appendix: Options Or Scenarios
Thin.
## Appendix: Source Notes
Thin.
""",
            encoding="utf-8",
        )
        self._write_substantive_required_files(survey_dir, include_report=False)

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("complete report must contain at least", result.stdout)

    def test_final_check_requires_quality_score_in_index(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)
        index_path = survey_dir / "index.md"
        index = index_path.read_text(encoding="utf-8")
        index = re.sub(
            r"(?ms)^## Final Report Quality Gate\n\n.*?(?=^## |\Z)",
            "## Final Report Quality Gate\n\nScore pending.\n",
            index,
        )
        index_path.write_text(index, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("index.md: Final Report Quality Gate must include a parseable 'Total Score: N / 100'", result.stdout)

    def test_report_below_pass_score_requires_continuation_decision(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, report_score=74, continuation_decision="Stop.")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("standard mode requires report score >= 90", result.stdout)

    def test_report_below_mode_pass_score_fails_even_with_stop_language(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=84,
            continuation_decision="Pass / Continue Decision: conditionally stop because the next action is clear.",
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("standard mode requires report score >= 90", result.stdout)

    def test_final_report_pass_score_does_not_require_report_stop_explanation(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=90,
            continuation_decision="Pass / Continue Decision: stop because the next action is clear.",
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_final_quality_gate_requires_anti_sycophancy_subscore(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=90,
            continuation_decision="Pass / Continue Decision: stop because the next action is clear.",
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        index_path = survey_dir / "index.md"
        index = index_path.read_text(encoding="utf-8").replace(
            "Anti-sycophancy / objective-function integrity: 18 / 20.\n"
            "Objective reconstruction quality: clear enough to preserve the original decision.\n"
            "User-frame challenge quality: the report challenged the prompt without rewriting it into a stronger claim.\n",
            "",
        )
        index_path.write_text(index, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Final Report Quality Gate must include anti-sycophancy / objective-function integrity", result.stdout)

    def test_evolver_final_allows_final_report_when_score_passes(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=90,
            continuation_decision="Pass / Continue Decision: final report is ready.",
            evolver_decision="Final.",
            evolver_evidence_needed="No desk-research target remains that could change this decision.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_evolver_decision_uses_only_first_canonical_line(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=92,
            evolver_decision="Narrow.\n\nKill would be tempting only if policy blocks the workflow.",
            evolver_evidence_needed="Official ToS pages and direct pricing evidence.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("evolver decision Narrow requires another round", result.stdout)

    def test_evolver_rejects_explanatory_decision_line(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=92,
            evolver_decision="Kill is possible, but the actual decision is Narrow.",
            evolver_evidence_needed="Official ToS pages and direct pricing evidence.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Decision first non-empty line must be exactly one of", result.stdout)

    def test_quick_mode_accepts_single_round_artifact(self) -> None:
        survey_dir = self.init_round(mode="quick")
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            include_wiki_notes=False,
            evolver_decision="Final.",
            evolver_evidence_needed="No desk-research target remains.",
        )
        for suffix in ("research", "brainstorm", "redteam", "synthesis", "evolver"):
            path = survey_dir / f"01-{suffix}.md"
            if path.exists():
                path.unlink()
        write_markdown(
            survey_dir / "01-round.md",
            "Round 1 Quick Survey",
            {
                "Research Question": "Should this be pursued as a direction?",
                "Evidence And Sources": "S1/E1/C1 support a directional read; source detail remains in JSONL.",
                "Brainstorming Checkpoint": "The practical next move is to decide whether more desk research would change the answer.",
                "Red-Team Challenge": "The strongest objection is that public evidence is too thin for a high-stakes decision.",
                "Synthesis": "The directional answer is sufficient for quick mode and can move to a final memo.",
                "Decision": "Final.",
                "Next Step": "Write the short final report and disclose that this was quick mode.",
            },
        )

        result = run_cli("check", str(survey_dir), "--mode", "quick")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_describes_deep_research_as_optional_capability_route(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("`deep-research` routing is required", skill)
        self.assertIn("prefer `deep-research`", skill)

    def test_skill_keeps_tavily_as_conditional_current_source_route(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("For current-source discovery, default to `tavily-search`", skill)
        self.assertIn("When current-source discovery matters and Tavily fits the source surface", skill)

    def test_skill_keeps_wiki_persistence_conditional(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("Skipped wiki persistence**: the survey ends with only local Markdown even though", skill)
        self.assertIn("when long-term persistence was needed", skill)

    def test_evolver_narrow_with_desk_research_evidence_requires_continuation(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            continuation_decision=(
                "Pass / Continue Decision: stop because no decision-changing unknown remains desk-researchable."
            ),
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("evolver decision Narrow requires another round", result.stdout)

    def test_evolver_narrow_cannot_stop_even_when_report_explains_external_validation(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            continuation_decision=(
                "Pass / Continue Decision: stop because no decision-changing unknown remains desk-researchable; "
                "the evolver next evidence requires external validation through user interviews."
            ),
            evolver_evidence_needed="User interviews and paid trial data.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("evolver decision Narrow requires another round", result.stdout)

    def test_evolver_narrow_mixed_desk_and_future_evidence_requires_continuation(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            continuation_decision=(
                "Pass / Continue Decision: pass; finalize the report because no decision-changing unknown remains desk-researchable, "
                "and the evolver next evidence requires external validation through future disclosures."
            ),
            evolver_decision="收窄",
            evolver_evidence_needed=(
                "Exchange PDF filings and financial statement breakdown.\n"
                "2026Q2/Q3 gross margin, expense ratio, operating cash flow, and inventory changes.\n"
                "DCF / scenario valuation model.\n"
                "未来披露。"
            ),
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("evolver decision Narrow requires another round", result.stdout)

    def test_evolver_kill_allows_stop_when_report_score_passes(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            continuation_decision=(
                "Pass / Continue Decision: stop because no decision-changing unknown remains desk-researchable."
            ),
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_allows_completed_round_without_final_report(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_allows_continuation_round_without_forcing_kill(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Narrow.",
            evolver_evidence_needed="Official ToS pages and direct buyer signals.",
        )

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("continuation required: evolver decision Narrow requires another round", result.stdout)

    def test_check_final_requires_final_report(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing file: report.md", result.stdout)

    def test_legacy_schema_does_not_skip_evolver_final_gate(self) -> None:
        survey_dir = self.init_round()
        metadata = survey_dir / ".super-survey.json"
        metadata.write_text(
            '{"topic": "AI recruiting agent", "language": "en", "report_schema_version": 1}\n',
            encoding="utf-8",
        )
        (survey_dir / "report.md").write_text(
            """# AI recruiting agent

## Executive Summary

Continue with a narrower policy-first validation path.

## Key Findings

Demand signals exist, but payment and policy evidence are incomplete.

## Comparison Or Analysis

Manual workflows and job trackers are the main substitutes.

## Recommendation

Run a policy-first round before building.

## Limitations

No direct buyer interviews were conducted.

## Source Notes

Sources were checked during this round and remain directional.
""",
            encoding="utf-8",
        )
        self._write_substantive_required_files(survey_dir, include_report=False)

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("legacy report schema detected", result.stdout)
        self.assertIn("evolver decision Narrow requires another round", result.stdout)

    def test_validate_evidence_rejects_duplicate_claim_ids(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)
        (survey_dir / "claims.jsonl").write_text(
            '{"claim_id":"C1","claim":"Users repeat this workflow.","supporting_evidence_ids":["E1"],"status":"supported"}\n'
            '{"claim_id":"C1","claim":"Policy risk matters.","supporting_evidence_ids":["E2"],"status":"supported"}\n'
            '{"claim_id":"C3","claim":"Paid willingness remains plausible but unproven.","supporting_evidence_ids":["E3"],"status":"partial"}\n',
            encoding="utf-8",
        )

        result = run_cli("validate-evidence", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("claims.jsonl: duplicate claim_id C1", result.stdout)

    def test_validate_evidence_rejects_claims_weakly_supported_by_linked_evidence(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)
        (survey_dir / "claims.jsonl").write_text(
            '{"claim_id":"C1","claim":"Mars has 500 million residents in 2026.","supporting_evidence_ids":["E1"],"status":"supported"}\n'
            '{"claim_id":"C2","claim":"Policy risk matters.","supporting_evidence_ids":["E2"],"status":"supported"}\n'
            '{"claim_id":"C3","claim":"Paid willingness remains plausible but unproven.","supporting_evidence_ids":["E3"],"status":"partial"}\n',
            encoding="utf-8",
        )

        result = run_cli("validate-evidence", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("claims.jsonl: C1 has weak support from linked evidence", result.stdout)

    def test_corrupt_metadata_warns_and_does_not_skip_registry_validation(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_registry=False)
        (survey_dir / ".super-survey.json").write_text("{not json", encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("metadata warning", result.stdout)
        self.assertIn("could not be parsed", result.stdout)
        self.assertIn("sources.jsonl: expected at least", result.stdout)

    def test_check_passes_when_every_required_section_has_substance(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_rejects_process_artifacts_that_only_summarize_framework_audit(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )

        replacements = {
            "00-brief.md": (
                "Research Framework",
                "Selected framework: product opportunity plus policy-risk framework.\n"
                "Dimensions to cover: user pain, workflow frequency, willingness to pay, policy constraints, substitutes, distribution, and implementation difficulty.\n"
                "Why this framework fits the decision: demand and launch constraints both matter.\n"
                "Dimensions intentionally out of scope: enterprise procurement and recruiter-side workflows."
            ),
            "01-research.md": (
                "Framework Coverage",
                "Framework dimensions covered: user pain, workflow frequency, policy constraints, substitutes, and early pricing signals.\n"
                "Weak or missing dimensions: willingness to pay and distribution economics.\n"
                "Next evidence target from framework gaps: official policy pages and direct buyer pricing signals."
            ),
            "01-brainstorm.md": (
                "Candidate Next Moves",
                "Compare policy, pricing, substitutes, distribution, and implementation difficulty as possible next moves."
            ),
            "01-redteam.md": (
                "Strongest Objections",
                "Users may not trust automation, policy can block delivery, and paid acquisition can weaken margin."
            ),
            "01-synthesis.md": (
                "Framework-Based Synthesis",
                "Strongest dimensions: workflow repetition and policy risk evidence.\n"
                "Weakest dimensions: direct willingness to pay and distribution economics.\n"
                "Cross-dimension judgment: demand is plausible, but policy and payment constraints should drive the next round."
            ),
            "01-evolver.md": (
                "Round Evidence Quality Gate",
                "Evidence coverage this round: directional signals exist.\n"
                "Framework coverage this round: demand and policy dimensions are covered; payment and distribution remain weak.\n"
                "Weakest evidence or framework dimensions: payment proof and distribution depth."
            ),
        }
        for filename, (heading, body) in replacements.items():
            path = survey_dir / filename
            text = path.read_text(encoding="utf-8")
            text = re.sub(
                rf"(?ms)^## {re.escape(heading)}\n\n.*?(?=^## |\Z)",
                f"## {heading}\n\n{body}\n",
                text,
            )
            path.write_text(text, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("00-brief.md: Research Framework must include subheadings", result.stdout)
        self.assertIn("01-research.md: Framework Coverage must include subheadings", result.stdout)
        self.assertIn("01-brainstorm.md: Candidate Next Moves must include subheadings", result.stdout)
        self.assertIn("01-redteam.md: Strongest Objections must include subheadings", result.stdout)
        self.assertIn("01-synthesis.md: Framework-Based Synthesis must include subheadings", result.stdout)
        self.assertIn("01-evolver.md: Round Evidence Quality Gate must include subheadings", result.stdout)

    def test_check_uses_evidence_driven_refined_framework_dimensions_from_index(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        brief_path = survey_dir / "00-brief.md"
        brief = brief_path.read_text(encoding="utf-8")
        brief = brief.replace(
            "Dimensions to cover: user pain, workflow frequency, willingness to pay, policy constraints, substitutes, distribution, and implementation difficulty.",
            "Dimensions to cover: user pain, workflow frequency.",
        )
        brief_path.write_text(brief, encoding="utf-8")

        index_path = survey_dir / "index.md"
        index = index_path.read_text(encoding="utf-8")
        index = index.replace(
            "Current dimensions: user pain, workflow frequency, willingness to pay, policy constraints, substitutes, distribution, and implementation difficulty.",
            "Current dimensions: policy constraints.\n"
            "Evidence trigger for changes: C2/E2 showed policy is the veto dimension for this round.\n"
            "Original question/core preserved: yes; the survey still evaluates whether to continue discovery.",
        )
        index_path.write_text(index, encoding="utf-8")

        replacements = {
            "01-research.md": "Framework Coverage",
            "01-brainstorm.md": "Candidate Next Moves",
            "01-redteam.md": "Strongest Objections",
            "01-synthesis.md": "Framework-Based Synthesis",
            "01-evolver.md": "Round Evidence Quality Gate",
        }
        for filename, heading in replacements.items():
            path = survey_dir / filename
            text = path.read_text(encoding="utf-8")
            text = re.sub(
                rf"(?ms)^## {re.escape(heading)}\n\n.*?(?=^## |\Z)",
                f"## {heading}\n\n### Policy Constraints\n\n"
                "Current judgment: platform rules are the decision bottleneck. "
                "Evidence impact: C2/E2 moves the next round toward official ToS review. "
                "Counterpoint: assisted workflows may still be allowed. "
                "Decision effect: continue only if a compliant workflow remains plausible.\n",
                text,
            )
            path.write_text(text, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_final_report_rejects_bullet_dominated_body(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=92,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        report_path = survey_dir / "report.md"
        report = report_path.read_text(encoding="utf-8")
        for heading in (
            "Executive Summary",
            "User Pain",
            "Main Narrative",
            "Decision Logic",
            "Final Recommendation",
            "What Could Change This Conclusion",
            "Next Actions",
            "Limits Of This Report",
        ):
            report = re.sub(
                rf"(?ms)^## {re.escape(heading)}\n\n.*?(?=^## |\Z)",
                f"## {heading}\n\n"
                "- Bullet one with a factual-looking claim.\n"
                "- Bullet two with another claim.\n"
                "- Bullet three with a terse conclusion.\n",
                report,
            )
        report_path.write_text(report, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("report.md: prose-first rule violated; report body uses too many list lines", result.stdout)

    def _write_substantive_required_files(
        self,
        survey_dir: Path,
        include_report: bool = True,
        report_score: int = 92,
        continuation_decision: str | None = None,
        include_wiki_notes: bool = True,
        include_registry: bool = True,
        evolver_decision: str = "Narrow.",
        evolver_evidence_needed: str = "Official ToS pages, pricing pages, and direct buyer signals.",
    ) -> None:
        if include_registry:
            write_jsonl(
                survey_dir / "sources.jsonl",
                [
                    {
                        "source_id": "S1",
                        "title": "Example",
                        "url": "https://example.com",
                        "source_type": "primary",
                        "date_checked": "2026-06-13",
                        "credibility": "medium",
                    },
                    {
                        "source_id": "S2",
                        "title": "Policy Example",
                        "url": "https://example.com/policy",
                        "source_type": "primary",
                        "date_checked": "2026-06-13",
                        "credibility": "high",
                    },
                    {
                        "source_id": "S3",
                        "title": "Pricing Example",
                        "url": "https://example.com/pricing",
                        "source_type": "secondary",
                        "date_checked": "2026-06-13",
                        "credibility": "medium",
                    },
                ],
            )
            write_jsonl(
                survey_dir / "evidence.jsonl",
                [
                    {
                        "evidence_id": "E1",
                        "source_id": "S1",
                        "quote_or_summary": "Users repeat this workflow.",
                        "locator": "page",
                        "confidence": "medium",
                    },
                    {
                        "evidence_id": "E2",
                        "source_id": "S2",
                        "quote_or_summary": "Policy constraints can affect automation.",
                        "locator": "terms",
                        "confidence": "high",
                    },
                    {
                        "evidence_id": "E3",
                        "source_id": "S3",
                        "quote_or_summary": "Comparable tools use paid subscriptions.",
                        "locator": "pricing page",
                        "confidence": "medium",
                    },
                ],
            )
            write_jsonl(
                survey_dir / "claims.jsonl",
                [
                    {
                        "claim_id": "C1",
                        "claim": "Users repeat this workflow.",
                        "supporting_evidence_ids": ["E1"],
                        "status": "supported",
                    },
                    {
                        "claim_id": "C2",
                        "claim": "Policy risk matters.",
                        "supporting_evidence_ids": ["E2"],
                        "status": "supported",
                    },
                    {
                        "claim_id": "C3",
                        "claim": "Paid willingness remains plausible but unproven.",
                        "supporting_evidence_ids": ["E3"],
                        "status": "partial",
                    },
                ],
            )
        wiki_status = (
            "Wiki Tool Attempted: karpathy-llm-wiki.\n"
            "Wiki Ingest Result: not built; no initialized project raw/wiki directory was available.\n"
            "Wiki Fallback Reason: local Markdown index maintained for this survey.\n"
            "Wiki Artifact Path: index.md only."
            if include_wiki_notes
            else "Not built: no initialized wiki backend."
        )
        quality_decision = continuation_decision or (
            "Pass / Continue Decision: pass; finalize the report because no decision-changing unknown remains desk-researchable, and the evolver next evidence requires external validation through user interviews."
        )
        write_markdown(
            survey_dir / "00-brief.md",
            "Survey Brief: AI recruiting agent",
            {
                "User Question": "Should we build this?",
                "Superpowers Brainstorming Gate": "Completed: decision, buyer, and stopping criteria recorded.",
                "Decision To Make": "Decide whether to continue.",
                "Research Lens": "Use a general product opportunity lens with policy and willingness-to-pay checks.",
                "Research Framework": (
                    "Selected framework: product opportunity plus policy-risk framework.\n"
                    "Dimensions to cover: user pain, workflow frequency, willingness to pay, policy constraints, substitutes, distribution, and implementation difficulty.\n"
                    "Why this framework fits the decision: the decision is whether to continue discovery, so both demand and launch constraints matter.\n"
                    "Dimensions intentionally out of scope: enterprise procurement and recruiter-side workflows are out of scope for this pass.\n\n"
                    "### User Pain\n"
                    "Core question: whether the target workflow is painful enough to motivate change. Evidence needed: repeated complaints and workaround behavior.\n\n"
                    "### Workflow Frequency\n"
                    "Core question: whether the job-search workflow happens often enough for repeated use. Evidence needed: application frequency and routine depth.\n\n"
                    "### Willingness To Pay\n"
                    "Core question: whether users would pay from a personal budget. Evidence needed: direct pricing signals and paid alternatives.\n\n"
                    "### Policy Constraints\n"
                    "Core question: whether platform rules allow the assisted workflow. Evidence needed: official ToS and enforcement signals.\n\n"
                    "### Substitutes\n"
                    "Core question: whether low-cost substitutes already solve enough of the problem. Evidence needed: spreadsheet, tracker, and incumbent usage.\n\n"
                    "### Distribution\n"
                    "Core question: whether the product can reach active job seekers efficiently. Evidence needed: channel signals and acquisition constraints.\n\n"
                    "### Implementation Difficulty\n"
                    "Core question: whether the workflow can be built reliably and safely. Evidence needed: technical constraints and operational risks."
                ),
                "Decision Evidence Standard": "Require current primary sources for policy claims and direct signals for payment claims.",
                "Decision Frame Integrity": (
                    "Original question: should we build this?\n"
                    "Original user frame: the user asks whether to build, which is an initial exploration frame rather than proof of demand.\n"
                    "Known facts: the target workflow is repeated and policy can affect automation.\n"
                    "Implicit assumptions: users will pay, channels are reachable, and assisted automation is allowed.\n"
                    "Subjective judgments: the idea feels promising because the workflow is annoying.\n"
                    "Missing information: direct buyer commitment, official policy boundaries, and acquisition economics.\n"
                    "Stakeholders: active job seekers, job boards, builders, compliance reviewers, and potential competitors.\n"
                    "Reframed objective: decide whether another discovery round is justified before implementation.\n"
                    "Competing objectives: speed, accuracy, compliance safety, user value, and build cost.\n"
                    "What not to optimize for: proving the initial idea, pleasing the user, or rejecting an exaggerated certainty claim.\n"
                    "Decision frame: evaluate whether to continue discovery, not whether guaranteed success is proven.\n"
                    "Not pre-decided: keep the original question intact instead of turning it into an easier-to-kill demand for certainty.\n"
                    "Allowed narrowing: narrow only when evidence or red-team critique justifies the narrower target."
                ),
                "Decision Optimization Contract": (
                    "Original question: should we build this?\n"
                    "Reconstructed objective function: maximize learning value and user benefit while limiting policy, cost, and build risk.\n"
                    "Candidate actions: continue desk research, run interviews, build a narrow prototype, wait, or stop.\n"
                    "Do nothing / wait / continue research option: waiting is acceptable if policy evidence remains weak.\n"
                    "Hard constraints: platform terms, privacy, budget, and reliability.\n"
                    "Soft constraints: speed, user trust, and implementation simplicity.\n"
                    "Missing constraints: exact budget, timeline, and risk tolerance.\n"
                    "Success criteria: a compliant paid workflow with reachable users.\n"
                    "Failure criteria: no policy-safe workflow or no credible payment path.\n"
                    "Opportunity cost: time spent here delays other product discovery.\n"
                    "Reversibility: desk research and interviews are reversible; full implementation is less reversible.\n"
                    "Implied expectations: users will trust assistance, pay enough, and tolerate a narrow workflow.\n"
                    "Decision-changing evidence: official policy blocks, paid pilot commitments, or strong substitute evidence."
                ),
                "Target Customer": "US software engineers actively applying for jobs.",
                "Success Criteria": "Evidence supports a paid workflow.",
                "Disqualifying Conditions": "Platform rules block reliable delivery.",
                "Initial Assumptions": "Users already apply repeatedly.",
                "Continuation Policy": (
                    "Start with the next research round; decide whether to continue only after evidence, red-team critique, synthesis, and the raw evolver decision are written.\n"
                    "Keep the round count open until the round artifacts determine whether to continue or stop."
                ),
            },
        )
        write_markdown(
            survey_dir / "index.md",
            "Survey Index: AI recruiting agent",
            {
                "Current Thesis": "The thesis is plausible but unproven.",
                "Current Evidence-Bound Conclusion": "Continue one narrowed round before final reporting.",
                "Round Ledger": "Round 1 found demand signals.",
                "Continuation Status": "Continue if the evolver says Narrow, Pivot, or Keep; finalize after Final/Kill plus passing report quality.",
                "Next Research Target": "Can policy and pricing evidence support a narrower workflow?",
                "Why Not Final Yet": "The latest round still needs either a Final/Kill decision or a final report gate.",
                "Open Questions": "Policy risk remains open.",
                "Source Inventory": "Official platform terms and competitor pages.",
                "Framework Refinement Log": (
                    "Current dimensions: user pain, workflow frequency, willingness to pay, policy constraints, substitutes, distribution, and implementation difficulty.\n"
                    "Evidence trigger for changes: no change yet; the first round still uses the initial framework.\n"
                    "Original question/core preserved: yes; the survey still evaluates whether to continue discovery."
                ),
                "Final Report Quality Gate": (
                    f"Total Score: {report_score} / 100.\n"
                    "Score Breakdown: objective integrity 18, sources 14, evidence 18, analysis 18, actionability 14, structure 8.\n"
                    "Anti-sycophancy / objective-function integrity: 18 / 20.\n"
                    "Objective reconstruction quality: clear enough to preserve the original decision.\n"
                    "User-frame challenge quality: the report challenged the prompt without rewriting it into a stronger claim.\n"
                    f"{quality_decision}\n"
                    "Lowest-Scoring Areas: evidence completeness and analysis depth remain monitored, but both are above the pass threshold.\n"
                    "Next Round Focus: none for desk research; move to user interviews if further validation is needed."
                ),
                "Wiki / Graph Index Status": wiki_status,
                "Decision Log": "Continue one narrowed round.",
            },
        )
        if include_report:
            write_markdown(
                survey_dir / "report.md",
                "AI recruiting agent",
                {
                    "Executive Summary": (
                        "Continue with a narrower policy-first validation path.\n"
                        "Confidence is medium because demand is visible but policy and payment remain unresolved."
                    ),
                    "User Pain": (
                        "Job seekers repeat a frustrating workflow across many applications, so the pain is concrete rather than abstract. The remaining question is whether the frustration changes behavior enough to justify switching from manual tracking.\n\n"
                    ),
                    "Workflow Frequency": (
                        "The workflow can recur several times per week during active job searches, which supports repeated use if trust is adequate. Frequency still varies by segment, so the report treats this as a validation target rather than settled retention proof.\n\n"
                    ),
                    "Willingness To Pay": (
                        "Comparable tools use paid subscriptions, but direct willingness-to-pay evidence remains partial and should constrain confidence. This dimension weakens the case for immediate build because comparable pricing is not the same as committed buyer demand.\n\n"
                    ),
                    "Policy Constraints": (
                        "Platform terms and automation limits can block the core workflow, so policy evidence has veto power over the idea. The recommendation therefore prioritizes official terms and assisted-workflow boundaries before any broad automation design.\n\n"
                    ),
                    "Substitutes": (
                        "Spreadsheets, job trackers, and manual application routines are credible substitutes with low switching cost. A viable product has to beat these substitutes on effort reduction or outcome quality, not only on interface polish.\n\n"
                    ),
                    "Distribution": (
                        "Distribution likely depends on search, communities, and browser workflows; paid acquisition may weaken margins. This makes high-intent entry points and organic workflow placement important evidence targets for the next pass.\n\n"
                    ),
                    "Implementation Difficulty": (
                        "Reliable form assistance, user confirmation, and policy-safe operation make the build harder than a simple wrapper. A narrow copilot path can reduce risk, but full automation should wait until reliability and policy boundaries are clearer."
                    ),
                    "Main Narrative": (
                        "The opportunity is visible because job seekers repeat the same painful workflow across many applications.\n"
                        "The first pass found demand signals, but it also made policy risk the central issue rather than a side note.\n"
                        "That changes the recommendation from building a broad automation agent to validating a narrower assisted workflow."
                    ),
                    "Decision Logic": (
                        "The recommendation follows from three linked judgments.\n"
                        "First, repeated manual effort creates plausible demand.\n"
                        "Second, platform restrictions can destroy the core workflow if ignored.\n"
                        "Third, payment evidence is not yet strong enough to justify full implementation."
                    ),
                    "Final Recommendation": (
                        "Run a policy-first validation round before building.\n"
                        "Start full implementation after the compliance boundary and willingness to pay are clearer."
                    ),
                    "What Could Change This Conclusion": (
                        "The conclusion would improve if official terms allow the assisted workflow and users commit to paid trials.\n"
                        "It would worsen if official terms block automation or users prefer spreadsheets and existing job trackers."
                    ),
                    "Next Actions": (
                        "Collect official terms, compare competitors, and interview five active job seekers.\n"
                        "Record willingness to pay, the exact tasks users would delegate, and the fallback workflow if automation is limited."
                    ),
                    "Limits Of This Report": (
                        "No direct buyer interviews were conducted.\n"
                        "No live policy review by counsel was performed, so legal risk remains directional."
                    ),
                    "Appendix: Evidence Register": (
                        "Claim: users repeat the workflow. Evidence: public workflow signals. Confidence: medium. Contradictions: direct payment proof is missing.\n"
                        "Claim: platform risk matters. Evidence: job boards can restrict automation. Confidence: medium."
                    ),
                    "Appendix: Method And Source Quality": (
                        "Use current source discovery, official policy pages, competitor pages, and confidence labels.\n"
                        "Primary policy pages carry more weight than forum anecdotes."
                    ),
                    "Appendix: Red-Team Notes": (
                        "The strongest objection is platform policy risk and weak trust in automation.\n"
                        "Users may also prefer simple spreadsheets if outcome quality is not provable."
                    ),
                    "Appendix: Options Or Scenarios": (
                        "Option A: continue policy validation. Option B: stop if terms block the workflow.\n"
                        "Option C: pivot to a personal job-search CRM if automation is too risky."
                    ),
                    "Appendix: Source Notes": (
                        "Sources were checked during this round and remain directional.\n"
                        "Future rounds should record URLs, dates checked, and contradictions."
                    ),
                },
            )
        write_markdown(
            survey_dir / "01-research.md",
            "Round 1 Research",
            {
                "Research Question": "Can users pay for this workflow?",
                "Source Registry Updates": (
                    "Canonical source registry: sources.jsonl.\n"
                    "This round adds S1 for the primary page and records only source_id-level notes here."
                ),
                "Claim And Evidence Notes": (
                    "Canonical claim/evidence registry: claims.jsonl and evidence.jsonl.\n"
                    "This round references C1 and E1 instead of duplicating the full evidence table."
                ),
                "Framework Coverage": (
                    "### User Pain\n"
                    "Finding: repeated application work creates visible pain. Evidence IDs: E1. Contradiction: pain intensity is not yet quantified. Confidence: medium.\n\n"
                    "### Workflow Frequency\n"
                    "Finding: active job seekers repeat the workflow enough to justify a repeated-use hypothesis. Evidence IDs: E1. Contradiction: frequency varies by user segment.\n\n"
                    "### Willingness To Pay\n"
                    "Finding: paid alternatives make payment plausible but not proven. Evidence IDs: E3. Contradiction: direct buyer commitment is missing.\n\n"
                    "### Policy Constraints\n"
                    "Finding: platform terms can affect automation scope. Evidence IDs: E2. Contradiction: assisted workflows may still be allowed.\n\n"
                    "### Substitutes\n"
                    "Finding: manual spreadsheets and job trackers remain credible substitutes. Evidence IDs: E1. Contradiction: substitutes may not solve execution burden.\n\n"
                    "### Distribution\n"
                    "Finding: channels are plausible but unproven. Evidence IDs: E3. Contradiction: paid acquisition may be inefficient.\n\n"
                    "### Implementation Difficulty\n"
                    "Finding: reliable assistance is harder than a simple wrapper. Evidence IDs: E2. Contradiction: a narrow copilot may reduce build risk.\n\n"
                    "Next evidence target from framework gaps: official policy pages and direct buyer pricing signals."
                ),
                "Findings": "There are repeated workflow signals.",
                "Data Quality Notes": (
                    "- Search Tool Used: tavily-search.\n"
                    "- Tavily Fallback Reason: none.\n"
                    "- Query And Filter Notes: official pages and competitor pages.\n"
                    "- Evidence is directional, not decisive."
                ),
            },
        )
        write_markdown(
            survey_dir / "01-brainstorm.md",
            "Round 1 Brainstorming Checkpoint",
            {
                "Brainstorming Status": "Completed after initial research.",
                "Current Framing": "Focus on job seekers rather than recruiters.",
                "Clarifying Questions": "Can policy risk be reduced?",
                "Candidate Next Moves": (
                    "### User Pain\n"
                    "Next move: test whether repeated frustration maps to a must-have workflow rather than a convenience.\n\n"
                    "### Workflow Frequency\n"
                    "Next move: estimate how often active job seekers repeat the exact task sequence.\n\n"
                    "### Willingness To Pay\n"
                    "Next move: compare paid tools and ask for direct price commitment.\n\n"
                    "### Policy Constraints\n"
                    "Next move: inspect official terms before designing any automation path.\n\n"
                    "### Substitutes\n"
                    "Next move: compare spreadsheets, trackers, and browser extensions as substitute paths.\n\n"
                    "### Distribution\n"
                    "Next move: identify search, community, and workflow-entry channels.\n\n"
                    "### Implementation Difficulty\n"
                    "Next move: split the build into assisted workflow, user confirmation, and automation boundary."
                ),
                "Preferred Exploration Path": "Check policy and pricing next.",
                "Design Notes For Next Round": "Use primary ToS pages and pricing evidence.",
            },
        )
        write_markdown(
            survey_dir / "01-redteam.md",
            "Round 1 Red-Team Challenge",
            {
                "Strongest Objections": (
                    "### User Pain\n"
                    "Objection: frustration may not be painful enough to change behavior if current workarounds are adequate.\n\n"
                    "### Workflow Frequency\n"
                    "Objection: the workflow may be intense only during short job-search windows, weakening retention.\n\n"
                    "### Willingness To Pay\n"
                    "Objection: users may like the idea but refuse to pay before outcomes are proven.\n\n"
                    "### Policy Constraints\n"
                    "Objection: platform terms may block the most valuable automation path.\n\n"
                    "### Substitutes\n"
                    "Objection: spreadsheets and existing trackers may be good enough for most users.\n\n"
                    "### Distribution\n"
                    "Objection: reaching active job seekers at the right moment may be expensive.\n\n"
                    "### Implementation Difficulty\n"
                    "Objection: reliability, user confirmation, and privacy constraints can turn a simple concept into a complex product."
                ),
                "Incumbent Response": "Job boards can block the workflow.",
                "Alternative Explanations Or Substitutes": "Users may prefer manual spreadsheets or existing job trackers.",
                "Data And Access Risks": "Data access can change without notice.",
                "Legal, ToS, Privacy, Or Compliance Risks": "Terms may restrict automated submission.",
                "Monetization And Distribution Risks": "Paid acquisition could erase margin.",
                "Kill Criteria Checked": "No verified kill criterion was found, but policy risk remains unresolved.",
                "Falsification Tests": "Stop if policy blocks the core workflow.",
            },
        )
        write_markdown(
            survey_dir / "01-synthesis.md",
            "Round 1 Synthesis",
            {
                "Updated Conclusion": "Continue only with a narrower workflow.",
                "Confidence": "Medium.",
                "Decision Rationale": "Continue because demand signals exist, but narrow around policy risk.",
                "Framework-Based Synthesis": (
                    "### User Pain\n"
                    "Judgment: user pain is plausible and supports continued discovery, but intensity still needs direct validation.\n\n"
                    "### Workflow Frequency\n"
                    "Judgment: repeated use is plausible during active job searches, though long-term retention is uncertain.\n\n"
                    "### Willingness To Pay\n"
                    "Judgment: this is one of the weakest dimensions because comparable pricing is not direct commitment.\n\n"
                    "### Policy Constraints\n"
                    "Judgment: policy is a veto dimension and should drive the next round before implementation.\n\n"
                    "### Substitutes\n"
                    "Judgment: substitutes are credible, so the product must outperform manual tracking on outcome or effort.\n\n"
                    "### Distribution\n"
                    "Judgment: channels are still speculative and should constrain confidence.\n\n"
                    "### Implementation Difficulty\n"
                    "Judgment: a narrow assisted workflow can reduce technical risk, but full automation remains risky.\n\n"
                    "Cross-dimension judgment: demand is plausible, but policy and payment constraints should drive the next round."
                ),
                "Sensitivity And Counterfactuals": (
                    "Key variable: policy permissiveness. Current assumption: assisted workflows may be allowed. If better: a broader product path opens. If worse: automation should be stopped. Evidence needed: official terms and enforcement examples. Decision impact: this is a veto variable.\n"
                    "Key variable: willingness to pay. Current assumption: paid intent is plausible but unproven. If better: a narrow paid prototype becomes attractive. If worse: continue only as a free utility or stop. Evidence needed: direct buyer commitments. Decision impact: changes build priority."
                ),
                "What Changed": "Policy risk became the main blocker.",
                "Remaining Unknowns": "Actual willingness to pay is unknown.",
                "Evolved Next Research Target": "Can a browser-assisted workflow comply with job-board terms?",
                "Recommended Next Action": "Run a policy-first round.",
            },
        )
        write_markdown(
            survey_dir / "01-evolver.md",
            "Round 1 Lightweight Evolver",
            {
                "Current Thesis": "The job seeker workflow may be viable if policy risk is manageable.",
                "Probe Results": (
                    "| Probe | Answer | Strength |\n"
                    "|---|---|---|\n"
                    "| Buyer | Active job seekers pay from personal budget | weak |"
                ),
                "Persona Judgments": (
                    "| Persona | Verdict | Reason |\n"
                    "|---|---|---|\n"
                    "| Skeptical buyer | concern | Trust and outcomes are unproven |"
                ),
                "Decision": evolver_decision,
                "Round Evidence Quality Gate": (
                    "### User Pain\n"
                    "Coverage quality: medium. Weakest gap: direct severity evidence. Next target: confirm whether pain changes behavior.\n\n"
                    "### Workflow Frequency\n"
                    "Coverage quality: medium. Weakest gap: segment-level frequency. Next target: estimate repeated use during active searches.\n\n"
                    "### Willingness To Pay\n"
                    "Coverage quality: weak. Weakest gap: direct payment proof. Next target: collect pricing commitment or comparable conversion evidence.\n\n"
                    "### Policy Constraints\n"
                    "Coverage quality: medium. Weakest gap: exact automation boundary. Next target: inspect official ToS pages.\n\n"
                    "### Substitutes\n"
                    "Coverage quality: medium. Weakest gap: substitute satisfaction. Next target: compare manual trackers and incumbents.\n\n"
                    "### Distribution\n"
                    "Coverage quality: weak. Weakest gap: acquisition channel proof. Next target: identify high-intent entry points.\n\n"
                    "### Implementation Difficulty\n"
                    "Coverage quality: medium. Weakest gap: reliability under policy constraints. Next target: narrow the build path.\n\n"
                    "Implied expectation check: users must trust the assistant and pay for repeated help.\n"
                    "Decision tree triggers: permissive policy moves to pricing; restrictive policy moves to pivot or stop.\n"
                    "Bayesian update needed: official terms and paid trial evidence.\n"
                    "Kill scope (if Kill): thesis / path / candidate action / original question.\n"
                    "Original question still open: yes unless the original decision itself is answered.\n"
                    "If original question remains open, write the pivot or next answer path: compare policy-safe alternatives.\n"
                    "Continue / stop implication: continue unless the raw decision is Final/Kill and final report quality later passes."
                ),
                "Next Research Target": "Can active US software job seekers use a browser-assisted copilot under platform constraints?",
                "Evidence Needed Next": evolver_evidence_needed,
            },
        )


if __name__ == "__main__":
    unittest.main()
