#!/usr/bin/env python3
"""books/ フォルダの .epub から本棚サイトを組み立てる。

使い方: python scripts/build.py <出力フォルダ>
  出力フォルダに、アプリ (index.html など)・books/・covers/・books.json を作ります。
"""
import hashlib
import json
import posixpath
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from html import unescape
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "books"
APP_DIR = ROOT / "app"

try:
    from PIL import Image
except ImportError:  # Pillow が無くても動く（表紙を縮小しないだけ）
    Image = None


def attr(el, name):
    m = re.search(r'\s' + name + r'\s*=\s*["\']([^"\']*)["\']', el, re.I)
    return m.group(1) if m else ""


def dc(opf, name):
    m = re.search(r'<dc:' + name + r'\b[^>]*>(.*?)</dc:' + name + r'>', opf, re.I | re.S)
    if not m:
        return ""
    text = re.sub(r'<!\[CDATA\[|\]\]>', '', m.group(1))
    return unescape(re.sub(r'<[^>]+>', '', text)).strip()


def read_epub(path):
    """タイトル・著者・表紙画像(bytes)を取り出す"""
    info = {"title": "", "author": "", "cover": None}
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        container = z.read("META-INF/container.xml").decode("utf-8", "replace")
        m = re.search(r'full-path\s*=\s*["\']([^"\']+)["\']', container)
        if not m or m.group(1) not in names:
            return info
        opf_path = m.group(1)
        opf = z.read(opf_path).decode("utf-8", "replace")
        base = posixpath.dirname(opf_path)
        info["title"] = dc(opf, "title")
        info["author"] = dc(opf, "creator")

        items = re.findall(r'<item\s[^>]*>', opf, re.I)
        href = ""
        for el in items:  # EPUB3
            if "cover-image" in attr(el, "properties").split():
                href = attr(el, "href")
                break
        if not href:  # EPUB2
            cover_id = ""
            for el in re.findall(r'<meta\s[^>]*>', opf, re.I):
                if attr(el, "name") == "cover":
                    cover_id = attr(el, "content")
            for el in items:
                if cover_id and attr(el, "id") == cover_id:
                    href = attr(el, "href")
                    break
        if not href:
            for el in items:
                if attr(el, "media-type").startswith("image/") and "cover" in (attr(el, "id") + attr(el, "href")).lower():
                    href = attr(el, "href")
                    break
        if href:
            p = posixpath.normpath(posixpath.join(base, unquote(href)))
            if p in names and not p.lower().endswith(".svg"):
                info["cover"] = z.read(p)
    return info


def save_cover(data, dest):
    if Image is None:
        dest.write_bytes(data)
        return
    img = Image.open(BytesIO(data))
    img = img.convert("RGB")
    img.thumbnail((360, 540))
    img.save(dest, "JPEG", quality=82, optimize=True)


def git_updated(path):
    """最後にコミットされた時刻（無ければファイルの更新時刻）"""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%ct", "--", str(path)], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        if out:
            return int(out) * 1000
    except Exception:
        pass
    return int(path.stat().st_mtime * 1000)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "_site_reader").resolve()
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(APP_DIR, out)
    (out / "books").mkdir()
    (out / "covers").mkdir()

    books = []
    for path in sorted(BOOKS_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() != ".epub":
            continue
        rel = path.relative_to(BOOKS_DIR).as_posix()
        digest = hashlib.sha1(path.read_bytes()).hexdigest()[:12]
        book_id = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:10]
        folder = path.parent.relative_to(BOOKS_DIR).as_posix()
        entry = {
            "id": book_id,
            "name": path.stem,
            "folder": "" if folder == "." else folder.replace("/", " / "),
            "file": "books/" + book_id + "-" + digest + ".epub",
            "size": path.stat().st_size,
            "updated": git_updated(path),
            "version": digest,
            "title": "",
            "author": "",
            "cover": "",
        }
        shutil.copy2(path, out / entry["file"])
        try:
            info = read_epub(path)
            entry["title"] = info["title"]
            entry["author"] = info["author"]
            if info["cover"]:
                cover = "covers/" + book_id + "-" + digest + ".jpg"
                save_cover(info["cover"], out / cover)
                entry["cover"] = cover
        except Exception as e:  # 壊れたEPUBでも一覧には出す
            print(f"警告: {rel} の情報を読めませんでした: {e}", file=sys.stderr)
        books.append(entry)
        print(f"  {rel}  →  {entry['title'] or entry['name']}")

    books.sort(key=lambda b: (b["folder"], b["name"]))
    manifest = {"generated": datetime.now(timezone.utc).isoformat(), "books": books}
    (out / "books.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(books)} 冊を {out} に書き出しました")


if __name__ == "__main__":
    main()
