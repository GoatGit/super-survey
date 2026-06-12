# Contributing

## English

Thank you for improving Super Survey. Keep changes small, evidence-backed, and easy to verify.

Before opening a pull request:

1. Run `python3 -m unittest discover -v`.
2. Run `python3 -m py_compile scripts/survey_round.py`.
3. If you change generated templates, update validation tests in `tests/`.
4. If you change skill behavior, update `SKILL.md` and the relevant README language sections.
5. Keep runtime dependencies limited to the Python standard library unless there is a strong reason.

For documentation changes, keep English, Chinese, and Japanese sections aligned.

## 中文

感谢改进 Super Survey。请保持变更小而清晰，并确保可以验证。

提交 PR 前：

1. 运行 `python3 -m unittest discover -v`。
2. 运行 `python3 -m py_compile scripts/survey_round.py`。
3. 如果修改模板生成内容，请同步更新 `tests/` 中的校验测试。
4. 如果修改技能行为，请同步更新 `SKILL.md` 和 README 中相关语言章节。
5. 除非有充分理由，运行时依赖应保持为 Python 标准库。

文档变更需要保持英文、中文、日文内容一致。

## 日本語

Super Survey への改善ありがとうございます。変更は小さく、検証しやすい形にしてください。

Pull request を作成する前に:

1. `python3 -m unittest discover -v` を実行してください。
2. `python3 -m py_compile scripts/survey_round.py` を実行してください。
3. 生成テンプレートを変更した場合は、`tests/` の検証テストも更新してください。
4. スキルの挙動を変更した場合は、`SKILL.md` と README の該当言語セクションを更新してください。
5. 強い理由がない限り、実行時依存は Python 標準ライブラリに留めてください。

ドキュメントを変更する場合は、英語・中国語・日本語の内容を揃えてください。
