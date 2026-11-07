#!/bin/sh
# src/page.html(본문) → index.html(GitHub Pages용 전체 문서)
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_templates.py >/dev/null
{
  printf '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  sed -n '1,/<\/style>/p' src/page.html
  printf '</head>\n<body>\n'
  sed -n '/<\/style>/,$p' src/page.html | tail -n +2
  printf '</body>\n</html>\n'
} > index.html
echo "built index.html"
