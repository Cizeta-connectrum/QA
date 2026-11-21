#!/usr/bin/env bash
# Cloudflare Pages のビルドコマンド: bash scripts/cf-build.sh
# 出力先: _site
set -euo pipefail

if ! [[ "${READER_PATH:-}" =~ ^[A-Za-z0-9_-]{16,}$ ]]; then
  echo "エラー: Cloudflare Pages の環境変数 READER_PATH（16文字以上の英数字）を設定してください。README を参照。" >&2
  exit 1
fi

python3 -m pip install --quiet --disable-pip-version-check pillow \
  || echo "警告: Pillow を入れられませんでした（表紙は縮小せずに使います）"

rm -rf _site
mkdir -p _site
python3 scripts/build.py "_site/$READER_PATH"

# 秘密のURL以外では何も見せない
printf '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Not Found</title>\n' > _site/index.html
cp _site/index.html _site/404.html
printf 'User-agent: *\nDisallow: /\n' > _site/robots.txt
cat > _site/_headers <<'HEADERS'
/*
  X-Robots-Tag: noindex, nofollow
  Referrer-Policy: no-referrer
HEADERS
