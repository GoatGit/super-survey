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
        self.assertIn("no implicit two-round cap", brief)
        self.assertIn("Source Type", research)
        self.assertIn("Freshness", research)
        self.assertIn("Contradictions", research)
        self.assertIn("Search Tool Used", research)
        self.assertIn("Tavily Fallback Reason", research)
        self.assertIn("## Alternative Explanations Or Substitutes", redteam)
        self.assertIn("## Kill Criteria Checked", redteam)
        self.assertIn("## Decision Rationale", synthesis)
        self.assertIn("Alternative", evolver)
        self.assertIn("## Executive Summary", report)
        self.assertIn("## Recommendation", report)

    def test_check_passes_when_every_required_section_has_substance(self) -> None:
        survey_dir = self.init_round()
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

Evidence is directional, not decisive.
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

## Next Research Target

Can active US software job seekers use a browser-assisted copilot under platform constraints?

## Evidence Needed Next

Official ToS pages, pricing pages, and direct buyer signals.
""",
            encoding="utf-8",
        )

        result = run_cli("check", str(survey_dir))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
