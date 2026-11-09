# 무료아카데미월드

학원을 열거나 운영하는 원장님이 돈 안 들이고 쓸 수 있는 것을 모은 정적 웹사이트입니다.

- **사설 모의고사 무료배포 새 글**: 오르비 무료배포 글의 제목·작성자·날짜·원문 링크 목록(`data/mock-feed.json`). 제작자 대부분이 재배포를 금지하므로 파일은 받지 않습니다. 오르비가 GitHub Actions 같은 서버 접속을 막아서(403) 자동 수집은 국내 PC에서 `python3 scripts/fetch_mock.py && sh scripts/build.sh`로 돌립니다.
- **바로 쓰는 양식** (`templates/`): 교습비등 반환기준 게시표, 교습비등 게시표, 강사 게시표, 원생 등록·상담 카드, 강사 계약서(근로·프리랜서), 해고 통지서, 퇴직금 정산 확인서, 재원·교육비 납입 증명서, 강사 채용 체크리스트, 원장 연간 행정·세무 일정. 브라우저에서 바로 입력하고 인쇄/PDF 저장.
- **교습비 환불 계산기**: 학원법 시행령 [별표 4] 기준.
- **무료 자료 링크**: 무료 학원 관리 프로그램, 교육청·법정 의무, 세무·회계, 인사·노무, 지원금·무료 컨설팅, 홍보·디자인, 학부모 소통·사무, 수업 준비, 무료 AI.

## 구성

- `src/page.html`: 사이트 본문 (자료 목록 `const R`, 양식 목록 `const FORMS`)
- `index.html`: `scripts/build.sh`로 생성하는 전체 문서 (직접 고치지 말고 src를 고친 뒤 빌드)
- `scripts/make_templates.py`: `templates/` 양식 생성

```sh
sh scripts/build.sh
```

## 자료 추가

`src/page.html`의 `const R` 배열에 한 줄을 넣고 빌드합니다.

```js
["분류ID", "이름", "운영 기관", "https://주소", "무엇을 할 수 있나", "아끼는 것", "free 또는 plan"]
```

분류ID: `erp` `admin` `tax` `labor` `fund` `class` `elem` `midexam` `highexam` `bank` `nonsul`

## 수록 원칙

- 평가원·교육청 기출 파일은 재배포하지 않고 공식 페이지로만 연결합니다 (대법원 2024. 7. 11. 선고 2021다272001 판결).
- 양식은 직접 작성했고, 반환기준표는 법령 원문입니다 (법령은 저작권 보호 대상 아님, 저작권법 제7조).

## GitHub Pages 배포

Settings → Pages → Branch: `main` / `(root)` 를 선택하면 `https://newclear2222-idea.github.io/Free-Academy/` 에 공개됩니다.
