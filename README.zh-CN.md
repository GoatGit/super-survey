# Super Survey

语言：[English](README.md) | 中文 | [日本語](README.ja.md)

Super Survey 是一个可复用的 Codex 技能，用于多轮产品、市场、技术和开源项目调研。它把模糊问题转化为有证据、反方挑战、综合判断和下一轮更具体问题的 Markdown 产物。

## 项目用途

Super Survey 适合不应停留在链接收集的决策：

- 产品机会调研
- 竞品和市场分析
- GitHub/开源项目筛选
- 技术可行性判断
- 投资/尽调式研究
- 需要反方挑战的战略探索

每次调研会生成：

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

## 安装

复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
rsync -a --delete super-survey/ ~/.codex/skills/super-survey/
```

显式调用：

```text
$super-survey 调研 AI 招聘助手是否值得做
```

## 命令行

创建调研：

```bash
python3 scripts/survey_round.py init "AI recruiting agent" --language en
python3 scripts/survey_round.py init "AI 招聘助手" --language zh
python3 scripts/survey_round.py init "AI採用エージェント" --language ja
```

创建并检查一轮：

```bash
python3 scripts/survey_round.py round surveys/2026-06-13-ai-招聘助手 1
python3 scripts/survey_round.py check surveys/2026-06-13-ai-招聘助手
```

`check` 会在缺文件、缺标题、任一必填章节为空、或内容仍像空模板时失败。轮次必须是正整数。

## 质量门

完整的一轮必须包含：

- 当前调研目标和决策标准
- 带来源日期或 URL 的当前证据
- brainstorming 检查点
- 发现与解释分离
- 反方挑战
- 带置信度和未知项的综合结论
- 轻量进化器输出，并明确 `保留 / 收窄 / 转向 / 放弃`
- 更新后的 `index.md`，记录 wiki 或 graph 索引状态

首选可选知识库后端是 `pin-llm-wiki`。如果项目没有初始化知识库后端，Super Survey 会在 `index.md` 里记录 Markdown-only 索引状态。

## 开发

运行测试：

```bash
python3 -m unittest discover -v
```

运行语法检查：

```bash
python3 -m py_compile scripts/survey_round.py
```

项目运行时只依赖 Python 标准库。

## 目录结构

```text
SKILL.md                         # Codex 技能说明
scripts/survey_round.py           # 调研产物生成器和校验器
references/lightweight-evolver.md # 轻量进化器流程
references/research-quality.md    # 证据质量参考
agents/openai.yaml                # 技能 UI 元数据
tests/                            # 回归测试
```

## 许可证

MIT。见 [license.txt](license.txt)。
