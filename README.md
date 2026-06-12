# Super Survey

Super Survey is a reusable agent skill for multi-round product, market, technical, and open-source research. It forces each round to produce evidence, red-team critique, synthesis, a sharper next question, and persisted Markdown artifacts.

Languages: English, Chinese, Japanese.

## What It Is

Super Survey is for decisions that should not stop at a link dump:

- product opportunity research
- competitor and market analysis
- open-source project scouting
- technical feasibility research
- investment-style diligence
- strategic exploration with adversarial critique

Each round writes:

```text
00-brief.md
01-research.md
01-brainstorm.md
01-redteam.md
01-synthesis.md
01-evolver.md
index.md
.super-survey.json
```

The built-in lightweight evolver turns uncertain findings into a sharper next-round target using assumption probes, five adversarial personas, and a `Keep / Narrow / Pivot / Kill` decision.

Super Survey also records process loops:

- `Superpowers Brainstorming Gate` in `00-brief.md`: records the initial framing.
- `NN-brainstorm.md` in every round: uses `$superpowers brainstorming` as a recurring checkpoint to compare next moves and choose the next-round direction.
- `Wiki / Graph Index Status` in `index.md`: records whether `pin-llm-wiki`, `llm-wiki`, or another document graph index was built, or why indexing was unavailable.

Preferred wiki backend: `pin-llm-wiki`. If `.pin-llm-wiki.yml` exists in the project, Super Survey should queue/ingest important source URLs into that project wiki after each round. If no initialized wiki or graph indexer exists, Super Survey falls back to a maintained Markdown `index.md`. It must not claim a wiki/graph exists unless an indexing command actually ran.

## Install

Copy this folder to your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
rsync -a --delete super-survey/ ~/.codex/skills/super-survey/
```

Then invoke it explicitly:

```text
$super-survey research whether an AI recruiting copilot is worth building
```

## Helper CLI

Create an English survey:

```bash
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI recruiting agent" --language en
```

Create a Chinese survey:

```bash
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI 招聘助手" --language zh
```

Create a Japanese survey:

```bash
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI採用エージェント" --language ja
```

Create and check a round:

```bash
python3 ~/.codex/skills/super-survey/scripts/survey_round.py round surveys/2026-06-12-ai-recruiting-agent 1
python3 ~/.codex/skills/super-survey/scripts/survey_round.py check surveys/2026-06-12-ai-recruiting-agent
```

`check` fails if files are missing, headings are missing, or artifacts are still empty templates.

## Optional Wiki Backend

Install `pin-llm-wiki` and initialize a project wiki when you want Super Survey sources to become a reusable knowledge base:

```bash
npx skills add ndjordjevic/pin-llm-wiki@pin-llm-wiki -g -y
```

Then initialize a wiki in the project root using the skill's `init` flow. After that, Super Survey can record important source URLs in the wiki via `queue` or `ingest` and log the result in `index.md`.

`code-review-graph` is useful for codebase analysis, but it is not a replacement for a Markdown research wiki.

## 中文说明

Super Survey 是一个通用调研技能，用于多轮产品、市场、技术和开源项目调研。它要求每一轮都产出证据、反方挑战、综合结论、进化后的下一轮问题，并把 Markdown 文档落盘。

适合：

- 产品机会调研
- 竞品和市场分析
- GitHub 开源项目筛选
- 技术可行性判断
- 投资/尽调式研究
- 需要反方挑战的战略探索

创建中文模板：

```bash
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI 招聘助手" --language zh
```

核心机制：

- `research`：证据和来源
- `brainstorm`：每轮使用 Superpowers brainstorming 重新框定问题、比较下一步
- `redteam`：反方挑战
- `synthesis`：阶段性判断
- `evolver`：用探针和五个角色把下一轮问题变得更具体
- `check`：防止空模板和伪完成
- `pin-llm-wiki`：可选项目知识库后端，用于沉淀来源和调研知识

## 日本語

Super Survey は、プロダクト、市場、技術、オープンソース調査のための汎用スキルです。各ラウンドで証拠、レッドチーム批判、統合結論、次の調査目標を Markdown として保存します。

向いている用途:

- プロダクト機会の調査
- 競合・市場分析
- GitHub オープンソース調査
- 技術的実現可能性の確認
- 投資・デューデリジェンス型の調査
- 反対意見を含む戦略検討

日本語テンプレートを作成:

```bash
python3 ~/.codex/skills/super-survey/scripts/survey_round.py init "AI採用エージェント" --language ja
```

主な仕組み:

- `research`: 証拠と情報源
- `brainstorm`: 各ラウンドで Superpowers brainstorming を使い、問いを再定義して次の方向を選ぶ
- `redteam`: 反論と失敗要因
- `synthesis`: 統合判断
- `evolver`: プローブと五つのペルソナで次の問いを絞り込む
- `check`: 空テンプレートや未完成の成果物を防ぐ

## License

MIT. See `license.txt`.
