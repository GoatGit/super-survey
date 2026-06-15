# Research Quality Reference

Use this reference for Super Survey rounds where the conclusion may drive product, investment, legal, or public positioning decisions.

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

After choosing lenses, write an explicit research framework. The framework is the reader-visible method: it says which dimensions the report covers, what each dimension is meant to answer, and where coverage is weak or intentionally out of scope.

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

Do not treat a framework as a prewritten conclusion. If a framework dimension is weak, say so and make it a candidate next-round target.

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

Do not let one strong claim hide a weak critical claim. Buyer clarity, data access, compliance, and willingness to pay often deserve separate evidence rows.

## Framework Coverage

At the end of each `NN-research.md`, summarize framework coverage in prose or a compact appendix-style view. Keep source and evidence details referenced by ID so the registry remains the source of truth:

| Framework Dimension | Evidence Status | Confidence | Contradictions | Next Evidence Need |
|---|---|---|---|---|

Good coverage means the report can explain both what was checked and what remains weak. If a dimension matters to the decision but lacks evidence, do not hide it in a generic "limitations" paragraph; either continue another round or name why desk research cannot reduce it.

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

Do not average blindly. A single score of 1 in data access, buyer clarity, or compliance may disqualify the idea.

## Evidence-First Stopping Rules

Stop or switch from research to validation when:

- The decision is clear enough for the user's stated stakes.
- More desk research will not improve the answer without interviews, experiments, legal review, or implementation tests.
- A kill criterion is met for the user's original decision frame, not for an exaggerated or easier-to-reject rewrite.
- The next useful step is build/test/ask users, not another evidence sweep.
- The user explicitly requested a bounded checkpoint.

Do not stop because an early brief predicted a round count, because the report prose says "external validation", or because a broad question was silently rewritten into a stronger claim. A bounded checkpoint is not proof of convergence; report unresolved quality risks and the next evidence target.

Continue only when the next round has a specific evidence target that could change the original decision.

## Evolver Gate

Before continuing to another round, apply the lightweight evolver. Continue only if the next round has a specific evidence target tied to claims, contradictions, or unknowns from the latest artifacts. If the next question is still generic, narrow by:

- customer segment
- geography
- use case
- data source
- distribution channel
- pricing assumption
- compliance constraint
