#!/bin/sh
# src/page.html(본문) → index.html(GitHub Pages용 전체 문서)
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_templates.py >/dev/null
{
  printf '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  cat <<'META'
<meta property="og:type" content="website">
<meta property="og:site_name" content="무료아카데미월드">
<meta property="og:title" content="무료아카데미월드 | 학원 운영비 아끼는 무료 자료 모음">
<meta property="og:description" content="초·중·고 기출, 무료 문제은행, 약술형 논술, 사설 모의고사부터 관리 프로그램·세무·노무·지원금·운영 양식까지 전부 무료.">
<meta property="og:url" content="https://newclear2222-idea.github.io/Free-Academy/">
<meta property="og:image" content="https://newclear2222-idea.github.io/Free-Academy/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f4fd1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%231f4fd1'/%3E%3Ctext x='32' y='44' font-size='34' text-anchor='middle' fill='white' font-family='sans-serif' font-weight='700'%3E무%3C/text%3E%3C/svg%3E">
META
  sed -n '1,/<\/style>/p' src/page.html
  printf '</head>\n<body>\n'
  sed -n '/<\/style>/,$p' src/page.html | tail -n +2
  printf '</body>\n</html>\n'
} > index.html
echo "built index.html"
