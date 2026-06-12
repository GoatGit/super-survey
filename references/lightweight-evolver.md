# Lightweight Evolver

Use this when a Super Survey round needs to turn mixed evidence into a sharper next research target. It borrows the useful parts of autoresearch-style `probe`, `reason`, and `improve` loops without requiring external plugins, git commits, or command-based metrics.

## Inputs

Read these files for the current survey:

- `00-brief.md`
- latest `NN-research.md`
- latest `NN-redteam.md`
- latest `NN-synthesis.md`
- `index.md`

If prior `NN-evolver.md` files exist, read the latest one to avoid repeating the same question.

## Step 1: Probe Assumptions

List the current thesis in one sentence. Then answer:

| Probe | Required Answer |
|---|---|
| Buyer | Who pays, from what budget, and why now? |
| Pain | What painful job happens repeatedly without this product? |
| Trigger | What event makes the user search for a solution? |
| Data | What data source or permission is required? |
| Distribution | How does the first user discover and trust it? |
| Incumbent | Who can copy or block this? |
| Compliance | What law, ToS, privacy, or platform rule can break it? |
| Falsifier | What evidence would make us stop? |

Mark each answer as strong, weak, or unknown.

## Step 2: Persona Reasoning

Run five short persona judgments. Each persona must give a verdict and one sentence of reasoning.

- Skeptical buyer: would they pay?
- Incumbent strategist: how would a larger competitor respond?
- Distribution realist: how will this reach users?
- Compliance reviewer: what can block launch?
- Builder/operator: what makes this hard to deliver reliably?

Use `support`, `concern`, or `reject` as the persona verdict.

## Step 3: Decision

Choose exactly one:

- **Keep**: thesis remains promising; next round should collect missing proof.
- **Narrow**: same idea, but restrict customer, geography, workflow, or feature surface.
- **Pivot**: adjacent idea is better than current thesis.
- **Kill**: stop researching unless the user brings new evidence.

Do not choose `Keep` if buyer, data, and distribution are all weak or unknown.

## Step 4: Generate Next Target

Write the next target as a testable question:

```text
Can [specific customer] achieve [specific valuable outcome] using [specific workflow/product] with [specific data/source/channel] under [specific constraint]?
```

Good:

```text
Can US software engineers actively job hunting pay $19/month for a browser-assisted job application copilot that uses public job APIs plus user-confirmed form filling without violating LinkedIn/Indeed ToS?
```

Bad:

```text
Research AI recruiting more.
```

## Step 5: Evidence Needed Next

Name the next round's evidence requirements:

- Primary sources to verify
- Repositories or tools to inspect
- Competitors to compare
- Pricing or willingness-to-pay signals
- Legal/ToS/compliance checks
- Small validation test if possible

## Output Template

Save this as `NN-evolver.md`:

```markdown
# Round NN Lightweight Evolver

## Current Thesis

-

## Probe Results

| Probe | Answer | Strength |
|---|---|---|

## Persona Judgments

| Persona | Verdict | Reason |
|---|---|---|

## Decision

Keep / Narrow / Pivot / Kill

## Next Research Target

-

## Evidence Needed Next

-
```
