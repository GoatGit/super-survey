# Changelog

All notable changes to Super Survey are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project intends to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- GitHub community files: CI workflow, issue templates, pull-request template, Code of Conduct, and Security Policy.
- Standard `LICENSE` file naming for GitHub license detection.

### Changed

- Renamed `license.txt` to `LICENSE`; updated links in all README languages.

## [0.1.0] - 2026-07-07

Initial public baseline of the Super Survey research skill.

### Added

- Staged research workflow: `00-brief.md`, then per-round `NN-evidence-plan.md`, `NN-research.md`, `NN-brainstorm.md`, `NN-redteam.md`, `NN-synthesis.md`, and `NN-evolver.md` artifacts with enforced dependency order.
- Explicit research modes (`quick`, `standard`, `deep`) with registry minimums and report score gates (80 / 90 / 95) and a `recommend-mode` helper for ambiguous requests.
- Evidence registry (`sources.jsonl`, `claims.jsonl`, `evidence.jsonl`) with source-link, duplicate-ID, and weak-support validation.
- Adaptive Research Framework routing: decision archetypes, lens packs, domain hints, framework contract, and evidence contract recorded in `00-brief.md`.
- Anti-sycophancy checks: objective-function reconstruction, decision frame integrity, object/action split, implied-expectation reverse-check, and anti-narrative regularizers.
- Lightweight evolver with raw `Keep` / `Narrow` / `Pivot` / `Kill` / `Final` decisions and residual vector `r_q/r_c/r_e/r_h/r_a/r_s/r_j` scoring.
- Stop-safety gates: residual / VOI / hard-constraint gates and workflow-state tracking (`continuing_round`, `ready_to_finalize`, `final_report_draft`, `final`).
- Terminal `report.md` with schema v4, prose-first report rules, `upgrade-report` for legacy reports, and a 100-point quality gate recorded in `index.md`.
- Source scope conventions: `local-only`, `local-first`, `current-first`, and `open`.
- Third-party source handling rules against prompt injection from fetched content.
- `scripts/survey_round.py` CLI: `init`, `round`/`plan`, `research`, `brainstorm`, `redteam`, `synthesis`, `evolve`, `check`, `check-final`, `finalize-report`, `upgrade-report`, `recommend-mode`, and `validate-evidence`.
- Regression test suite (114 tests) using only the Python standard library.
- Multilingual documentation: English, Chinese, and Japanese READMEs plus a trilingual contributing guide.
- Companion-skill routing conventions for search, deep research, VOC, competitor analysis, brainstorming, and wiki persistence.
- Research paper "Resisting AI Sycophancy in Open-Ended Research" in Chinese and English.

## Types of changes

- **Added** for new features.
- **Changed** for changes in existing behavior.
- **Deprecated** for soon-to-be-removed features.
- **Removed** for removed features.
- **Fixed** for bug fixes.
- **Security** for vulnerability fixes.

[Unreleased]: https://github.com/GoatGit/super-survey/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/GoatGit/super-survey/releases/tag/v0.1.0
