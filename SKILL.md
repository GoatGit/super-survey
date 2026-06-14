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
2. Choose a generic research lens and evidence standard without forcing the work into a narrow fixed category.
3. Gather evidence from current sources when facts may have changed.
4. Re-enter a brainstorming checkpoint to reframe the problem and compare next moves.
5. Separate findings from interpretation.
6. Include a red-team challenge: why the idea may fail, why evidence may be weak, what alternative explanations or substitutes exist, and what constraints invalidate the thesis.
7. Check explicit kill criteria before recommending another round.
8. Synthesize a clearer conclusion with confidence level, decision rationale, and remaining unknowns.
9. Run the lightweight evolver to sharpen or kill the next-round target.
10. Decide whether to continue using the report quality score and continuation rules; never stop because a fixed round count was reached.
11. Maintain the lightweight evidence registry: `sources.jsonl`, `claims.jsonl`, and `evidence.jsonl`.
12. Validate citations and claim support with `survey_round.py validate-evidence` or the integrated `check` command.
13. Update an index and attempt wiki/graph indexing, or record why it was unavailable.
14. Write or update the final `report.md` before giving a final answer.
15. Write the round artifacts to disk before giving a final answer.

Do not stop after collecting links. The value of this skill is sharper judgment after each loop.

Empty templates are not artifacts. A round is incomplete until each file contains substantive findings, critique, synthesis, and evolved next-target content.

`index.md` is a navigation and decision log. It is not the final report. The final complete deliverable must be a full `report.md`, written in the selected artifact language and updated before the user-facing answer. Do not treat `report.md` as a short chat summary.

## Workflow

### Optional Companion Skills

Super Survey is the research loop owner. It may route specific subtasks to companion skills when they are available, but they are optional and must not become hard dependencies. If a companion is missing, continue with the common Super Survey workflow and record the fallback in the relevant artifact.

Recommended companion routing:

| Need | Prefer | Record where |
|---|---|---|
| Brainstorming checkpoints, reframing, next-move comparison | `superpowers:brainstorming` or equivalent brainstorming workflow | `00-brief.md`, `NN-brainstorm.md` |
| Current web search, recent facts, source discovery | `tavily-search` first; built-in web search or another current-source search tool only as fallback | `NN-research.md` Source List and Data Quality Notes |
| Formal long report, many citations, HTML/PDF, strict citation validation, extensive source triangulation | `deep-research` or equivalent deep research/reporting skill | `NN-research.md`, `report.md`, registry JSONL files, `index.md` |
| Customer voice / VOC / Reddit or review mining | customer-research, reddit-research, or equivalent VOC workflow | `NN-research.md` Evidence Table and `NN-redteam.md` alternatives |
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
   - expected depth or maximum rounds
   - whether the user wants autonomous continuation or checkpoint approval

2. **Per-round checkpoint**: after each research pass and before the next round, use brainstorming to:
   - restate what changed
   - ask or record any new clarifying question
   - propose 2-3 possible next moves
   - choose the next-round direction
   - decide whether to continue, narrow, pivot, or stop

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
python3 <skill-dir>/scripts/survey_round.py validate-evidence surveys/2026-06-12-ai-recruiting-agent
python3 <skill-dir>/scripts/survey_round.py check surveys/2026-06-12-ai-recruiting-agent
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
- Decision evidence standard
- Target user/customer
- Success criteria
- Disqualifying conditions
- Initial assumptions
- Planned research rounds or continuation policy

Do not plan around a fixed default such as two or three rounds. If the user does not specify a fixed round count, write the plan as a quality-driven continuation policy: start with the first round, score the report, then continue while the score is below threshold or decision-changing unknowns remain reducible through desk research or available tools.

If the user only wants a quick answer, still create a lightweight `00-brief.md`, one synthesis file, and `report.md`.

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

Use stable IDs such as `S1`, `E1`, and `C1`. Every evidence item must reference an existing `source_id`. Every supported, partial, or contested claim must reference existing `evidence_id` values.

### 2. Research Round

For each round, create or update:

```text
NN-research.md
NN-brainstorm.md
NN-redteam.md
NN-synthesis.md
NN-evolver.md
index.md
report.md
```

`NN-research.md` should contain:

- Research question for this round
- Source list with dates/URLs where applicable
- Claim-level evidence table with source type, freshness, confidence, and contradictions
- Notes on data quality, freshness, and whether Tavily or a fallback search path was used

`NN-brainstorm.md` should contain:

- Brainstorming status
- Current framing after the research pass
- Clarifying questions or explicit assumptions
- 2-3 possible next moves
- Chosen direction
- Design notes for the next round

`NN-redteam.md` should contain:

- Strongest objections
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
- What changed from prior round
- Best next question
- Recommended next action

`report.md` should be a complete, standalone report that a user can read smoothly without opening every round artifact. It is not an audit checklist. Put the human-readable argument first and move dense evidence, source, method, red-team, scenario, and scoring material into appendices.

Prose-first rule: before the first evidence appendix, `report.md` should read as narrative prose with short lists where helpful. Do not place Markdown evidence tables, source inventories, claim registers, or audit checklists in the body. Tables belong in appendices or the JSONL registry.

The readable body should contain:

- Executive summary with the answer, confidence, key reason, strongest caveat, and next action.
- Reader's path: who the report is for, what decision it supports, and what to read first.
- Main narrative: the situation, why it matters, what changed across rounds, and why the conclusion follows.
- Decision logic: the reasoning chain, tradeoffs, and why alternatives were rejected.
- Final recommendation: who should act, who should not act, conditions, and confidence.
- What could change the conclusion: upgrade/downgrade/pivot/kill triggers.
- Next actions with concrete steps, monitoring metrics, stop/continue triggers, and owner/timeframe where useful.
- Limits of the report: missing data, uncertainty, freshness, and external validation needs.

Appendices should contain:

- Evidence register with claim-level evidence, confidence, contradictions, freshness, and source names.
- Method and source quality, including search tools used, source types, confidence rules, and fallback notes.
- Red-team notes with strongest objections, substitutes, kill criteria, and falsification tests.
- Options or scenarios with pros, cons, trigger conditions, and expected implications.
- Report quality score with total score, score breakdown, pass/continue decision, lowest-scoring areas, and next-round focus.
- Source notes with source inventory, dates checked, URLs, and companion/wiki/indexing notes.

For non-trivial surveys, `report.md` must be longer and more complete than `NN-synthesis.md`, but length alone is not quality. It should read like a coherent memo with supporting appendices, not a pile of evidence tables. A report that only contains a few bullets is incomplete; a report that opens with long source tables before explaining the judgment is also incomplete.

New surveys use report schema v2. Legacy reports with the older six-section structure remain readable and may pass `check` with warnings, but should be upgraded with `survey_round.py upgrade-report <survey-dir>` and then expanded before final delivery. `upgrade-report` appends missing v2 sections and updates metadata; it does not write the report for you.

### 2.5 Research Lens

Use a research lens as a lightweight emphasis guide, not a hard decision-type branch. A survey can combine lenses when needed.

Pick or write 1-3 lenses that best match the question:

- **Buyer / user lens**: who has the problem, budget, authority, urgency, and switching cost?
- **Workflow lens**: what repeated job, trigger, inputs, outputs, and failure modes matter?
- **Market / competitor lens**: what substitutes, incumbents, pricing, distribution, and moats matter?
- **Technical lens**: what feasibility, performance, integration, data, reliability, and maintenance risks matter?
- **Policy / trust lens**: what legal, ToS, privacy, compliance, safety, or reputational constraints matter?
- **Open-source lens**: what license, maintainers, release cadence, issues, adoption, API stability, and ecosystem risks matter?
- **Custom lens**: define the lens when the survey does not fit the examples above.

Do not force every survey into a predefined category. The lens only determines which evidence deserves extra attention; the common research loop still applies.

`NN-evolver.md` should contain the output of the built-in lightweight evolver:

- Probe questions and answers
- Persona judgments
- Keep / pivot / kill decision
- Report quality gate: current score, weakest dimensions, pass/fail reason, and next-round focus
- Next-round target
- Evidence needed next

### 3. Evolve The Target

At the end of each round, run the built-in lightweight evolver. It is inspired by autoresearch-style `probe`, `reason`, and `improve` loops, but it is research-native: it evolves questions and decisions, not code.

Read `references/lightweight-evolver.md` when the research target is broad, ambiguous, commercially important, or after round 1.

The evolver must:

1. Probe assumptions until the weak point is explicit.
2. Run adversarial reasoning across at least five personas.
3. Decide whether to keep, pivot, narrow, or kill the thesis.
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
- Round summaries
- Open questions
- Source inventory
- Wiki / Graph Index Status
- Decision log

After each round, wiki persistence is a required attempt, not a nice-to-have. Do this before finalizing the round:

1. **Load and use a Karpathy-style LLM Wiki skill when available.**
   - If `karpathy-llm-wiki` is installed, read its `SKILL.md` and follow its ingest workflow.
   - If the environment has an `Astro-Han/karpathy-llm-wiki` checkout or equivalent raw/wiki structure, use that workflow.
   - Persist at least: survey topic, latest thesis, final recommendation, high-value source URLs, and links to `report.md` / key round files.
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

Super Survey supports arbitrary positive round numbers, but the number itself is not the stopping rule. The helper accepts `round <survey-dir> 3`, `round <survey-dir> 4`, and later rounds when the report quality gate says another pass is needed.

Score `report.md` on a 100-point rubric before finalizing:

| Dimension | Points | What Good Looks Like |
|---|---:|---|
| Problem and scope definition | 15 | Clear decision, audience, assumptions, non-goals, and success/failure criteria |
| Source and method quality | 20 | Current sources where needed, primary sources preferred, search tools/fallbacks recorded |
| Evidence completeness | 20 | Claim-level evidence, contradictions, confidence, source freshness, and enough coverage for the decision |
| Analysis and red-team quality | 20 | Synthesis across evidence, alternatives, objections, kill criteria, and falsification tests |
| Actionability | 15 | Concrete recommendation, next actions, owners/timeframes when useful, monitoring and stop/continue triggers |
| Structure and readability | 10 | Standalone narrative first, appendices second, clear headings, readable tables, no template residue |

Mode-specific thresholds are stricter for deeper work. `quick` can pass at 80 when the user only needs directional triage. `standard` should pass at 90. `deep` should pass at 95 and use larger source/claim/evidence coverage. Do not lower the standard mode just because a report is short; choose `quick` explicitly when speed matters more than completeness.

Default `standard` thresholds:

- `>= 90`: pass. Stop only if the report says no decision-changing unknown remains desk-researchable.
- `80-89`: conditional. Stop only if the report explicitly states that no decision-changing unknowns remain and the next useful evidence requires external validation.
- `< 80`: fail. Continue with another round focused on the lowest-scoring dimensions.

Continue another round when:

- The conclusion depends on unresolved facts.
- The red-team found serious unanswered objections.
- The target is still too broad to act on.
- A next-round question could materially change the decision.
- The latest synthesis lists remaining unknowns that can still be reduced by desk research, current-source search, competitor checks, policy review, source triangulation, or repository analysis.
- The evolver says `Keep`, `Narrow`, or `Pivot` and names evidence that is publicly or tool-accessibly obtainable.
- `report.md` scores below the selected mode's pass threshold and the weak dimensions are improvable by another evidence pass.

Stop when:

- The report score passes the threshold and the next action is clear.
- The idea is disqualified.
- More research would not change the decision without external validation.
- The user asked for a fixed number of rounds.

Stopping after any number of rounds is allowed only when the quality score and synthesis explain why another desk-research round would not materially change the decision, or why the next evidence requires external validation such as interviews, experiments, purchase data, private financials, or future company disclosures. If the stop reason is weak, create the next round instead of finalizing.

### 6. Quality Gate

Before reporting a round as complete:

1. Run `survey_round.py validate-evidence <survey-dir>` to validate source, claim, and evidence registry links.
2. Run `survey_round.py check <survey-dir>`.
3. Fix missing files, missing headings, empty required sections, or empty-template artifacts.
4. Confirm every required section contains substantive content, not only placeholders such as `Status:`, `Notes:`, `Option A:`, or table headers.
5. Confirm `sources.jsonl`, `claims.jsonl`, and `evidence.jsonl` meet the selected mode's minimum coverage and have no orphan links.
6. Confirm `00-brief.md` has a research lens and decision evidence standard specific enough to guide source selection.
7. Confirm `NN-research.md` records source type, freshness, confidence, contradictions, search tool used, and Tavily fallback reason if Tavily was not used for current-source discovery.
8. Confirm `NN-redteam.md` checks substitutes, alternative explanations, and explicit kill criteria.
9. Confirm `NN-synthesis.md` states decision rationale, not only a conclusion.
10. Confirm `NN-evolver.md` has a concrete `Keep / Narrow / Pivot / Kill` decision.
11. Confirm `00-brief.md` records Round 0 brainstorming and each `NN-brainstorm.md` records the per-round checkpoint.
12. Confirm `index.md` reflects the latest thesis, open questions, source inventory, wiki/graph status, and decision log.
13. Confirm `report.md` is complete, standalone, updated with the latest synthesis, and reads as a coherent report: executive summary, reader's path, main narrative, decision logic, final recommendation, change triggers, next actions, limits, then appendices for evidence, method/source quality, red-team notes, scenarios, quality score, and source notes.
14. Confirm the `Report Quality Score` section includes total score, score breakdown, pass/continue decision, lowest-scoring areas, and next-round focus.
15. Confirm the report body obeys prose-first rules and does not put evidence tables before the first appendix.
16. If score is below the selected mode's threshold, create another round focused on the weakest dimensions. Stop only when the mode gate and no-decision-changing-unknown rules are satisfied.
17. If `check` reports a legacy report warning, run `upgrade-report` and fill the appended sections before presenting the report as final.
18. Treat companion routing notes as auditable: the artifact must say which tool was used, what failed if fallback happened, and where the result was recorded.
19. Confirm wiki persistence was attempted and `index.md` records `Wiki Tool Attempted`, `Wiki Ingest Result`, `Wiki Fallback Reason`, and `Wiki Artifact Path`.

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
- **Round-count autopilot**: the survey stops because it reached a familiar count, while the report score is weak or unknowns remain desk-researchable. Fix by scoring the report and creating the next round around the lowest-scoring dimensions.
