---
name: super-survey
description: Use when researching product opportunities, markets, open-source projects, competitors, technical feasibility, or business ideas that need multiple evidence-backed rounds and adversarial critique.
---

# Super Survey

## Overview

Super Survey turns a vague research target into progressively sharper conclusions through repeated research, red-team critique, synthesis, and persisted artifacts. Use it for product discovery, market validation, open-source project scouting, investment-style diligence, or strategic decisions.

The foundational anti-sycophancy theory paper for this skill is `如何拒绝AI谄媚人类.md`. It explains why open-ended research should be treated as constrained decision optimization rather than direct answer generation. Use it as the conceptual basis for objective reconstruction, constraint modeling, implied-expectation checks, scenarios, Bayesian updating, and decision-tree output.

## Operating Rules

Every survey round follows one staged judgment loop:

1. Frame the user's wording as a starting point, not the objective function.
2. Choose a generic research lens, explicit framework dimensions, and evidence standard.
3. Write the evidence plan and minimum direct evidence before current-source search.
4. Gather evidence, update `sources.jsonl`, `claims.jsonl`, and `evidence.jsonl`, and separate findings from interpretation.
5. Re-enter brainstorming after research to compare reframes and next evidence moves.
6. Red-team the strongest current argument, substitutes, weak evidence, constraints, and kill criteria.
7. Synthesize a conditional judgment with confidence, decision rationale, and remaining unknowns.
8. Run the lightweight evolver and use its raw `Keep / Narrow / Pivot / Kill / Final` decision for continuation.
9. Keep `index.md` as the round workbench and decision ledger; write `report.md` only after the raw evolver decision is `Final` or `Kill`.
10. Run `survey_round.py check` for rounds and `check-final` before final delivery.

Move beyond collecting links. The value of this skill is sharper judgment after each loop.

Empty templates are not artifacts. A round is incomplete until each file contains substantive findings, critique, synthesis, and evolved next-target content.

`index.md` is the per-round workbench, navigation page, and decision log. Reserve `report.md` for the final complete deliverable: a full standalone report in the selected artifact language, written after the raw evolver decision is `Final` or `Kill`, then validated with the final quality gate before the user-facing answer. During continuing rounds, update `index.md` for progress, decisions, and next targets.

Use front-loaded guidance to improve research quality before the agent starts collecting evidence. Do not compensate for weak research by raising after-the-fact thresholds. The brief and round templates should surface decision-critical variables, minimum direct evidence, implied-expectation reverse-checks, constraint-specific recommendation branches, and anti-narrative regularizers early enough to guide source selection and synthesis.

## Workflow

### Optional Companion Skills

Super Survey is the research loop owner. It may route specific subtasks to companion skills when they are available, while keeping them optional rather than hard dependencies. If a companion is missing, continue with the common Super Survey workflow and record the fallback in the relevant artifact.

Recommended companion routing:

| Need | Prefer | Record where |
|---|---|---|
| Brainstorming checkpoints, reframing, next-move comparison | `superpowers:brainstorming` or equivalent brainstorming workflow | `00-brief.md`, `NN-brainstorm.md` |
| Current web search, recent facts, source discovery | Use the Current Source Search rule below | `NN-research.md` Source Registry Updates and Data Quality Notes |
| Formal long report, many citations, HTML/PDF, strict citation validation, extensive source triangulation | `deep-research` or equivalent deep research/reporting skill | `NN-research.md`, `report.md`, registry JSONL files, `index.md` |
| Customer voice / VOC / Reddit or review mining | customer-research, reddit-research, or equivalent VOC workflow | `NN-research.md` Claim And Evidence Notes and `NN-redteam.md` alternatives |
| Competitor matrix, positioning map, SWOT | competitive-research or equivalent competitor-analysis workflow | `NN-research.md`, optional competitor notes, `NN-synthesis.md` |
| Long-term source and knowledge persistence | Prefer `karpathy-llm-wiki` / `Astro-Han/karpathy-llm-wiki`; local `llm-wiki`, `pin-llm-wiki`, or another indexer are valid alternatives when they fit the project | `index.md` Wiki / Graph Index Status |
| Reusable marketing or growth ideas after the research conclusion | `marketing-ideas` or equivalent ideation skill | `NN-synthesis.md` Recommended Next Action |

Use companions to gather or package evidence while keeping Super Survey's judgment loop in charge. The final round still must include findings, red-team critique, synthesis, evolver decision, and persisted artifacts. Record a companion skill as used only when it actually ran.

For a formal long report, a large citation-backed report, many citations, HTML/PDF output, strict citation validation, or publication-style source audit, prefer `deep-research` or an equivalent companion when available. If no suitable companion is available, continue with Super Survey, record the capability gap, and keep red-team critique, evolver decision, and final decision convergence inside Super Survey.

Recommended optional setup:

- Install or enable Superpowers brainstorming when available; if absent, record `Assumed` and perform a lightweight written checkpoint inside the survey artifacts.
- Install or enable a Karpathy-style LLM Wiki when long-term knowledge accumulation matters. Prefer `karpathy-llm-wiki` / `Astro-Han/karpathy-llm-wiki`; use local `llm-wiki` as the next fallback, and `pin-llm-wiki` only when project wiki config exists. If absent, maintain Markdown-only `index.md` and record the exact failure.
- Install or enable `tavily-search` when the Current Source Search rule applies.

### Current Source Search

When current-source discovery matters and Tavily fits the source surface, prefer `tavily-search` as the first discovery path.

Use built-in web search or another search tool when one of these conditions applies:

- `tvly` is not installed.
- Tavily is not authenticated.
- The Tavily command fails or times out.
- Tavily returns clearly insufficient results for the needed source type.
- The task needs a source surface Tavily does not cover well.

When current-source discovery matters, record the search path in `NN-research.md` under Data Quality Notes. Make Tavily use or fallback explicit and auditable.

Record search execution in `NN-research.md`:

- Current Source Discovery: `yes` or `no`.
- Search tool used: `tavily-search`, fallback web search, or another named tool.
- Query examples or domains searched.
- Fallback reason, if any.
- Any freshness limits, date filters, domain filters, or source-type filters.

This is a tool-selection rule, not a research-type branch. It applies across product, market, technical, policy, open-source, and custom lenses when current sources matter. Stable local/code/document-only surveys can mark current-source discovery as not needed.

### Ideal Execution Flow

Use this execution architecture for standard and deep surveys. It implements the
anti-sycophancy paper through objective reconstruction, evidence planning,
multi-start brainstorming, counterfactual and red-team testing, sensitivity
analysis, implied-expectation checks, Bayesian updating, scenario/decision-tree
synthesis, and final human-readable reporting.

| Node | Work | Runtime method |
|---|---|---|
| Brief / Frame Contract | Preserve the original question, reconstruct the objective function, split facts/assumptions/inferences/value judgments, define constraints, candidate actions, and the research framework. | Objective reconstruction; assumption split; object/action split; constraint modeling |
| Evidence Plan / Minimum Direct Evidence | Define decision-critical variables, minimum direct evidence, priority source types, disconfirming evidence, missing-evidence handling, and framework-level evidence needs before source collection. | Evidence standard; counterfactual probes; sensitivity variables; anti-narrative regularizers |
| Research | Collect current and primary evidence according to the plan, update source/claim/evidence registries, record contradictions, confidence, freshness, and framework coverage. | Claim-level evidence; source freshness; contradiction tracking; Bayesian update inputs |
| Post-Research Brainstorming | Re-open candidate explanations after evidence exists, compare multi-start perspectives, identify likely errors, next evidence moves, and evidence-triggered framework refinements. | Multi-start perspectives; counterfactual reframing; sensitivity focus; framework refinement |
| Redteam | Attack the strongest current argument, substitutes, hidden assumptions, kill criteria, and anti-narrative regularizers. | Counterfactual testing; adversarial validation; regularization against popular narratives |
| Synthesis | Integrate evidence and objections into sensitivity analysis, implied-expectation reverse-checks, Bayesian updates, scenarios, decision trees, and constraint-specific recommendation branches. | Sensitivity analysis; implied-expectation reverse-check; Bayesian updating; scenarios; decision tree output |
| Evolver | Decide Keep / Narrow / Pivot / Kill / Final, separate future facts from desk-researchable gaps, and generate the next-round target or finalization rationale. | Multi-start search control; adversarial validation; evidence-driven continuation |
| Final Report | Write a standalone human decision memo with body chapters from the framework, decision logic, recommendation, change triggers, next actions, limits, and appendices. | Decision memo; constraint-specific recommendation; quality gate |

### Superpowers Brainstorming Loop

Use `$superpowers brainstorming` throughout the survey. It has two roles:

1. **Round 0 framing**: before research starts, clarify:
   - the practical decision the survey must support
   - audience / buyer / target user
   - success criteria and disqualifying conditions
   - depth mode
   - whether the user wants autonomous continuation or checkpoint approval

2. **Per-round checkpoint**: after each research pass and before the next round, use brainstorming to:
   - restate what changed
   - ask or record any new clarifying question
   - propose 2-3 possible next moves
   - compare candidate exploration paths
   - record the preferred exploration path and assumptions

Brainstorming proposes routes; the latest `NN-evolver.md` decision owns the machine-readable continue/stop decision.

For quick exploratory requests, keep each checkpoint lightweight: explicit assumptions and a concise next-move comparison are enough when the user already gave enough constraints.

Record Round 0 in `00-brief.md` under `Superpowers Brainstorming Gate`. Record each round checkpoint in `NN-brainstorm.md`.

Allowed Round 0 statuses:

- `Completed`: brainstorming was used.
- `Assumed`: enough constraints were present; assumptions were recorded.
- `Skipped by user`: user explicitly skipped it.

Fill Round 0 and per-round brainstorming fields with status, assumptions, or the completed checkpoint.

### Initialize Survey

Create a survey directory under the current project unless the user specifies another root:

```text
surveys/YYYY-MM-DD-topic-slug/
```

Use the helper to initialize the survey and start the first staged round:

```bash
python3 <skill-dir>/scripts/survey_round.py init "AI recruiting agent" --mode standard
python3 <skill-dir>/scripts/survey_round.py init "AI recruiting agent" --language zh --mode quick
python3 <skill-dir>/scripts/survey_round.py init "AI recruiting agent" --language ja --mode deep
python3 <skill-dir>/scripts/survey_round.py round surveys/2026-06-12-ai-recruiting-agent 1
```

Resolve `<skill-dir>` to the directory containing this `SKILL.md` so the workflow works across Codex, agent, and local installs.

Supported artifact languages: `en`, `zh`, and `ja`. Use the user's language by default. The helper stores the language in `.super-survey.json`; `round` and `check` reuse it automatically.

Supported modes:

| Mode | Use When | Minimum Registry | Report Gate |
|---|---|---:|---|
| `quick` | Directional scan or early triage | 1 source, 1 claim, 1 evidence item | score >=80, shorter report |
| `standard` | Default reusable research report | 3 sources, 3 claims, 3 evidence items | score >=90 |
| `deep` | Formal or high-stakes report, many citations, strict audit needs | 8 sources, 6 claims, 8 evidence items | score >=95, route long packaging to `deep-research` when available |

Write `00-brief.md` with:

- User question
- Superpowers Brainstorming Gate
- Practical decision to make
- Research lens
- Research framework with explicit dimensions and one `###` subsection per dimension
- Decision evidence standard
- Decision frame integrity
- Decision Optimization Contract: original question, reconstructed objective function, candidate actions, wait/continue option, constraints, success/failure criteria, opportunity cost, reversibility, implied expectations, implied-expectation reverse-check, decision-critical variables, minimum direct evidence, constraint-specific recommendations, anti-narrative regularizers, and decision-changing evidence
- Target user/customer
- Success criteria
- Disqualifying conditions
- Initial assumptions
- Continuation policy

In `Decision Frame Integrity`, split the user's wording into known facts, unverified assumptions, subjective judgments, missing information, and stakeholders. Then state the reframed objective, competing objectives, and what the survey should not optimize for. This is the anti-sycophancy / anti-local-optimum check: the survey should optimize the real decision, not the user's first phrasing, emotional stance, or an easier-to-kill stronger claim.

Also separate object quality from action attractiveness. A good object is not automatically a good action: good company does not automatically mean good stock; good product does not automatically mean good business; good technology does not automatically mean good project; good open-source library does not automatically mean good dependency. Record hard constraints, soft constraints, user-specific constraints, missing constraints, and implied expectations before deciding what evidence can change the action.

The `Decision Optimization Contract` makes the objective executable. It states the decision variables, constraints, candidate actions, opportunity cost, reversibility, and evidence that would change the action. This contract is domain-generic: use it for product, market, technical, open-source, diligence, strategy, or custom research without turning Super Survey into a securities-specific workflow.

Keep the number of rounds open, and reserve stop conclusions for completed round artifacts. `00-brief.md` must preserve the user's original question and record the decision frame without rewriting it into a stronger or easier-to-kill claim. Any narrowing must say what evidence, assumption, or red-team objection justifies the narrower frame. `00-brief.md` states the continuation policy: start with the next evidence round, update `index.md` after the round, then decide whether to continue only after evidence, red-team critique, synthesis, and the raw evolver decision are written. Actual round history belongs in `index.md`.

Make the research framework travel through the whole workflow. Once `00-brief.md` names framework dimensions, every round artifact must use those dimensions as its thinking structure. Keep each dimension lightweight when needed, and write actual dimension-level reasoning instead of a generic audit note such as "framework coverage checked."

If the user only wants a quick answer, use `--mode quick` and keep the artifact set lightweight. A quick survey can use one combined `NN-round.md` containing research, evidence, brainstorming, red-team critique, synthesis, decision, and next step, or it can use the full split artifact set when that is clearer. It needs `report.md` only at final delivery. The sections can be concise, and validation still includes red-team critique and the evolver decision.

Create these registry files during initialization:

```text
sources.jsonl
claims.jsonl
evidence.jsonl
```

Minimum JSONL schemas:

- `sources.jsonl`: `source_id`, `title`, `url`, `source_type`, `date_checked`, `credibility`
- `evidence.jsonl`: `evidence_id`, `source_id`, `quote_or_summary`, `locator`, `confidence`
- `claims.jsonl`: `claim_id`, `claim`, `supporting_evidence_ids`, `status`

Use stable IDs such as `S1`, `E1`, and `C1`. Every evidence item must reference an existing `source_id`. Every supported, partial, or contested claim must reference existing `evidence_id` values. The helper also rejects duplicate IDs and obviously weak claim-support pairs, such as a claim with numbers, entities, or key terms absent from the linked evidence. This is a lightweight guard; human citation judgment remains required.

### Staged Research Round

For each standard or deep round, run the workflow as ordered process nodes. The
Markdown files are the outputs of those nodes, not a checklist to fill after the
answer is already known. Read `references/artifact-contracts.md` when authoring,
reviewing, or debugging the detailed contents of each stage artifact:

```text
NN-evidence-plan.md
NN-research.md
NN-brainstorm.md
NN-redteam.md
NN-synthesis.md
NN-evolver.md
index.md
```

Do the work in this order:

| Process node | Work to do now | Stage output |
|---|---|---|
| Evidence Plan | Define the round target, decision-critical variables, minimum direct evidence, priority source types, disconfirming evidence, and missing-evidence handling by framework dimension before any current-source collection. | `NN-evidence-plan.md` |
| Research | Search, read, measure, and register evidence according to the written evidence plan. Separate findings from interpretation; update `sources.jsonl`, `claims.jsonl`, and `evidence.jsonl`; record framework coverage, contradictions, direct-evidence gaps, source freshness, and the search path used. | `NN-research.md` plus registry JSONL updates |
| Post-Research Brainstorming | Re-open the question after evidence exists. Compare candidate explanations, multi-start perspectives, reframes, and next evidence moves based on the written research findings. | `NN-brainstorm.md` |
| Redteam | Attack the strongest current argument that emerged from research and brainstorming. Test substitutes, hidden assumptions, anti-narrative regularizers, kill criteria, and what would make the thesis false. | `NN-redteam.md` |
| Synthesis | Integrate the evidence and objections into a conditional judgment. Run sensitivity analysis, implied-expectation reverse-checks, Bayesian updates, scenarios, decision trees, and constraint-specific recommendation branches. | `NN-synthesis.md` |
| Evolver | Decide Keep / Narrow / Pivot / Kill / Final from the completed synthesis. Separate desk-researchable gaps from future facts or non-desk validation, then name the next-round target or finalization rationale. | `NN-evolver.md` and `index.md` updates |

Use the staged CLI to create the output file for the current node, then fill that
file with substantive content before moving to the next node:

1. `round` / `plan`: create and complete `NN-evidence-plan.md`.
2. `research`: create and complete `NN-research.md` after `NN-evidence-plan.md` is written.
3. `brainstorm`: create and complete `NN-brainstorm.md` after `NN-research.md` is written.
4. `redteam`: create and complete `NN-redteam.md` after `NN-brainstorm.md` is written.
5. `synthesis`: create and complete `NN-synthesis.md` after `NN-redteam.md` is written.
6. `evolve`: create and complete `NN-evolver.md` after `NN-synthesis.md` is written.

At each node, read the upstream artifact from disk before writing the downstream
artifact. The downstream artifact should cite or build on upstream content
already written to disk. The agent should not use these files as an after-action
audit trail for a conclusion formed earlier; the files are the thinking path
itself. If source search or a final conclusion happened before the evidence plan
was written, restart from the proper node, record the corrected sequence, and
continue from there.

This artifact dependency order is a prompt-level workflow discipline first and a
CLI convenience second: each process node does its own work, writes its own
output, and then hands that written output to the next process node.

For quick mode, a single `NN-round.md` can replace the split round artifacts when it contains the same essential thinking: research question, evidence plan, evidence and sources, brainstorming checkpoint, red-team challenge, synthesis, raw decision, and next step.

Create or update `report.md` only after the latest evolver decision is `Final` or `Kill`. While the latest decision is `Keep`, `Narrow`, or `Pivot`, use `index.md` for the current thesis, round summaries, continuation status, next research target, and why the survey is still in progress.

After the raw evolver decision is `Final` or `Kill`, draft `report.md` as a complete, standalone report that a user can read smoothly without opening every round artifact. It is not an audit checklist. Put the human-readable argument first and move dense evidence, source, method, red-team, scenario, and scoring material into appendices. Use `references/artifact-contracts.md` for the detailed final report body and appendix contract.

Prose-first rule: before the first evidence appendix, `report.md` should read as narrative prose with short lists where helpful. Place Markdown evidence tables, source inventories, claim registers, and audit checklists in appendices or the JSONL registry.

Draft the report section by section from the argument rather than the audit trail. Final report citations must be standalone: cite source titles, Markdown links, footnotes, or an appendix reference list with URLs and enough source context to read without opening the JSONL files. Use `C1`, `E1`, and other registry IDs only inside working artifacts and JSONL registries.

The readable body should contain, before appendices:

- Executive summary with the answer, confidence, key reason, strongest caveat, and next action.
- Framework dimension chapters: each effective framework dimension from `index.md` / `00-brief.md` must become a top-level body heading such as `## Market Environment` or `## User Pain`, with narrative analysis under it. Put the dimension analysis in the body rather than under a generic `Framework Dimension Analysis` heading, method note, scorecard, evidence appendix, or source audit.
- Main narrative: the situation, why it matters, what changed across rounds, and why the conclusion follows.
- Decision logic: the reasoning chain, tradeoffs, and why alternatives were rejected.
- Final recommendation: who should act, who should wait, conditions, and confidence.
- What could change the conclusion: upgrade/downgrade/pivot/kill triggers.
- Next actions with concrete steps, monitoring metrics, stop/continue triggers, and owner/timeframe where useful.
- Limits of the report: missing data, uncertainty, freshness, and external validation needs.

For non-trivial surveys, `report.md` must be longer and more complete than `NN-synthesis.md`, but length alone is not quality. It should read like a coherent memo with supporting appendices, not a pile of evidence tables. A report that only contains a few bullets is incomplete; a report that opens with long source tables before explaining the judgment is also incomplete. A report that names a research framework but does not analyze those dimensions as body subchapters is incomplete.

New surveys use report schema v3. Legacy reports with older report schemas remain readable, and the final delivery gate expects the v3 schema. Run `survey_round.py upgrade-report <survey-dir>` and then expand the appended sections before final delivery. `upgrade-report` appends missing v3 report sections and updates metadata; you still write the report content.

### Research Lens And Framework

Use a research lens as a lightweight emphasis guide, not a hard decision-type branch. Use a research framework as the reader-visible method for how the report will systematically examine the question. A survey can combine lenses and frameworks when needed.

Pick or write 1-3 lenses that best match the question, such as buyer/user, workflow, market/competitor, technical, policy/trust, open-source, or a custom lens. Then select or write a research framework with explicit dimensions. The framework answers: what dimensions will this research cover, what question does each dimension answer, and which dimensions are weak or intentionally out of scope?

The framework must travel through the whole workflow. `00-brief.md` defines the dimensions; `NN-evidence-plan.md`, `NN-research.md`, `NN-brainstorm.md`, `NN-redteam.md`, `NN-synthesis.md`, and `NN-evolver.md` each expand those same dimensions with `###` subheadings in their framework-relevant section. The final `report.md` then turns the dimensions into readable body chapters. This prevents the common failure mode where the agent lists materials first and only adds a framework audit note afterward.

Evidence can refine the framework, but only explicitly. If a round shows that the initial dimensions are too broad, missing a veto dimension, or no longer match the evidence, update `index.md` under `Framework Refinement Log` with:

- `Current dimensions: ...`
- `Evidence trigger for changes: ...`
- `Original question/core preserved: ...`

After that, use the current dimensions from `index.md` in later round artifacts. Make framework revisions explicit in `index.md`; a revision is valid only when it is evidence-triggered and preserves the user's original decision frame.

Fit the framework to the user's actual question rather than forcing every survey into a predefined category. The lens determines which evidence deserves extra attention; the framework makes the research method visible to readers. The common Super Survey loop still applies, and a framework is a method, not a prewritten conclusion or a narrow decision-type branch. Read `references/research-quality.md` for framework starters and domain examples.

### Anti-Sycophancy / Anti-Local-Optimum Checks

Treat the user's prompt as an initial point in the search space. Before gathering evidence or stating a thesis, ask whether the prompt embeds a target function, hidden constraint, desired answer, or exaggerated claim. Record this in `00-brief.md` rather than silently accepting it.

Use these checks across domains:

- Separate known facts, unverified assumptions, subjective judgments, missing information, and stakeholders.
- Reconstruct the objective and list competing objectives before collecting sources.
- Record hard constraints, soft constraints, user-specific constraints, missing constraints, and object/action split: a good object is not automatically a good action.
- Use multi-start perspectives, Sensitivity And Counterfactuals, Bayesian update, decision tree reasoning, implied-expectation reverse-check, anti-narrative regularizers, and constraint-specific recommendation branches when the decision stakes justify them.
- Preserve the user's actual decision and stakes. If a kill criterion only rejects an exaggerated version of the prompt, choose `Narrow` or `Pivot` instead of ending the survey.

`NN-evolver.md` should contain the output of the built-in lightweight evolver:

- Probe questions and answers
- Persona judgments
- Keep / Narrow / Pivot / Kill / Final decision
- Round evidence quality gate: one `### <framework dimension>` subsection per brief-defined dimension, then evidence coverage, weakest dimensions, implied expectation check and reverse-check, future facts vs desk-researchable gaps, anti-narrative regularizers, decision tree triggers, Bayesian update needed, Kill scope, original question still open, continue/stop implication, and next-round focus
- Next-round target
- Evidence needed next

### Evolve The Target

At the end of each round, run the built-in lightweight evolver. It is inspired by autoresearch-style `probe`, `reason`, and `improve` loops, but it is research-native: it evolves questions and decisions, not code.

Read `references/lightweight-evolver.md` when the research target is broad, ambiguous, commercially important, or after round 1.

The evolver must:

1. Probe assumptions until the weak point is explicit.
2. Run adversarial reasoning across at least five personas.
3. Decide `Keep`, `Narrow`, `Pivot`, `Kill`, or `Final` using a single raw decision label, not an explanatory paragraph.
4. Generate the next-round target as a testable question.
5. Name the evidence that would change the decision.
6. When the decision is `Kill`, write the Kill scope: thesis, path, candidate action, or original question. Also state whether the original question is still open and what pivot or next answer path remains.

Rewrite the target into a more specific question. Examples:

- From: "Is AI recruiting worth doing?"
- To: "Can a semi-automated job-search copilot for US software engineers charge $19/month without violating job-board terms?"

Prefer narrower customer, geography, channel, workflow, and pricing assumptions.

External autoresearch tools are optional. If available, prefer adversarial planning modes such as `probe`, `reason`, or `improve`. Use metric-based code optimization loops only when the research question has a command-based measurable metric.

### Wiki / Graph Index

Always maintain `index.md` with:

- Current thesis
- Current evidence-bound conclusion
- Round ledger
- Continuation status
- Next research target
- Why the survey is not final yet
- Open questions
- Source inventory
- Framework refinement log
- Wiki / Graph Index Status
- Decision log

When long-term persistence is needed, route the survey into a wiki or graph index before final delivery. Prefer `karpathy-llm-wiki` / `Astro-Han/karpathy-llm-wiki`; fall back to local `llm-wiki`, project `pin-llm-wiki`, another document/graph indexer, or Markdown-only `index.md` when needed. Claim a wiki or graph was built only when the ingest/indexing command or file write actually ran. If only `index.md` was updated, say that directly.

When wiki persistence is needed, `index.md` records:

- `Wiki Persistence Needed: ...`
- `Wiki Tool Attempted: ...`
- `Wiki Ingest Result: ...`
- `Wiki Fallback Reason: ...`
- `Wiki Artifact Path: ...`

For bounded or one-off surveys, mark `Wiki Persistence Needed: no` and keep `index.md` as the persistence artifact. `code-review-graph` is not a substitute for the survey wiki; use it only when the survey target is a code repository and code structure analysis is needed.

### Final Quality Gate And Continuation

Super Survey supports arbitrary positive round numbers; evidence quality and the raw evolver decision define the stopping rule. The brief keeps future round counts open.

Score the final `report.md` on a 100-point rubric before finalizing, and record that score in `index.md` under `Final Report Quality Gate`. Before `report.md` exists, record provisional quality notes in `NN-evolver.md` and `index.md` as provisional notes only.

| Dimension | Points | What Good Looks Like |
|---|---:|---|
| Anti-sycophancy / objective-function integrity | 20 | User framing is challenged, the original question is preserved, the objective function is reconstructed, stronger easy-to-kill claims are avoided, constraints and implied expectations are explicit |
| Source, method, and framework quality | 15 | Current sources where needed, primary sources preferred, search tools/fallbacks recorded, research framework stated, body chapters cover the framework dimensions, and coverage gaps are disclosed |
| Evidence completeness | 20 | Claim-level evidence, contradictions, confidence, source freshness, and enough coverage for the decision |
| Analysis and red-team quality | 20 | Synthesis across evidence, alternatives, objections, kill criteria, and falsification tests |
| Actionability | 15 | Concrete recommendation, next actions, owners/timeframes when useful, monitoring and stop/continue triggers |
| Structure and readability | 10 | Standalone narrative first, appendices second, clear headings, readable tables, no template residue |

`index.md` must include the anti-sycophancy / objective-function integrity subscore in the final quality gate. The helper treats a missing subscore as a final-gate failure because a high total score should not hide a report that simply accepts the user's initial framing.

Mode-specific thresholds are stricter for deeper work. `quick` can pass at 80 when the user only needs directional triage. `standard` should pass at 90. `deep` should pass at 95 and use larger source/claim/evidence coverage. Use `quick` explicitly when speed matters more than completeness; keep `standard` and `deep` thresholds intact for reusable reports.

Use raw gates to decide whether to stop:

- `Keep`, `Narrow`, or `Pivot` always require another round.
- `Final` means no desk-research target remains that could materially change the user's original decision, so the loop can move to final report writing.
- `Kill` means the current thesis is not worth another desk-research round or should switch to non-desk validation.
- Stop only after `report.md` exists, the `index.md` final quality score passes the selected mode threshold, the latest decision is `Final` or `Kill`, and `check-final` passes.
- `report.md` may explain uncertainty, future disclosure needs, or external validation needs, but the helper relies only on the raw evolver decision and the score threshold.

Run `survey_round.py check <survey-dir>` before treating a round as complete. It validates round artifacts, registry links, framework coverage, companion notes when required, and the latest raw evolver gate. Use `validate-evidence` only for focused registry debugging.

Run `survey_round.py check-final <survey-dir>` before presenting the survey as final. If it fails because the report is legacy or thin, run `upgrade-report` when needed, expand the report, or create another round focused on the weakest dimensions.

Before final delivery, confirm the essentials: substantive sections, valid registry IDs, framework dimensions carried through the split artifacts or quick artifact, current-source search notes when needed, standalone report citations, prose-first body, final score in `index.md`, wiki status fields when persistence was needed, and no premature final report while the evolver says `Keep`, `Narrow`, or `Pivot`.

If the check fails, say the round is still in progress and report the next fix.

## Evidence Standard

Use current sources for market, legal, pricing, platform policy, repository activity, APIs, company facts, and competitor claims. Mark inference explicitly.

For current-source discovery, follow the Current Source Search rule above and document the chosen search path or fallback.

Use this confidence scale:

- **High**: multiple current primary sources or direct measurements agree.
- **Medium**: credible secondary sources plus some direct evidence.
- **Low**: weak public data, anecdotes, extrapolation, or unverified claims.

Read `references/research-quality.md` when the task is high-stakes, market-facing, legal/compliance-sensitive, or likely to become a public report.

## Output Style

Final user-facing responses should be concise and decision-oriented:

- Where the files were written
- Link or path to `report.md`
- Current conclusion
- Strongest objection
- What changed after red-team critique
- Recommended next round or action

Save the full research document to disk and summarize the important parts in chat.

Use the same language as the user's request unless they ask otherwise. When writing survey artifacts, keep all headings, findings, red-team critique, synthesis, and evolver output in one selected language: English (`en`), Chinese (`zh`), or Japanese (`ja`). Source titles and quoted terms may stay in their original language.

## Common Failure Modes

- **Link dump**: sources are collected but no decision changes. Fix by updating synthesis and evolver.
- **Weak red-team**: objections are generic. Fix by naming incumbents, data blockers, legal risks, and user apathy.
- **Generic next round**: target remains broad. Fix by narrowing customer, geography, workflow, data source, channel, or price.
- **One-time brainstorming**: brainstorming appears only in `00-brief.md`. Fix by adding `NN-brainstorm.md` for each round and using it to choose the next move.
- **False graph claim**: index tooling was mentioned but not run. Fix by saying only `index.md` was updated.
- **Skipped wiki persistence**: the survey ends with only local Markdown when long-term persistence was needed and a suitable wiki/indexer was available. Fix by reading the relevant skill or tool guide, running/performing ingest, and recording the artifact path.
- **Template theater**: files exist but contain placeholders. Fix before final response.
- **Index-as-report**: `index.md` is updated but no standalone final report exists. Fix by writing `report.md` before answering.
- **Thin final report**: `report.md` repeats only a short synthesis and omits methodology, evidence table, red-team critique, scenarios, action plan, or open questions. Fix by expanding it into a standalone report.
- **Audit-table report**: `report.md` starts with dense source tables, claim registers, or checklist sections and stays hard to read. Fix by writing a narrative body first and moving audit material into appendices.
- **Registry-ID citations**: `report.md` cites `C1`, `E1`, or similar IDs that require opening JSONL files. Fix by replacing them with source titles, Markdown links, footnotes, and URLs.
- **Framework-as-audit-note**: framework dimensions appear only as a list or coverage checklist, while `brief`, `research`, `brainstorm`, `redteam`, `synthesis`, `evolver`, or `report.md` jump to generic narrative. Fix by using the brief-defined dimensions as `###` subheadings in every framework-relevant stage and as body chapters in the final report.
- **Round-count autopilot**: the survey stops because it reached a familiar count, while the report score is weak or unknowns remain desk-researchable. Fix by scoring the report and creating the next round around the lowest-scoring dimensions.
- **Sycophantic framing / local optimum**: the survey accepts the user's stance as fact, optimizes the initial wording, or rewrites the question into a stronger easy-to-kill claim. Fix by rebuilding the objective in `Decision Frame Integrity`, checking multiple perspectives, and making recommendations conditional on the facts that would change them.
