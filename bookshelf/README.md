# 本棚（EPUBリーダー）

`books/` フォルダに `.epub` ファイルを入れるだけで、スマホ（iPhone・Android）やPCのブラウザで本のように読めるWebアプリです。

- 本棚に表紙・タイトル・著者が並びます。サブフォルダを作ると、その名前ごとに棚が分かれます。
- ページは、左右のタップ、スワイプ、キーボードの ← → でめくれます。PCの広い画面では見開き2ページで表示します。
- 目次から章へ移動できます。下のスライダーで好きな位置へも移動できます。
- 文字サイズ、書体（ゴシック・明朝）、行間、背景（白・セピア・黒）を変えられます。
- 読んだ位置は端末ごとに自動で保存され、次に開いたとき続きから読めます。
- ホーム画面に追加すると、アプリと同じように開けます。

## 仕組み

```
GitHub（非公開リポジトリ）の books/ に .epub を入れてコミット
        ↓  Cloudflare Pages が自動でビルド（1〜2分）
表紙・タイトルを取り出して本棚を作成
        ↓
秘密のURLに公開
https://<プロジェクト名>.pages.dev/<秘密の文字列>/
```

公開されるのは、推測できない長い文字列のURLだけです。それ以外のURLでは何も表示されず、検索エンジンにも載りません。
URLを知っている人はログインなしで読めます。

> **ご注意**
> - 本のファイルは、リポジトリを見られる人には見えてしまいます。リポジトリは必ず **Private（非公開）** にしてください。
> - Cloudflare Pages に置けるのは **1ファイル25MBまで** です。それより大きい .epub は公開されません（ビルドのログに警告が出ます）。

## 最初の設定（1回だけ）

### 1. GitHub に非公開リポジトリを作る
新しいリポジトリを **Private** で作り、このフォルダの中身（`app/`、`books/`、`scripts/`、`README.md`、`.gitignore`）を入れます。

### 2. Cloudflare Pages とつなぐ
1. [Cloudflare](https://dash.cloudflare.com/sign-up) に無料で登録してログインします。
2. 左のメニューの **Workers & Pages**（「コンピューティング」の中にある場合もあります）→ **作成（Create）** を押します。
3. **Pages** を選び、**Git リポジトリをインポート（Import an existing Git repository / Connect to Git）** を選びます。
4. GitHub との連携を求められたら許可します。そのとき、読み取りを許すリポジトリは **このリポジトリだけ（Only select repositories）** にするのがおすすめです。
5. リポジトリを選び、次のとおり設定します。

| 項目 | 設定する値 |
|---|---|
| プロジェクト名 | 好きな名前（URLの `〇〇.pages.dev` になります） |
| 本番ブランチ（Production branch） | `main` |
| フレームワーク プリセット | なし（None） |
| ビルド コマンド | `bash scripts/cf-build.sh` |
| ビルド出力ディレクトリ | `_site` |
| 環境変数（Environment variables） | 名前 `READER_PATH`、値は英数字16文字以上のランダムな文字列（例：`k7Qm2xVb9PzR4tLw8NcY`） |

6. **保存してデプロイ（Save and Deploy）** を押します。1〜2分で完了します。

### 3. URLを開く
`https://<プロジェクト名>.pages.dev/<READER_PATH の値>/`
（例：`https://my-books.pages.dev/k7Qm2xVb9PzR4tLw8NcY/`）

このURLを、読んでもらいたい人に伝えてください。

### URLを変えたいとき（読める人を入れ替えたいとき）
Cloudflare のプロジェクトの **設定 → 変数とシークレット** で `READER_PATH` の値を変えます。そのあと **デプロイ** タブで最新のデプロイを **再試行（Retry deployment）** します。古いURLは使えなくなります。

### もっと厳しく制限したいとき（任意）
Cloudflare の **Zero Trust → Access** を使うと、登録したメールアドレスの人だけがログインして読めるようにできます（50人まで無料）。

## 本の追加・削除

- **追加**：GitHubでリポジトリの `books` フォルダを開き、**Add file → Upload files** で `.epub` をドラッグして **Commit changes** を押します。Cloudflare が自動でビルドし、1〜2分で本棚に並びます。
- **削除**：GitHub上でファイルを開き、ゴミ箱アイコンで削除してコミットします。
- **棚を分ける**：`books/小説/〇〇.epub` のようにフォルダに入れると、棚が分かれます。
- **本を差し替える**：同じ名前のファイルをアップロードし直すと更新されます。

## ホーム画面に追加する

- **iPhone（Safari）**：共有ボタン → 「ホーム画面に追加」
- **Android（Chrome）**：右上の ︙ → 「ホーム画面に追加」（または「アプリをインストール」）
- **PC（Chrome / Edge）**：アドレスバー右側のインストールアイコン、またはブックマーク

## 手元で試す

```bash
READER_PATH=test1234567890abcd bash scripts/cf-build.sh
cd _site && python -m http.server 8000
```

ブラウザで http://localhost:8000/test1234567890abcd/ を開きます。

## ファイル構成

| パス | 内容 |
|---|---|
| `books/` | ここに `.epub` を入れる |
| `app/index.html` | 読書アプリ本体（[epub.js](https://github.com/futurepress/epub.js) を使用） |
| `app/manifest.webmanifest`、`app/*.png` | ホーム画面用のアイコンと設定 |
| `scripts/build.py` | `books/` から本の一覧（`books.json`）と表紙画像を作る |
| `scripts/cf-build.sh` | Cloudflare Pages のビルドコマンド（秘密のURLの下に組み立てる） |
