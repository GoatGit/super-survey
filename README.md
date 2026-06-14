# Super Survey

Language: English | [中文](README.zh-CN.md) | [日本語](README.ja.md)

Super Survey is a reusable agent skill and research workflow for multi-round product, market, technical, and open-source research. It turns a vague research target into evidence-backed Markdown artifacts with red-team critique, synthesis, and a sharper next-round question. It is designed for Skills-compatible agents and can also be used directly through its bundled CLI.

## What It Does

Super Survey is for decisions that should not stop at a link dump:

- product opportunity research
- competitor and market analysis
- open-source project scouting
- technical feasibility research
- investment-style diligence
- strategic exploration with adversarial critique

Each survey creates persistent artifacts:

```text
surveys/YYYY-MM-DD-topic-slug/
├── 00-brief.md
├── 01-research.md
├── 01-brainstorm.md
├── 01-redteam.md
├── 01-synthesis.md
├── 01-evolver.md
├── index.md
├── report.md
└── .super-survey.json
```

## Install

Install directly with the Skills CLI:

```bash
npx skills add GoatGit/super-survey
```

Codex users can also copy this repository into the Codex skills directory:

```bash
mkdir -p ~/.codex/skills
rsync -a --delete super-survey/ ~/.codex/skills/super-survey/
```

Then invoke it explicitly:

```text
$super-survey research whether an AI recruiting copilot is worth building
```

## CLI

Create a survey:

```bash
python3 scripts/survey_round.py init "AI recruiting agent" --language en
python3 scripts/survey_round.py init "AI 招聘助手" --language zh
python3 scripts/survey_round.py init "AI採用エージェント" --language ja
```

Create and validate a round:

```bash
python3 scripts/survey_round.py round surveys/2026-06-13-ai-recruiting-agent 1
python3 scripts/survey_round.py check surveys/2026-06-13-ai-recruiting-agent
python3 scripts/survey_round.py upgrade-report surveys/2026-06-13-ai-recruiting-agent
```

`check` fails when required files are missing, headings are missing, any required section is empty, artifacts still look like templates, or the v2 report lacks a parseable quality score. Round numbers must be positive integers. Older six-section reports are accepted with a warning; run `upgrade-report` to append the full report schema and then fill the new sections.

## skills.sh Readiness

This repository is structured for Skills CLI discovery and skills.sh indexing:

- root-level `SKILL.md` with `name` and `description` frontmatter
- `agents/openai.yaml` UI metadata
- bundled helper script under `scripts/`
- supporting references under `references/`
- MIT license, tests, and multilingual README files

Validate discovery:

```bash
npx skills add GoatGit/super-survey --list
```

## Quality Gates

A complete round must include:

- current target and decision criteria
- a research lens and decision evidence standard that guide source selection without forcing a narrow category
- current claim-level evidence with source type, freshness, confidence, contradictions, and search tool used
- a brainstorming checkpoint
- findings separated from interpretation
- red-team critique with substitutes, alternative explanations, and kill criteria checked
- synthesis with confidence, decision rationale, and unknowns
- lightweight evolver output with `Keep / Narrow / Pivot / Kill`
- explicit continue/stop decision driven by report quality, not a fixed round count
- updated `index.md` with wiki or graph indexing status
- standalone `report.md` as the complete final report: readable narrative first, appendices for evidence/source/method/red-team/scenario details second

`report.md` uses a 100-point quality gate:

| Dimension | Points |
|---|---:|
| Problem and scope definition | 15 |
| Source and method quality | 20 |
| Evidence completeness | 20 |
| Analysis and red-team quality | 20 |
| Actionability | 15 |
| Structure and readability | 10 |

`>=90` can finalize when no decision-changing desk-research unknown remains. `80-89` is conditional and must explicitly explain why no further desk research would change the decision. `<80` must continue another round focused on the lowest-scoring dimensions.

The final report should read like a human memo, not an audit table. Start with the answer, reader's path, main narrative, decision logic, recommendation, change triggers, next actions, and limits. Put evidence registers, source quality, red-team notes, scenarios, quality score, and source inventory in appendices so rigor is preserved without breaking readability.

The evolver runs before the report quality score. It is a round-level step that converts the latest synthesis and red-team critique into `Keep / Narrow / Pivot / Kill` plus a sharper next-round focus. The quality score is a report-level gate applied to the updated `report.md`. If the score fails, the next round uses the report's lowest-scoring dimensions and the evolver's focus as input.

The preferred optional wiki companion is `Astro-Han/karpathy-llm-wiki`. `lewislulu/llm-wiki-skill`, local `llm-wiki`, and `pin-llm-wiki` remain useful fallbacks when they better match the environment. If no initialized wiki backend exists, Super Survey records Markdown-only indexing status in `index.md`.

Super Survey can route subtasks to optional companion skills for search, deep reports, VOC/customer research, competitor analysis, brainstorming, and wiki persistence. For current-source discovery, it should try `tavily-search` first and document any fallback. These companions gather or package evidence; Super Survey remains responsible for the final judgment loop.

## Workflow

```mermaid
flowchart TD
    A[User research question] --> B[00-brief.md<br/>decision, lens, evidence standard]
    B --> C[Round research<br/>sources and claim-level evidence]
    C --> D{Need companion skill?}
    D -->|Current sources| D1[Tavily first<br/>fallback web search]
    D -->|Long report| D2[Deep Research]
    D -->|VOC / user language| D3[Customer or Reddit research]
    D -->|Competitors| D4[Competitive research]
    D -->|Knowledge persistence| D5[Astro-Han/karpathy-llm-wiki<br/>or llm-wiki fallback]
    D -->|No| E[Brainstorm checkpoint]
    D1 --> C
    D2 --> C
    D3 --> C
    D4 --> C
    D5 --> I[index.md]
    C --> E[Brainstorm checkpoint]
    E --> F[Red-team critique<br/>risks, substitutes, kill criteria]
    F --> G[Synthesis<br/>confidence and rationale]
    G --> H[Evolver<br/>Keep / Narrow / Pivot / Kill]
    H --> Q[Report quality score<br/>100-point gate]
    Q --> I[index.md<br/>sources, decisions, wiki status]
    Q -->|Score below threshold<br/>or weak dimensions remain| C
    Q -->|Pass threshold<br/>no decision-changing unknowns| J[report.md<br/>complete final report]
    J --> K[Final answer<br/>decision-oriented summary]
```

## Inspiration: Karpathy's autoresearch

Super Survey's lightweight evolver is inspired by Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch), with respect and attribution. Autoresearch gives an AI agent a real training setup, lets it modify code, run short experiments, check whether a metric improved, keep or discard the change, and repeat.

Super Survey adapts that loop to product, market, technical, and open-source research:

| Dimension | Karpathy autoresearch | Super Survey evolver |
|---|---|---|
| Goal | Improve a model or code path through experiments | Sharpen a research thesis into an actionable decision |
| Input | Training code, fixed evaluation, experiment logs | Evidence, sources, constraints, red-team critique |
| Feedback | A comparable scalar metric such as validation loss | Structured judgment: evidence strength, risks, confidence |
| Decision | Keep or discard a code change | Keep, Narrow, Pivot, or Kill a thesis |
| Output | Better code/model plus experiment history | A narrower next-round research target plus evidence needs |

In short: autoresearch is metric-driven optimization; Super Survey is judgment-driven narrowing. When a survey has a measurable benchmark, Super Survey can borrow more of the autoresearch style. When the question is about buyer intent, compliance, distribution, or strategic risk, the loop stays evidence-first and decision-oriented instead of pretending every answer can be reduced to one number.

## Development

Run the test suite with the Python standard library:

```bash
python3 -m unittest discover -v
```

Run syntax validation:

```bash
python3 -m py_compile scripts/survey_round.py
```

The project intentionally keeps runtime dependencies to the Python standard library.

## Project Layout

```text
SKILL.md                         # agent skill instructions
scripts/survey_round.py           # survey artifact generator and validator
references/lightweight-evolver.md # evolver process reference
references/research-quality.md    # evidence and quality reference
agents/openai.yaml                # skill UI metadata
tests/                            # regression tests
```

## License

MIT. See [license.txt](license.txt).
