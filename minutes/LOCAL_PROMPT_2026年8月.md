# ローカルClaude Code用プロンプト（2026年8月分議事録）

以下をそのまま貼り付けてください。

---

品質管理部門の月次定例会議議事録の2026年8月分を作成してください。

作業ディレクトリ:
/Users/tsujinoyasumitsu/Library/Application Support/Claude/local-agent-mode-sessions/e091fe98-b9c2-4dab-8dc5-82ac12d44f15/f81027ba-a77b-46d6-9c63-f85e73a0b629/local_c056cbcc-72cc-4163-b763-05cd15f9511d/outputs/

まず HANDOFF_定例会議議事録作成_引き継ぎ資料.md を読み、create_minutes_july.py と 7月分 docx を確認してください。

## やること
1. create_minutes_july.py を create_minutes_august.py にコピーし、2026年7月 → 2026年8月 に置換（議題、概要、検索条件日付、xlsx名、集計表）。
2. 下記の収集済みデータを反映。
3. 集計進捗表を最新15ヶ月（2025/6〜2026/8）にスライド。2026/4 列は「XXX」のまま。
4. iCAS（1.苦情）と JAAME（8.PMDA、9.規格・法規制）は私が貼り付ける結果を反映。
5. 会議日時と文書番号（QM-500-0067_20YYMMDD00X）を私に確認。
6. 実行して docx を出力し、7月分と書式が揃っていることを確認。

## 収集済みデータ（2026年8月）

### 3. 文献検索
PubMed: (landmarker OR coDiagnostiX OR NobelClinician OR Simplant OR BlueSkyPlan OR RealGuide OR ImplantStudio) AND (("2026/08/01"[Date - Publication] : "2026/08/31"[Date - Publication]))
結果 2件（両方 Epub 日付、過去運用どおり計上）
- Davide Silvestri, "Standardized Digital Volumetric Evaluation of Removed Tooth Structure: A New Technique", Int J Prosthodont. 2026 Aug 20. doi:10.11607/ijp.9736, https://pubmed.ncbi.nlm.nih.gov/42629653/
  ※RealGuide 5.0 を歯冠形成量評価に使用（ガイドサージェリーではない。LANDmarker関連とするか要判断）
- Lina Maiza, "A Digital Stackable Guide Protocol for FP1 Full-Arch Esthetic Reconstruction With Monolithic Zirconia", J Esthet Restor Dent. 2026 Aug 26. doi:10.1111/jerd.70256, https://pubmed.ncbi.nlm.nih.gov/42644316/
  ※coDiagnostiX によるスタッカブルガイド症例報告（LANDmarker関連）
Google Scholar ("landmarker" dental implant, 2026): 顔ランドマーク推定と手指トラッキングのみ → 0件

### 7. FDA、EU
FDA TPLC (LLZ, 892.2050) 2026年8月掲載: FUJIFILM Healthcare Americas 8/26、Merge Healthcare 8/21・8/4 の3件。すべて歯科非関連 → 0件として記録。
ICIJ: クラウドから取得不可(403)。ローカルブラウザで再確認、無理なら過去実績どおり0件で仮置き＋注記。

### その他（既定値、要確認）
2.監査 0件、4.学会 0件、5.工程不具合 0件、6.アンケート 0件、10.CAPA 0件

### 未取得（私が貼り付けます）
- 1.苦情: iCAS 件数（iCAT製販合計、全製品合計、①〜⑨内訳）
- 8.PMDA: JAAME 回収（歯科で検索、LANDmarker非関連は「参考として記載」注釈）、安全性情報件数
- 9.規格・法規制: JAAME 法令通知（災害・海外情勢関連は除外）

## 参考
クラウド側の暫定版: GitHub cizeta-connectrum/qa ブランチ claude/exciting-mendel-ir9lgv の minutes/create_minutes_august.py。上記データ入力済み。書式は7月分スクリプトを正とすること。
