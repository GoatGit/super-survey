# Super Survey

言語: [English](README.md) | [中文](README.zh-CN.md) | 日本語

Super Survey は、agent のための汎用調査 skill です。制約付き意思決定最適化ワークフローとして、株式、プロダクト、オープンソース専用のテンプレートではありません。同じループを、プロダクト機会、市場、技術的実現可能性、OSS 採用、デューデリジェンス、政策、戦略、そしてリンク集ではなく根拠ある判断が必要な問いに使えます。

このプロジェクトは、この論文の具体的な実装です。[如何拒绝AI谄媚人类.md](如何拒绝AI谄媚人类.md) の思想をそのまま調査ワークフローに落とし込みます。この論文は、オープンエンドな調査を直接回答生成ではなく、制約付き意思決定最適化として扱うべきだと主張します。Super Survey はその考え方を、目的関数、制約、暗黙の仮定、証拠基準、反論、統合判断、次ラウンドの問いを段階的に作るワークフローに落とし込みます。

主に次の 3 つを担います:

- 曖昧な問いを、目的、制約、調査フレームワーク、証拠基準が明確な調査タスクに変える。
- 証拠、レッドチーム批判、暗黙の期待値チェック、シナリオ、ベイズ更新によって思い込みの結論を減らす。
- 多ラウンドの反復を通じて、人間の意思決定者が本当に必要とする最終レポートに近づけていく。

## 第一原理

Super Survey は、2 つの第一原理から始まります:

1. 世界はランダムでノイズが多く、確実に予測できるものではありません。初期の直感は、偏りや不完全な情報につながりやすいものです。すべてのタスクは、「先に結論を決め、その結論を支える証拠を集める」罠を避けなければなりません。
2. ユーザーの問いは出発点であり、目的関数ではありません。証拠を探したり結論へ収束したりする前に、ユーザーのフレーミング、暗黙の仮定、本当に最適化すべき目標を点検します。

この 2 つの原理により、ワークフローは事後に門限を厳しくするよりも、事前ガイダンスを重視します。証拠収集の前に、目的、制約、判断に重要な変数、最低限の直接証拠、暗黙の期待値、反ナラティブ正則化を定義し、agent がユーザーのフレームを早く受け入れすぎたり、好ましい結論を支える材料だけを集めたりしないようにします。

## 理論的基礎

論文は投資例を使っていますが、この skill の実装は広く汎用的です。Super Survey は、目的関数の再構築、制約モデリング、暗黙期待チェック、最低限の直接証拠、対抗検証、感度分析、ベイズ更新、シナリオ分析、意思決定ツリー、prose-first の最終レポートを、さまざまな調査タスクへ一般化します。

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
├── 01-evidence-plan.md
├── 01-research.md
├── 01-brainstorm.md
├── 01-redteam.md
├── 01-synthesis.md
├── 01-evolver.md
├── sources.jsonl
├── claims.jsonl
├── evidence.jsonl
├── index.md
├── report.md              # final-only; 停止ゲート通過後に作成
└── .super-survey.json
```

## インストール

Skills CLI で直接インストールします:

```bash
npx skills add GoatGit/super-survey
```

Codex ユーザーは Codex skills ディレクトリへコピーすることもできます:

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
python3 scripts/survey_round.py init "formal market report" --mode deep
```

ラウンドを作成して検証します。各段階コマンドで生成されたファイルに実質的な内容を書いてから、次の段階コマンドを実行します:

```bash
python3 scripts/survey_round.py round surveys/2026-06-13-ai採用エージェント 1
python3 scripts/survey_round.py research surveys/2026-06-13-ai採用エージェント 1
python3 scripts/survey_round.py brainstorm surveys/2026-06-13-ai採用エージェント 1
python3 scripts/survey_round.py redteam surveys/2026-06-13-ai採用エージェント 1
python3 scripts/survey_round.py synthesis surveys/2026-06-13-ai採用エージェント 1
python3 scripts/survey_round.py evolve surveys/2026-06-13-ai採用エージェント 1
python3 scripts/survey_round.py check surveys/2026-06-13-ai採用エージェント
python3 scripts/survey_round.py check-final surveys/2026-06-13-ai採用エージェント
python3 scripts/survey_round.py upgrade-report surveys/2026-06-13-ai採用エージェント
```

証拠レジストリのリンクだけを直接デバッグ:

```bash
python3 scripts/survey_round.py validate-evidence surveys/2026-06-13-ai採用エージェント
```

コマンドの意味:

- `round` / `plan`: 段階化 CLI のラウンドを開始し、`NN-evidence-plan.md` だけを作成します。すべてのラウンド成果物を一度に作ることはしません。
- `research`: `NN-evidence-plan.md` に実質的な内容が入っている場合だけ `NN-research.md` を作成します。
- `brainstorm`: `NN-research.md` に実質的な内容が入っている場合だけ `NN-brainstorm.md` を作成します。
- `redteam`: `NN-brainstorm.md` に実質的な内容が入っている場合だけ `NN-redteam.md` を作成します。
- `synthesis`: `NN-redteam.md` に実質的な内容が入っている場合だけ `NN-synthesis.md` を作成します。
- `evolve`: `NN-synthesis.md` に実質的な内容が入っている場合だけ `NN-evolver.md` を作成します。
- `check`: ラウンド成果物、`index.md`、証拠レジストリ、companion routing 記録、最新エボルバーの生判断を検証します。`report.md` は要求しません。
- `check-final`: `check` の内容に加えて、最終 `report.md`、prose-first ルール、`index.md` に記録されたモード別品質スコア、残差ゲート、ハード制約ゲート、最新エボルバー判断が `Final` または `Kill` であることを検証します。
- `upgrade-report`: 古いレポートに完全な report schema を追加します。古い 6 セクションのレポートは読めますが final gate は通過できません。アップグレード後は新しいセクションを埋めてください。
- `validate-evidence`: `sources.jsonl`、`claims.jsonl`、`evidence.jsonl` の直接デバッグ専用です。通常のラウンド検証は `check` / `check-final` を使います。

最新判断が `Keep`、`Narrow`、または `Pivot` の場合、`check` は継続 warning 付きで成功できます。これにより、早すぎる `Kill` を誘導せず次ラウンドへ進めます。ラウンド番号は正の整数である必要があります。

## モードと証拠レジストリ

モード選択は明示的に行います。既定は `standard` です。ユーザーが quick / brief / fast / 初期スキャン / 低リスクの方向確認を明示した場合だけ `quick` を使い、deep / formal / long report / 多数の引用 / 厳密な監査 / 出版品質 / 重要な意思決定メモを明示した場合は `deep` を使います。

| モード | 用途 | 最低レジストリ要件 | レポートゲート |
|---|---|---:|---|
| `quick` | ユーザーが明示的に quick、brief、fast、初期スキャン、低リスク方向確認を求めた場合 | 1 情報源、1 主張、1 証拠 | スコア >=80 |
| `standard` | 既定の再利用可能な調査レポート。通常の「X をやる / 買う / 採用する価値があるか」の調査依頼を含む | 3 情報源、3 主張、3 証拠 | スコア >=90 |
| `deep` | ユーザーが明示的に deep、formal、long report、多数の引用、厳密な監査、出版品質、重要な意思決定メモを求めた場合 | 8 情報源、6 主張、8 証拠 | スコア >=95 |

`quick` モードでは、`NN-round.md` が今回の調査問い、証拠計画、証拠と情報源、brainstorming チェックポイント、レッドチーム、統合結論、生判断、次の行動を含む場合、standard/deep の分割ラウンド成果物を置き換えられます。

投資、法律、医療、セキュリティ、本番障害、重大な事業コミットメントのような高リスク行動判断では、`quick` を最終納品モードとして使わないでください。`standard` または `deep` を使い、段階成果物、証拠網羅、品質ゲートを判断リスクに合わせます。

高リスク行動の依頼に「quick / fast」のような速度要求が含まれる場合も、モードは `standard` または `deep` のままにし、最終要約を短くする形で対応します。

要求が曖昧な場合は、`init` の前に `python3 scripts/survey_round.py recommend-mode --text "<request>"` を実行できます。

軽量な証拠レジストリは、本文の読みやすさを保ちながら監査可能性を残します:

- `sources.jsonl`: `source_id`, `title`, `url`, `source_type`, `date_checked`, `credibility`
- `evidence.jsonl`: `evidence_id`, `source_id`, `quote_or_summary`, `locator`, `confidence`
- `claims.jsonl`: `claim_id`, `claim`, `supporting_evidence_ids`, `status`

すべての evidence は既存の source を参照する必要があります。supported、partial、contested の claim は既存の evidence を参照する必要があります。チェッカーは重複 ID と、supported/partial claim がリンク先 evidence と明らかに対応していない弱い支援関係も検出します。密な証拠表は本文ではなく、付録または JSONL に置きます。

`C1`、`E1` のような registry ID は作業ファイル用です。最終 `report.md` では、それらを情報源タイトル、Markdown リンク、脚注、または URL を含む付録参照に置き換え、JSONL レジストリを開かなくても読める形にします。

## skills.sh 収録準備

このリポジトリは、Skills CLI の発見と skills.sh のインデックスに向けた構成になっています:

- ルート階層の `SKILL.md` に `name` と `description` frontmatter を配置
- `agents/openai.yaml` の UI メタデータ
- `scripts/` 配下の補助スクリプト
- `references/` 配下の参考資料
- MIT ライセンス、テスト、多言語 README ファイル

発見できることを検証:

```bash
npx skills add GoatGit/super-survey --list
```

## 調査フレームワーク

`調査レンズ` はどの証拠を重視するかを決めます。`調査フレームワーク` は、調査全体がどの方法で問いを体系的に検討したかを読者に示します。各調査では、採用したフレームワーク、次元、弱い次元、意図的に除外した次元を明記し、その次元を `00-brief.md`、各ラウンド成果物、最終レポートの共通構造として使います。

フレームワークを選ぶ前に、反迎合のフレーミング確認を行います。ユーザーの表現を、既知の事実、未検証の仮定、主観的判断、欠落情報、主要ステークホルダーに分け、そのうえで目的を意思決定の言葉に置き直します。これにより、ユーザーの初期表現、より中止しやすい強い命題、または耳ざわりは良いが本当の判断に答えない結論へ最適化することを防ぎます。

良い対象が、そのまま良い行動になるわけではありません。良い会社は必ずしも良い株ではなく、良いプロダクトは必ずしも良い事業ではなく、良い技術は必ずしも良いプロジェクトではなく、良い OSS ライブラリは必ずしも良い依存先ではありません。Super Survey は、現在の制約、価格やコスト、タイミング、保守負担、リスク、代替案の下で、その行動が魅力的かを評価します。

最重要の記述ルールは、フレームワークを最後に付ける監査チェックリストにしないことです。`00-brief.md` が次元を定義し、`NN-evidence-plan.md`、`NN-research.md`、`NN-brainstorm.md`、`NN-redteam.md`、`NN-synthesis.md`、`NN-evolver.md` は同じ次元を Markdown 小見出しとして展開します。最終 `report.md` では、それらを付録より前の読みやすい本文章にします。

段階化 CLI が依存順序を強制します。まず `NN-evidence-plan.md` を書き、その後で `NN-research.md`、`NN-brainstorm.md`、`NN-redteam.md`、`NN-synthesis.md`、最後に `NN-evolver.md` を作成します。下流の成果物は、最終結論を予測するのではなく、すでに書かれた上流の発見を参照します。

## 理想フローと論文メソッドの対応

反シコファンシー論文から抽象した実行アーキテクチャです:

| ノード | 担う作業 | 対応する論文メソッド |
|---|---|---|
| Brief / Frame Contract | 元の問いを保持し、目的関数を再構築し、事実、仮定、推論、価値判断を分け、制約、候補行動、調査フレームワークを定義します。 | 4.1, 4.2, 4.3, 6.2 |
| Evidence Plan / Minimum Direct Evidence | 情報源収集の前に、今回減らす対象残差、判断に重要な変数、最低限の直接証拠、優先情報源、反証、欠落証拠の扱い、フレームワーク別の証拠需要を定義します。 | 3.7.3, 3.7.4, 5.2, 5.3, 6.2 |
| Research | 証拠計画に沿って現在情報と一次情報を集め、source/claim/evidence レジストリを更新し、矛盾、信頼度、鮮度、フレームワーク網羅を記録します。 | 4.2, 4.5, 4.7, 4.9, 5.1 |
| Post-Research Brainstorming | 証拠が存在した後に候補説明を開き直し、multi-start 視点、起こりやすい誤り、次の証拠行動、証拠で必要になったフレームワーク修正を比較します。 | 4.4, 4.5, 4.6, 5.3 |
| Redteam | 現時点の最強主張、代替案、隠れた仮定、停止条件、反ナラティブ正則化を攻撃します。 | 4.5, 4.8, 4.12, 5.2 |
| Synthesis | 証拠と反論を、感度分析、暗黙期待の逆算、ベイズ更新、シナリオ、意思決定ツリー、制約別推奨に統合します。 | 4.6, 4.7, 4.9, 4.10, 4.11 |
| Evolver | 残差を評価し、VOI と調査コストを比較し、Keep / Narrow / Pivot / Kill / Final を決め、未来の事実と desk research で減らせるギャップを分け、次ラウンド目標または最終化理由を生成します。 | 3.7.1-3.7.4, 5.2-5.5, 6.2-6.5 |
| Final Report | フレームワーク本文章、判断ロジック、推奨、変化トリガー、次の行動、範囲、付録を備えた、人間向けの独立した判断メモを書きます。 | 4.10, 4.11, 6.3-6.5 |

証拠によってフレームワークを修正する必要がある場合は、`index.md` の `フレームワーク修正ログ` に現在の次元、変更の証拠トリガー、元の問い/中核が保持されていることを記録します。以後のラウンドは修正後の次元を使います。黙ってフレームワークをずらしてはいけません。

よく使う起点:

| 調査タイプ | フレームワーク次元 |
|---|---|
| プロダクト機会 | ユーザーの痛み、頻度、支払い意思、代替手段、流通、継続、信頼/コンプライアンス、実装難度 |
| 市場/競合 | 需要、供給、競争、価格、チャネル、切替コスト、規制、成長ドライバー |
| 技術実現性 | 要件、アーキテクチャ、データ/API アクセス、性能、信頼性、セキュリティ、運用、保守 |
| OSS 採用 | ライセンス、メンテナー健全性、リリース頻度、issue 対応、API 安定性、エコシステム、代替案、採用リスク |
| 投資/デューデリジェンス | マクロ、業界、会社、財務品質、バリュエーション、カタリスト、資金フロー、リスク |

証券系の調査では、市場、業界、会社のフレームワークを組み合わせられます。市場はマクロ、流動性、利益、バリュエーション、リスク選好、資金フローを見る。業界は需要、供給、競争、政策、技術、サイクル、バリュエーションを見る。会社はビジネスモデル、財務品質、成長性、競争優位、バリュエーション、カタリスト、リスクを見る。これらは例であり、固定分岐ではありません。

## 品質ゲート

README は運用の形だけを示します。完全な agent チェックリストは `SKILL.md` にあります。

ゲートは 4 つです:

- `check` はラウンドゲートです。成果物、レジストリリンクと弱い支援関係、明示的な修正を含むフレームワーク網羅、必要な companion 記録、最新エボルバーの生判断を検証します。判断が `Keep`、`Narrow`、`Pivot` の場合は継続 warning 付きで成功できます。
- エボルバーは方向ゲートです。`Keep`、`Narrow`、`Pivot` は次ラウンド作成と `index.md` 更新を意味します。`Final` は最終レポート作成へ進めることを意味し、`Kill` は現在の仮説を止めるか desk research 以外へ切り替えることを意味します。
- 残差 / VOI / ハード制約ゲートは停止安全ゲートです。最新エボルバーと `index.md` は `r_q/r_c/r_e/r_h/r_a/r_s/r_j` の 0-3 評価、対象残差、期待情報価値、調査コスト、VOI がコストを上回るか、ハード制約が満たされているかを記録します。
- `check-final` は納品ゲートです。完全な prose-first の `report.md`、モード別スコアの合格、残差ゲートの合格、ハード制約ゲートの合格、最新エボルバーの生判断が `Final` または `Kill` であることを要求します。

最終納品では、`index.md` に記録する 100 点の品質ゲートを使います:

| 観点 | 点数 |
|---|---:|
| 反シコファンシー / 目的関数の整合性 | 20 |
| 情報源、方法、フレームワークの品質 | 15 |
| 証拠の完全性 | 20 |
| 分析とレッドチームの品質 | 20 |
| 実行可能性 | 15 |
| 構成と読みやすさ | 10 |

`index.md` の最終品質ゲートには、反シコファンシー / 目的関数の整合性のサブスコアを記録します。情報源が多くても、ユーザーの初期フレームをそのまま受け入れたり、問いを判断しやすい強い主張に書き換えたり、目的関数の再構築不足を高い総合点で隠したりするレポートは最終ゲートを通過しません。

モードしきい値はハードゲートです。`quick >=80`、`standard >=90`、`deep >=95`。最終レポートが選択モードのしきい値を下回る場合、最低スコア領域に焦点を当てて次のラウンドを続けます。ヘルパーは停止判断に、生のエボルバー判断、スコアしきい値、残差ゲート、ハード制約ゲートだけを使います。`report.md` の「将来の開示」や「外部検証」といった説明文は停止ルールとして解析しません。

残差ベクトルは、論文の「残差駆動の証拠反復」を運用化したものです。`r_q` は問いのフレーミング、`r_c` は制約、`r_e` は証拠、`r_h` は仮説、`r_a` は対抗検証、`r_s` は感度、`r_j` は実行可能性を表します。いずれかの残差が `3` なら意思決定レベルのギャップです。そのギャップを desk research で減らせる具体的な行動があり、VOI がコストを上回るなら継続します。残差が `3` ではなく、ハード制約が通り、残りの desk research の VOI がコストを下回る場合にのみ最終レポートへ進みます。

生のエボルバー判断は機械可読の行であり、ローカライズされた説明文ではありません。どの言語の成果物でも、`判断` 見出し下の最初の非空行は厳密に `Keep`、`Narrow`、`Pivot`、`Kill`、`Final` のいずれかにしてください。翻訳や説明はその次の行以降に書きます。

最終レポートは人が読み通せる判断メモとして書きます。本文では結論、フレームワーク次元ごとの本文章、主要な物語、判断ロジック、最終推奨、結論を変える条件、次の行動、範囲を先に示します。証拠レジスター、情報源品質、レッドチームメモ、シナリオ、情報源一覧は付録に置きます。品質スコアは `index.md` の最終レポート品質ゲートに記録し、`report.md` には書きません。フレームワーク次元は本文のトップレベル Markdown 見出しとして現れる必要があり、方法メモや付録だけに置いてはいけません。引用は単独で読める情報源リンクまたは情報源説明にし、`C*` / `E*` registry ID にしてはいけません。本文が箇条書きや監査表に支配されている場合は最終ゲートを通過しません。

Companion skills は、検索、長文レポート、VOC/顧客調査、競合分析、brainstorming、wiki への蓄積のための任意の補助です。現在の情報源発見が必要な場合は `tavily-search` を優先し、検索経路または fallback を記録します。正式な長文レポート、多数の引用、HTML/PDF 出力、厳密な citation 検証には、利用できる場合に `deep-research` を優先できます。長期的な知識再利用が必要な場合だけ wiki 蓄積を使います。最終的な判断ループは Super Survey が担います。

## 呼び出しフロー

```mermaid
flowchart TD
    A[ユーザーの調査問い] --> B[00-brief.md<br/>Brief / Frame Contract]
    B --> P[NN-evidence-plan.md<br/>Evidence Plan / Minimum Direct Evidence]
    P --> C[NN-research.md<br/>情報源検索、claim-level レジストリ、フレームワーク網羅]
    C --> D{調査段階で companion が必要?}
    D -->|現在情報| D1[Tavily 優先<br/>または適した検索ツール]
    D -->|長い証拠包装| D2[Deep Research 優先]
    D -->|VOC / ユーザーの言葉| D3[Customer または Reddit research]
    D -->|競合| D4[Competitive research]
    D1 --> C
    D2 --> C
    D3 --> C
    D4 --> C
    C --> E[NN-brainstorm.md<br/>Post-Research Brainstorming]
    E --> X{対象を絞って証拠を追加する?}
    X -->|はい| C
    X -->|いいえ| F[NN-redteam.md<br/>リスク、代替案、停止条件]
    F --> G[NN-synthesis.md<br/>感度、ベイズ更新、意思決定ツリー]
    G --> H[NN-evolver.md<br/>Keep / Narrow / Pivot / Kill / Final]
    H --> V{残差 / VOI / ハード制約}
    V -->|残差3 + VOI > コスト| I[index.md<br/>作業台: 次回目標と未最終化理由]
    I --> P
    V -->|Final / Kill + ゲート合格| J[report.md を作成<br/>フレームワーク次元を本文章にする]
    J --> R[check-final<br/>スコア、残差、ハード制約、prose-first ゲート]
    R -->|いずれか未合格| I
    R -->|すべて合格| K[最終回答<br/>判断志向の要約]
```

## インスピレーション: Karpathy の autoresearch

Super Survey の軽量エボルバーは、敬意と帰属を込めて Andrej Karpathy の [autoresearch](https://github.com/karpathy/autoresearch) から着想を得ています。autoresearch の中心的な考え方は、AI agent に実際の学習環境を与え、コードを変更させ、短い実験を走らせ、指標が改善したかを確認し、変更を保持または破棄して反復することです。

Super Survey は、このループをプロダクト、市場、技術、オープンソース調査向けに適用しています:

| 観点 | Karpathy autoresearch | Super Survey エボルバー |
|---|---|---|
| 目的 | 実験を通じてモデルまたはコードを改善する | 調査仮説を実行可能な判断へ近づける |
| 入力 | 学習コード、固定評価、実験ログ | 証拠、情報源、制約、レッドチーム批判 |
| フィードバック | validation loss など比較可能な単一指標 | 証拠の強さ、リスク、信頼度にもとづく構造化判断 |
| 判断 | コード変更を保持または破棄する | `Keep` 維持、`Narrow` 絞り込み、`Pivot` ピボット、`Kill` 中止、または `Final` 最終化する |
| 出力 | 改善されたコード/モデルと実験履歴 | より絞られた次回調査目標と必要な証拠 |

要するに、autoresearch は指標駆動の最適化であり、Super Survey は判断駆動の絞り込みです。調査対象に明確な benchmark がある場合、Super Survey は autoresearch に近い形を取れます。一方で、買い手の意欲、コンプライアンス、流通、戦略リスクが中心の問いでは、すべてを一つの数値に還元したふりをせず、証拠優先かつ意思決定志向のループを保ちます。

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
SKILL.md                         # agent skill 指示
scripts/survey_round.py           # 調査成果物の生成・検証 CLI
references/lightweight-evolver.md # 軽量エボルバーの手順
references/research-quality.md    # 証拠品質リファレンス
agents/openai.yaml                # スキル UI メタデータ
tests/                            # 回帰テスト
```

## ライセンス

MIT。詳しくは [license.txt](license.txt) を参照してください。
