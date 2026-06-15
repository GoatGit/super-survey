# Research Quality Reference

Use this reference for Super Survey rounds where the conclusion may drive product, investment, legal, or public positioning decisions.

The foundational theory paper for Super Survey's anti-sycophancy stance is `如何拒绝AI谄媚人类.md`. It uses an investment example to show a broader pattern: open-ended research can fall into local optima when the agent accepts the user's initial wording as the objective function. This reference translates that paper into reusable quality checks for product, market, technical, open-source, and diligence research.

## Source Hierarchy

Prefer sources in this order:

1. Primary sources: official docs, filings, API docs, repository metadata, pricing pages, standards, laws, platform policies.
2. Direct measurements: local tests, API responses, repository stats, scraped public counts with method documented.
3. Reputable secondary sources: established media, analyst reports, credible expert writing.
4. Community signals: GitHub issues, Reddit, forums, social posts. Treat these as qualitative, not definitive.

## Research Lens And Framework Selection

Use lenses to emphasize evidence needs without turning Super Survey into a fixed set of special cases. Pick 1-3 lenses, or define a custom lens, then keep the same common research loop.

Useful lenses:

- **Buyer / user lens**: budget, authority, urgency, switching cost, willingness to pay, trust.
- **Workflow lens**: repeated job, trigger event, inputs, outputs, handoffs, failure modes.
- **Market / competitor lens**: substitutes, incumbents, pricing, distribution, differentiation, moat.
- **Technical lens**: feasibility, performance, integration, data access, reliability, maintenance.
- **Policy / trust lens**: law, ToS, privacy, compliance, safety, reputation, review burden.
- **Open-source lens**: license, maintainer activity, releases, issue response, adoption, API stability.
- **Custom lens**: define the lens when the survey needs another perspective.

The lens is not the answer. It only decides which claims require stronger evidence.

## Anti-Sycophancy / Anti-Local-Optimum Checks

Treat the user's question as the initial point, not the objective function. Before choosing sources or writing a thesis, rebuild the problem frame:

- Split the prompt into known facts, unverified assumptions, subjective judgments, missing information, and stakeholders.
- Restate the real decision objective and list competing objectives.
- Name what the survey should not optimize for, such as pleasing the user, proving an initial hunch, or rejecting an exaggerated version of the question.
- Generate multiple plausible explanations before selecting a thesis.
- Test sensitivity: which assumptions would change the conclusion if false?
- Use a decision tree when the facts are still uncertain: if A is true, recommend one path; if B is true, recommend another.

Good research challenges the user's frame without being adversarial for its own sake. The goal is a more faithful decision model, not a more comfortable answer.

## Decision Robustness Tools

Use these tools when a conclusion may drive spending, investment, adoption, architecture, legal, public, or strategic choices.

### Object Quality vs Action Attractiveness

Separate "is the object good?" from "is the action attractive now?" A good object is not automatically a good action:

- Good company does not automatically mean good stock.
- Good product does not automatically mean good business.
- Good technology does not automatically mean good project.
- Good open-source library does not automatically mean good dependency.

Action attractiveness depends on current constraints, price or cost, timing, opportunity cost, maintenance burden, reversibility, and alternatives.

### Constraint Model

Record:

- Hard constraints: legal, platform, budget, time, security, data access, policy, irreversible risk.
- Soft constraints: preferences, operational capacity, acceptable complexity, brand/reputation sensitivity.
- User-specific constraints: horizon, budget, risk tolerance, existing exposure, team skill, deployment environment.
- Missing constraints: information that would materially change the recommendation if supplied.

When constraints are missing, make the recommendation conditional rather than pretending a universal answer exists.

### Implied Expectations

Ask what must already be true for the current action to be attractive. Examples:

- Product: current pricing or adoption assumes what conversion, retention, and distribution costs?
- Technical: current architecture assumes what reliability, scale, latency, vendor stability, and maintenance capacity?
- Open source: adopting this dependency assumes what maintainer health, API stability, license safety, and ecosystem support?
- Investment/diligence: current price implies what growth, margin, valuation, risk appetite, and opportunity cost?

If implied expectations are aggressive, the report should show what evidence would need to beat those expectations.

### Scenario And Decision Tree

Prefer conditional actions when facts remain uncertain:

- If favorable assumptions hold, what action follows?
- If neutral assumptions hold, what should be watched or delayed?
- If adverse assumptions hold, what should be avoided, reduced, pivoted, or stopped?
- If the user is already committed, what is the hold/reduce/exit path?
- If the user is not yet committed, what is the wait/test/enter path?

This keeps the output useful without collapsing uncertainty into one overconfident conclusion.

### Bayesian Update Table

For high-stakes decisions, track the hypothesis dynamically:

| Hypothesis | Current Evidence Strength | Raises Confidence | Lowers Confidence | Falsifies |
|---|---|---|---|---|

Use this in `NN-synthesis.md`, `NN-evolver.md`, or the final report appendix when the decision should be updated as new evidence arrives.

After choosing lenses, write an explicit research framework. The framework is the reader-visible method: it says which dimensions the survey covers, what each dimension is meant to answer, and where coverage is weak or intentionally out of scope.

Framework starters:

| Survey type | Useful dimensions |
|---|---|
| Product opportunity | user pain, frequency, willingness to pay, substitutes, distribution, retention, trust/compliance, implementation difficulty |
| Market / competitor | demand, supply, competition, pricing, channels, switching cost, regulation, growth drivers |
| Technical feasibility | requirements, architecture path, data/API access, performance, reliability, security, operations, maintenance cost |
| Open-source adoption | license, maintainer health, release cadence, issue response, API stability, ecosystem, alternatives, adoption risk |
| Investment / diligence | macro, industry, company, financial quality, valuation, catalysts, capital flows, risks |
| Custom | define 5-9 dimensions that fit the user's decision |

Securities-style research can compose these domain frameworks:

- Market view: macro, liquidity, earnings, valuation, risk appetite, fund flows.
- Industry view: demand, supply, competition, policy, technology, cycle, valuation.
- Company view: business model, financial quality, growth, competitive advantage, valuation, catalysts, risks.

Treat a framework as a research method rather than a prewritten conclusion. If a framework dimension is weak, say so and make it a candidate next-round target.

The framework must structure the whole workflow, not just the final `report.md`. In `00-brief.md`, each dimension should become a `###` subsection that states the core question, evidence needed, and current boundary. In each round file, the framework-relevant section should use the same dimension subheadings:

- `NN-research.md`: findings, evidence IDs, contradictions, confidence, and next evidence need by dimension.
- `NN-brainstorm.md`: next evidence moves or reframes by dimension.
- `NN-redteam.md`: strongest objection, alternative explanation, falsifier, and decision implication by dimension.
- `NN-synthesis.md`: current judgment, confidence, contradictions, and decision effect by dimension.
- `NN-evolver.md`: coverage quality, weakest gap, and whether a concrete next evidence target remains by dimension.

Keep these subsections concise in quick mode. The important rule is structural: the reader should see how each stage reasoned through the framework rather than seeing only a final audit note.

## Evidence-Driven Framework Refinement

A framework is allowed to evolve when evidence shows that the initial dimensions are wrong, too broad, or missing a veto dimension. Record every framework revision in `index.md` under `Framework Refinement Log`:

- `Current dimensions: ...`
- `Evidence trigger for changes: ...`
- `Original question/core preserved: ...`

After this log is written, later round artifacts should use the refined dimensions. The revision must preserve the user's original decision frame and keep the question equally faithful to the user's intent.

## Claim-Level Evidence

Important claims should be evaluated individually. The canonical records live in `sources.jsonl`, `claims.jsonl`, and `evidence.jsonl`; `NN-research.md` should reference `source_id`, `claim_id`, and `evidence_id` values instead of copying a full evidence table into the round body.

Use this shape as the mental model for registry fields or appendix summaries, not as a required Markdown table in every round:

| Claim | Evidence | Source | Source Type | Freshness | Confidence | Contradictions |
|---|---|---|---|---|---|---|

Guidance:

- **Source Type**: primary, direct measurement, reputable secondary, community signal, inference.
- **Freshness**: date checked and whether the fact is stable, recently changed, or likely to change.
- **Confidence**: high, medium, low, based on the claim's own evidence, not the overall thesis.
- **Contradictions**: conflicting evidence, missing evidence, or "none found after checking X".

Evaluate critical claims separately so weak critical claims stay visible even when another claim is strong. Buyer clarity, data access, compliance, and willingness to pay often deserve separate evidence rows.

The helper performs a lightweight support check for supported/partial claims: duplicate IDs, orphan links, missing linked evidence, and obvious claim-evidence mismatch are errors. This catches cases where a claim cites an unrelated evidence item. It does not replace human review of quote interpretation, source credibility, or nuanced inference.

Registry IDs are process references, not final-report citations. `C1`, `E1`, and similar IDs are useful inside `NN-research.md` and other working files, while final `report.md` uses source titles, Markdown links, footnotes, or an appendix reference list with URLs. A standalone report should be understandable without opening `claims.jsonl` or `evidence.jsonl`.

## Framework Coverage

In `NN-research.md`, write framework coverage as prose under one `###` subheading per framework dimension. Keep source and evidence details referenced by ID so the registry remains the source of truth. A compact table may be used in an appendix, but the round body should stay readable.

| Framework Dimension | Evidence Status | Confidence | Contradictions | Next Evidence Need |
|---|---|---|---|---|

Good coverage means the report can explain both what was checked and what remains weak. If a dimension matters to the decision but lacks evidence, surface it as a concrete gap: either continue another round or name why desk research has reached its limit.

## Final Report Framework Chapters

In final `report.md`, framework dimensions are body-level analysis, not just audit metadata. Make each effective framework dimension its own top-level body chapter before the appendices.

Example:

```markdown
## Market Environment

## Industry Theme

## Company Business Structure
```

For securities-style reports, dimensions such as market environment, industry theme, company business structure, financial quality, valuation, institutional expectations, fund flows, technicals, catalysts, and risks should be readable as report chapters before the appendices. Evidence tables, source audits, registry IDs, and final quality scores belong outside the report body; record the quality gate in `index.md` and use source links in `report.md`.

Write final reports section by section. Each body section should state its decision purpose, key claim, supporting or weakening evidence IDs, strongest counterpoint, and implication for the reader. If a section can only be written as a checklist or source table, keep researching or narrow the section question before finalizing.

## Required Checks

For each important claim, ask:

- Is this fact current?
- Is the source primary?
- Does a conflicting source exist?
- Is the claim about ability, adoption, willingness to pay, legality, or user behavior?
- What evidence would disprove it?
- What substitute or alternative explanation could explain the same signal?

## Red-Team Prompts

Use at least five:

- Why would users not pay for this?
- What incumbent can add this feature faster?
- What data source breaks the product if access changes?
- What workflow is too painful for onboarding?
- What legal, ToS, privacy, or platform risk blocks distribution?
- What cheaper manual workaround already exists?
- Is AI actually necessary, or is this just automation dressed up as AI?
- What metric would prove this is not working after two weeks?

## Kill Criteria

Before recommending another round, write 1-3 kill criteria and check whether the round found them.

Good kill criteria are concrete:

- "Primary platform ToS forbids the required workflow."
- "No evidence of a paying buyer or paid workaround after checking the top five substitutes."
- "Required data source is unavailable, unstable, or legally unusable."
- "The best incumbent already offers the core workflow at lower switching cost."

Avoid vague kill criteria:

- "Market seems small."
- "Users may not care."
- "Competition exists."

If a kill criterion is met, recommend kill or pivot unless the user supplies new constraints.

## Decision Rubric

Score each opportunity from 1 to 5:

- Pain intensity
- Frequency
- Buyer clarity
- Willingness to pay
- Data access
- Distribution path
- AI advantage
- Incumbent defensibility
- Implementation difficulty, reverse scored
- Compliance risk, reverse scored

Use the rubric with veto awareness. A single score of 1 in data access, buyer clarity, or compliance may disqualify the idea.

## Evidence-First Stopping Rules

Stop or switch from research to validation when:

- The decision is clear enough for the user's stated stakes.
- More desk research will not improve the answer without interviews, experiments, legal review, or implementation tests.
- A kill criterion is met for the user's original decision frame, not for an exaggerated or easier-to-reject rewrite.
- The next useful step is build/test/ask users, not another evidence sweep.
- The user explicitly requested a bounded checkpoint.

Stop based on the raw evolver decision, the quality gate, and the user's original decision frame. Treat early round-count plans, report prose about "external validation", and stronger rewrites of broad questions as warning signs; report unresolved quality risks and the next evidence target.

Continue only when the next round has a specific evidence target that could change the original decision.

Use `Final` when the research has converged enough for the user's original decision and the remaining useful work is reporting, monitoring, user validation, legal review, or implementation. Use `Kill` when the current thesis should stop or switch away from desk research because the evidence and red-team critique no longer support another research round.

## Evolver Gate

Before continuing to another round, apply the lightweight evolver. Continue only if the next round has a specific evidence target tied to claims, contradictions, or unknowns from the latest artifacts. If the next question is still generic, narrow by:

- customer segment
- geography
- use case
- data source
- distribution channel
- pricing assumption
- compliance constraint
