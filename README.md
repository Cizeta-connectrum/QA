# ConversationQA - Meeting Notes & Q&A Platform

## 概要 / Overview

ConversationQA は、会議の議事録を管理しながら、議事録に対してコメント・質問ができるプラットフォームです。Google Apps Script と Google Workspace API を使用して、複数のユーザーがリアルタイムで会議情報を共有できます。

**ConversationQA** is a platform for managing meeting notes while allowing users to ask questions and leave comments on those notes. It leverages Google Apps Script and Google Workspace APIs to enable multiple users to share meeting information in real-time.

## 機能 / Features

### 主な機能 / Main Features

- **会議管理** / **Meeting Management**
  - 新しい会議を作成・管理
  - 会議の詳細情報（日時、参加者、説明）を記録
  - Create and manage new meetings
  - Record meeting details (date, time, participants, description)

- **議事録作成** / **Meeting Notes**
  - 会議ごとに議事録を作成・編集
  - Create and edit meeting notes for each meeting

- **会話機能** / **Conversation Features**
  - メモ、質問、コメントを投稿可能
  - 会議に対するフィードバックをリアルタイムで共有
  - Post notes, questions, and comments
  - Share feedback on meetings in real-time

- **複数言語対応** / **Multi-language Support**
  - 日本語と英語に対応
  - Support for Japanese and English

- **検索機能** / **Search Functionality**
  - キーワードベースの検索
  - タイプ別のフィルタリング
  - Keyword-based search
  - Filtering by type (notes, questions, comments)

- **ユーザー認証** / **User Authentication**
  - Google Workspace 連携
  - ユーザー登録・管理
  - Google Workspace integration
  - User registration and management

- **モバイル対応** / **Mobile Responsive**
  - スマートフォン・タブレット対応
  - Responsive design for smartphones and tablets

## 技術スタック / Tech Stack

- **フロントエンド** / **Frontend**
  - HTML5
  - CSS3 (モダンレイアウト / Modern Layout)
  - JavaScript (Vanilla)

- **バックエンド** / **Backend**
  - Google Apps Script (GAS)
  - Google Sheets API
  - Google Drive API

- **インフラ** / **Infrastructure**
  - Google Workspace
  - Google Cloud Platform

## セットアップ / Setup

### 必要な環境 / Prerequisites

- Google Workspace アカウント / Google Workspace Account
- Google Cloud Project
- clasp（オプション）/ clasp (Optional)

### インストール手順 / Installation

1. **Google Apps Script プロジェクトを作成**
   - Google Drive で新しいスプレッドシートを作成
   - ツール > スクリプトエディタ をクリック

2. **ファイルをコピー**
   - `Code.js` の内容をスクリプトエディタにコピー
   - スプレッドシートの名前を決定

3. **デプロイ**
   - スクリプトエディタで「新しいデプロイ」をクリック
   - 「ウェブアプリ」を選択
   - デプロイリンクをコピーして使用

### Using clasp

```bash
# clasp をグローバルインストール
npm install -g @google/clasp

# Google にログイン
clasp login

# プロジェクトを初期化
clasp create --type standalone

# ファイルをプッシュ
clasp push

# ウェブアプリをデプロイ
clasp deploy
```

## 使い方 / Usage

### 会議の作成 / Creating a Meeting

1. アプリを開き、「新しい会議」ボタンをクリック
2. 会議情報を入力（タイトル、日付、説明、参加者）
3. 「作成」をクリック

### 議事録の作成 / Creating Meeting Notes

1. 会議をクリックして詳細画面を開く
2. 「議事録」セクションに内容を入力
3. 「保存」をクリック

### コメント・質問の投稿 / Posting Comments/Questions

1. 会議詳細画面で、入力欄にテキストを入力
2. タイプを選択（メモ、質問、コメント）
3. 「送信」をクリック

### 検索 / Searching

1. 左サイドバーから「検索」を選択
2. キーワードを入力
3. オプションでタイプでフィルタリング
4. 「検索」をクリック

### 言語切り替え / Changing Language

右上の言語セレクタから日本語または英語を選択

## ファイル構成 / File Structure

```
/QA
├── appsscript.json      # GAS 設定ファイル
├── Code.js              # メインロジック（バックエンド）
├── index.html           # メインUI（HTML）
├── styles.html          # スタイル（CSS）
├── script.html          # クライアントスクリプト（JavaScript）
├── README.md            # このファイル
└── product-definitions/ # 製品定義書（QAボット・社内教育用データ）→ product-definitions/README.md
```

## Google Sheets 構造 / Google Sheets Structure

### Meetings シート
| 列 | 説明 |
|---|---|
| ID | 会議のユニークID |
| Title | 会議タイトル |
| Date | 会議日 |
| Description | 会議説明 |
| Participants | 参加者 |
| Notes | 議事録 |
| Created By | 作成者 |
| Created At | 作成日時 |
| Updated At | 更新日時 |
| Status | ステータス |

### Conversations シート
| 列 | 説明 |
|---|---|
| ID | コメントのユニークID |
| Meeting ID | 関連する会議ID |
| Type | タイプ（note/question/comment） |
| Author | 投稿者 |
| Content | 内容 |
| Timestamp | タイムスタンプ |
| Likes | いいねの数 |
| Status | ステータス |

### Users シート
| 列 | 説明 |
|---|---|
| Email | ユーザーメール |
| Name | ユーザー名 |
| Department | 部門 |
| Joined Date | 参加日 |
| Status | ステータス |

## デプロイ / Deployment

### Web App as Executing User

スクリプトをデプロイする際に、以下の設定で行うことをお勧めします：

- **実行**：このスクリプトを実行するユーザー
- **アクセス**：全員（認証が必要）

## トラブルシューティング / Troubleshooting

### 権限エラー / Permission Errors

Google Apps Script の初回実行時に、必要な権限の承認を行う必要があります。

### スプレッドシートの初期化に失敗

`initializeSheets()` 関数が正常に実行されていることを確認してください。

## ライセンス / License

MIT License

## サポート / Support

問題が発生した場合は、GitHub Issues で報告してください。

If you encounter any issues, please report them on GitHub Issues.

## 今後の改善予定 / Future Improvements

- [ ] AI による会議要約機能
- [ ] スマートフォンアプリ版
- [ ] メール通知機能
- [ ] 会議録音・文字起こし機能
- [ ] 組織内での権限管理

## 開発情報 / Development Info

- **ブランチ**：`claude/conversationqa-app-o9zwjz`
- **デプロイ先**：https://conversationqa.netlify.app/
