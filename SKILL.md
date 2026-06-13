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
10. Update an index and attempt wiki/graph indexing, or record why it was unavailable.
11. Write or update the final `report.md` before giving a final answer.
12. Write the round artifacts to disk before giving a final answer.

Do not stop after collecting links. The value of this skill is sharper judgment after each loop.

Empty templates are not artifacts. A round is incomplete until each file contains substantive findings, critique, synthesis, and evolved next-target content.

`index.md` is a navigation and decision log. It is not the final report. The final complete deliverable must be `report.md`, written in the selected artifact language and updated before the user-facing answer.

## Workflow

### Optional Companion Skills

Super Survey is the research loop owner. It may route specific subtasks to companion skills when they are available, but they are optional and must not become hard dependencies. If a companion is missing, continue with the common Super Survey workflow and record the fallback in the relevant artifact.

Recommended companion routing:

| Need | Prefer | Record where |
|---|---|---|
| Brainstorming checkpoints, reframing, next-move comparison | `superpowers:brainstorming` or equivalent brainstorming workflow | `00-brief.md`, `NN-brainstorm.md` |
| Current web search, recent facts, source discovery | `tavily-search`, built-in web search, or another current-source search tool | `NN-research.md` Source List and Data Quality Notes |
| Long citation-backed report, extensive source triangulation | `deep-research` or equivalent deep research/reporting skill | `NN-research.md`, `NN-synthesis.md`, `index.md` |
| Customer voice / VOC / Reddit or review mining | customer-research, reddit-research, or equivalent VOC workflow | `NN-research.md` Evidence Table and `NN-redteam.md` alternatives |
| Competitor matrix, positioning map, SWOT | competitive-research or equivalent competitor-analysis workflow | `NN-research.md`, optional competitor notes, `NN-synthesis.md` |
| Long-term source and knowledge persistence | `pin-llm-wiki`, `llm-wiki`, or another document/wiki indexer | `index.md` Wiki / Graph Index Status |
| Reusable marketing or growth ideas after the research conclusion | `marketing-ideas` or equivalent ideation skill | `NN-synthesis.md` Recommended Next Action |

Use companions to gather or package evidence, not to bypass Super Survey's judgment loop. The final round still must include findings, red-team critique, synthesis, evolver decision, and persisted artifacts. Never claim a companion skill ran unless it actually ran.

Recommended optional setup:

- Install or enable Superpowers brainstorming when available; if absent, record `Assumed` and perform a lightweight written checkpoint inside the survey artifacts.
- Install or enable `pin-llm-wiki` or `llm-wiki` when long-term knowledge accumulation matters; if absent, maintain Markdown-only `index.md`.
- Install or enable a current-source search skill/tool when the survey depends on recent market, policy, pricing, API, repository, or company facts.

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
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI recruiting agent"
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI recruiting agent" --language zh
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI recruiting agent" --language ja
python3 ~/.codex/skills/super-survey/scripts/survey_round.py round surveys/2026-06-12-ai-recruiting-agent 1
python3 ~/.codex/skills/super-survey/scripts/survey_round.py check surveys/2026-06-12-ai-recruiting-agent
```

Supported artifact languages: `en`, `zh`, and `ja`. Use the user's language by default. The helper stores the language in `.super-survey.json`; `round` and `check` reuse it automatically.

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
- Planned research rounds

If the user only wants a quick answer, still create a lightweight `00-brief.md`, one synthesis file, and `report.md`.

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
- Notes on data quality and freshness

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

`report.md` should be a complete, standalone report that a user can read without opening every round artifact. It should contain:

- Executive summary
- Key findings
- Comparison or analysis
- Recommendation
- Limitations
- Source notes

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

After each round, attempt one of these in order:

1. **Preferred: `pin-llm-wiki` project wiki.**
   - If `.pin-llm-wiki.yml` exists in the current project, queue or ingest the round's important source URLs with `pin-llm-wiki`, then record the command/result in `index.md`.
   - If `pin-llm-wiki` is installed but the project is not initialized, record `Not built: pin-llm-wiki installed but .pin-llm-wiki.yml is missing; run pin-llm-wiki init first`.
2. **Fallback: `llm-wiki` personal wiki.**
   - If a personal `llm-wiki` skill/tool is available and the user wants global knowledge accumulation, ingest the survey summary or source list there, then record the command/result.
3. **Fallback: other graph/document indexer.**
   - If a document graph tool is available, index the survey directory and record the command/result.
4. **Fallback: Markdown only.**
   - If no wiki/indexer is available, update `index.md` and record `Not built: no initialized pin-llm-wiki, llm-wiki, or document graph indexer available`.

Never claim a wiki or graph was built unless the indexing command actually ran. If only `index.md` was updated, say that directly.

`code-review-graph` is not a substitute for the survey wiki. Use it only when the survey target is a code repository and code structure analysis is needed.

### 5. Decide Whether To Continue

Continue another round when:

- The conclusion depends on unresolved facts.
- The red-team found serious unanswered objections.
- The target is still too broad to act on.
- A next-round question could materially change the decision.

Stop when:

- The next action is clear.
- The idea is disqualified.
- More research would not change the decision without external validation.
- The user asked for a fixed number of rounds.

### 6. Quality Gate

Before reporting a round as complete:

1. Run `survey_round.py check <survey-dir>`.
2. Fix missing files, missing headings, empty required sections, or empty-template artifacts.
3. Confirm every required section contains substantive content, not only placeholders such as `Status:`, `Notes:`, `Option A:`, or table headers.
4. Confirm `00-brief.md` has a research lens and decision evidence standard specific enough to guide source selection.
5. Confirm `NN-research.md` records source type, freshness, confidence, and contradictions for important claims.
6. Confirm `NN-redteam.md` checks substitutes, alternative explanations, and explicit kill criteria.
7. Confirm `NN-synthesis.md` states decision rationale, not only a conclusion.
8. Confirm `NN-evolver.md` has a concrete `Keep / Narrow / Pivot / Kill` decision.
9. Confirm `00-brief.md` records Round 0 brainstorming and each `NN-brainstorm.md` records the per-round checkpoint.
10. Confirm `index.md` reflects the latest thesis, open questions, source inventory, wiki/graph status, and decision log.
11. Confirm `report.md` is complete, standalone, and updated with the latest synthesis.

If the check fails, say the round is still in progress; do not present it as finished.

## Evidence Standard

Use current sources for market, legal, pricing, platform policy, repository activity, APIs, company facts, and competitor claims. Mark inference explicitly.

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
- **Template theater**: files exist but contain placeholders. Fix before final response.
- **Index-as-report**: `index.md` is updated but no standalone final report exists. Fix by writing `report.md` before answering.
