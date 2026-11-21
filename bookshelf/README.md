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
books/ に .epub を入れてコミット
        ↓  GitHub Actions が自動で実行（1〜2分）
表紙・タイトルを取り出して本棚を作成
        ↓
GitHub Pages の「秘密のURL」に公開
https://<アカウント名>.github.io/<リポジトリ名>/<秘密の文字列>/
```

公開されるのは、推測できない長い文字列のURLだけです。それ以外のURLでは何も表示されず、検索エンジンにも載りません。
URLを知っている人はログインなしで読めます。

> **ご注意**：本のファイルは、リポジトリを見られる人には見えてしまいます。リポジトリは必ず **Private（非公開）** にしてください。

## 最初の設定（1回だけ）

1. **リポジトリを作る**
   GitHubで新しいリポジトリを **Private** で作り、このフォルダの中身（`app/`、`books/`、`scripts/`、`.github/`、`README.md`）を入れます。

2. **秘密の文字列を登録する**
   リポジトリの **Settings → Secrets and variables → Actions → New repository secret** を開き、次のとおり登録します。
   - Name：`READER_PATH`
   - Secret：英数字で16文字以上のランダムな文字列（例：`k7Qm2xVb9PzR4tLw8NcY`）

   この文字列がURLの一部になります。URLを変えたいとき（読める人を入れ替えたいとき）は、この値を変えて再実行してください。

3. **GitHub Pages を有効にする**
   **Settings → Pages → Build and deployment → Source** で **GitHub Actions** を選びます。

4. **初回の公開**
   **Actions** タブの「本棚を公開」で **Run workflow** を押します。緑のチェックがつけば完了です。

5. **URLを開く**
   `https://<アカウント名>.github.io/<リポジトリ名>/<READER_PATH の値>/`
   （例：`https://example.github.io/books/k7Qm2xVb9PzR4tLw8NcY/`）

## 本の追加・削除

- **追加**：GitHubでリポジトリの `books` フォルダを開き、**Add file → Upload files** で `.epub` をドラッグして **Commit changes** を押します。1〜2分で本棚に並びます。
- **削除**：GitHub上でファイルを開き、ゴミ箱アイコンで削除してコミットします。
- **棚を分ける**：`books/小説/〇〇.epub` のようにフォルダに入れると、棚が分かれます。
- **本を差し替える**：同じ名前のファイルをアップロードし直すと更新されます。

## ホーム画面に追加する

- **iPhone（Safari）**：共有ボタン → 「ホーム画面に追加」
- **Android（Chrome）**：右上の ︙ → 「ホーム画面に追加」（または「アプリをインストール」）
- **PC（Chrome / Edge）**：アドレスバー右側のインストールアイコン、またはブックマーク

## 手元で試す

```bash
pip install pillow
python scripts/build.py _site_reader
cd _site_reader && python -m http.server 8000
```

ブラウザで http://localhost:8000/ を開きます。

## ファイル構成

| パス | 内容 |
|---|---|
| `books/` | ここに `.epub` を入れる |
| `app/index.html` | 読書アプリ本体（[epub.js](https://github.com/futurepress/epub.js) を使用） |
| `app/manifest.webmanifest`、`app/*.png` | ホーム画面用のアイコンと設定 |
| `scripts/build.py` | `books/` から本の一覧（`books.json`）と表紙画像を作る |
| `.github/workflows/deploy.yml` | プッシュするたびに自動で組み立てて GitHub Pages に公開 |
