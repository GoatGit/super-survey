# Lightweight Evolver

Use this when a Super Survey round needs to turn mixed evidence into a sharper next research target. It borrows the useful parts of autoresearch-style `probe`, `reason`, and `improve` loops without requiring external plugins, git commits, or command-based metrics.

## Inputs

Read these files for the current survey:

- `00-brief.md`
- latest `NN-evidence-plan.md`
- latest `NN-research.md`
- latest `NN-brainstorm.md`
- latest `NN-redteam.md`
- latest `NN-synthesis.md`
- `index.md`

If prior `NN-evolver.md` files exist, read the latest one to avoid repeating the same question.

Follow the artifact dependency order. `NN-evolver.md` is the last round artifact: complete it only after the current round's evidence plan, research, brainstorming, red-team, and synthesis files contain written content. The evolver should judge upstream evidence and synthesis already on disk, not invent what those artifacts would have said.

When the latest files include a research framework or framework coverage section, treat weak or missing framework dimensions as first-class inputs. A next round should usually target the weakest decision-relevant dimension rather than collect more generic sources.

Also read the `Decision Frame Integrity` section in `00-brief.md`. Treat the user's original wording as an initial point, not the objective function. If the current thesis relies on unverified assumptions, subjective judgments, or a stronger easy-to-kill rewrite of the user's question, prefer `Narrow` or `Pivot` with a corrected next target instead of `Kill`.

Also read the `Decision Optimization Contract`. Carry forward its decision-critical variables, minimum direct evidence, implied expectations, constraint-specific recommendation branches, and anti-narrative regularizers.

Also read the latest residual and hard-constraint notes in `index.md`. The evolver is the direction selector for residual-driven evidence iteration: it should choose the next round that can reduce the most decision-critical residual per unit cost, or explain why another desk-research move has low expected information value.

## Step 1: Probe Assumptions

List the current thesis in one sentence, copied or tightly derived from the latest `NN-synthesis.md` and `index.md`. Keep it faithful to the user's original question and the latest artifacts, and reserve the final recommendation until the probes are answered. Then answer:

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
| Implied expectation reverse-check | What current action, price, adoption, dependency, or strategy assumption must be true? |
| Constraint branch | What recommendation changes for different user states, budgets, horizons, reversibility, or risk tolerance? |
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

For each useful persona, keep the target function explicit: what that persona optimizes, what evidence they need, and what error they are most likely to make.

## Step 3: Decision

Choose exactly one:

- **Keep**: thesis remains promising; next round should collect missing proof.
- **Narrow**: same idea, but restrict customer, geography, workflow, or feature surface.
- **Pivot**: adjacent idea is better than current thesis.
- **Kill**: the current thesis is not worth another desk-research round because the evidence, red-team critique, and original decision frame now support stopping or switching to non-desk validation.
- **Final**: no desk-research target remains that could materially change the user's original decision, so the work can move to the final report quality gate.

Choose `Narrow`, `Pivot`, or `Kill` when buyer, data, and distribution are all weak or unknown.

Before choosing, check whether an explicit kill criterion was met and whether it applies to the user's original decision frame. If the kill criterion only rejects an exaggerated version of the question, choose `Narrow` or `Pivot` and write the corrected next target instead.

Before choosing, also check:

- Residual vector: score `r_q/r_c/r_e/r_h/r_a/r_s/r_j` from 0-3 and identify whether any component is a decision-level gap.
- VOI vs cost: would the next desk-research action likely change the action, reduce a major uncertainty, or correct a flawed judgment enough to justify its cost?
- Hard constraints: are there legal, policy, budget, data, safety, responsibility, or user-specific constraints that block finalization regardless of the score?
- Soft residuals: which gaps can be weighted and traded off by task risk?
- Implied expectation reverse-check: which hidden future assumptions remain unsupported?
- Future facts vs desk-researchable gaps: which uncertainties require time/interviews/experiments, and which can still be reduced by another desk research round?
- Anti-narrative regularizers: what popular story, user preference, recency signal, or elegant explanation could be overfitting the answer?
- Constraint-specific recommendation branches: does the best action differ by user state, budget, horizon, reversibility, or risk tolerance?
- Most conclusion-changing variable: what single variable would most change the next decision if updated?

The `Decision` section's first non-empty line must be exactly one raw label: `Keep`, `Narrow`, `Pivot`, `Kill`, or `Final` (or the selected language equivalent). Put explanation in the surrounding sections, not on the decision line.

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

If the next evidence requirement needs interviews, experiments, legal review, or implementation rather than more desk research, say so in `Evidence Needed Next`. That can justify `Final` when the thesis remains usable and no desk-research target remains, or `Kill` when the current thesis should stop or switch to non-desk validation. Otherwise choose `Narrow` or `Pivot` and continue with the desk-research target.

If any residual is still `3` and there is a desk-research move with `VOI greater than cost: yes`, choose `Keep`, `Narrow`, or `Pivot` and name that residual as the next target. If no residual is at `3`, hard constraints are satisfied, and the remaining desk-research VOI is below cost, choose `Final` when the original decision can be answered or `Kill` when the current thesis/path should stop.

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

Keep / Narrow / Pivot / Kill / Final

## Round Evidence Quality Gate

- For each framework dimension, record coverage quality, weakest gap, and whether a concrete next evidence target remains.
- Residual vector r_q/r_c/r_e/r_h/r_a/r_s/r_j (0-3):
- Any residual at 3: yes / no
- Target residual for next round:
- Expected information value of next research:
- Research cost:
- VOI greater than cost: yes / no
- Hard constraints satisfied: yes / no
- Blocking hard constraints:
- Soft residuals that can be weighted:
- Evidence coverage this round:
- Framework coverage this round:
- Weakest evidence or framework dimensions:
- Implied expectation reverse-check:
- future facts vs desk-researchable gaps:
- Anti-narrative regularizers:
- Constraint-specific recommendation branches:
- Most conclusion-changing variable:
- Continue / stop implication:
- Next-round focus:

## Next Research Target

-

## Evidence Needed Next

-
```
