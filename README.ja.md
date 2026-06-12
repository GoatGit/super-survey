# Super Survey

言語: [English](README.md) | [中文](README.zh-CN.md) | 日本語

Super Survey は、プロダクト、市場、技術、オープンソース調査のための再利用可能な Codex スキルです。曖昧な調査対象を、証拠、レッドチーム批判、統合判断、次回のより具体的な問いを含む Markdown 成果物に変換します。

## 概要

Super Survey は、リンク集で終わらせるべきではない意思決定に向いています:

- プロダクト機会の調査
- 競合・市場分析
- オープンソースプロジェクトの調査
- 技術的実現可能性の確認
- 投資・デューデリジェンス型の調査
- 反対意見を含む戦略検討

各調査では次の成果物を作成します:

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

## インストール

Codex skills ディレクトリへコピーします:

```bash
mkdir -p ~/.codex/skills
rsync -a --delete super-survey/ ~/.codex/skills/super-survey/
```

明示的に呼び出します:

```text
$super-survey AI採用エージェントが作る価値のある機会か調査して
```

## CLI

調査を作成:

```bash
python3 scripts/survey_round.py init "AI recruiting agent" --language en
python3 scripts/survey_round.py init "AI 招聘助手" --language zh
python3 scripts/survey_round.py init "AI採用エージェント" --language ja
```

ラウンドを作成して検証:

```bash
python3 scripts/survey_round.py round surveys/2026-06-13-ai採用エージェント 1
python3 scripts/survey_round.py check surveys/2026-06-13-ai採用エージェント
```

`check` は、必要ファイルの欠落、見出しの欠落、必須セクションの空欄、または空テンプレートのままの成果物を検出すると失敗します。ラウンド番号は正の整数である必要があります。

## 品質ゲート

完了したラウンドには次が必要です:

- 現在の調査対象と判断基準
- 必要に応じて日付または URL 付きの証拠
- brainstorming チェックポイント
- 発見と解釈の分離
- レッドチーム批判
- 信頼度と未解決事項を含む統合結論
- `維持 / 絞り込み / ピボット / 中止` を明示した軽量エボルバー出力
- wiki または graph インデックス状態を記録した更新済み `index.md`

推奨される任意の wiki バックエンドは `pin-llm-wiki` です。初期化済みの wiki バックエンドがない場合、Super Survey は `index.md` に Markdown-only のインデックス状態を記録します。

## 開発

テストを実行:

```bash
python3 -m unittest discover -v
```

構文チェック:

```bash
python3 -m py_compile scripts/survey_round.py
```

実行時依存は Python 標準ライブラリのみです。

## プロジェクト構成

```text
SKILL.md                         # Codex スキル指示
scripts/survey_round.py           # 調査成果物の生成・検証 CLI
references/lightweight-evolver.md # 軽量エボルバーの手順
references/research-quality.md    # 証拠品質リファレンス
agents/openai.yaml                # スキル UI メタデータ
tests/                            # 回帰テスト
```

## ライセンス

MIT。詳しくは [license.txt](license.txt) を参照してください。
