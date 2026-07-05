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
- Target residual to reduce: identify the primary residual (`r_q`, `r_c`, `r_e`, `r_h`, `r_a`, `r_s`, or `r_j`), why this is the steepest useful direction, expected information value, research cost, and the result that would make another desk-research round unnecessary.
- Decision-critical variables that could change the recommendation.
- Minimum direct evidence: what must be observed directly, what is only background, what cannot substitute for direct proof, and how the Framework Profile Router / Evidence Contract changes those requirements.
- Source plan: primary or official sources, direct measurements, registry updates, current-source search path, and companion routing if needed.
- Disconfirming evidence and substitutes that would weaken or falsify the current path.
- Missing evidence handling: whether the gap needs another desk-research pass, non-desk validation, future facts, interviews, experiments, legal review, or explicit uncertainty.
- Framework evidence map: one `### <framework dimension>` subsection per brief-defined or evidence-refined dimension, naming the dimension weight, veto status, minimum direct evidence, preferred source type, disconfirming evidence, and what to do if the evidence is missing.

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
- Residual vector `r_q/r_c/r_e/r_h/r_a/r_s/r_j`, each scored 0-3. `0` means resolved for the decision, `1` means minor gap, `2` means material but manageable gap, and `3` means decision-level gap.
- Target residual for the next round, expected information value of next research, research cost, and `VOI greater than cost: yes/no`.
- Hard constraints satisfied, blocking hard constraints, and soft residuals that can be weighted.
- Evidence coverage, weakest dimensions, implied expectation check and reverse-check, future facts vs desk-researchable gaps, anti-narrative regularizers, decision tree triggers, Bayesian update needed, Kill scope, original question still open, continue/stop implication, and next-round focus.
- Next-round target.
- Evidence needed next.

## Index

`index.md` should contain:

- Current thesis and current evidence-bound conclusion.
- Round ledger and decision log.
- Continuation status with machine-readable workflow state, pending approval, resume action, last completed stage, next research target, and why the survey is not final yet.
- Open questions and source inventory.
- Framework refinement log.
- Residual Gate: residual vector, whether any residual is at 3, highest residual, pass/fail/pending status, and the next descent direction.
- Hard Constraint Gate: whether hard constraints are satisfied, blocking hard constraints, and pass/fail/pending status.
- Wiki / Graph Index Status.
- Final Report Quality Gate after `report.md` exists.

`Continuation Status` must distinguish real blockers from transient host/tool
approval. Use `Workflow State: awaiting_tool_approval` only while an actual tool
approval is pending, and include `Pending Approval:` plus `Resume Action:`. Once
approval is granted, resume that action immediately and move the state back to
the active stage; do not leave the survey parked at approval.

The workflow state must also match the latest gate: `continuing_round` after
`Keep`, `Narrow`, or `Pivot`; `ready_to_finalize` after `Final` or `Kill` before
`report.md` exists; `final_report_draft` while a final report exists but still
needs final checks; and `final` only for delivery-ready surveys with
`Resume Action: none`.

## Final Report

`report.md` is the final standalone deliverable. Its body should read as a
human decision memo, while dense audit material belongs in appendices.

The readable body should contain:

- Executive summary with the answer, confidence, key reason, strongest caveat, and next action.
- Framework dimension sections: each effective framework dimension from `index.md` / `00-brief.md` gets a readable body section before appendices. These sections are derived from the current Framework Contract, not from a rigid industry template. They may be top-level chapters or nested under the narrative / decision logic when that reads better, but each dimension needs substantive analysis, not only a checklist mention.
- Main narrative: the situation, why it matters, what changed across rounds, and why the conclusion follows.
- Decision logic: reasoning chain, tradeoffs, and why alternatives were rejected.
- Final recommendation: who should act, who should wait, conditions, and confidence.
- What could change the conclusion: upgrade, downgrade, pivot, or kill triggers.
- Next actions with concrete steps, monitoring metrics, stop/continue triggers, and owner/timeframe where useful.
- Limits of the report: missing data, uncertainty, freshness, and external validation needs.

Appendices should contain:

- Evidence/source appendix with a `Decision-Critical Claims` mapping: decisive claims, status, source titles, URLs, dates checked, and confidence notes. Summarize decisive evidence and keep full registry detail in JSONL.
- Method and source quality, including search tools used, source types, confidence rules, fallback notes, Framework Profile Router choices, Evidence Contract coverage, and companion-routing notes.
- Red-team notes with strongest objections, substitutes, kill criteria, and falsification tests.
- Options or scenarios with pros, cons, trigger conditions, and expected implications.
- Source notes with source inventory, dates checked, URLs, and companion/wiki/indexing notes.

Keep final report citations standalone. Use source titles, Markdown links,
footnotes, URLs, or an appendix reference list in `report.md`; reserve `C*` and
`E*` registry IDs for working artifacts and JSONL registries. Every registered
source URL used by supported, partial, or contested decision-critical claims
should appear in the final report appendix so the reader can audit the report
without opening JSONL files.

For round artifacts, do not fill every framework dimension with boilerplate just
to satisfy the shape. The active round should expand the dimensions tied to the
target residual and any veto dimensions. Dimensions with no new evidence may be
listed as `Deferred dimensions:` or `Unchanged dimensions:` with a short reason.

## Adaptive Research Framework

The Adaptive Research Framework is a routing layer, not a replacement for the
staged workflow. It should be visible in `00-brief.md` and carried through the
round artifacts as the current framework state.

`00-brief.md` should record:

- Framework Profile Router: primary decision archetype, secondary archetypes,
  selected lens packs, domain hints, profiles considered but rejected, and why
  the selected profile fits the real decision.
- Framework Contract: active dimensions, veto dimensions, intentionally
  deferred or out-of-scope dimensions, chapter weights, and why each dimension
  affects the action recommendation.
- Evidence Contract: minimum direct evidence by dimension, preferred source
  types by dimension, disconfirming evidence by dimension, evidence that cannot
  substitute for direct proof, and the weakest expected evidence area.

Use decision archetypes such as product opportunity, market entry,
competitor/positioning analysis, technical feasibility, open-source adoption,
adoption/procurement, investment/diligence, policy/trust risk, or a custom
archetype. Industry/domain hints may raise the evidence standard or add veto
dimensions, but they must not become rigid industry templates.

If evidence shows the original profile is wrong, record the change in
`index.md` under Framework Refinement Log with the evidence trigger and a note
that the original question/core is preserved. A profile refinement is valid only
when it follows from evidence, residuals, red-team critique, or hard constraints.

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
- stopping gate: residual vector, whether any residual is at `3`, VOI vs cost, hard constraints, and blocking hard constraints
- next step

Use quick mode for low-stakes triage. For investment, legal, medical, security,
production, or major business commitment decisions, use standard or deep mode
before final delivery.
