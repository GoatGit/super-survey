# Artifact Contracts

Use this reference when authoring, reviewing, or debugging Super Survey round
artifacts. `SKILL.md` keeps the execution protocol concise; this file preserves
the detailed content contract for each staged artifact.

## Contents

- Evidence Plan
- Research
- Post-Research Brainstorming
- Redteam
- Synthesis
- Evolver
- Index
- Final Report
- Quick Mode

## Evidence Plan

`NN-evidence-plan.md` should contain:

- Round decision target for this round, tied to the original question and the latest `index.md` state.
- Decision-critical variables that could change the recommendation.
- Minimum direct evidence: what must be observed directly, what is only background, and what cannot substitute for direct proof.
- Source plan: primary or official sources, direct measurements, registry updates, current-source search path, and companion routing if needed.
- Disconfirming evidence and substitutes that would weaken or falsify the current path.
- Missing evidence handling: whether the gap needs another desk-research pass, non-desk validation, future facts, interviews, experiments, legal review, or explicit uncertainty.
- Framework evidence map: one `### <framework dimension>` subsection per brief-defined or evidence-refined dimension, naming the minimum direct evidence, preferred source type, disconfirming evidence, and what to do if the evidence is missing.

## Research

`NN-research.md` should contain:

- Research question for this round.
- Source registry updates by `source_id`; `sources.jsonl` remains the canonical source list.
- Claim and evidence notes by `claim_id` / `evidence_id`; `claims.jsonl` and `evidence.jsonl` remain the canonical evidence registry.
- Framework coverage: one `### <framework dimension>` subsection per brief-defined or evidence-refined dimension.
- For each framework dimension: findings, source role, minimum direct evidence, evidence IDs, contradictions, confidence, decision-critical variables tested, and next evidence target.
- Notes on data quality, freshness, dynamic source reproducibility, and whether Tavily or a fallback search path was used.

## Post-Research Brainstorming

`NN-brainstorm.md` should contain:

- Brainstorming status.
- Current framing after the research pass.
- Clarifying questions or explicit assumptions.
- Candidate next moves organized under one `### <framework dimension>` subsection per brief-defined or evidence-refined dimension.
- Multi-start perspective notes: each useful role should state its target function, needed evidence, and most likely error.
- The decision-critical uncertainty that the next evidence move would reduce.
- Preferred exploration path, not a final continue/stop decision.
- Design notes for the next round.

## Redteam

`NN-redteam.md` should contain:

- Strongest objections organized under one `### <framework dimension>` subsection per brief-defined or evidence-refined dimension.
- Better-funded incumbent, stronger alternative, or substitute response when relevant.
- Alternative explanations or substitutes.
- Data, legal, distribution, trust, monetization, maintenance, adoption, or policy risks as relevant to the research lens.
- Anti-narrative regularizers: what popular narrative, user preference, recent signal, consensus story, or elegant explanation could be overfitting the answer.
- Kill criteria checked.
- Reasons the target audience, buyer, user, maintainer, market, or decision-maker may not care.
- What would make the thesis false.

## Synthesis

`NN-synthesis.md` should contain:

- Updated conclusion.
- Confidence: low / medium / high.
- Decision rationale: why the recommendation follows from the evidence.
- Framework-based synthesis: one `### <framework dimension>` subsection per brief-defined or evidence-refined dimension.
- Strongest dimensions, weakest dimensions, cross-dimension judgment, and framework gaps affecting confidence.
- Action attractiveness vs object quality.
- Bayesian update and decision tree.
- Sensitivity And Counterfactuals: key variables, the most conclusion-changing variable, current assumptions, favorable/adverse counterfactuals, evidence needed, desk-researchable gaps, and decision impact.
- Implied-expectation reverse-check: what current action, price, choice, adoption, dependency, architecture, or commitment already assumes, and what direct evidence would have to support those expectations.
- Constraint-specific recommendation branches: what changes for different budgets, horizons, risk tolerance, existing exposure, team capacity, reversibility, compliance burden, or other user/context states.
- What changed from the prior round.
- Best next question.
- Recommended next action.

## Evolver

`NN-evolver.md` should contain:

- Probe questions and answers.
- Persona judgments.
- Raw decision: exactly one of `Keep`, `Narrow`, `Pivot`, `Kill`, or `Final`.
- Round evidence quality gate with one `### <framework dimension>` subsection per brief-defined or evidence-refined dimension.
- Evidence coverage, weakest dimensions, implied expectation check and reverse-check, future facts vs desk-researchable gaps, anti-narrative regularizers, decision tree triggers, Bayesian update needed, Kill scope, original question still open, continue/stop implication, and next-round focus.
- Next-round target.
- Evidence needed next.

## Index

`index.md` should contain:

- Current thesis and current evidence-bound conclusion.
- Round ledger and decision log.
- Continuation status, next research target, and why the survey is not final yet.
- Open questions and source inventory.
- Framework refinement log.
- Wiki / Graph Index Status.
- Final Report Quality Gate after `report.md` exists.

## Final Report

`report.md` is the final standalone deliverable. Its body should read as a
human decision memo, while dense audit material belongs in appendices.

The readable body should contain:

- Executive summary with the answer, confidence, key reason, strongest caveat, and next action.
- Framework dimension chapters: each effective framework dimension from `index.md` / `00-brief.md` becomes a top-level body heading with narrative analysis.
- Main narrative: the situation, why it matters, what changed across rounds, and why the conclusion follows.
- Decision logic: reasoning chain, tradeoffs, and why alternatives were rejected.
- Final recommendation: who should act, who should wait, conditions, and confidence.
- What could change the conclusion: upgrade, downgrade, pivot, or kill triggers.
- Next actions with concrete steps, monitoring metrics, stop/continue triggers, and owner/timeframe where useful.
- Limits of the report: missing data, uncertainty, freshness, and external validation needs.

Appendices should contain:

- Evidence/source appendix with decisive claims, source titles, URLs, dates checked, and confidence notes; summarize decisive evidence and keep full registry detail in JSONL.
- Method and source quality, including search tools used, source types, confidence rules, fallback notes, and companion-routing notes.
- Red-team notes with strongest objections, substitutes, kill criteria, and falsification tests.
- Options or scenarios with pros, cons, trigger conditions, and expected implications.
- Source notes with source inventory, dates checked, URLs, and companion/wiki/indexing notes.

Keep final report citations standalone. Use source titles, Markdown links,
footnotes, URLs, or an appendix reference list in `report.md`; reserve `C*` and
`E*` registry IDs for working artifacts and JSONL registries.

## Quick Mode

For quick mode, a single `NN-round.md` can replace the split artifacts when it
contains the same essential thinking:

- research question
- evidence plan
- evidence and sources
- brainstorming checkpoint
- red-team challenge
- synthesis
- raw decision: first non-empty decision line must be exactly `Keep`, `Narrow`, `Pivot`, `Kill`, or `Final`
- next step

Use quick mode for low-stakes triage. For investment, legal, medical, security,
production, or major business commitment decisions, use standard or deep mode
before final delivery.
