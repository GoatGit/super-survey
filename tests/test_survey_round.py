from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "survey_round.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        text=True,
        capture_output=True,
    )


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

## Source List

## Evidence Table

## Findings

## Data Quality Notes
""",
            encoding="utf-8",
        )

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("01-research.md: section '## Source List' appears to be empty", result.stdout)
        self.assertIn("01-research.md: section '## Evidence Table' appears to be empty", result.stdout)

    def test_check_rejects_missing_search_tool_notes(self) -> None:
        survey_dir = self.init_round()
        research = survey_dir / "01-research.md"
        research.write_text(
            """# Round 1 Research

## Research Question

Can this target customer pay for this workflow?

## Source List

| Source | URL | Date Checked | Notes |
|---|---|---|---|
| Example | https://example.com | 2026-06-13 | Primary page |

## Evidence Table

| Claim | Evidence | Source | Source Type | Freshness | Confidence | Contradictions |
|---|---|---|---|---|---|---|
| Users repeat the task | Forum posts and product pages | Example | Secondary | Checked this round | Medium | No direct payment proof |

## Findings

There are repeated workflow signals.

## Data Quality Notes

Evidence is directional, not decisive.
""",
            encoding="utf-8",
        )

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
        redteam = (survey_dir / "01-redteam.md").read_text(encoding="utf-8")
        synthesis = (survey_dir / "01-synthesis.md").read_text(encoding="utf-8")
        evolver = (survey_dir / "01-evolver.md").read_text(encoding="utf-8")
        index = (survey_dir / "index.md").read_text(encoding="utf-8")

        self.assertIn("## Research Lens", brief)
        self.assertIn("## Decision Evidence Standard", brief)
        self.assertIn("## Decision Frame Integrity", brief)
        self.assertIn("## Initial Assumptions", brief)
        self.assertIn("## Continuation Policy", brief)
        self.assertNotIn("## Planned Rounds", brief)
        self.assertNotIn("Round 1:", brief)
        self.assertIn("Do not predict the number of rounds", brief)
        self.assertIn("Source Type", research)
        self.assertIn("Freshness", research)
        self.assertIn("Contradictions", research)
        self.assertIn("Search Tool Used", research)
        self.assertIn("Tavily Fallback Reason", research)
        self.assertIn("## Alternative Explanations Or Substitutes", redteam)
        self.assertIn("## Kill Criteria Checked", redteam)
        self.assertIn("## Decision Rationale", synthesis)
        self.assertIn("Alternative", evolver)
        self.assertIn("## Round Evidence Quality Gate", evolver)
        self.assertNotIn("## Report Quality Gate", evolver)
        self.assertNotIn("Current report quality score", evolver)
        self.assertFalse((survey_dir / "report.md").exists())
        self.assertIn("## Current Evidence-Bound Conclusion", index)
        self.assertNotIn("## Current Best Conclusion", index)
        self.assertIn("## Round Ledger", index)
        self.assertIn("## Continuation Status", index)
        self.assertIn("## Next Research Target", index)
        self.assertIn("## Why Not Final Yet", index)
        self.assertIn("Wiki Tool Attempted", index)
        self.assertIn("Wiki Ingest Result", index)
        self.assertIn("Mode:", brief)
        self.assertIn("Minimum Sources:", brief)
        self.assertIn("Target Report Length:", brief)

    def test_init_creates_evidence_registry_files_and_mode_metadata(self) -> None:
        survey_dir = self.init_round(mode="deep")

        metadata = (survey_dir / ".super-survey.json").read_text(encoding="utf-8")
        self.assertIn('"mode": "deep"', metadata)
        for filename in ("sources.jsonl", "claims.jsonl", "evidence.jsonl"):
            self.assertTrue((survey_dir / filename).exists(), filename)
            self.assertEqual((survey_dir / filename).read_text(encoding="utf-8"), "")

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
        self.assertIn("00-brief.md: continuation policy must not predict specific round outcomes", result.stdout)

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

    def test_check_rejects_missing_wiki_attempt_notes(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, include_wiki_notes=False)

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

    def test_upgrade_report_appends_v2_sections_and_metadata(self) -> None:
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
        self.assertIn("## Reader's Path", report)
        self.assertIn("## Appendix: Evidence Register", report)
        self.assertIn('"report_schema_version": 2', metadata.read_text(encoding="utf-8"))

    def test_v2_report_rejects_thin_content(self) -> None:
        survey_dir = self.init_round()
        (survey_dir / "report.md").write_text(
            """# AI recruiting agent

## Executive Summary
Thin.
## Reader's Path
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
## Report Quality Score
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

    def test_v2_report_rejects_missing_quality_score(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)
        report = (survey_dir / "report.md").read_text(encoding="utf-8")
        report = report.replace("\n## Report Quality Score\n\n", "\n## ")
        report = report.replace(
            "Total Score: 92 / 100.\nScore Breakdown: scope 14, sources 19, evidence 18, analysis 18, actionability 14, structure 9.\nPass / Continue Decision: pass; finalize the report because no decision-changing unknown remains desk-researchable.\nLowest-Scoring Areas: evidence completeness and analysis depth remain monitored, but both are above the pass threshold.\nNext Round Focus: none for desk research; move to user interviews if further validation is needed.\n\n## Appendix: Source Notes",
            "Appendix: Source Notes",
        )
        (survey_dir / "report.md").write_text(report, encoding="utf-8")

        result = run_cli("check-final", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing heading '## Report Quality Score'", result.stdout)

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
            (survey_dir / "sources.jsonl").write_text(
                '{"source_id":"S1","title":"Example","url":"https://example.com","source_type":"primary","date_checked":"2026-06-13","credibility":"medium"}\n'
                '{"source_id":"S2","title":"Policy Example","url":"https://example.com/policy","source_type":"primary","date_checked":"2026-06-13","credibility":"high"}\n'
                '{"source_id":"S3","title":"Pricing Example","url":"https://example.com/pricing","source_type":"secondary","date_checked":"2026-06-13","credibility":"medium"}\n',
                encoding="utf-8",
            )
            (survey_dir / "evidence.jsonl").write_text(
                '{"evidence_id":"E1","source_id":"S1","quote_or_summary":"Users repeat this workflow.","locator":"page","confidence":"medium"}\n'
                '{"evidence_id":"E2","source_id":"S2","quote_or_summary":"Policy constraints can affect automation.","locator":"terms","confidence":"high"}\n'
                '{"evidence_id":"E3","source_id":"S3","quote_or_summary":"Comparable tools use paid subscriptions.","locator":"pricing page","confidence":"medium"}\n',
                encoding="utf-8",
            )
            (survey_dir / "claims.jsonl").write_text(
                '{"claim_id":"C1","claim":"Users repeat this workflow.","supporting_evidence_ids":["E1"],"status":"supported"}\n'
                '{"claim_id":"C2","claim":"Policy risk matters.","supporting_evidence_ids":["E2"],"status":"supported"}\n'
                '{"claim_id":"C3","claim":"Paid willingness remains plausible but unproven.","supporting_evidence_ids":["E3"],"status":"partial"}\n',
                encoding="utf-8",
            )
        wiki_status = (
            "Wiki Tool Attempted: karpathy-llm-wiki.\n"
            "Wiki Ingest Result: not built; no initialized project raw/wiki directory was available.\n"
            "Wiki Fallback Reason: local Markdown index maintained for this survey.\n"
            "Wiki Artifact Path: index.md only."
            if include_wiki_notes
            else "Not built: no initialized wiki backend."
        )
        (survey_dir / "00-brief.md").write_text(
            """# Survey Brief: AI recruiting agent

## User Question

Should we build this?

## Superpowers Brainstorming Gate

Completed: decision, buyer, and stopping criteria recorded.

## Decision To Make

Decide whether to continue.

## Research Lens

Use a general product opportunity lens with policy and willingness-to-pay checks.

## Decision Evidence Standard

Require current primary sources for policy claims and direct signals for payment claims.

## Decision Frame Integrity

Original question: should we build this?
Decision frame: evaluate whether to continue discovery, not whether guaranteed success is proven.
Not pre-decided: do not rewrite the question into an easier-to-kill demand for certainty.
Allowed narrowing: narrow only when evidence or red-team critique justifies the narrower target.

## Target Customer

US software engineers actively applying for jobs.

## Success Criteria

Evidence supports a paid workflow.

## Disqualifying Conditions

Platform rules block reliable delivery.

## Initial Assumptions

Users already apply repeatedly.

## Continuation Policy

Start with the next research round; decide whether to continue only after evidence, red-team critique, synthesis, and the raw evolver decision are written.
Do not predict the number of rounds or prewrite a stop conclusion in the brief.
""",
            encoding="utf-8",
        )
        (survey_dir / "index.md").write_text(
            """# Survey Index: AI recruiting agent

## Current Thesis

The thesis is plausible but unproven.

## Current Evidence-Bound Conclusion

Continue one narrowed round before final reporting.

## Round Ledger

Round 1 found demand signals.

## Continuation Status

Continue if the evolver says Narrow, Pivot, or Keep; finalize only after Kill plus passing report quality.

## Next Research Target

Can policy and pricing evidence support a narrower workflow?

## Why Not Final Yet

The latest round still needs either a Kill decision or a final report gate.

## Open Questions

Policy risk remains open.

## Source Inventory

Official platform terms and competitor pages.

## Wiki / Graph Index Status

{wiki_status}

## Decision Log

Continue one narrowed round.
""".format(wiki_status=wiki_status),
            encoding="utf-8",
        )
        if include_report:
            quality_decision = continuation_decision or (
                "Pass / Continue Decision: pass; finalize the report because no decision-changing unknown remains desk-researchable, and the evolver next evidence requires external validation through user interviews."
            )
            (survey_dir / "report.md").write_text(
                f"""# AI recruiting agent

## Executive Summary

Continue with a narrower policy-first validation path.
Confidence is medium because demand is visible but policy and payment remain unresolved.

## Reader's Path

Read the executive summary for the decision, the narrative for the reasoning, and the appendices for audit details.
This report supports a go/no-go validation decision for active US software engineers.

## Main Narrative

The opportunity is visible because job seekers repeat the same painful workflow across many applications.
The first pass found demand signals, but it also made policy risk the central issue rather than a side note.
That changes the recommendation from building a broad automation agent to validating a narrower assisted workflow.

## Decision Logic

The recommendation follows from three linked judgments.
First, repeated manual effort creates plausible demand.
Second, platform restrictions can destroy the core workflow if ignored.
Third, payment evidence is not yet strong enough to justify full implementation.

## Final Recommendation

Run a policy-first validation round before building.
Do not start full implementation until the compliance boundary and willingness to pay are clearer.

## What Could Change This Conclusion

The conclusion would improve if official terms allow the assisted workflow and users commit to paid trials.
It would worsen if official terms block automation or users prefer spreadsheets and existing job trackers.

## Next Actions

Collect official terms, compare competitors, and interview five active job seekers.
Record willingness to pay, the exact tasks users would delegate, and the fallback workflow if automation is limited.

## Limits Of This Report

No direct buyer interviews were conducted.
No live policy review by counsel was performed, so legal risk remains directional.

## Appendix: Evidence Register

Claim: users repeat the workflow. Evidence: public workflow signals. Confidence: medium. Contradictions: direct payment proof is missing.
Claim: platform risk matters. Evidence: job boards can restrict automation. Confidence: medium.

## Appendix: Method And Source Quality

Use current source discovery, official policy pages, competitor pages, and confidence labels.
Primary policy pages carry more weight than forum anecdotes.

## Appendix: Red-Team Notes

The strongest objection is platform policy risk and weak trust in automation.
Users may also prefer simple spreadsheets if outcome quality is not provable.

## Appendix: Options Or Scenarios

Option A: continue policy validation. Option B: stop if terms block the workflow.
Option C: pivot to a personal job-search CRM if automation is too risky.

## Report Quality Score

Total Score: {report_score} / 100.
Score Breakdown: scope 14, sources 19, evidence 18, analysis 18, actionability 14, structure 9.
{quality_decision}
Lowest-Scoring Areas: evidence completeness and analysis depth remain monitored, but both are above the pass threshold.
Next Round Focus: none for desk research; move to user interviews if further validation is needed.

## Appendix: Source Notes

Sources were checked during this round and remain directional.
Future rounds should record URLs, dates checked, and contradictions.
""",
                encoding="utf-8",
            )
        (survey_dir / "01-research.md").write_text(
            """# Round 1 Research

## Research Question

Can users pay for this workflow?

## Source List

| Source | URL | Date Checked | Notes |
|---|---|---|---|
| Example | https://example.com | 2026-06-13 | Primary page |

## Evidence Table

| Claim | Evidence | Source | Source Type | Freshness | Confidence | Contradictions |
|---|---|---|---|---|---|---|
| Users repeat the task | Forum posts and product pages | Example | Secondary | Checked this round | Medium | No direct payment proof |

## Findings

There are repeated workflow signals.

## Data Quality Notes

- Search Tool Used: tavily-search.
- Tavily Fallback Reason: none.
- Query And Filter Notes: official pages and competitor pages.
- Evidence is directional, not decisive.
""",
            encoding="utf-8",
        )
        (survey_dir / "01-brainstorm.md").write_text(
            """# Round 1 Brainstorming Checkpoint

## Brainstorming Status

Completed after initial research.

## Current Framing

Focus on job seekers rather than recruiters.

## Clarifying Questions

Can policy risk be reduced?

## Alternative Next Moves

Compare policy, pricing, or open-source tools.

## Chosen Direction

Check policy and pricing next.

## Design Notes For Next Round

Use primary ToS pages and pricing evidence.
""",
            encoding="utf-8",
        )
        (survey_dir / "01-redteam.md").write_text(
            """# Round 1 Red-Team Challenge

## Strongest Objections

Users may not trust automation.

## Incumbent Response

Job boards can block the workflow.

## Alternative Explanations Or Substitutes

Users may prefer manual spreadsheets or existing job trackers.

## Data And Access Risks

Data access can change without notice.

## Legal, ToS, Privacy, Or Compliance Risks

Terms may restrict automated submission.

## Monetization And Distribution Risks

Paid acquisition could erase margin.

## Kill Criteria Checked

No verified kill criterion was found, but policy risk remains unresolved.

## Falsification Tests

Stop if policy blocks the core workflow.
""",
            encoding="utf-8",
        )
        (survey_dir / "01-synthesis.md").write_text(
            """# Round 1 Synthesis

## Updated Conclusion

Continue only with a narrower workflow.

## Confidence

Medium.

## Decision Rationale

Continue because demand signals exist, but narrow around policy risk.

## What Changed

Policy risk became the main blocker.

## Remaining Unknowns

Actual willingness to pay is unknown.

## Evolved Next Research Target

Can a browser-assisted workflow comply with job-board terms?

## Recommended Next Action

Run a policy-first round.
""",
            encoding="utf-8",
        )
        (survey_dir / "01-evolver.md").write_text(
            """# Round 1 Lightweight Evolver

## Current Thesis

The job seeker workflow may be viable if policy risk is manageable.

## Probe Results

| Probe | Answer | Strength |
|---|---|---|
| Buyer | Active job seekers pay from personal budget | weak |

## Persona Judgments

| Persona | Verdict | Reason |
|---|---|---|
| Skeptical buyer | concern | Trust and outcomes are unproven |

## Decision

{evolver_decision}

## Round Evidence Quality Gate

Evidence coverage this round: directional signals exist, but buyer payment and policy constraints remain weak.
Weakest evidence dimensions: evidence completeness and analysis depth.
Continue / stop implication: continue unless the raw decision is Kill and final report quality later passes.
Next-round focus: official policy pages, direct buyer signals, and contradiction checks.

## Next Research Target

Can active US software job seekers use a browser-assisted copilot under platform constraints?

## Evidence Needed Next

{evolver_evidence_needed}
""".format(evolver_decision=evolver_decision, evolver_evidence_needed=evolver_evidence_needed),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
