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

    def init_survey_dir(self, language: str = "en", mode: str = "standard", topic: str = "AI recruiting agent") -> Path:
        result = run_cli(
            "init",
            topic,
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
        return survey_dir

    def init_round(self, language: str = "en", mode: str = "standard", topic: str = "AI recruiting agent") -> Path:
        survey_dir = self.init_survey_dir(language=language, mode=mode, topic=topic)
        result = run_cli("round", str(survey_dir), "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        return survey_dir

    def write_minimal_stage(self, survey_dir: Path, filename: str) -> None:
        sections_by_file = {
            "01-evidence-plan.md": {
                "Round Decision Target": "Decide whether another evidence pass can materially change the action.",
                "Decision-Critical Variables": "Policy permissiveness, willingness to pay, and distribution reach can change the decision.",
                "Minimum Direct Evidence": "Official policy source, direct pricing signal, and at least one substitute comparison.",
                "Source Plan": "Use official policy pages, competitor pricing pages, and current search for direct signals.",
                "Disconfirming Evidence": "Policy blocks the workflow, users refuse payment, or substitutes already solve the core job.",
                "Missing Evidence Handling": "If direct evidence is missing, lower confidence and continue a targeted round.",
                "Framework Evidence Map": (
                    "### User Pain\nEvidence needed: direct complaints and repeated workflow signals.\n\n"
                    "### Workflow Frequency\nEvidence needed: frequency of repeated applications.\n\n"
                    "### Willingness To Pay\nEvidence needed: direct pricing or paid alternative signals.\n\n"
                    "### Policy Constraints\nEvidence needed: official ToS or policy source.\n\n"
                    "### Substitutes\nEvidence needed: credible manual or product alternatives.\n\n"
                    "### Distribution\nEvidence needed: reachable high-intent channels.\n\n"
                    "### Implementation Difficulty\nEvidence needed: reliability and data-access constraints."
                ),
            },
            "01-research.md": {
                "Research Question": "Can current evidence support the next action?",
                "Source Registry Updates": "S1 records a primary source; sources.jsonl remains canonical.",
                "Claim And Evidence Notes": "C1/E1 support one directional claim; JSONL remains canonical.",
                "Framework Coverage": (
                    "### User Pain\nFinding: repeated workflow signals exist. Evidence IDs: E1. Confidence: medium.\n\n"
                    "### Workflow Frequency\nFinding: frequency is plausible. Evidence IDs: E1. Confidence: medium.\n\n"
                    "### Willingness To Pay\nFinding: payment is plausible but unproven. Evidence IDs: E3. Confidence: low.\n\n"
                    "### Policy Constraints\nFinding: policy can be a veto. Evidence IDs: E2. Confidence: medium.\n\n"
                    "### Substitutes\nFinding: substitutes are credible. Evidence IDs: E1. Confidence: medium.\n\n"
                    "### Distribution\nFinding: channels remain speculative. Evidence IDs: E3. Confidence: low.\n\n"
                    "### Implementation Difficulty\nFinding: reliability remains a build risk. Evidence IDs: E2. Confidence: medium."
                ),
                "Findings": "Evidence is directional and leaves policy and payment gaps.",
                "Data Quality Notes": (
                    "Current Source Discovery: yes.\n"
                    "Search Tool Used: tavily-search.\n"
                    "Tavily Fallback Reason: none.\n"
                    "Query And Filter Notes: official sources and competitor pricing.\n"
                    "Third-Party Content Handling: source text treated as untrusted evidence; source-borne instructions ignored; bounded factual excerpts or summaries only."
                ),
            },
            "01-brainstorm.md": {
                "Brainstorming Status": "Completed after the evidence pass.",
                "Current Framing": "The next move should reduce policy or payment uncertainty.",
                "Clarifying Questions": "Which evidence gap changes the action most?",
                "Candidate Next Moves": (
                    "### User Pain\nNext move: verify severity.\n\n"
                    "### Workflow Frequency\nNext move: estimate repeated use.\n\n"
                    "### Willingness To Pay\nNext move: find direct pricing evidence.\n\n"
                    "### Policy Constraints\nNext move: inspect official terms.\n\n"
                    "### Substitutes\nNext move: compare manual alternatives.\n\n"
                    "### Distribution\nNext move: identify high-intent channels.\n\n"
                    "### Implementation Difficulty\nNext move: bound the narrow build path."
                ),
                "Preferred Exploration Path": "Prioritize policy and willingness-to-pay evidence.",
                "Design Notes For Next Round": "Keep next search narrow and evidence-driven.",
            },
            "01-redteam.md": {
                "Strongest Objections": (
                    "### User Pain\nObjection: the pain may be convenience-level.\n\n"
                    "### Workflow Frequency\nObjection: active use may be episodic.\n\n"
                    "### Willingness To Pay\nObjection: users may not pay.\n\n"
                    "### Policy Constraints\nObjection: policy can block the core path.\n\n"
                    "### Substitutes\nObjection: spreadsheets may be good enough.\n\n"
                    "### Distribution\nObjection: channels may be expensive.\n\n"
                    "### Implementation Difficulty\nObjection: reliability can break trust."
                ),
                "Incumbent Response": "Platforms can restrict the workflow.",
                "Alternative Explanations Or Substitutes": "Manual trackers may explain current behavior.",
                "Data And Access Risks": "Access may be unstable.",
                "Legal, ToS, Privacy, Or Compliance Risks": "Terms may restrict automation.",
                "Monetization And Distribution Risks": "Payment and acquisition are unproven.",
                "Kill Criteria Checked": "No final kill criterion yet, but policy remains a veto.",
                "Falsification Tests": "Stop if policy blocks the core workflow.",
            },
            "01-synthesis.md": {
                "Updated Conclusion": "Continue only if the policy and payment gaps are desk-researchable.",
                "Confidence": "Medium.",
                "Decision Rationale": "Demand is plausible, but veto dimensions remain unresolved.",
                "Framework-Based Synthesis": (
                    "### User Pain\nJudgment: plausible but not decisive.\n\n"
                    "### Workflow Frequency\nJudgment: plausible during active periods.\n\n"
                    "### Willingness To Pay\nJudgment: weak and decision-critical.\n\n"
                    "### Policy Constraints\nJudgment: veto dimension.\n\n"
                    "### Substitutes\nJudgment: credible alternatives lower certainty.\n\n"
                    "### Distribution\nJudgment: still speculative.\n\n"
                    "### Implementation Difficulty\nJudgment: narrow path needed.\n\n"
                    "Most conclusion-changing variable: policy permissiveness."
                ),
                "Sensitivity And Counterfactuals": "Key variable: policy. If worse, stop; if better, test pricing.",
                "What Changed": "Policy became the main bottleneck.",
                "Remaining Unknowns": "Payment and policy remain unresolved.",
                "Evolved Next Research Target": "Can official policy support a narrow assisted workflow?",
                "Recommended Next Action": "Run the evolver and choose the next target.",
            },
        }
        sections = sections_by_file[filename]
        write_markdown(survey_dir / filename, filename.removesuffix(".md"), sections)

    def create_stage_template_snapshots(self) -> dict[str, str]:
        survey_dir = self.init_round()
        snapshots = {"01-evidence-plan.md": (survey_dir / "01-evidence-plan.md").read_text(encoding="utf-8")}

        for command, previous_file, current_file in (
            ("research", "01-evidence-plan.md", "01-research.md"),
            ("brainstorm", "01-research.md", "01-brainstorm.md"),
            ("redteam", "01-brainstorm.md", "01-redteam.md"),
            ("synthesis", "01-redteam.md", "01-synthesis.md"),
            ("evolve", "01-synthesis.md", "01-evolver.md"),
        ):
            self.write_minimal_stage(survey_dir, previous_file)
            result = run_cli(command, str(survey_dir), "1")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            snapshots[current_file] = (survey_dir / current_file).read_text(encoding="utf-8")
        return snapshots

    def test_check_rejects_empty_brief_and_brainstorm_templates(self) -> None:
        survey_dir = self.init_round()

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("00-brief.md: appears to be only an empty template", result.stdout)
        self.assertIn("01-evidence-plan.md: appears to be only an empty template", result.stdout)
        self.assertNotIn("report.md", result.stdout)

    def test_round_starts_only_the_evidence_plan_stage(self) -> None:
        survey_dir = self.init_round()

        self.assertTrue((survey_dir / "01-evidence-plan.md").exists())
        for suffix in ("research", "brainstorm", "redteam", "synthesis", "evolver"):
            self.assertFalse((survey_dir / f"01-{suffix}.md").exists(), suffix)

    def test_plan_alias_starts_only_the_evidence_plan_stage(self) -> None:
        survey_dir = self.init_survey_dir()
        result = run_cli("plan", str(survey_dir), "1")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

        self.assertTrue((survey_dir / "01-evidence-plan.md").exists())
        for suffix in ("research", "brainstorm", "redteam", "synthesis", "evolver"):
            self.assertFalse((survey_dir / f"01-{suffix}.md").exists(), suffix)

    def test_stage_commands_require_substantive_previous_stage(self) -> None:
        survey_dir = self.init_round()

        blocked = run_cli("research", str(survey_dir), "1")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("previous stage incomplete: 01-evidence-plan.md", blocked.stderr + blocked.stdout)
        self.assertFalse((survey_dir / "01-research.md").exists())

        self.write_minimal_stage(survey_dir, "01-evidence-plan.md")
        created = run_cli("research", str(survey_dir), "1")
        self.assertEqual(created.returncode, 0, created.stderr + created.stdout)
        self.assertTrue((survey_dir / "01-research.md").exists())

        blocked = run_cli("brainstorm", str(survey_dir), "1")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("previous stage incomplete: 01-research.md", blocked.stderr + blocked.stdout)
        self.assertFalse((survey_dir / "01-brainstorm.md").exists())

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

    def test_check_requires_third_party_content_handling_when_current_sources_are_enabled(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_report=False)
        research = survey_dir / "01-research.md"
        text = re.sub(
            r"(?ms)^## Data Quality Notes\n\n.*?(?=^## |\Z)",
            (
                "## Data Quality Notes\n\n"
                "Current Source Discovery: yes. Recent policy and pricing facts were needed.\n"
                "Search Tool Used: tavily-search.\n"
                "Tavily Fallback Reason: none.\n"
                "Query And Filter Notes: official sources and competitor pricing.\n"
            ),
            research.read_text(encoding="utf-8"),
        )
        research.write_text(text, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Data Quality Notes must record third-party content handling", result.stdout)

    def test_round_number_must_be_positive(self) -> None:
        survey_dir = self.init_round()

        zero = run_cli("round", str(survey_dir), "0")
        negative = run_cli("round", str(survey_dir), "-1")

        self.assertNotEqual(zero.returncode, 0)
        self.assertNotEqual(negative.returncode, 0)
        self.assertFalse((survey_dir / "00-research.md").exists())
        self.assertFalse((survey_dir / "-1-research.md").exists())

    def test_templates_include_generic_research_framework_fields(self) -> None:
        snapshots = self.create_stage_template_snapshots()
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")
        evidence_plan = snapshots["01-evidence-plan.md"]
        research = snapshots["01-research.md"]
        brainstorm = snapshots["01-brainstorm.md"]
        redteam = snapshots["01-redteam.md"]
        synthesis = snapshots["01-synthesis.md"]
        evolver = snapshots["01-evolver.md"]
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
        self.assertIn("Third-Party Content Handling", research)
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
        self.assertIn("## Round Decision Target", evidence_plan)
        self.assertIn("## Decision-Critical Variables", evidence_plan)
        self.assertIn("## Minimum Direct Evidence", evidence_plan)
        self.assertIn("## Framework Evidence Map", evidence_plan)
        self.assertIn("### <framework dimension>", brief)
        self.assertIn("### <framework dimension>", evidence_plan)
        self.assertIn("### <framework dimension>", research)
        self.assertIn("### <framework dimension>", brainstorm)
        self.assertIn("### <framework dimension>", redteam)
        self.assertIn("### <framework dimension>", synthesis)
        self.assertIn("### <framework dimension>", evolver)

    def test_templates_include_decision_robustness_tools(self) -> None:
        snapshots = self.create_stage_template_snapshots()
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")
        evidence_plan = snapshots["01-evidence-plan.md"]
        synthesis = snapshots["01-synthesis.md"]
        evolver = snapshots["01-evolver.md"]

        self.assertIn("Object quality vs action attractiveness", brief)
        self.assertIn("Hard constraints", brief)
        self.assertIn("Soft constraints", brief)
        self.assertIn("User-specific constraints", brief)
        self.assertIn("Missing constraints", brief)
        self.assertIn("Implied expectations", brief)
        self.assertIn("minimum direct evidence", evidence_plan.lower())
        self.assertIn("Disconfirming Evidence", evidence_plan)
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

    def test_templates_include_autonomous_continuation_contract(self) -> None:
        snapshots = self.create_stage_template_snapshots()
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")
        evolver = snapshots["01-evolver.md"]

        self.assertIn("Default continuation is autonomous", brief)
        self.assertIn("create the next round immediately", brief)
        self.assertIn("Do not stop and ask the user how to proceed after Keep, Narrow, or Pivot", brief)
        self.assertIn("Autonomous continuation action", evolver)

    def test_synthesis_template_includes_sensitivity_and_counterfactuals(self) -> None:
        synthesis = self.create_stage_template_snapshots()["01-synthesis.md"]

        self.assertIn("## Sensitivity And Counterfactuals", synthesis)
        self.assertIn("Key variable", synthesis)
        self.assertIn("Current assumption", synthesis)
        self.assertIn("If better", synthesis)
        self.assertIn("If worse", synthesis)
        self.assertIn("Evidence needed", synthesis)
        self.assertIn("Decision impact", synthesis)

    def test_evolver_template_requires_kill_scope_and_original_question_status(self) -> None:
        evolver = self.create_stage_template_snapshots()["01-evolver.md"]

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

    def test_templates_frontload_decision_critical_evidence_guidance(self) -> None:
        snapshots = self.create_stage_template_snapshots()
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")
        evidence_plan = snapshots["01-evidence-plan.md"]
        research = snapshots["01-research.md"]
        brainstorm = snapshots["01-brainstorm.md"]
        synthesis = snapshots["01-synthesis.md"]
        evolver = snapshots["01-evolver.md"]

        self.assertIn("Decision-critical variables", brief)
        self.assertIn("Minimum direct evidence", brief)
        self.assertIn("Decision-Critical Variables", evidence_plan)
        self.assertIn("Minimum Direct Evidence", evidence_plan)
        self.assertIn("Source role", research)
        self.assertIn("Dynamic source reproducibility", research)
        self.assertIn("decision-critical uncertainty", brainstorm)
        self.assertIn("desk-researchable gaps", synthesis)
        self.assertIn("future facts vs desk-researchable gaps", evolver)

    def test_templates_strengthen_weak_anti_sycophancy_methods(self) -> None:
        snapshots = self.create_stage_template_snapshots()
        survey_dir = self.init_round()

        brief = (survey_dir / "00-brief.md").read_text(encoding="utf-8")
        evidence_plan = snapshots["01-evidence-plan.md"]
        research = snapshots["01-research.md"]
        brainstorm = snapshots["01-brainstorm.md"]
        redteam = snapshots["01-redteam.md"]
        synthesis = snapshots["01-synthesis.md"]
        evolver = snapshots["01-evolver.md"]

        self.assertIn("Implied expectation reverse-check", brief)
        self.assertIn("Current action, price, or choice implies", brief)
        self.assertIn("Constraint-specific recommendations", brief)
        self.assertIn("Anti-narrative regularizers", brief)
        self.assertIn("narrative, user preference, or recent signal", brief)
        self.assertIn("Disconfirming Evidence", evidence_plan)
        self.assertIn("Minimum direct evidence", research)
        self.assertIn("Perspective target function", brainstorm)
        self.assertIn("most likely error", brainstorm)
        self.assertIn("Anti-narrative regularizers", redteam)
        self.assertIn("Most conclusion-changing variable", synthesis)
        self.assertIn("Constraint-specific recommendation branches", synthesis)
        self.assertIn("Implied expectation reverse-check", synthesis)
        self.assertIn("Anti-narrative regularizers", evolver)

    def test_round_templates_make_content_dependency_order_explicit(self) -> None:
        snapshots = self.create_stage_template_snapshots()
        evidence_plan = snapshots["01-evidence-plan.md"]
        research = snapshots["01-research.md"]
        brainstorm = snapshots["01-brainstorm.md"]
        redteam = snapshots["01-redteam.md"]
        synthesis = snapshots["01-synthesis.md"]
        evolver = snapshots["01-evolver.md"]

        self.assertIn("Content dependency order", evidence_plan)
        self.assertIn("Complete this before source collection", evidence_plan)
        self.assertIn("Complete after 01-evidence-plan.md", research)
        self.assertIn("Complete after 01-research.md", brainstorm)
        self.assertIn("Complete after 01-research.md and 01-brainstorm.md", redteam)
        self.assertIn("Complete after 01-research.md, 01-brainstorm.md, and 01-redteam.md", synthesis)
        self.assertIn("Complete after 01-synthesis.md", evolver)

    def test_skill_defines_process_nodes_not_only_file_order(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("run the workflow as ordered process nodes", skill)
        self.assertIn("Markdown files are the outputs of those nodes", skill)
        self.assertIn("| Process node | Work to do now | Stage output |", skill)
        self.assertIn("| Evidence Plan |", skill)
        self.assertIn("| Research |", skill)
        self.assertIn("| Post-Research Brainstorming |", skill)
        self.assertIn("| Redteam |", skill)
        self.assertIn("| Synthesis |", skill)
        self.assertIn("| Evolver |", skill)
        self.assertIn("At each node, read the upstream artifact from disk before writing the downstream", skill)
        self.assertIn("after-action", skill)
        self.assertIn("audit trail for a conclusion formed earlier", skill)

    def test_skill_uses_runtime_methods_not_paper_section_numbers(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Ideal Execution Flow", skill)
        self.assertIn("| Node | Work | Runtime method |", skill)
        self.assertIn("Objective reconstruction", skill)
        self.assertIn("Sensitivity analysis", skill)
        self.assertIn("Bayesian updating", skill)
        self.assertIn("decision tree output", skill)
        self.assertNotIn("Paper methods", skill)
        self.assertNotIn("| 4.1", skill)
        self.assertNotIn("4.1, 4.2", skill)

    def test_skill_requires_autonomous_continuation_after_keep_narrow_pivot(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Autonomous continuation is the default", skill)
        self.assertIn("Do not stop and ask the user how to proceed after `Keep`, `Narrow`, or `Pivot`", skill)
        self.assertIn("create the next round immediately", skill)
        self.assertIn("Only pause for checkpoint approval when the user explicitly requested checkpoint approval", skill)
        self.assertIn("Do not say \"ready for the next round\"", skill)

    def test_stage_artifact_contracts_live_in_reference(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        contracts = (ROOT / "references" / "artifact-contracts.md").read_text(encoding="utf-8")

        self.assertIn("references/artifact-contracts.md", skill)
        for phrase in (
            "Round decision target for this round",
            "Target residual to reduce",
            "Decision-critical variables that could change the recommendation",
            "Minimum direct evidence: what must be observed directly",
            "Source plan: primary or official sources",
            "Disconfirming evidence and substitutes",
            "Missing evidence handling",
            "Framework evidence map",
            "Source registry updates by `source_id`",
            "Claim and evidence notes by `claim_id` / `evidence_id`",
            "Multi-start perspective notes",
            "Preferred exploration path, not a final continue/stop decision",
            "Anti-narrative regularizers",
            "Sensitivity And Counterfactuals",
            "Implied-expectation reverse-check",
            "Constraint-specific recommendation branches",
            "Residual vector `r_q/r_c/r_e/r_h/r_a/r_s/r_j`",
            "VOI greater than cost",
            "Hard constraints satisfied",
            "Residual Gate",
            "Hard Constraint Gate",
            "Evidence/source appendix",
            "Method and source quality",
            "Red-team notes",
            "Options or scenarios",
            "Source notes",
        ):
            self.assertIn(phrase, contracts)

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

    def test_docs_prefer_front_loaded_guidance_over_harder_thresholds(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "README.zh-CN.md": (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "README.ja.md": (ROOT / "README.ja.md").read_text(encoding="utf-8"),
            "SKILL.md": (ROOT / "SKILL.md").read_text(encoding="utf-8"),
            "references/research-quality.md": (ROOT / "references" / "research-quality.md").read_text(encoding="utf-8"),
        }

        self.assertIn("front-loaded guidance", docs["README.md"])
        self.assertIn("事前引导", docs["README.zh-CN.md"])
        self.assertIn("事前ガイダンス", docs["README.ja.md"])
        self.assertIn("Do not compensate for weak research by raising after-the-fact thresholds", docs["SKILL.md"])
        self.assertIn("decision-critical variables", docs["references/research-quality.md"])
        self.assertIn("artifact dependency order", docs["SKILL.md"])
        self.assertIn("Implied expectation reverse-check", docs["references/research-quality.md"])
        self.assertIn("Anti-narrative regularizers", docs["references/research-quality.md"])

    def test_readmes_describe_staged_cli_and_ideal_flow_mapping(self) -> None:
        readmes = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "README.zh-CN.md": (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "README.ja.md": (ROOT / "README.ja.md").read_text(encoding="utf-8"),
        }
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        for text in readmes.values():
            self.assertIn("Evidence Plan / Minimum Direct Evidence", text)
            self.assertIn("Brief / Frame Contract", text)
            self.assertIn("Post-Research Brainstorming", text)
            self.assertIn("4.1", text)
            self.assertIn("4.12", text)
        self.assertIn("Evidence Plan / Minimum Direct Evidence", skill)
        self.assertIn("Brief / Frame Contract", skill)
        self.assertIn("Post-Research Brainstorming", skill)
        self.assertIn("python3 scripts/survey_round.py research", readmes["README.md"])
        self.assertIn("python3 scripts/survey_round.py brainstorm", readmes["README.md"])
        self.assertIn("python3 scripts/survey_round.py evolve", readmes["README.md"])
        self.assertIn("阶段化 CLI", readmes["README.zh-CN.md"])
        self.assertIn("段階化 CLI", readmes["README.ja.md"])

    def test_lightweight_evolver_reference_includes_strengthened_methods(self) -> None:
        evolver_ref = (ROOT / "references" / "lightweight-evolver.md").read_text(encoding="utf-8")

        self.assertIn("artifact dependency order", evolver_ref)
        self.assertIn("Implied expectation reverse-check", evolver_ref)
        self.assertIn("future facts vs desk-researchable gaps", evolver_ref)
        self.assertIn("Anti-narrative regularizers", evolver_ref)
        self.assertIn("constraint-specific recommendation branches", evolver_ref)
        self.assertIn("residual-driven evidence iteration", evolver_ref)
        self.assertIn("VOI greater than cost", evolver_ref)
        self.assertIn("Hard constraints satisfied", evolver_ref)

    def test_docs_describe_residual_voi_and_hard_constraint_gates(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "README.zh-CN.md": (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "README.ja.md": (ROOT / "README.ja.md").read_text(encoding="utf-8"),
            "SKILL.md": (ROOT / "SKILL.md").read_text(encoding="utf-8"),
            "references/research-quality.md": (ROOT / "references" / "research-quality.md").read_text(encoding="utf-8"),
        }

        self.assertIn("residual / VOI / hard-constraint gate", docs["README.md"])
        self.assertIn("残差 / VOI / 硬约束门", docs["README.zh-CN.md"])
        self.assertIn("残差 / VOI / ハード制約ゲート", docs["README.ja.md"])
        self.assertIn("r_q/r_c/r_e/r_h/r_a/r_s/r_j", docs["SKILL.md"])
        self.assertIn("VOI stopping rule", docs["SKILL.md"])
        self.assertIn("hard constraints are pass/fail", docs["SKILL.md"])
        self.assertIn("Residual-Driven Evidence Iteration", docs["references/research-quality.md"])
        self.assertIn("VOI And Hard Constraints", docs["references/research-quality.md"])
        self.assertIn("Goodhart Check", docs["references/research-quality.md"])

    def test_readmes_map_latest_paper_residual_chapters(self) -> None:
        readmes = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "README.zh-CN.md": (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "README.ja.md": (ROOT / "README.ja.md").read_text(encoding="utf-8"),
        }

        for text in readmes.values():
            self.assertIn("3.7.1-3.7.4", text)
            self.assertIn("5.2-5.5", text)
            self.assertIn("6.2-6.5", text)
            self.assertIn("3.7.3, 3.7.4", text)

    def test_docs_refer_to_current_schema_version(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("report schema v4", skill)
        self.assertNotIn("report schema v3", skill)

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

    def test_readme_opening_emphasizes_principles_paper_and_generality(self) -> None:
        readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        readme_ja = (ROOT / "README.ja.md").read_text(encoding="utf-8")

        self.assertIn("general-purpose research skill", readme_en)
        self.assertIn("concrete implementation of the paper", readme_en)
        self.assertIn("two first principles", readme_en)
        self.assertIn("not a domain-specific stock, product, or open-source template", readme_en)

        self.assertIn("通用调研技能", readme_zh)
        self.assertIn("这篇论文的具体实现", readme_zh)
        self.assertIn("两条第一性原理", readme_zh)
        self.assertIn("不是证券、产品或开源项目的特例模板", readme_zh)

        self.assertIn("汎用調査 skill", readme_ja)
        self.assertIn("この論文の具体的な実装", readme_ja)
        self.assertIn("2 つの第一原理", readme_ja)
        self.assertIn("株式、プロダクト、オープンソース専用のテンプレートではありません", readme_ja)

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
        research = self.create_stage_template_snapshots()["01-research.md"]

        self.assertIn("## Source Registry Updates", research)
        self.assertIn("## Claim And Evidence Notes", research)
        self.assertIn("sources.jsonl", research)
        self.assertIn("claims.jsonl", research)
        self.assertIn("evidence.jsonl", research)
        self.assertNotIn("| Source | URL | Date Checked | Notes |", research)
        self.assertNotIn("| Claim | Evidence | Source | Source Type | Freshness | Confidence | Contradictions |", research)

    def test_brainstorm_template_does_not_own_continue_stop_decision(self) -> None:
        brainstorm = self.create_stage_template_snapshots()["01-brainstorm.md"]

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

    def test_legacy_metadata_cannot_skip_v4_final_gates_even_with_current_report_headings(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=94,
            evolver_decision="Final.",
            evolver_evidence_needed="No desk-research target remains.",
        )
        metadata = survey_dir / ".super-survey.json"
        metadata.write_text(
            '{"topic": "AI recruiting agent", "language": "en", "report_schema_version": 3}\n',
            encoding="utf-8",
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
        self.assertIn('"report_schema_version": 4', metadata.read_text(encoding="utf-8"))
        index = (survey_dir / "index.md").read_text(encoding="utf-8")
        self.assertIn("## Residual Gate", index)
        self.assertIn("## Hard Constraint Gate", index)
        self.assertIn("Residual vector r_q/r_c/r_e/r_h/r_a/r_s/r_j", index)

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

    def test_round_check_requires_evolver_residual_vector(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        evolver_path = survey_dir / "01-evolver.md"
        evolver = re.sub(
            r"^Residual vector r_q/r_c/r_e/r_h/r_a/r_s/r_j \(0-3\):.*\n",
            "",
            evolver_path.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        )
        evolver_path.write_text(evolver, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Round Evidence Quality Gate must record r_q/r_c/r_e/r_h/r_a/r_s/r_j", result.stdout)

    def test_round_check_requires_evolver_voi_fields(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            include_report=False,
            evolver_decision="Kill.",
            evolver_evidence_needed="None.",
        )
        evolver_path = survey_dir / "01-evolver.md"
        evolver = evolver_path.read_text(encoding="utf-8")
        for field in (
            "Expected information value of next research",
            "Research cost",
            "VOI greater than cost",
        ):
            evolver = re.sub(rf"^{re.escape(field)}:.*\n", "", evolver, flags=re.MULTILINE)
        evolver_path.write_text(evolver, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Round Evidence Quality Gate must record expected information value", result.stdout)
        self.assertIn("Round Evidence Quality Gate must record research cost", result.stdout)
        self.assertIn("Round Evidence Quality Gate must state 'VOI greater than cost: yes/no'", result.stdout)

    def test_final_check_rejects_high_residual_even_with_passing_score(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=94,
            evolver_decision="Final.",
            evolver_evidence_needed="No desk-research target remains.",
        )
        for path in (survey_dir / "index.md", survey_dir / "01-evolver.md"):
            text = path.read_text(encoding="utf-8").replace(
                "r_q=0, r_c=1, r_e=1, r_h=1, r_a=1, r_s=1, r_j=0",
                "r_q=0, r_c=1, r_e=3, r_h=1, r_a=1, r_s=1, r_j=0",
            )
            text = text.replace("Any residual at 3: no", "Any residual at 3: yes")
            text = text.replace("Highest residual: 1", "Highest residual: 3")
            path.write_text(text, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("final residual gate cannot pass with any residual at 3", result.stdout)
        self.assertIn("final decision cannot pass with any residual at 3", result.stdout)

    def test_final_check_requires_hard_constraints_satisfied(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=94,
            evolver_decision="Final.",
            evolver_evidence_needed="No desk-research target remains.",
        )
        for path in (survey_dir / "index.md", survey_dir / "01-evolver.md"):
            text = path.read_text(encoding="utf-8").replace(
                "Hard constraints satisfied: yes",
                "Hard constraints satisfied: no",
            )
            text = text.replace(
                "Hard constraint gate status: pass",
                "Hard constraint gate status: fail",
            )
            path.write_text(text, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("final hard constraint gate requires 'Hard constraints satisfied: yes'", result.stdout)
        self.assertIn("final hard constraint gate must state 'Hard constraint gate status: pass'", result.stdout)
        self.assertIn("final decision requires hard constraints satisfied", result.stdout)

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
                "Evidence Plan": "Test the decision-critical demand and policy variables before treating the quick scan as final.",
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

    def test_quick_round_requires_evidence_plan_section(self) -> None:
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

        self.assertEqual(result.returncode, 1)
        self.assertIn("01-round.md: missing heading '## Evidence Plan'", result.stdout)

    def test_localized_raw_decision_label_is_rejected(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            evolver_decision="最终成稿",
            evolver_evidence_needed="No desk-research target remains.",
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("Decision first non-empty line must be exactly one of Keep, Narrow, Pivot, Kill, or Final", result.stdout)

    def test_high_stakes_action_cannot_finalize_in_quick_mode(self) -> None:
        survey_dir = self.init_round(language="zh", mode="quick", topic="小米公司股票是否值得买入")
        self._write_substantive_required_files(
            survey_dir,
            include_report=True,
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
            "第1轮 Quick Survey",
            {
                "本轮问题": "小米公司股票是否值得买入？",
                "证据计划": "验证当前价格、财务质量、估值、风险和用户约束这些会改变行动的变量。",
                "证据与来源": "S1/E1/C1 支持方向性判断；完整登记在 JSONL。",
                "Brainstorming 检查点": "比较买入、等待和继续调研。",
                "反方挑战": "最大反方是公开资料不足以支持高风险买入行动。",
                "综合结论": "应升级到标准或深度模式，而不是用 quick 最终交付。",
                "决策": "Final.",
                "下一步": "升级模式并补充正式尽调证据。",
            },
        )

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("quick mode is for low-stakes directional triage", result.stdout)

    def test_recommend_mode_defaults_to_standard_for_normal_research_requests(self) -> None:
        result = run_cli("recommend-mode", "--text", "调研小米公司股票现在值不值得买入？")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "standard")

    def test_recommend_mode_returns_quick_only_for_explicit_low_stakes_triage(self) -> None:
        result = run_cli("recommend-mode", "--text", "Please give me a quick directional scan of this topic.")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "quick")

    def test_recommend_mode_does_not_use_quick_for_high_stakes_action_even_when_fast_requested(self) -> None:
        result = run_cli("recommend-mode", "--text", "快速调研小米公司股票现在值不值得买入？")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "standard")
        self.assertIn("needs standard or deep mode", result.stdout)

    def test_recommend_mode_returns_deep_for_formal_or_publication_requests(self) -> None:
        result = run_cli("recommend-mode", "--text", "Need a formal long report with many citations and strict audit.")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "deep")

    def test_skill_describes_deep_research_as_optional_capability_route(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("`deep-research` routing is required", skill)
        self.assertIn("prefer `deep-research`", skill)

    def test_skill_keeps_tavily_as_conditional_current_source_route(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("For current-source discovery, default to `tavily-search`", skill)
        self.assertIn("When current-source discovery matters and Tavily fits the source surface", skill)

    def test_skill_treats_third_party_sources_as_untrusted_evidence(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("untrusted third-party", skill)
        self.assertIn("tool-use requests", skill)
        self.assertIn("Third-party content handling", skill)

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
            evolver_decision="Narrow",
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
        self.assertIn("start the next round immediately", result.stdout)
        self.assertIn("do not stop to ask the user how to proceed", result.stdout)

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
            "01-evidence-plan.md": (
                "Framework Evidence Map",
                "Framework dimensions covered: user pain, workflow frequency, policy constraints, substitutes, and early pricing signals.\n"
                "Weak or missing dimensions: willingness to pay and distribution economics.\n"
                "Minimum direct evidence still needs source-level planning."
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
        self.assertIn("01-evidence-plan.md: Framework Evidence Map must include subheadings", result.stdout)
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
            "01-evidence-plan.md": "Framework Evidence Map",
            "01-research.md": "Framework Coverage",
            "01-brainstorm.md": "Candidate Next Moves",
            "01-redteam.md": "Strongest Objections",
            "01-synthesis.md": "Framework-Based Synthesis",
            "01-evolver.md": "Round Evidence Quality Gate",
        }
        for filename, heading in replacements.items():
            path = survey_dir / filename
            text = path.read_text(encoding="utf-8")
            extra = ""
            if filename == "01-evolver.md":
                extra = (
                    "\n\n"
                    "Residual vector r_q/r_c/r_e/r_h/r_a/r_s/r_j (0-3): r_q=0, r_c=1, r_e=1, r_h=1, r_a=1, r_s=1, r_j=0.\n"
                    "Any residual at 3: no.\n"
                    "Target residual for next round: r_e unless the decision is Final or Kill.\n"
                    "Expected information value of next research: low because only external validation remains.\n"
                    "Research cost: low.\n"
                    "VOI greater than cost: no.\n"
                    "Hard constraints satisfied: yes.\n"
                    "Blocking hard constraints: none for final desk-research delivery.\n"
                    "Soft residuals that can be weighted: evidence completeness and actionability.\n"
                )
            text = re.sub(
                rf"(?ms)^## {re.escape(heading)}\n\n.*?(?=^## |\Z)",
                f"## {heading}\n\n### Policy Constraints\n\n"
                "Current judgment: platform rules are the decision bottleneck. "
                "Evidence impact: C2/E2 moves the next round toward official ToS review. "
                "Counterpoint: assisted workflows may still be allowed. "
                f"Decision effect: continue only if a compliant workflow remains plausible.{extra}\n",
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
                    "Residual gate status: pass.\n"
                    "Hard constraint gate status: pass.\n"
                    "Goodhart check: score supports judgment rather than replacing it.\n"
                    f"{quality_decision}\n"
                    "Lowest-Scoring Areas: evidence completeness and analysis depth remain monitored, but both are above the pass threshold.\n"
                    "Next Round Focus: none for desk research; move to user interviews if further validation is needed."
                ),
                "Residual Gate": (
                    "Residual vector r_q/r_c/r_e/r_h/r_a/r_s/r_j (0-3): r_q=0, r_c=1, r_e=1, r_h=1, r_a=1, r_s=1, r_j=0.\n"
                    "Any residual at 3: no.\n"
                    "Highest residual: 1.\n"
                    "Residual gate status: pass.\n"
                    "Next descent direction: external validation, not another desk-research pass."
                ),
                "Hard Constraint Gate": (
                    "Hard constraints satisfied: yes.\n"
                    "Blocking hard constraints: none for desk research; policy remains a monitor for implementation.\n"
                    "Hard constraint gate status: pass."
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
            survey_dir / "01-evidence-plan.md",
            "Round 1 Evidence Plan",
            {
                "Round Decision Target": "Decide whether another desk-research round can materially change the build decision.",
                "Target Residual To Reduce": (
                    "Primary residual: r_e evidence residual.\n"
                    "Why this residual is the steepest useful direction: policy and payment evidence can change the action.\n"
                    "Expected information value: high if official policy or pricing evidence changes the recommendation.\n"
                    "Research cost: low to medium desk research.\n"
                    "What result would make another round unnecessary: no desk-researchable evidence target remains."
                ),
                "Decision-Critical Variables": (
                    "Policy permissiveness, willingness to pay, distribution reach, substitute strength, and implementation reliability are the variables most likely to change the action."
                ),
                "Minimum Direct Evidence": (
                    "Official policy evidence is required for platform constraints. Direct pricing or comparable paid conversion evidence is required for willingness to pay. Substitute comparison evidence is required before claiming differentiation."
                ),
                "Source Plan": (
                    "Use official platform terms, competitor pricing pages, current source search, and registry-backed claim/evidence entries. Companion routing can be used if VOC or competitor data is needed."
                ),
                "Disconfirming Evidence": (
                    "Policy blocks the workflow, users refuse payment, substitutes already solve the job, or implementation requires unreliable automation."
                ),
                "Missing Evidence Handling": (
                    "If direct policy or payment evidence is missing, lower confidence and continue a targeted desk-research round. If the gap requires interviews or legal review, record that it is not desk-researchable."
                ),
                "Framework Evidence Map": (
                    "### User Pain\n"
                    "Minimum direct evidence: direct workflow complaints or repeated workaround behavior. Source type: user language or direct observation. Missing evidence means confidence stays medium.\n\n"
                    "### Workflow Frequency\n"
                    "Minimum direct evidence: repeated use frequency during active searches. Source type: direct user signal or credible survey. Missing evidence means retention remains uncertain.\n\n"
                    "### Willingness To Pay\n"
                    "Minimum direct evidence: paid alternatives, commitments, or pricing conversion. Source type: pricing pages and user commitments. Missing evidence means no full build recommendation.\n\n"
                    "### Policy Constraints\n"
                    "Minimum direct evidence: official ToS or enforcement guidance. Source type: primary platform source. Missing evidence keeps policy as a veto dimension.\n\n"
                    "### Substitutes\n"
                    "Minimum direct evidence: credible manual or product alternatives. Source type: competitor pages and user workarounds. Missing evidence weakens differentiation.\n\n"
                    "### Distribution\n"
                    "Minimum direct evidence: reachable channels or high-intent entry points. Source type: search/community/channel evidence. Missing evidence weakens go-to-market confidence.\n\n"
                    "### Implementation Difficulty\n"
                    "Minimum direct evidence: reliability, data access, and operational constraints. Source type: technical docs and implementation probes. Missing evidence keeps build risk elevated."
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
                    "Residual vector r_q/r_c/r_e/r_h/r_a/r_s/r_j (0-3): r_q=0, r_c=1, r_e=1, r_h=1, r_a=1, r_s=1, r_j=0.\n"
                    "Any residual at 3: no.\n"
                    "Target residual for next round: r_e unless the decision is Final or Kill.\n"
                    "Expected information value of next research: low if only interviews/legal review remain; high if policy pages remain unchecked.\n"
                    "Research cost: low to medium.\n"
                    "VOI greater than cost: no.\n"
                    "Hard constraints satisfied: yes.\n"
                    "Blocking hard constraints: none for final desk-research delivery.\n"
                    "Soft residuals that can be weighted: evidence completeness and actionability.\n"
                    "Continue / stop implication: continue unless the raw decision is Final/Kill and final report quality later passes."
                ),
                "Next Research Target": "Can active US software job seekers use a browser-assisted copilot under platform constraints?",
                "Evidence Needed Next": evolver_evidence_needed,
            },
        )


if __name__ == "__main__":
    unittest.main()
