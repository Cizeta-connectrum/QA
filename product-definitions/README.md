# 製品定義書（Product Definitions）

社内 QA ボットおよび社内教育で使う「製品定義書」を、Google Drive に蓄積した資料から整理して管理するディレクトリです。

- **ソース（一次資料）**: Google Drive（カタログ、取扱説明書、約款、FAQ、議事録など）
- **成果物（整理済みデータ）**: このリポジトリ（Markdown + YAML + JSONL）

## ディレクトリ構成

```
product-definitions/
├── README.md                 # このファイル（運用ルール）
├── SCHEMA.md                 # 製品定義書の章立てと各項目の書き方
├── templates/                # 新しい製品を追加するときの雛形
│   ├── definition.template.md
│   ├── faq.template.md
│   └── sources.template.yaml
├── sources/
│   └── registry.yaml         # Drive ソース台帳（全製品共通）
├── products/
│   └── <product-id>/
│       ├── definition.md     # 製品定義書（人が読む正本）
│       ├── faq.md            # Q&A 集（QA ボットの主入力）
│       ├── glossary.md       # 用語集
│       └── sources.yaml      # この製品が参照した Drive ファイル一覧
├── scripts/
│   └── build_qa_dataset.py   # faq.md / glossary.md → dist/*.jsonl に変換
└── dist/
    └── <product-id>.qa.jsonl # QA ボット取り込み用（RAG / ファインチューニング）
```

## 運用フロー

1. **ソース登録**: 参照する Drive ファイルを `sources/registry.yaml` と `products/<id>/sources.yaml` に登録する（file id・タイトル・種別・版）。
2. **定義書更新**: `SCHEMA.md` の章立てに従って `definition.md` を更新する。数値・型番・価格は必ず出典（`source:` ラベル）を付ける。
3. **FAQ 更新**: `faq.md` に Q/A を追加する。1 つの Q に 1 つの A。回答本文には出典 ID を書く。
4. **データ生成**: `python3 scripts/build_qa_dataset.py` を実行して `dist/` を再生成する。
5. **コミット**: 定義書・FAQ・dist を同じコミットに含める。

## 書き方のルール

- 事実（仕様・価格・規格）と、判断・推奨（営業トーク・運用上の推奨）を分ける。
- 出典のない記述は `⚠️ 未確認` を付ける。QA ボットはこの印が付いた項目を回答に使わない前提。
- 日付のある情報（価格、対応機種、キット内訳）は「時点」を明記する。
- 個人名・患者情報・契約者固有情報は書かない。

## 現在の製品

| product-id | 製品名 | 状態 |
|---|---|---|
| `landmarker` | LANDmarker / Landmark System（株式会社アイキャット） | 初版 |
| `drclear` | Dr.Clear（クリア医療器械技術・常州 / Bondent Group。日本は試験販売段階） | 初版 |
