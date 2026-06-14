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

    def init_round(self, language: str = "en") -> Path:
        result = run_cli(
            "init",
            "AI recruiting agent",
            "--root",
            str(self.root),
            "--date",
            "2026-06-13",
            "--language",
            language,
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
        self.assertIn("report.md: appears to be only an empty template", result.stdout)

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
        report = (survey_dir / "report.md").read_text(encoding="utf-8")

        self.assertIn("## Research Lens", brief)
        self.assertIn("## Decision Evidence Standard", brief)
        self.assertIn("## Initial Assumptions", brief)
        self.assertIn("## Planned Rounds", brief)
        self.assertIn("report quality is below the pass threshold", brief)
        self.assertIn("Source Type", research)
        self.assertIn("Freshness", research)
        self.assertIn("Contradictions", research)
        self.assertIn("Search Tool Used", research)
        self.assertIn("Tavily Fallback Reason", research)
        self.assertIn("## Alternative Explanations Or Substitutes", redteam)
        self.assertIn("## Kill Criteria Checked", redteam)
        self.assertIn("## Decision Rationale", synthesis)
        self.assertIn("Alternative", evolver)
        self.assertIn("## Report Quality Gate", evolver)
        self.assertIn("## Executive Summary", report)
        self.assertIn("## Methodology And Source Quality", report)
        self.assertIn("## Evidence Table", report)
        self.assertIn("## Red-Team Critique", report)
        self.assertIn("## Options Or Scenarios", report)
        self.assertIn("## Action Plan", report)
        self.assertIn("## Open Questions And Next Round", report)
        self.assertIn("## Report Quality Score", report)
        self.assertIn("Score Breakdown", report)
        self.assertIn("## Recommendation", report)

    def test_legacy_report_schema_warns_but_does_not_fail(self) -> None:
        survey_dir = self.init_round()
        metadata = survey_dir / ".super-survey.json"
        metadata.write_text('{"topic": "AI recruiting agent", "language": "en"}\n', encoding="utf-8")
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

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("legacy report schema detected", result.stdout)

    def test_upgrade_report_appends_v2_sections_and_metadata(self) -> None:
        survey_dir = self.init_round()
        metadata = survey_dir / ".super-survey.json"
        metadata.write_text('{"topic": "AI recruiting agent", "language": "en"}\n', encoding="utf-8")
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
        self.assertIn("## Research Question And Scope", report)
        self.assertIn('"report_schema_version": 2', metadata.read_text(encoding="utf-8"))

    def test_v2_report_rejects_thin_content(self) -> None:
        survey_dir = self.init_round()
        (survey_dir / "report.md").write_text(
            """# AI recruiting agent

## Executive Summary
Thin.
## Research Question And Scope
Thin.
## Methodology And Source Quality
Thin.
## Key Findings
Thin.
## Evidence Table
Thin.
## Analysis
Thin.
## Red-Team Critique
Thin.
## Options Or Scenarios
Thin.
## Recommendation
Thin.
## Action Plan
Thin.
## Open Questions And Next Round
Thin.
## Report Quality Score
Thin.
## Limitations
Thin.
## Source Notes
Thin.
""",
            encoding="utf-8",
        )
        self._write_substantive_required_files(survey_dir, include_report=False)

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("complete report must contain at least", result.stdout)

    def test_v2_report_rejects_missing_quality_score(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)
        report = (survey_dir / "report.md").read_text(encoding="utf-8")
        report = report.replace("\n## Report Quality Score\n\n", "\n## ")
        report = report.replace(
            "Total Score: 92 / 100.\nScore Breakdown: scope 14, sources 19, evidence 18, analysis 18, actionability 14, structure 9.\nPass / Continue Decision: pass; finalize the report because no decision-changing unknown remains desk-researchable.\nLowest-Scoring Areas: evidence completeness and analysis depth remain monitored, but both are above the pass threshold.\nNext Round Focus: none for desk research; move to user interviews if further validation is needed.\n\n## Limitations",
            "Limitations",
        )
        (survey_dir / "report.md").write_text(report, encoding="utf-8")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing heading '## Report Quality Score'", result.stdout)

    def test_report_below_pass_score_requires_continuation_decision(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir, report_score=74, continuation_decision="Stop.")

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("score below 80 must continue", result.stdout)

    def test_report_conditional_score_requires_no_decision_changing_unknowns(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(
            survey_dir,
            report_score=84,
            continuation_decision="Pass / Continue Decision: conditionally stop because the next action is clear.",
        )

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 1)
        self.assertIn("score 80-89 must state that no decision-changing unknowns remain", result.stdout)

    def test_check_passes_when_every_required_section_has_substance(self) -> None:
        survey_dir = self.init_round()
        self._write_substantive_required_files(survey_dir)

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def _write_substantive_required_files(
        self,
        survey_dir: Path,
        include_report: bool = True,
        report_score: int = 92,
        continuation_decision: str | None = None,
    ) -> None:
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

## Target Customer

US software engineers actively applying for jobs.

## Success Criteria

Evidence supports a paid workflow.

## Disqualifying Conditions

Platform rules block reliable delivery.

## Initial Assumptions

Users already apply repeatedly.

## Planned Rounds

Round 1 checks demand and policy risk.
""",
            encoding="utf-8",
        )
        (survey_dir / "index.md").write_text(
            """# Survey Index: AI recruiting agent

## Current Thesis

The thesis is plausible but unproven.

## Round Summaries

Round 1 found demand signals.

## Open Questions

Policy risk remains open.

## Source Inventory

Official platform terms and competitor pages.

## Wiki / Graph Index Status

Not built: no initialized wiki backend.

## Decision Log

Continue one narrowed round.
""",
            encoding="utf-8",
        )
        if include_report:
            quality_decision = continuation_decision or (
                "Pass / Continue Decision: pass; finalize the report because no decision-changing unknown remains desk-researchable."
            )
            (survey_dir / "report.md").write_text(
                f"""# AI recruiting agent

## Executive Summary

Continue with a narrower policy-first validation path.
Confidence is medium because demand is visible but policy and payment remain unresolved.

## Research Question And Scope

Assess whether a job-search copilot is worth further validation for active US software engineers.
The report does not claim the product is ready to build.

## Methodology And Source Quality

Use current source discovery, official policy pages, competitor pages, and confidence labels.
Primary policy pages carry more weight than forum anecdotes.

## Key Findings

Demand signals exist, but payment and policy evidence are incomplete.
The strongest positive signal is repeated manual effort across applications.

## Evidence Table

Claim: users repeat the workflow. Evidence: public workflow signals. Confidence: medium. Contradictions: direct payment proof is missing.
Claim: platform risk matters. Evidence: job boards can restrict automation. Confidence: medium.

## Analysis

Manual workflows and job trackers are the main substitutes.
The opportunity is attractive only if the workflow avoids prohibited automation.

## Red-Team Critique

The strongest objection is platform policy risk and weak trust in automation.
Users may also prefer simple spreadsheets if outcome quality is not provable.

## Options Or Scenarios

Option A: continue policy validation. Option B: stop if terms block the workflow.
Option C: pivot to a personal job-search CRM if automation is too risky.

## Recommendation

Run a policy-first round before building.
Do not start full implementation until the compliance boundary is clear.

## Action Plan

Collect official terms, compare competitors, and interview five active job seekers.
Record willingness to pay and the exact tasks users would delegate.

## Open Questions And Next Round

Next round should test compliance, willingness to pay, and fallback workflows.
If official terms block the workflow, the next round should pivot or kill.

## Report Quality Score

Total Score: {report_score} / 100.
Score Breakdown: scope 14, sources 19, evidence 18, analysis 18, actionability 14, structure 9.
{quality_decision}
Lowest-Scoring Areas: evidence completeness and analysis depth remain monitored, but both are above the pass threshold.
Next Round Focus: none for desk research; move to user interviews if further validation is needed.

## Limitations

No direct buyer interviews were conducted.
No live policy review by counsel was performed.

## Source Notes

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

Narrow.

## Report Quality Gate

Current report quality score: 92 / 100.
Lowest-scoring dimensions: evidence completeness and analysis depth.
Pass / continue reason: pass because no decision-changing unknown remains desk-researchable.
Next-round focus if score is below threshold: none.

## Next Research Target

Can active US software job seekers use a browser-assisted copilot under platform constraints?

## Evidence Needed Next

Official ToS pages, pricing pages, and direct buyer signals.
""",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
