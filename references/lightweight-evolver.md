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

List the current thesis in one sentence, copied or tightly derived from the latest `NN-synthesis.md` and `index.md`. Do not invent a stronger thesis, rewrite the user's original question into an easier-to-kill claim, or state a final recommendation before the probes are answered. Then answer:

| Probe | Required Answer |
|---|---|
| Buyer | Who pays, from what budget, and why now? |
| Pain | What painful job happens repeatedly without this product? |
| Trigger | What event makes the user search for a solution? |
| Data | What data source or permission is required? |
| Distribution | How does the first user discover and trust it? |
| Incumbent | Who can copy or block this? |
| Compliance | What law, ToS, privacy, or platform rule can break it? |
| Alternative | What substitute or non-product explanation could explain the signal? |
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
- **Kill**: the current thesis is not worth another desk-research round because the evidence, red-team critique, and original decision frame now support stopping or switching to non-desk validation.

Do not choose `Keep` if buyer, data, and distribution are all weak or unknown.

Before choosing, check whether an explicit kill criterion was met and whether it applies to the user's original decision frame. If the kill criterion only rejects an exaggerated version of the question, choose `Narrow` or `Pivot` and write the corrected next target instead.

The `Decision` section's first non-empty line must be exactly one raw label: `Keep`, `Narrow`, `Pivot`, or `Kill` (or the selected language equivalent). Put explanation in the surrounding sections, not on the decision line.

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
- Kill criteria or stopping evidence to check first

If the next evidence requirement needs interviews, experiments, legal review, or implementation rather than more desk research, say so in `Evidence Needed Next`. That can justify `Kill` only when no desk-research target remains that could change the original decision; otherwise choose `Narrow` or `Pivot` and continue with the desk-research target.

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

## Round Evidence Quality Gate

-

## Next Research Target

-

## Evidence Needed Next

-
```
