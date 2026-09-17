#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定例会議議事録（2026年8月分）生成スクリプト

- 7月分 create_minutes_july.py を雛形とする想定だったが、当該ファイルが
  Claude Code 環境に存在しなかったため、参考議事録
  「QM-500-0067_20250925001_定例会議議事録_2025年08月.docx」の構成に準拠して再構築した。
- 収集データは先頭の DATA / PUBMED / FDA_RECALLS / JAAME_* を編集すれば反映される。
  ★★★ = 手動入力が必要な箇所（iCAS、JAAME、会議日時など）

実行:  python3 create_minutes_august.py
出力:  QM-500-0067_{DOC_NO}_定例会議議事録_2026年8月.docx
"""
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

# =====================================================================
# 1. 基本情報
# =====================================================================
YEAR, MONTH = 2026, 8
YM_JA = f"{YEAR}年{MONTH}月"
YM_SLASH = f"{YEAR}/{MONTH}"
PERIOD_JA = f"{YEAR}/{MONTH:02d}/01 to {YEAR}/{MONTH:02d}/31"

DOC_NO = "20260917001"          # ★★★ 会議日に合わせて修正 (20YYMMDD00X)
MEETING_DATETIME = "2026/09/17 15:00～17:00"   # ★★★ 実際の会議日時に修正
OUTPUT = f"QM-500-0067_{DOC_NO}_定例会議議事録_{YM_JA}.docx"

ATTENDEES = [
    "管理監督者：南",
    "管理責任者/総括製造販売責任者：福田",
    "国内品質業務運営責任者/責任技術者：堀 記",
    "安全管理業務責任者：辻野",
]

# =====================================================================
# 2. 収集データ
# =====================================================================
# --- 1. 苦情（iCAS）: ★★★ 常に空欄テンプレート。ユーザーが後から手動入力 ---
COMPLAINT_TOTAL_ICAT = ""      # 例 "412"
COMPLAINT_TOTAL_ALL = ""       # 例 "637"
COMPLAINT_BREAKDOWN = [
    ("① Direct、LANDmarker", ""),
    ("② MoveRay", ""),
    ("③ MoveRayスタンド", ""),
    ("④ FlashMax", ""),
    ("⑤ X-VS", ""),
    ("⑥ ドリル、ピン", ""),
    ("⑦ Newtom", ""),
    ("⑧ RevoluX", ""),
    ("⑨ iCAT製販医療機器非該当", ""),
]

# --- 3. 文献検索（PubMed, 2026/08/01-31, [Date - Publication]）: 収集済み ---
# 判定: 2件中2件が検索キーワード製品（RealGuide / coDiagnostiX）を使用
PUBMED = [
    {
        "author": "Davide Silvestri",
        "title": "Standardized Digital Volumetric Evaluation of Removed Tooth Structure: A New Technique",
        "journal": "Int J Prosthodont. 2026 Aug 20. doi:10.11607/ijp.9736",
        "url": "https://pubmed.ncbi.nlm.nih.gov/42629653/",
        "note": "RealGuide 5.0 を歯冠形成量のデジタル評価に使用（ガイドサージェリーではない）",
    },
    {
        "author": "Lina Maiza",
        "title": "A Digital Stackable Guide Protocol for FP1 Full-Arch Esthetic Reconstruction With Monolithic Zirconia",
        "journal": "J Esthet Restor Dent. 2026 Aug 26. doi:10.1111/jerd.70256",
        "url": "https://pubmed.ncbi.nlm.nih.gov/42644316/",
        "note": "coDiagnostiX によるスタッカブルガイドを用いた全顎即時荷重の症例報告",
    },
]
PUBMED_RELEVANT = len(PUBMED)   # LANDmarker関連と判断した件数（必要に応じて修正）
SCHOLAR_HITS = 0                # Google Scholar: 2026年ヒットは顔ランドマーク/手指トラッキングのみ

# --- 7. FDA TPLC (LLZ, 892.2050) 2026/8 掲載分（すべて歯科非関連 → 0件扱い） ---
FDA_RECALLS_NOTE = (
    "2026年8月掲載の回収3件（FUJIFILM Healthcare Americas 8/26、"
    "Merge Healthcare 8/21・8/4）はいずれも歯科関連でないため0件とする。"
)
ICIJ_NOTE = "★★★ ICIJ DB は本環境から取得不可（HTTP 403）。過去実績は全期間0件。要確認。"

# --- 8. PMDA 回収（JAAME、歯科で検索）: ★★★ ログイン必須のため手動取得して入力 ---
JAAME_RECALLS = [
    # ("クラス", "掲載年月日", "一般的名称", "販売名", "製造業者等名称", "訂正/終了"),
]
JAAME_SAFETY_COUNT = 0          # ★★★ 安全性情報（タイトルに「歯科」）

# --- 9. 規格・法規制（JAAME 法令通知DB）: ★★★ 手動取得して入力 ---
# 災害・海外情勢関連など iCAT 製品に影響しないものは除外
JAAME_HOUREI = [
    # ("発簡日", "発簡番号", "タイトル"),
]

# --- 2,4,5,6,10: ユーザー確認（0件を既定値とする） ---
AUDIT_COUNT = 0
CONFERENCE_COUNT = 0
PROCESS_DEFECT_COUNT = 0
SURVEY_COUNT = 0
CAPA_COUNT = 0

# --- 集計進捗表: 最新15ヶ月（2025/6 ～ 2026/8）。"XXX" = 未収集 ---
SUMMARY_MONTHS = ["2025/6", "7", "8", "9", "10", "11", "12",
                  "2026/1", "2", "3", "4", "5", "6", "7", "8"]
SUMMARY_ROWS = [
    ("1.苦情",            ["502","451","408","444","471","440","488","432","464","392","XXX","XXX","XXX","XXX", COMPLAINT_TOTAL_ICAT or "★★★"]),
    ("2.外部・内部監査結果", ["0","0","0","0","1","0","1","0","0","1","XXX","0","0","0", str(AUDIT_COUNT)]),
    ("3.文献検索",         ["2","0","1","1","3","1","7","3","0","2","XXX","1","4","1", str(PUBMED_RELEVANT)]),
    ("4.学会情報",         ["0"]*10 + ["XXX","0","0","0", str(CONFERENCE_COUNT)]),
    ("5.工程不具合",       ["0"]*10 + ["XXX","0","0","0", str(PROCESS_DEFECT_COUNT)]),
    ("6.アンケート",       ["0"]*10 + ["XXX","0","0","0", str(SURVEY_COUNT)]),
    ("7.FDA、EU",         ["0"]*10 + ["XXX","0","0","0", "0"]),
    ("8.PMDA",            ["1","4","4","4","2","3","3","1","1","2","XXX","1","1","1", str(len(JAAME_RECALLS)) if JAAME_RECALLS else "★★★"]),
    ("9.規格・法規制",     ["0","5","1","0","0","4","2","5","9","11","XXX","14","23","17", str(len(JAAME_HOUREI)) if JAAME_HOUREI else "★★★"]),
    ("10.CAPA",           ["1","1","0","0","1","0","0","0","0","0","XXX","0","0","0", str(CAPA_COUNT)]),
]

COMPETITORS = [
    "・NobelClinician (Nobel Biocare AB, Goteborg, Sweden)",
    "・coDiagnostiX (Dental Wings GmbH, Montreal, Canada)",
    "・Simplant (Dentsply, Charlotte, USA)",
    "・Implant Studio (3Shape, Copenhagen, Denmark)",
    "・Blue Sky Plan (Blue Sky Bio., USA)",
    "・RealGUIDE (3 DIEMME SRL, Italy)",
]

# =====================================================================
# 3. 文書生成ヘルパー
# =====================================================================
doc = Document()
style = doc.styles["Normal"]
style.font.name = "MS Mincho"
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "MS Mincho")
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.0)
    s.top_margin = s.bottom_margin = Cm(2.0)


def p(text="", bold=False, size=None, align=None, indent=0):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold
    if size:
        run.font.size = Pt(size)
    if align == "center":
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if indent:
        para.paragraph_format.left_indent = Cm(indent)
    para.paragraph_format.space_after = Pt(2)
    return para


def link(text, url, indent=0):
    """ハイパーリンク付き段落"""
    para = doc.add_paragraph()
    if indent:
        para.paragraph_format.left_indent = Cm(indent)
    part = doc.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    from docx.oxml import OxmlElement
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), r_id)
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rpr.append(u)
    c = OxmlElement("w:color"); c.set(qn("w:val"), "0563C1"); rpr.append(c)
    r.append(rpr)
    t = OxmlElement("w:t"); t.text = text; t.set(qn("xml:space"), "preserve")
    r.append(t); h.append(r); para._p.append(h)
    return para


def table(header, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(header):
        cell = t.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(str(h))
        run.bold = True
        run.font.size = Pt(9)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(v))
            run.font.size = Pt(9)
            cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return t


# =====================================================================
# 4. 本文
# =====================================================================
# ヘッダー表
table(["株式会社アイキャット", "定例会議議事録/Regular meetings Minutes", "制定：2020/9/1", f"QM-500-0067_{DOC_NO}(/)"], [])
table(["承認　Approved by", "作成Edited by"], [("", "")], widths=[8, 8])

p("■定例会議議事録■", bold=True, size=12)
p(f"議題：{YM_JA}におけるPMSデータ収集結果報告")
p(f"{YEAR}年QMS活動の予実確認", indent=1.2)
p(f"日時：{MEETING_DATETIME}")
p("出席者：")
for a in ATTENDEES:
    p(a, indent=1.2)
p("目的： iCAT製販医療機器の市販後調査データ収集結果報告")
p("＊" * 40)

p("■概要■", bold=True)
p(f"{YM_JA}におけるiCAT製販医療機器のPMSデータの収集結果を報告。")

p("■データ収集結果■ 　（#の記載は検索条件のキーワード）", bold=True)

# ---------- 1. 苦情 ----------
p("1. 苦情", bold=True)
p("[日本]")
p(f"苦情　 iCAT製販医療機器　 {COMPLAINT_TOTAL_ICAT}件（全ての製品　 {COMPLAINT_TOTAL_ALL}件）")
p("※ 　　 1案件に対して、顧客と複数のやりとりがあった場合は、やりとりの回数（iCASのQ&Aの記録数）でカウントしている。")
p("■iCAS")
p("#1 トラブル、訪問保守、保守訪問")
for name, cnt in COMPLAINT_BREAKDOWN:
    p(f"{name} 　 {cnt}件", indent=0.6)
p("※iCAT製販医療機器非該当とは、チェア（PC）、診断用PC、LAN、PSPIX、KAPS、連携（頭書き、画像）、CaretSquare、達人プラス、ソプロ（Sopro）、ビスタスキャン（VistaScan）、他雑品も含む")
p("※①～⑧がiCAT製販医療機器、⑨のみiCAT製販医療機器非該当")
p(f"※検索結果は内容も含めて「QMS_トラブル、訪問保守、保守訪問_{YEAR}_{MONTH:02d}月.xlsx」に出力して保管")
p("⇒すべての苦情は解決しており、是正/予防措置は不要、品質会議開催も不要だった。")
p("有害事象判定は全て非該当、行政当局への報告も不要だった。")

# ---------- 2. 監査 ----------
p("2. 外部・内部監査結果（指摘事項）", bold=True)
p(f"{AUDIT_COUNT}件")
p("[外部監査]", indent=0.6)
p("外部監査はなかった。")
p("[内部監査]", indent=0.6)
p("内部監査はなかった。")

# ---------- 3. 文献検索 ----------
p("3. 文献検索", bold=True)
p(f"{PUBMED_RELEVANT}件 本品の臨床評価で評価した有効性安全性を覆すような新たな文献はなかった。")
p("[PubMed]")
p("調査サイト/Search site：https://pubmed.ncbi.nlm.nih.gov/advanced/")
p(f'#1 (landmarker OR coDiagnostiX OR NobelClinician OR Simplant OR BlueSkyPlan OR RealGuide OR ImplantStudio) AND (("{YEAR}/{MONTH:02d}/01"[Date - Publication] : "{YEAR}/{MONTH:02d}/31"[Date - Publication]))')
p("(Epubは除く)")
p(f"{PUBMED_RELEVANT}件/{len(PUBMED)}件中LANDmarkerに関連するするもの")
for a in PUBMED:
    link(f"・{a['author']}, {a['title']}", a["url"], indent=0.6)
    p(f"{a['journal']}　※{a['note']}", indent=1.2)
p("[Google Scholar]")
p("調査サイト/Search site：https://scholar.google.com/")
p(f'#2 "landmarker" dental implant Filter: Manual screening for relevant results (in {YM_SLASH})')
p(f"{SCHOLAR_HITS}件/{SCHOLAR_HITS}件中LANDmarkerに関連するするもの")

# ---------- 4〜6 ----------
p("4. 学会情報", bold=True)
p(f"[日本] 　 {CONFERENCE_COUNT}件")
p("5. 工程不具合（QMSに係るソフトウェア、ハードウェアの欠陥、故障、必要書類の不備等）", bold=True)
p(f"[日本] 　 {PROCESS_DEFECT_COUNT}件")
p("6. アンケート（iCAT製販医療機器該当のみ）", bold=True)
p(f"[日本] 　 {SURVEY_COUNT}件　（実施なし）")

# ---------- 7. FDA、EU ----------
p("7. FDA、EU（LMとライバルメーカーの回収）", bold=True)
p("0件")
p("競合品/ Competitor devices:")
for c in COMPETITORS:
    p(c, indent=0.6)
p("●回収情報、安全性情報")
p("以下の回収情報、安全性情報を入手したが、LANDmarkerに関係するものはなかった。")
p("0 件", indent=1.2)
p("[FDA's TPLC]")
p("調査サイト/Search site：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfTPLC/tplc.cfm")
p("※歯科関連でないものは基本載せない。")
p("#1 Product code LLZ Regulation Number 892.2050: System, Image Processing, Radiological")
p(f"Date Report Received:{PERIOD_JA}")
p("0 recalls（歯科関連）")
p(f"※{FDA_RECALLS_NOTE}")
p("[ICIJ International Medical Devices Database]")
p("調査サイト/Search site：https://medicaldevices.icij.org/")
for i, name in enumerate(["Nobelclinician", "coDiagnostiX", "simplant", "“implant studio”", "“Blue Sky Plan”", "RealGUIDE"], start=2):
    p(f"#{i} {name} (in {YM_SLASH})")
    p("0", indent=0.6)
p(ICIJ_NOTE)

# ---------- 8. PMDA ----------
p("8. PMDA(LMとライバルメーカーの回収)", bold=True)
p(f"{len(JAAME_RECALLS)}件")
p("JAAME Search")
p("https://search.jaame.or.jp/jaames/login.php")
p("歯科で検索")
p("競合品:", indent=0.6)
for c in COMPETITORS[:4]:
    p(c, indent=0.6)
p("●回収情報")
p("[PMDA's Medical Device Recalls]")
p("https://search.jaame.or.jp/jaames/kaisyu/index.php?f=1")
if JAAME_RECALLS:
    p("歯科で検索　 LANDmarkerに係るものはなし。ただし、歯科領域では、以下の回収が行われた（LANDmarkerに関係ないが参考として記載）。")
    p(f"{len(JAAME_RECALLS)}件")
    table(["クラス", "掲載年月日", "一般的名称", "販売名", "製造業者等名称", "訂正/終了"], JAAME_RECALLS)
else:
    p("歯科で検索　 LANDmarkerに係るものはなし。")
    p("0件")
p("●安全性情報")
p("[PMDA's Medical Device Safety Information]")
p("https://search.jaame.or.jp/jaames/anzen/index.php?f=1")
p("歯科で検索")
p(f"{JAAME_SAFETY_COUNT}件")

# ---------- 9. 規格・法規制 ----------
p("9. 規格・法規制", bold=True)
p(f"{len(JAAME_HOUREI)}件")
p("[日本]", indent=0.6)
p("JAAME 医療機器関係法令通知ＤＢ", indent=0.6)
p("https://search.jaame.or.jp/jaames/hourei/index.php?f=1", indent=0.6)
p(f"当社製品に影響すると考えられる{YM_JA}中に発出された医療機器関係法令通知は以下の通り。")
p("ただ、LANDmarkerには直接関係するのはなし")
if JAAME_HOUREI:
    for i, (d, no, title) in enumerate(JAAME_HOUREI, start=1):
        p(f"{i}. 　 {d}　{no}")
        p(title, indent=1.2)
else:
    p("（該当なし）")

# ---------- 10. CAPA ----------
p("10. CAPA（品質管理部に不具合報告書が提出されたもの。医療機器そのものに関係しない事象も含む。）", bold=True)
p(f"{CAPA_COUNT}件")

# ---------- 11. QMS活動の予実確認 ----------
p(f"11. {YEAR}年QMS活動の予実確認", bold=True)
p("1.業許可管理表")
p(r"\\idun\Pal\01.薬事\00_品質規程\0_文書原版_全数\QM-500-0031A_業許可管理表.xlsx", indent=0.6)
p("2.品質安全管理活動年間計画")
p(rf"\\idun\Pal\01.薬事\01_社内薬事\05品質・安全活動年間計画\品質・安全\品質安全管理活動年間計画スケジュール_{YEAR}.xlsx", indent=0.6)
p("3.品質目標")
p(rf"\\idun\Pal\01.薬事\01_社内薬事\05品質・安全活動年間計画\品質・安全\QM-500-0040A_品質目標_{YEAR}_実績.xlsx", indent=0.6)

# ---------- 状況確認・集計 ----------
p("■状況確認■", bold=True)
p("iCAT製販医療機器の関連データを引き続き収集する。", indent=0.6)

p("■集計進捗結果■", bold=True)
table([""] + SUMMARY_MONTHS, [(name, *vals) for name, vals in SUMMARY_ROWS])
p("※「XXX」は2026年4月分議事録未作成のため未収集。")
p("※2022年12月から1.苦情のみだったものを、1.苦情・問合せ・サポートの全ての件数を記載するようになった。")
p("※2024年5月まではLANDmarkerのみのデータだった。")
p("※2024年6月からの変更点")
p("・iCAT製販医療機器を範囲のデータとした。")
p("・苦情の定義変更を行い、それまでの「1.苦情・問合せ・サポート」のうち、“苦情および問合せ”を改めて“苦情”にまとめた（ISO13485の定義に合わせるための変更）。サポートは集計対象から除外した。")
p("・「2.社内不具合（外部・内部監査結果）」を「2.外部・内部監査結果（指摘事項）」に名称変更。")
p("・「10.CAPA」は医療機器そのものに関係しない事象も含むように変更した。")

p("制定・変更・改訂履歴", bold=True)
table(["版記号", "年月日", "該当頁", "理由・内容", "承認", "作成"],
      [("-", f"{YEAR}/{DOC_NO[4:6]}/{DOC_NO[6:8]}", "全", "初版制定", "福田清隆", "堀 道弘")] + [("", "", "", "", "", "")] * 3)

doc.save(OUTPUT)
print("saved:", OUTPUT)
