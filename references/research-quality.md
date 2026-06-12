# Research Quality Reference

Use this reference for Super Survey rounds where the conclusion may drive product, investment, legal, or public positioning decisions.

## Source Hierarchy

Prefer sources in this order:

1. Primary sources: official docs, filings, API docs, repository metadata, pricing pages, standards, laws, platform policies.
2. Direct measurements: local tests, API responses, repository stats, scraped public counts with method documented.
3. Reputable secondary sources: established media, analyst reports, credible expert writing.
4. Community signals: GitHub issues, Reddit, forums, social posts. Treat these as qualitative, not definitive.

## Required Checks

For each important claim, ask:

- Is this fact current?
- Is the source primary?
- Does a conflicting source exist?
- Is the claim about ability, adoption, willingness to pay, legality, or user behavior?
- What evidence would disprove it?

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

## Evolver Gate

Before continuing to another round, apply the lightweight evolver. Continue only if the next round has a specific evidence target. If the next question is still generic, narrow by:

- customer segment
- geography
- use case
- data source
- distribution channel
- pricing assumption
- compliance constraint
