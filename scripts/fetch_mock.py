#!/usr/bin/env python3
"""오르비의 사설 모의고사·N제 무료배포 글 목록을 모아 사이트에 넣는다.

파일은 받지 않는다. 제작자 대부분이 "교육 목적 사용 가능, 재배포 금지"로
배포하므로 제목·작성자·날짜·원문 링크만 모으고, 다운로드는 원문 글에서 한다.

  python3 scripts/fetch_mock.py              # 오르비에서 가져와 갱신
  python3 scripts/fetch_mock.py --html a.html # 저장한 목록 HTML로 파서 점검
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "mock-feed.json"
PAGE = ROOT / "src" / "page.html"
UA = "FreeAcademyWorld-feed/1.0 (+https://github.com/newclear2222-idea/Free-Academy)"
TAGS = ["무료배포", "무료 배포", "실모", "모의고사", "N제"]
PAGES = 2
KEEP = 300

WANT = re.compile(r"모의고사|모의평가|모고|실모|N제|문제지|시험지|하프|파이널|주간지|월간지")
FREE = re.compile(r"무료|배포|공유|나눔")
DROP = re.compile(r"판매|구매|할인|예약|이벤트|후기|질문|답지\s*있|구합|찾습|채점|등급컷|모집")

SUBJECTS = [
    ("통합", r"통합과학|통합사회|통과|통사"),
    ("국어", r"국어|언매|화작|문학|독서|비문학"),
    ("수학", r"수학|미적|확통|기하|수[12]|공통"),
    ("영어", r"영어"),
    ("한국사", r"한국사"),
    ("물리", r"물리|물1|물2"),
    ("화학", r"화학|화1|화2"),
    ("생명", r"생명|생1|생2|생물"),
    ("지구", r"지구|지1|지2"),
    ("사회", r"사문|사회문화|생윤|윤사|한지|세지|동아시아|세계사|정법|경제|사탐"),
]


def subject(title):
    title = re.sub(r"대학수학능력시험|수학능력", "", title)
    for name, pat in SUBJECTS:
        if re.search(pat, title):
            return name
    return "기타"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ko"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


POST = re.compile(r'href="(?:https?://orbi\.kr)?/(0\d{8,11})(?:/[^"]*)?"[^>]*>(.*?)</a>', re.S)
DATE = re.compile(r'title="@?(\d{4}-\d{2}-\d{2})[ T]\d{2}:\d{2}')
AUTHOR = re.compile(r'href="(?:https?://orbi\.kr)?/profile/\d+"[^>]*>(.*?)</a>', re.S)


def parse(page):
    """목록 HTML에서 (id, 제목, 작성자, 날짜)를 뽑는다. 글 하나는 <li> 하나."""
    out = []
    for chunk in re.split(r"<li[\s>]", page)[1:]:
        posts = [(i, text(t)) for i, t in POST.findall(chunk)]
        posts = [(i, t) for i, t in posts if t and not re.fullmatch(r"[\d/: ]+", t)]
        d = DATE.search(chunk)
        if not posts or not d:
            continue
        pid, title = posts[0]
        a = AUTHOR.search(chunk)
        out.append({"id": pid, "title": title, "author": text(a.group(1)) if a else "",
                    "date": d.group(1)})
    return out


def keep(item):
    t = item["title"]
    return WANT.search(t) and FREE.search(t) and not DROP.search(t)


def main():
    found = []
    if len(sys.argv) > 2 and sys.argv[1] == "--html":
        found = parse(Path(sys.argv[2]).read_text("utf-8"))
        for f in found:
            print(("O " if keep(f) else "  ") + f["date"], f["title"])
        return
    errors = 0
    for tag in TAGS:
        for n in range(1, PAGES + 1):
            url = f"https://orbi.kr/list/tag/{urllib.parse.quote(tag)}?page={n}"
            try:
                found += parse(fetch(url))
            except Exception as e:  # 한 페이지 실패는 건너뛴다
                errors += 1
                print("skip", url, e, file=sys.stderr)
            time.sleep(2)
    old = json.loads(DATA.read_text("utf-8")) if DATA.exists() else {"items": []}
    items = {i["id"]: i for i in old["items"]}
    added = 0
    for f in found:
        if keep(f) and f["id"] not in items:
            f["subject"] = subject(f["title"])
            items[f["id"]] = f
            added += 1
    print(f"parsed {len(found)}, added {added}, errors {errors}")
    if not found and errors:
        sys.exit("오르비에서 아무것도 받지 못했습니다")
    data = {"updated": time.strftime("%Y-%m-%d"),
            "items": sorted(items.values(), key=lambda i: (i["date"], i["id"]), reverse=True)[:KEEP]}
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", "utf-8")
    inject(data)


def inject(data):
    """src/page.html 의 MOCK 표시 사이에 최신 목록을 넣는다."""
    s = PAGE.read_text("utf-8")
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    s2 = re.sub(r"(/\*MOCK\*/).*?(/\*/MOCK\*/)", lambda m: m.group(1) + blob + m.group(2), s, flags=re.S)
    PAGE.write_text(s2, "utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--inject":
        inject(json.loads(DATA.read_text("utf-8")))
    else:
        main()
