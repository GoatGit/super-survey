---
name: super-survey
description: Use when researching product opportunities, markets, open-source projects, competitors, technical feasibility, or business ideas that need multiple evidence-backed rounds and adversarial critique.
---

# Super Survey

## Overview

Super Survey turns a vague research target into progressively sharper conclusions through repeated research, red-team critique, synthesis, and persisted artifacts. Use it for product discovery, market validation, open-source project scouting, investment-style diligence, or strategic decisions.

## Required Behavior

Every survey round must:

0. Use Superpowers brainstorming as a recurring checkpoint, not only a kickoff gate.
1. State the current research target and decision criteria.
2. Choose a generic research lens, explicit research framework, and evidence standard without forcing the work into a narrow fixed category.
3. Gather evidence from current sources when facts may have changed.
4. Re-enter a brainstorming checkpoint to reframe the problem and compare candidate next moves.
5. Separate findings from interpretation.
6. Include a red-team challenge: why the idea may fail, why evidence may be weak, what alternative explanations or substitutes exist, and what constraints invalidate the thesis.
7. Check explicit kill criteria before recommending another round.
8. Synthesize a clearer conclusion with confidence level, decision rationale, and remaining unknowns.
9. Run the lightweight evolver to sharpen or kill the next-round target.
10. Decide whether to continue using the latest evolver decision; use final report quality only after the stop gate moves to `report.md`.
11. Maintain the lightweight evidence registry: `sources.jsonl`, `claims.jsonl`, and `evidence.jsonl`.
12. Validate citations and claim support with the integrated `survey_round.py check` / `check-final` commands; use `validate-evidence` only for focused registry debugging.
13. Update an index and attempt wiki/graph indexing, or record why it was unavailable.
14. Use `index.md` as the per-round workbench and decision ledger.
15. Write `report.md` only after the stop gate passes and before giving a final answer.
16. Write the round artifacts to disk before giving a final answer.

Do not stop after collecting links. The value of this skill is sharper judgment after each loop.

Empty templates are not artifacts. A round is incomplete until each file contains substantive findings, critique, synthesis, and evolved next-target content.

`index.md` is the per-round workbench, navigation page, and decision log. It is not the final report. During continuing rounds, update `index.md` instead of drafting `report.md`. The final complete deliverable must be a full `report.md`, written in the selected artifact language, only after the stop gate passes and before the user-facing answer. Do not treat `report.md` as a short chat summary.

## Workflow

### Optional Companion Skills

Super Survey is the research loop owner. It may route specific subtasks to companion skills when they are available, but they are optional and must not become hard dependencies. If a companion is missing, continue with the common Super Survey workflow and record the fallback in the relevant artifact.

Recommended companion routing:

| Need | Prefer | Record where |
|---|---|---|
| Brainstorming checkpoints, reframing, next-move comparison | `superpowers:brainstorming` or equivalent brainstorming workflow | `00-brief.md`, `NN-brainstorm.md` |
| Current web search, recent facts, source discovery | `tavily-search` first; built-in web search or another current-source search tool only as fallback | `NN-research.md` Source Registry Updates and Data Quality Notes |
| Formal long report, many citations, HTML/PDF, strict citation validation, extensive source triangulation | `deep-research` or equivalent deep research/reporting skill | `NN-research.md`, `report.md`, registry JSONL files, `index.md` |
| Customer voice / VOC / Reddit or review mining | customer-research, reddit-research, or equivalent VOC workflow | `NN-research.md` Claim And Evidence Notes and `NN-redteam.md` alternatives |
| Competitor matrix, positioning map, SWOT | competitive-research or equivalent competitor-analysis workflow | `NN-research.md`, optional competitor notes, `NN-synthesis.md` |
| Long-term source and knowledge persistence | `karpathy-llm-wiki` / `Astro-Han/karpathy-llm-wiki` first; local `llm-wiki` second; `pin-llm-wiki` or another indexer only as fallback | `index.md` Wiki / Graph Index Status |
| Reusable marketing or growth ideas after the research conclusion | `marketing-ideas` or equivalent ideation skill | `NN-synthesis.md` Recommended Next Action |

Use companions to gather or package evidence, not to bypass Super Survey's judgment loop. The final round still must include findings, red-team critique, synthesis, evolver decision, and persisted artifacts. Never claim a companion skill ran unless it actually ran.

`deep-research` routing is required when the user asks for any of these: a formal long report, a large citation-backed report, many citations, HTML/PDF output, strict citation validation, or publication-style source audit. In that case, load and use `deep-research` as a companion for evidence persistence and long-report packaging, then return to Super Survey for red-team critique, evolver decision, and final decision convergence.

Recommended optional setup:

- Install or enable Superpowers brainstorming when available; if absent, record `Assumed` and perform a lightweight written checkpoint inside the survey artifacts.
- Install or enable a Karpathy-style LLM Wiki when long-term knowledge accumulation matters. Prefer `karpathy-llm-wiki` / `Astro-Han/karpathy-llm-wiki`; use local `llm-wiki` as the next fallback, and `pin-llm-wiki` only when project wiki config exists. If absent, maintain Markdown-only `index.md` and record the exact failure.
- Install or enable `tavily-search` when the survey depends on recent market, policy, pricing, API, repository, or company facts.

### Tavily-First Current Source Search

When facts may have changed, use `tavily-search` as the default current-source discovery path.

Before using built-in web search or another search tool, first try Tavily unless the user explicitly asks not to use it. A valid fallback requires one of these conditions:

- `tvly` is not installed.
- Tavily is not authenticated.
- The Tavily command fails or times out.
- Tavily returns clearly insufficient results for the needed source type.
- The task needs a source surface Tavily does not cover well.

When falling back, record the reason in `NN-research.md` under Data Quality Notes. Do not silently replace Tavily with another search path.

Record search execution in `NN-research.md`:

- Search tool used: `tavily-search`, fallback web search, or another named tool.
- Query examples or domains searched.
- Fallback reason, if any.
- Any freshness limits, date filters, domain filters, or source-type filters.

This is a tool-selection rule, not a research-type branch. It applies across product, market, technical, policy, open-source, and custom lenses whenever current sources matter.

### 0. Superpowers Brainstorming Loop

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

Brainstorming proposes routes; it does not own the raw continue/stop decision. The latest `NN-evolver.md` decision is the only machine-readable round decision.

For quick exploratory requests, keep each checkpoint lightweight: explicit assumptions and a concise next-move comparison are enough. Do not let brainstorming become a blocker when the user already gave enough constraints.

Record Round 0 in `00-brief.md` under `Superpowers Brainstorming Gate`. Record each round checkpoint in `NN-brainstorm.md`.

Allowed Round 0 statuses:

- `Completed`: brainstorming was used.
- `Assumed`: enough constraints were present; assumptions were recorded.
- `Skipped by user`: user explicitly skipped it.

Do not leave Round 0 or per-round brainstorming fields blank.

### 1. Initialize

Create a survey directory under the current project unless the user specifies another root:

```text
surveys/YYYY-MM-DD-topic-slug/
```

Use the helper when useful:

```bash
python3 <skill-dir>/scripts/survey_round.py init "AI recruiting agent" --mode standard
python3 <skill-dir>/scripts/survey_round.py init "AI recruiting agent" --language zh --mode quick
python3 <skill-dir>/scripts/survey_round.py init "AI recruiting agent" --language ja --mode deep
python3 <skill-dir>/scripts/survey_round.py round surveys/2026-06-12-ai-recruiting-agent 1
python3 <skill-dir>/scripts/survey_round.py check surveys/2026-06-12-ai-recruiting-agent
python3 <skill-dir>/scripts/survey_round.py check-final surveys/2026-06-12-ai-recruiting-agent
python3 <skill-dir>/scripts/survey_round.py validate-evidence surveys/2026-06-12-ai-recruiting-agent
python3 <skill-dir>/scripts/survey_round.py upgrade-report surveys/2026-06-12-ai-recruiting-agent
```

Resolve `<skill-dir>` to the directory containing this `SKILL.md`; do not assume a Codex-only install path.

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
- Target user/customer
- Success criteria
- Disqualifying conditions
- Initial assumptions
- Continuation policy

Do not predict how many rounds the survey will take, and do not prewrite a stop conclusion in `00-brief.md`. `00-brief.md` must preserve the user's original question and record the decision frame without rewriting it into a stronger or easier-to-kill claim. Any narrowing must say what evidence, assumption, or red-team objection justifies the narrower frame. `00-brief.md` must state only the continuation policy: start with the next evidence round, update `index.md` after the round, then decide whether to continue only after evidence, red-team critique, synthesis, and the raw evolver decision are written. Actual round history belongs in `index.md`, not in the brief.

The research framework is not a report-only appendix. Once `00-brief.md` names framework dimensions, every round artifact must use those dimensions as its thinking structure. Keep each dimension lightweight when needed, but do not collapse the work into a generic audit note such as "framework coverage checked."

If the user only wants a quick answer, use `--mode quick` and keep the full artifact set lightweight. A quick survey still needs `00-brief.md`, `NN-research.md`, `NN-brainstorm.md`, `NN-redteam.md`, `NN-synthesis.md`, `NN-evolver.md`, `index.md`, and registry JSONL files. It needs `report.md` only at final delivery. The sections can be concise, but validation should not bypass red-team critique or the evolver.

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

Use stable IDs such as `S1`, `E1`, and `C1`. Every evidence item must reference an existing `source_id`. Every supported, partial, or contested claim must reference existing `evidence_id` values. The helper also rejects duplicate IDs and obviously weak claim-support pairs, such as a claim with numbers, entities, or key terms that do not appear in the linked evidence. This is a lightweight guard, not a substitute for human citation judgment.

### 2. Research Round

For each round, create or update:

```text
NN-research.md
NN-brainstorm.md
NN-redteam.md
NN-synthesis.md
NN-evolver.md
index.md
```

`NN-research.md` should contain:

- Research question for this round
- Source registry updates by `source_id`; `sources.jsonl` remains the canonical source list
- Claim and evidence notes by `claim_id` / `evidence_id`; `claims.jsonl` and `evidence.jsonl` remain the canonical evidence registry
- Framework coverage: one `### <framework dimension>` subsection per brief-defined dimension, covering findings, evidence IDs, contradictions, confidence, and next evidence target
- Notes on data quality, freshness, and whether Tavily or a fallback search path was used

`NN-brainstorm.md` should contain:

- Brainstorming status
- Current framing after the research pass
- Clarifying questions or explicit assumptions
- Candidate next moves organized under one `### <framework dimension>` subsection per brief-defined dimension
- Preferred exploration path, not a final continue/stop decision
- Design notes for the next round

`NN-redteam.md` should contain:

- Strongest objections organized under one `### <framework dimension>` subsection per brief-defined dimension
- Better-funded incumbent response
- Alternative explanations or substitutes
- Data, legal, distribution, trust, and monetization risks
- Kill criteria checked
- Reasons users may not care
- What would make the thesis false

`NN-synthesis.md` should contain:

- Updated conclusion
- Confidence: low / medium / high
- Decision rationale: why the recommendation follows from the evidence
- Framework-based synthesis: one `### <framework dimension>` subsection per brief-defined dimension, then strongest dimensions, weakest dimensions, cross-dimension judgment, and framework gaps affecting confidence
- What changed from prior round
- Best next question
- Recommended next action

Do not write or update `report.md` while the latest evolver decision is `Keep`, `Narrow`, or `Pivot`. Use `index.md` for the current thesis, round summaries, continuation status, next research target, and why the survey is not final yet.

When the stop gate is ready, `report.md` should be a complete, standalone report that a user can read smoothly without opening every round artifact. It is not an audit checklist. Put the human-readable argument first and move dense evidence, source, method, red-team, scenario, and scoring material into appendices.

Prose-first rule: before the first evidence appendix, `report.md` should read as narrative prose with short lists where helpful. Do not place Markdown evidence tables, source inventories, claim registers, or audit checklists in the body. Tables belong in appendices or the JSONL registry.

Draft the report section by section, not by pasting the audit trail. For each body section, write the section's decision purpose, the key claim, the evidence IDs that support or weaken it, the strongest counterpoint, and the implication for the reader. If a section cannot do that in prose, the survey probably needs another evidence pass or a narrower section question.

The readable body should contain:

- Executive summary with the answer, confidence, key reason, strongest caveat, and next action.
- Reader's path: who the report is for, what decision it supports, and what to read first.
- Research method and framework: the framework used, why it fits, which dimensions were covered, and which dimensions remain weak or out of scope.
- Framework dimension analysis: each framework dimension must become a body subheading, such as `### Market environment` or `### User pain`, with narrative analysis under it. Do not leave dimensions only in the method section, scorecard, evidence appendix, or source audit.
- Main narrative: the situation, why it matters, what changed across rounds, and why the conclusion follows.
- Decision logic: the reasoning chain, tradeoffs, and why alternatives were rejected.
- Final recommendation: who should act, who should not act, conditions, and confidence.
- What could change the conclusion: upgrade/downgrade/pivot/kill triggers.
- Next actions with concrete steps, monitoring metrics, stop/continue triggers, and owner/timeframe where useful.
- Limits of the report: missing data, uncertainty, freshness, and external validation needs.

Appendices should contain:

- Evidence register appendix with decisive claim IDs and source IDs; do not copy the full JSONL registry into the report.
- Method and source quality, including search tools used, source types, confidence rules, and fallback notes.
- Red-team notes with strongest objections, substitutes, kill criteria, and falsification tests.
- Options or scenarios with pros, cons, trigger conditions, and expected implications.
- Report quality score with total score, score breakdown, pass/continue decision, lowest-scoring areas, and next-round focus.
- Source notes with source inventory, dates checked, URLs, and companion/wiki/indexing notes.

For non-trivial surveys, `report.md` must be longer and more complete than `NN-synthesis.md`, but length alone is not quality. It should read like a coherent memo with supporting appendices, not a pile of evidence tables. A report that only contains a few bullets is incomplete; a report that opens with long source tables before explaining the judgment is also incomplete. A report that names a research framework but does not analyze those dimensions as body subchapters is incomplete.

New surveys use report schema v2. Legacy reports with the older six-section structure remain readable, but they do not satisfy the final delivery gate. Run `survey_round.py upgrade-report <survey-dir>` and then expand the appended sections before final delivery. `upgrade-report` appends missing v2 sections and updates metadata; it does not write the report for you.

### 2.5 Research Lens And Framework

Use a research lens as a lightweight emphasis guide, not a hard decision-type branch. Use a research framework as the reader-visible method for how the report will systematically examine the question. A survey can combine lenses and frameworks when needed.

Pick or write 1-3 lenses that best match the question:

- **Buyer / user lens**: who has the problem, budget, authority, urgency, and switching cost?
- **Workflow lens**: what repeated job, trigger, inputs, outputs, and failure modes matter?
- **Market / competitor lens**: what substitutes, incumbents, pricing, distribution, and moats matter?
- **Technical lens**: what feasibility, performance, integration, data, reliability, and maintenance risks matter?
- **Policy / trust lens**: what legal, ToS, privacy, compliance, safety, or reputational constraints matter?
- **Open-source lens**: what license, maintainers, release cadence, issues, adoption, API stability, and ecosystem risks matter?
- **Custom lens**: define the lens when the survey does not fit the examples above.

After choosing lenses, select or write a research framework with explicit dimensions. The framework answers: what dimensions will this research cover, what question does each dimension answer, and which dimensions are weak or intentionally out of scope?

The framework must travel through the whole workflow. `00-brief.md` defines the dimensions; `NN-research.md`, `NN-brainstorm.md`, `NN-redteam.md`, `NN-synthesis.md`, and `NN-evolver.md` each expand those same dimensions with `###` subheadings in their framework-relevant section. The final `report.md` then turns the dimensions into readable body chapters. This prevents the common failure mode where the agent lists materials first and only adds a framework audit note afterward.

Evidence can refine the framework, but only explicitly. If a round shows that the initial dimensions are too broad, missing a veto dimension, or no longer match the evidence, update `index.md` under `Framework Refinement Log` with:

- `Current dimensions: ...`
- `Evidence trigger for changes: ...`
- `Original question/core preserved: ...`

After that, use the current dimensions from `index.md` in later round artifacts. Do not silently change the framework in `NN-research.md` or `report.md`. A framework revision is valid only when it is evidence-triggered and preserves the user's original decision frame.

Useful framework starters:

- **Product opportunity framework**: user pain, frequency, willingness to pay, substitutes, distribution, retention, trust/compliance, implementation difficulty.
- **Market / competitor framework**: demand, supply, competition, pricing, channels, switching cost, regulation, growth drivers.
- **Technical feasibility framework**: requirements, architecture path, data/API access, performance, reliability, security, operations, maintenance cost.
- **Open-source adoption framework**: license, maintainer health, release cadence, issue response, API stability, ecosystem, alternatives, adoption risk.
- **Investment / diligence framework**: macro, industry, company, financial quality, valuation, catalysts, capital flows, risks.
- **Custom framework**: name the dimensions when the topic needs another method.

For securities-style research, a domain framework can be composed without making Super Survey a securities-only tool:

- Market view: macro, liquidity, earnings, valuation, risk appetite, fund flows.
- Industry view: demand, supply, competition, policy, technology, cycle, valuation.
- Company view: business model, financial quality, growth, competitive advantage, valuation, catalysts, risks.

Do not force every survey into a predefined category. The lens determines which evidence deserves extra attention; the framework makes the research method visible to readers. The common Super Survey loop still applies, and a framework is not a prewritten conclusion or a narrow decision-type branch.

`NN-evolver.md` should contain the output of the built-in lightweight evolver:

- Probe questions and answers
- Persona judgments
- Keep / Narrow / Pivot / Kill decision
- Round evidence quality gate: one `### <framework dimension>` subsection per brief-defined dimension, then evidence coverage, weakest dimensions, continue/stop implication, and next-round focus
- Next-round target
- Evidence needed next

### 3. Evolve The Target

At the end of each round, run the built-in lightweight evolver. It is inspired by autoresearch-style `probe`, `reason`, and `improve` loops, but it is research-native: it evolves questions and decisions, not code.

Read `references/lightweight-evolver.md` when the research target is broad, ambiguous, commercially important, or after round 1.

The evolver must:

1. Probe assumptions until the weak point is explicit.
2. Run adversarial reasoning across at least five personas.
3. Decide whether to keep, pivot, narrow, or kill the thesis using a single raw decision label, not an explanatory paragraph.
4. Generate the next-round target as a testable question.
5. Name the evidence that would change the decision.

Rewrite the target into a more specific question. Examples:

- From: "Is AI recruiting worth doing?"
- To: "Can a semi-automated job-search copilot for US software engineers charge $19/month without violating job-board terms?"

Prefer narrower customer, geography, channel, workflow, and pricing assumptions.

External autoresearch tools are optional. If available, prefer adversarial planning modes such as `probe`, `reason`, or `improve`. Do not use metric-only code optimization loops as the main survey engine unless the research question has a command-based measurable metric.

### 4. Wiki / Graph Index

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

After each round, wiki persistence is a required attempt, not a nice-to-have. Do this before finalizing the round:

1. **Load and use a Karpathy-style LLM Wiki skill when available.**
   - If `karpathy-llm-wiki` is installed, read its `SKILL.md` and follow its ingest workflow.
   - If the environment has an `Astro-Han/karpathy-llm-wiki` checkout or equivalent raw/wiki structure, use that workflow.
   - Persist at least: survey topic, latest thesis, current evidence-bound conclusion, continuation status, high-value source URLs, and links to `index.md` / key round files. Add `report.md` only after it exists.
2. **Fallback: local `llm-wiki`.**
   - If local `llm-wiki` is installed, read its `SKILL.md`.
   - If `~/llm-wiki/wiki/index.md` is missing, follow that skill's auto-init behavior when applicable.
   - Create or update a topic/source page for the survey and update wiki index/log according to the skill.
3. **Fallback: `pin-llm-wiki` project wiki.**
   - If `.pin-llm-wiki.yml` exists in the current project, queue or ingest the round's important source URLs with `pin-llm-wiki`, then record the command/result in `index.md`.
   - If `pin-llm-wiki` is installed but the project is not initialized, record `Not built: pin-llm-wiki installed but .pin-llm-wiki.yml is missing; run pin-llm-wiki init first`.
4. **Fallback: other graph/document indexer.**
   - If a document graph tool is available, index the survey directory and record the command/result.
5. **Fallback: Markdown only.**
   - Use this only after the attempts above are impossible or fail. Update `index.md` and record the specific failure, not a generic statement.

`index.md` must include these audit fields under `Wiki / Graph Index Status`:

- `Wiki Tool Attempted: ...`
- `Wiki Ingest Result: ...`
- `Wiki Fallback Reason: ...`
- `Wiki Artifact Path: ...`

Never claim a wiki or graph was built unless the ingest/indexing command or file write actually ran. If only `index.md` was updated, say that directly. Do not skip wiki persistence merely because the user did not explicitly ask for it; Super Survey surveys are long-lived research artifacts by default.

`code-review-graph` is not a substitute for the survey wiki. Use it only when the survey target is a code repository and code structure analysis is needed.

### 5. Report Quality Score And Continuation

Super Survey supports arbitrary positive round numbers, but the number itself is not the stopping rule. The helper accepts `round <survey-dir> 3`, `round <survey-dir> 4`, and later rounds when the completed round's evidence and evolver decision say another pass is needed. The brief must not predict those future rounds.

Score the final `report.md` on a 100-point rubric before finalizing. Before `report.md` exists, record provisional quality notes in `NN-evolver.md` and `index.md`; do not let those notes masquerade as a final report score.

| Dimension | Points | What Good Looks Like |
|---|---:|---|
| Problem and scope definition | 15 | Clear decision, audience, assumptions, non-goals, and success/failure criteria |
| Source, method, and framework quality | 20 | Current sources where needed, primary sources preferred, search tools/fallbacks recorded, research framework stated, body chapters cover the framework dimensions, and coverage gaps are disclosed |
| Evidence completeness | 20 | Claim-level evidence, contradictions, confidence, source freshness, and enough coverage for the decision |
| Analysis and red-team quality | 20 | Synthesis across evidence, alternatives, objections, kill criteria, and falsification tests |
| Actionability | 15 | Concrete recommendation, next actions, owners/timeframes when useful, monitoring and stop/continue triggers |
| Structure and readability | 10 | Standalone narrative first, appendices second, clear headings, readable tables, no template residue |

Mode-specific thresholds are stricter for deeper work. `quick` can pass at 80 when the user only needs directional triage. `standard` should pass at 90. `deep` should pass at 95 and use larger source/claim/evidence coverage. Do not lower the standard mode just because a report is short; choose `quick` explicitly when speed matters more than completeness.

Machine continuation gate:

- Stop only when both raw gates pass: `report.md` score is at or above the selected mode threshold, and the latest `NN-evolver.md` decision is `Kill`.
- `Keep`, `Narrow`, or `Pivot` always require another round. Do not use `report.md` explanations such as "future disclosure", "external validation", or "no decision-changing unknowns" to override the evolver's raw decision.
- `Kill` means the research loop can move to final report writing. The survey stops only after `report.md` exists, its score passes, and `check-final` passes. The report should still explain the kill rationale for readers, but the helper does not parse that prose as a stopping signal.
- `survey_round.py check` may pass with a continuation warning when the latest decision is `Keep`, `Narrow`, or `Pivot`; that means the round artifacts are valid and the next round must be created. `survey_round.py check-final` must fail for those decisions.

Report score thresholds:

- `quick`: score must be `>= 80`.
- `standard`: score must be `>= 90`.
- `deep`: score must be `>= 95`.

Continue another round when:

- The conclusion depends on unresolved facts.
- The red-team found serious unanswered objections.
- The target is still too broad to act on.
- A next-round question could materially change the decision.
- The latest synthesis lists remaining unknowns that can still be reduced by desk research, current-source search, competitor checks, policy review, source triangulation, or repository analysis.
- The evolver says `Keep`, `Narrow`, or `Pivot`.
- After final report drafting, `report.md` scores below the selected mode's pass threshold and the weak dimensions are improvable by another evidence pass.

Stop when:

- `Kill + pass`: the latest evolver decision is `Kill` and the report score passes the selected mode threshold.
- The user explicitly stops or asks for a bounded checkpoint; still report unresolved quality risks instead of pretending the survey converged.

Do not let report prose decide whether to stop. `report.md` can explain uncertainty, future disclosure needs, and external validation needs for the reader, but the helper relies only on the latest evolver decision and, for `check-final`, the score threshold.

### 6. Quality Gate

Before reporting a round as complete:

1. Run `survey_round.py check <survey-dir>` for round artifacts, registry validation, and the latest raw evolver gate.
2. Use `survey_round.py validate-evidence <survey-dir>` only when debugging registry errors directly.
3. Fix missing files, missing headings, empty required sections, or empty-template artifacts.
4. Confirm every required section contains substantive content, not only placeholders such as `Status:`, `Notes:`, `Option A:`, or table headers.
5. Confirm `sources.jsonl`, `claims.jsonl`, and `evidence.jsonl` meet the selected mode's minimum coverage, have no duplicate IDs, have no orphan links, and do not contain obviously weak supported/partial claim-evidence pairs.
6. Confirm `00-brief.md` has a research lens, research framework, and decision evidence standard specific enough to guide source selection and reader expectations.
7. Confirm `00-brief.md` declares framework dimensions and expands each one under a `###` subheading; do not leave the framework as only a list.
8. Confirm `NN-research.md`, `NN-brainstorm.md`, `NN-redteam.md`, `NN-synthesis.md`, and `NN-evolver.md` each expand the brief-defined dimensions, or the evidence-refined dimensions recorded in `index.md`, under `###` subheadings in their framework-relevant sections.
9. Confirm `NN-research.md` records source type, freshness, confidence, contradictions, framework coverage, search tool used, and Tavily fallback reason if Tavily was not used for current-source discovery.
10. Confirm `NN-redteam.md` checks substitutes, alternative explanations, and explicit kill criteria.
11. Confirm `NN-synthesis.md` states decision rationale and framework-based synthesis, not only a conclusion.
12. Confirm `NN-evolver.md` has a concrete `Keep / Narrow / Pivot / Kill` decision.
13. Confirm `00-brief.md` records Round 0 brainstorming and each `NN-brainstorm.md` records the per-round checkpoint.
14. Confirm `index.md` reflects the latest thesis, current evidence-bound conclusion, round ledger, continuation status, next research target, why it is not final yet, open questions, source inventory, framework refinement log, wiki/graph status, and decision log.
15. If the evolver says `Keep`, `Narrow`, or `Pivot`, update `index.md`, create the next round, and do not write `report.md` yet.
16. If the evolver says `Kill`, write `report.md` as the final standalone report.
17. Confirm `report.md` is complete, standalone, updated with the latest synthesis, and reads as a coherent report: executive summary, reader's path, research method and framework, framework dimension analysis with one subheading per dimension, main narrative, decision logic, final recommendation, change triggers, next actions, limits, then appendices for evidence, method/source quality, red-team notes, scenarios, quality score, and source notes.
18. Confirm the `Report Quality Score` section includes total score, score breakdown, pass/continue decision, lowest-scoring areas, and next-round focus.
19. Confirm the report body obeys prose-first rules: it is not bullet-dominated and does not put evidence tables before the first appendix.
20. Run `survey_round.py check-final <survey-dir>` before presenting the survey as final.
21. If score is below the selected mode's threshold, create another round focused on the weakest dimensions and remove or revise premature final-report claims.
22. Stop only when both gates pass: the mode/report score gate and the raw evolver decision gate.
23. If `check-final` reports a legacy report schema error, run `upgrade-report` and fill the appended sections before presenting the report as final.
24. Treat companion routing notes as auditable: the artifact must say which tool was used, what failed if fallback happened, and where the result was recorded.
25. Confirm wiki persistence was attempted and `index.md` records `Wiki Tool Attempted`, `Wiki Ingest Result`, `Wiki Fallback Reason`, and `Wiki Artifact Path`.

If the check fails, say the round is still in progress; do not present it as finished.

## Evidence Standard

Use current sources for market, legal, pricing, platform policy, repository activity, APIs, company facts, and competitor claims. Mark inference explicitly.

For current-source discovery, default to `tavily-search` and document any fallback.

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

Do not dump the full research document into chat; save it to disk and summarize the important parts.

Use the same language as the user's request unless they ask otherwise. When writing survey artifacts, keep all headings, findings, red-team critique, synthesis, and evolver output in one selected language: English (`en`), Chinese (`zh`), or Japanese (`ja`). Source titles and quoted terms may stay in their original language.

## Common Failure Modes

- **Link dump**: sources are collected but no decision changes. Fix by updating synthesis and evolver.
- **Weak red-team**: objections are generic. Fix by naming incumbents, data blockers, legal risks, and user apathy.
- **Generic next round**: target remains broad. Fix by narrowing customer, geography, workflow, data source, channel, or price.
- **One-time brainstorming**: brainstorming appears only in `00-brief.md`. Fix by adding `NN-brainstorm.md` for each round and using it to choose the next move.
- **False graph claim**: index tooling was mentioned but not run. Fix by saying only `index.md` was updated.
- **Skipped wiki persistence**: the survey ends with only local Markdown even though `karpathy-llm-wiki` or `llm-wiki` was available. Fix by reading that skill, running/performing ingest, and recording the artifact path.
- **Template theater**: files exist but contain placeholders. Fix before final response.
- **Index-as-report**: `index.md` is updated but no standalone final report exists. Fix by writing `report.md` before answering.
- **Thin final report**: `report.md` repeats only a short synthesis and omits methodology, evidence table, red-team critique, scenarios, action plan, or open questions. Fix by expanding it into a standalone report.
- **Audit-table report**: `report.md` starts with dense source tables, claim registers, or checklist sections and never becomes readable. Fix by writing a narrative body first and moving audit material into appendices.
- **Framework-as-audit-note**: framework dimensions appear only as a list or coverage checklist, while `brief`, `research`, `brainstorm`, `redteam`, `synthesis`, `evolver`, or `report.md` jump to generic narrative. Fix by using the brief-defined dimensions as `###` subheadings in every framework-relevant stage and as body chapters in the final report.
- **Round-count autopilot**: the survey stops because it reached a familiar count, while the report score is weak or unknowns remain desk-researchable. Fix by scoring the report and creating the next round around the lowest-scoring dimensions.
