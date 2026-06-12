# Super Survey

Language: English | [中文](README.zh-CN.md) | [日本語](README.ja.md)

Super Survey is a reusable Codex skill for multi-round product, market, technical, and open-source research. It turns a vague research target into evidence-backed Markdown artifacts with red-team critique, synthesis, and a sharper next-round question.

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
└── .super-survey.json
```

## Install

Copy this repository into your Codex skills directory:

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
```

`check` fails when required files are missing, headings are missing, any required section is empty, or artifacts still look like templates. Round numbers must be positive integers.

## Quality Gates

A complete round must include:

- current target and decision criteria
- current evidence with source dates or URLs where applicable
- a brainstorming checkpoint
- findings separated from interpretation
- red-team critique
- synthesis with confidence and unknowns
- lightweight evolver output with `Keep / Narrow / Pivot / Kill`
- updated `index.md` with wiki or graph indexing status

The preferred optional wiki backend is `pin-llm-wiki`. If no initialized wiki backend exists, Super Survey records Markdown-only indexing status in `index.md`.

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
SKILL.md                         # Codex skill instructions
scripts/survey_round.py           # survey artifact generator and validator
references/lightweight-evolver.md # evolver process reference
references/research-quality.md    # evidence and quality reference
agents/openai.yaml                # skill UI metadata
tests/                            # regression tests
```

## License

MIT. See [license.txt](license.txt).
