# Research Quality Reference

Use this reference for Super Survey rounds where the conclusion may drive product, investment, legal, or public positioning decisions.

## Source Hierarchy

Prefer sources in this order:

1. Primary sources: official docs, filings, API docs, repository metadata, pricing pages, standards, laws, platform policies.
2. Direct measurements: local tests, API responses, repository stats, scraped public counts with method documented.
3. Reputable secondary sources: established media, analyst reports, credible expert writing.
4. Community signals: GitHub issues, Reddit, forums, social posts. Treat these as qualitative, not definitive.

## Research Lens Selection

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

## Claim-Level Evidence

Important claims should be evaluated individually. Use a table shaped like:

| Claim | Evidence | Source | Source Type | Freshness | Confidence | Contradictions |
|---|---|---|---|---|---|---|

Guidance:

- **Source Type**: primary, direct measurement, reputable secondary, community signal, inference.
- **Freshness**: date checked and whether the fact is stable, recently changed, or likely to change.
- **Confidence**: high, medium, low, based on the claim's own evidence, not the overall thesis.
- **Contradictions**: conflicting evidence, missing evidence, or "none found after checking X".

Do not let one strong claim hide a weak critical claim. Buyer clarity, data access, compliance, and willingness to pay often deserve separate evidence rows.

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

## Stopping Rules

Stop or switch from research to validation when:

- The decision is clear enough for the user's stated stakes.
- More desk research will not improve the answer without interviews, experiments, legal review, or implementation tests.
- A kill criterion is met.
- The next useful step is build/test/ask users, not another evidence sweep.
- The user requested a fixed number of rounds.

Continue only when the next round has a specific evidence target that could change the decision.

## Evolver Gate

Before continuing to another round, apply the lightweight evolver. Continue only if the next round has a specific evidence target. If the next question is still generic, narrow by:

- customer segment
- geography
- use case
- data source
- distribution channel
- pricing assumption
- compliance constraint
