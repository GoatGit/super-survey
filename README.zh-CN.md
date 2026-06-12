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

用 Skills CLI 直接安装：

```bash
npx skills add GoatGit/super-survey
```

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

## skills.sh 收录准备

这个仓库已按 Skills CLI 发现和 skills.sh 索引的方式组织：

- 根目录 `SKILL.md`，包含 `name` 和 `description` frontmatter
- `agents/openai.yaml` UI 元数据
- `scripts/` 下的辅助脚本
- `references/` 下的参考资料
- MIT 许可证、测试和多语言 README 文件

验证发现能力：

```bash
npx skills add GoatGit/super-survey --list
```

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

## 灵感来源：Karpathy 的 autoresearch

Super Survey 的轻量进化器受到 Andrej Karpathy 的 [autoresearch](https://github.com/karpathy/autoresearch) 启发，并向这个思路致敬。autoresearch 的核心是让 AI agent 在真实训练环境中修改代码、短跑实验、检查指标是否改善、保留或丢弃改动，然后继续循环。

Super Survey 把这个循环改造到产品、市场、技术和开源调研里：

| 维度 | Karpathy autoresearch | Super Survey 进化器 |
|---|---|---|
| 目标 | 通过实验改进模型或代码路径 | 把调研论点推进到可行动决策 |
| 输入 | 训练代码、固定评测、实验日志 | 证据、来源、约束、反方挑战 |
| 反馈 | 可比较的单一指标，例如 validation loss | 结构化判断：证据强度、风险、置信度 |
| 决策 | 保留或丢弃代码改动 | 保留、收窄、转向或放弃论点 |
| 输出 | 更好的代码/模型和实验历史 | 更窄的下一轮调研目标和所需证据 |

简言之：autoresearch 是指标驱动的优化；Super Survey 是判断驱动的收窄。当调研对象有明确 benchmark 时，Super Survey 可以更接近 autoresearch 的方式；当问题涉及买方意愿、合规、分发或战略风险时，它会保持证据优先和决策导向，而不是假装所有问题都能压成一个数字。

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
