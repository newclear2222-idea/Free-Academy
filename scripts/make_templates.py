"""학원 운영 양식(templates/)을 생성한다. python3 scripts/make_templates.py"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "templates")
os.makedirs(OUT, exist_ok=True)

CSS = """
:root { --ink:#1d2433; --muted:#5d6676; --line:#9aa3b2; --soft:#eef1f6; --pen:#1f4fd1; }
* { box-sizing:border-box; }
body { margin:0; background:#e9ecf1; color:var(--ink);
  font-family:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif; font-size:14px; line-height:1.55; }
.bar { position:sticky; top:0; background:#fff; border-bottom:1px solid #d5d9e0; padding:10px max(16px, env(safe-area-inset-left,0px));
  display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
.bar a, .bar button { font:inherit; font-size:13px; padding:6px 12px; border-radius:8px; border:1px solid #c7cdd6; background:#fff; color:var(--ink); text-decoration:none; cursor:pointer; }
.bar button { background:var(--ink); color:#fff; border-color:var(--ink); }
.bar span { color:var(--muted); font-size:13px; }
.sheet { background:#fff; width:210mm; max-width:calc(100% - 32px); min-height:297mm; margin:20px auto; padding:16mm 15mm; box-shadow:0 1px 4px rgba(0,0,0,.12); }
h1 { font-size:22px; margin:0 0 4px; text-align:center; letter-spacing:.02em; }
.sub { text-align:center; color:var(--muted); font-size:12px; margin:0 0 14px; }
h2 { font-size:15px; margin:18px 0 6px; }
table { width:100%; border-collapse:collapse; margin:6px 0; table-layout:fixed; }
th, td { border:1px solid var(--line); padding:7px 8px; vertical-align:top; word-break:keep-all; overflow-wrap:anywhere; }
th { background:var(--soft); font-weight:600; text-align:center; }
td.blank { height:30px; }
.tall td { height:42px; }
.note { font-size:12px; color:var(--muted); }
.sign { margin-top:22px; display:grid; gap:10px; justify-items:end; }
.check li { list-style:none; margin:4px 0; }
.check li::before { content:"□ "; }
ul.check { padding-left:4px; }
.wrapx { overflow-x:auto; }
@media print {
  body { background:#fff; }
  .bar { display:none; }
  .sheet { box-shadow:none; margin:0; width:auto; max-width:none; min-height:0; padding:0; }
  @page { size:A4; margin:14mm; }
}
"""

def page(title, body, source=""):
    src = f'<p class="note">근거: {source}</p>' if source else ""
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;600&display=swap">
<style>{CSS}</style></head>
<body>
<div class="bar"><a href="../index.html">← 무료아카데미월드</a><button type="button" onclick="window.print()">인쇄 / PDF로 저장</button>
<span>칸을 눌러 바로 입력한 뒤 인쇄할 수 있습니다. 학원명 등은 직접 고쳐 쓰세요.</span></div>
<div class="sheet" contenteditable="true" spellcheck="false">
{body}
{src}
<p class="note">무료아카데미월드 제공 양식 · 자유롭게 고쳐 쓰고 인쇄해 사용하세요. 법령은 바뀔 수 있으니 관할 교육지원청 안내를 함께 확인하세요.</p>
</div>
</body></html>
"""

def blanks(cols, rows):
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join("<tr>" + "".join('<td class="blank"></td>' for _ in cols) + "</tr>" for _ in range(rows))
    return f'<div class="wrapx"><table><tr>{head}</tr>{body}</table></div>'

T = {}

# 1. 교습비등 반환기준 게시표 (학원법 시행령 별표 4) — 법령은 저작권 보호 대상이 아님(저작권법 제7조)
T["refund-standard.html"] = page("교습비등 반환기준 게시표", """
<h1>교습비등 반환기준</h1>
<p class="sub">「학원의 설립·운영 및 과외교습에 관한 법률 시행령」 제18조 및 [별표 4] · 학습자가 잘 보이는 곳에 게시</p>
<table>
<tr><th style="width:26%">반환사유</th><th style="width:22%">반환사유 발생일</th><th colspan="2">반환금액</th></tr>
<tr><td>학습자가 학원으로부터 격리된 경우 (감염병 등)</td><td>격리된 날</td>
<td colspan="2">이미 납부한 교습비등 − (일할 계산한 금액 × 교습 시작일부터 격리된 날 전날까지의 일수)</td></tr>
<tr><td>학원의 등록 말소, 교습정지, 학원이 교습을 할 수 없게 된 경우</td><td>교습을 할 수 없게 된 날</td>
<td colspan="2">이미 납부한 교습비등 − (일할 계산한 금액 × 교습 시작일부터 교습을 할 수 없게 된 날 전날까지의 일수)</td></tr>
<tr><td rowspan="4">학습자 본인의 의사로 수강을 포기한 경우<br><b>교습기간 1개월 이내</b></td><td rowspan="4">수강을 포기한 날</td>
<td style="width:30%">교습 시작 전</td><td>이미 납부한 교습비등 <b>전액</b></td></tr>
<tr><td>총 교습시간의 1/3 경과 전</td><td>이미 납부한 교습비등의 <b>2/3</b></td></tr>
<tr><td>총 교습시간의 1/3 경과 후 ~ 1/2 경과 전</td><td>이미 납부한 교습비등의 <b>1/2</b></td></tr>
<tr><td>총 교습시간의 1/2 경과 후</td><td>반환하지 않음</td></tr>
<tr><td rowspan="2">학습자 본인의 의사로 수강을 포기한 경우<br><b>교습기간 1개월 초과</b></td><td rowspan="2">수강을 포기한 날</td>
<td>교습 시작 전</td><td>이미 납부한 교습비등 <b>전액</b></td></tr>
<tr><td>교습 시작 후</td><td>반환사유가 생긴 달의 반환액(1개월 이내 기준으로 계산) + 나머지 달의 교습비등 <b>전액</b></td></tr>
</table>
<ul class="note">
<li>총 교습시간은 교습기간 중의 총 교습시간이며, 반환금액은 반환사유가 생긴 날까지 지난 교습시간을 기준으로 계산합니다.</li>
<li>원격교습은 실제 수강한 부분(인터넷 수강·학습기기 저장분)에 해당하는 금액을 뺀 금액을 반환합니다.</li>
<li>반환사유가 생긴 날부터 <b>5일 이내</b>에 반환해야 합니다. 반환하지 않으면 300만원 이하 과태료 대상입니다.</li>
</ul>
<div class="sign"><div>학원명: ______________________ &nbsp; 설립·운영자: ____________ (인)</div></div>
""", "학원법 시행령 제18조, [별표 4] 교습비등 반환기준 (국가법령정보센터 law.go.kr)")

# 2. 교습비등 게시표
T["tuition-board.html"] = page("교습비등 게시표", """
<h1>교습비등 게시표</h1>
<p class="sub">교육지원청에 등록(신고)한 금액과 같게 적고 학원 안 잘 보이는 곳에 게시합니다.</p>
<table><tr><th style="width:22%">학원명</th><td></td><th style="width:18%">등록번호</th><td></td></tr></table>
<div class="wrapx"><table class="tall">
<tr><th>교습과정</th><th>교습과목</th><th>정원</th><th>교습기간</th><th>총 교습시간(분)</th><th>교습비</th><th colspan="4">기타경비</th><th>합계</th></tr>
<tr><th></th><th></th><th></th><th></th><th></th><th></th><th>모의고사비</th><th>재료비</th><th>피복비</th><th>급식비·기숙사비·차량비</th><th></th></tr>
""" + "".join("<tr>" + "<td></td>"*11 + "</tr>" for _ in range(9)) + """
</table></div>
<ul class="note">
<li>기타경비는 학원법 시행령 [별표 1]에 정한 항목(모의고사비, 재료비, 피복비, 급식비, 기숙사비, 차량비)만 받을 수 있습니다.</li>
<li>등록한 금액을 넘겨 받거나, 게시하지 않으면 행정처분·과태료 대상입니다. 교습비를 바꿀 때는 교육지원청에 먼저 변경 등록하세요.</li>
</ul>
""", "학원법 제15조, 시행령 제3조의2 [별표 1]")

# 3. 강사 게시표
T["teacher-board.html"] = page("강사 게시표", """
<h1>강사 게시표</h1>
<p class="sub">학원에 근무하는 강사의 인적사항을 학습자가 보기 쉬운 곳에 게시합니다.</p>
""" + blanks(["연번", "성명", "담당 과목", "최종 학력(학교·전공)", "채용일", "교육청 등록일"], 12) + """
<ul class="note"><li>강사를 채용·해임하면 15일 이내에 교육지원청에 등록·통보해야 합니다 (나이스 학원민원서비스에서 온라인 신고 가능).</li>
<li>원장이 직접 강의하는 경우에도 강사로 등록해야 합니다.</li></ul>
""", "학원법 제13조, 시행령 제12조, 시·도 학원 조례")

# 4. 수강 등록 신청서 (원생 등록 카드)
ENROLL_CSS = """
<style>
.ehead { display:grid; grid-template-columns: 1fr 30mm; gap:10px; align-items:stretch; }
.photo { border:1px dashed var(--line); display:grid; place-items:center; color:var(--muted); font-size:12px; min-height:38mm; text-align:center; }
.two { display:grid; grid-template-columns: 1fr 1fr; gap:10px; }
.sec { display:flex; align-items:center; gap:8px; margin:16px 0 6px; }
.sec h2 { margin:0; }
.sec span { font-size:12px; color:var(--muted); }
td.c, th.c { text-align:center; }
.boxes { display:flex; flex-wrap:wrap; gap:4px 14px; }
.office { margin-top:14px; border:1.5px solid var(--ink); }
.office th { background:#dfe4ec; }
@media (max-width:640px) { .ehead, .two { grid-template-columns: 1fr; } .photo { min-height:24mm; } }
</style>
"""

def score_rows(n):
    return "".join("<tr>" + '<td class="blank"></td>' * 7 + "</tr>" for _ in range(n))

T["enroll-form.html"] = page("수강 등록 신청서", ENROLL_CSS + """
<h1>원생 등록·상담 카드</h1>
<p class="sub">______________ 학원 · 등록번호 ________ · 담당 강사 ________</p>

<table>
<tr><th style="width:17%">학생 이름</th><td></td><th style="width:17%">성별</th><td>□ 남 □ 여</td></tr>
<tr><th>생년월일</th><td></td><th>학생 연락처</th><td></td></tr>
<tr><th>학교·학년</th><td colspan="3">________ 학교 ____학년</td></tr>
<tr><th>주소</th><td colspan="3"></td></tr>
<tr><th>보호자 연락처</th><td colspan="3"></td></tr>
<tr><th>비상 연락처</th><td></td><th>알게 된 경로</th><td>□ 지인 □ 블로그 □ 지도 □ 전단 □ 기타</td></tr>
</table>

<table style="margin-top:10px">
<tr><th style="width:17%">학교 시험 점수</th><td style="height:44px"></td></tr>
<tr><th>입학 테스트 점수</th><td style="height:44px"></td></tr>
</table>

<div class="sec"><h2>특이사항</h2></div>
<table>
<tr><th style="width:20%">학습 성향</th><td><div class="boxes"><span>□ 꼼꼼함</span><span>□ 빠르지만 실수 많음</span><span>□ 질문을 잘 함</span><span>□ 집중 시간 짧음</span><span>□ 숙제 관리 필요</span></div></td></tr>
<tr><th>목표</th><td>□ 내신 □ 수능·모의고사 □ 선행 □ 기초 보충 □ 특목·자사고 □ 기타 ______ &nbsp; 목표 점수·등급: ______</td></tr>
<tr><th>이전 학원 / 과외</th><td>기관 ________ · 기간 ________ · 그만둔 이유 ________________</td></tr>
<tr><th>건강·알레르기</th><td>□ 없음 □ 있음: ________________ (복용 약, 주의할 점)</td></tr>
<tr><th>등하원</th><td>□ 혼자 □ 보호자 픽업 □ 학원 차량 (탑승 위치: ________) · 형제자매 재원: □ 없음 □ 있음 ______</td></tr>
<tr><th>보호자 요청</th><td style="height:46px"></td></tr>
<tr><th>상담자 메모</th><td style="height:46px"></td></tr>
</table>

<div class="sec"><h2>희망 수업</h2></div>
<table>
<tr><th style="width:17%">희망 과목·반</th><td></td><th style="width:17%">희망 요일·시간</th><td></td></tr>
<tr><th>수업 시작 예정일</th><td></td><th>상담자</th><td></td></tr>
</table>

<table class="office">
<tr><th colspan="6">학원 기록란</th></tr>
<tr><th>상담일</th><td></td><th>등록일</th><td></td><th>첫 수업일</th><td></td></tr>
<tr><th>관리 프로그램 등록</th><td>□ 완료</td><th>교재 지급</th><td>□ 완료</td><th>학부모 안내</th><td>□ 완료</td></tr>
</table>
""")

# 7. 강사 채용 체크리스트
T["hiring-checklist.html"] = page("강사 채용 체크리스트", """
<h1>강사 채용 체크리스트</h1>
<p class="sub">빠뜨리면 과태료가 나오는 항목 위주로 정리했습니다.</p>
<table><tr><th style="width:18%">강사 이름</th><td></td><th style="width:18%">채용 예정일</th><td></td></tr></table>
<h2>채용 전</h2>
<ul class="check">
<li>자격 확인: 전문대 졸업 이상 또는 4년제 대학 2년 이상 수료 (재학·휴학증명서 불가)</li>
<li>최종학력증명서 받기 (졸업장 말고 증명서, 발급 3개월 이내)</li>
<li>성범죄경력 및 아동학대 범죄전력 조회 회신서 받기 (경찰청 범죄경력회보서 발급시스템 crims.police.go.kr 또는 관할 경찰서, 무료)</li>
<li>채용일은 범죄경력 조회일 이후로 잡기 (조회일 이전 날짜로 채용 불가)</li>
</ul>
<p class="note">성범죄경력 미조회 1차 과태료 300만원, 아동학대 범죄전력 미조회 1차 250만원.</p>
<h2>채용할 때</h2>
<ul class="check">
<li>근로계약서 작성·교부 (고용노동부 표준근로계약서) 또는 프리랜서(사업소득 3.3%) 계약서 작성</li>
<li>근로자라면 4대보험 취득 신고 (입사일 다음 달 15일까지), 두루누리 지원 대상인지 확인</li>
<li>프리랜서라면 매월 원천징수(3.3%) 신고·납부 일정 등록</li>
</ul>
<h2>채용 후 15일 이내</h2>
<ul class="check">
<li>교육지원청에 강사 채용 등록 (나이스 학원민원서비스 hakwon.neis.go.kr 온라인 가능)</li>
<li>강사 게시표에 이름·과목·학력 추가</li>
<li>올해 아동학대 신고의무자 교육(1시간 이상, 무료 온라인) 이수 안내</li>
</ul>
<h2>퇴사할 때</h2>
<ul class="check">
<li>해임일부터 15일 이내 교육지원청에 해임 통보</li>
<li>4대보험 상실 신고, 퇴직금(1년 이상 근무, 주 15시간 이상) 14일 이내 지급</li>
<li>강사 게시표에서 삭제</li>
</ul>
""", "학원법 시행령 제12조 [별표 3], 아동·청소년의 성보호에 관한 법률 제56조, 아동복지법 제29조의3, 근로기준법 제17조")

# 8. 원장 연간 일정
T["yearly-calendar.html"] = page("원장 연간 행정·세무 일정", """
<h1>원장 연간 행정·세무 일정</h1>
<p class="sub">개인사업자 학원(부가가치세 면세) 기준 · 기한이 주말·공휴일이면 다음 날까지</p>
<div class="wrapx"><table>
<tr><th style="width:16%">시기</th><th style="width:34%">할 일</th><th>메모</th></tr>
<tr><td>매월 10일</td><td>원천세 신고·납부 (강사 급여·3.3% 사업소득)</td><td>홈택스. 반기 납부 승인 사업장은 1월·7월</td></tr>
<tr><td>매월 10일</td><td>4대보험료 납부</td><td>두루누리 지원은 기한 내 완납해야 다음 달 차감</td></tr>
<tr><td>매월 말일</td><td>사업소득 간이지급명세서 제출 (프리랜서 강사)</td><td>홈택스</td></tr>
<tr><td>1월 16일~31일</td><td>등록면허세(면허분) 정기분 납부</td><td>위택스. 납부 내역은 나이스 학원민원서비스에 등록</td></tr>
<tr><td>2월 10일</td><td>면세사업자 사업장현황신고</td><td>전년도 수입금액 신고. 홈택스 신고도움 서비스 이용</td></tr>
<tr><td>3월 10일</td><td>근로소득 연말정산, 지급명세서 제출</td><td>근로자 강사·직원이 있는 경우</td></tr>
<tr><td>5월 31일</td><td>종합소득세 신고·납부</td><td>성실신고확인 대상은 6월 30일</td></tr>
<tr><td>11월 30일</td><td>종합소득세 중간예납</td><td>국세청 고지서 확인</td></tr>
<tr><td>12월 31일까지</td><td>아동학대 신고의무자 교육 (매년 1시간 이상)</td><td>원장·강사·직원 모두. 미실시 시 과태료</td></tr>
<tr><td>연중 수시</td><td>강사 채용·해임 15일 이내 신고</td><td>나이스 학원민원서비스</td></tr>
<tr><td>연중 수시</td><td>교습비 변경 시 교육지원청에 먼저 변경 등록</td><td>방학 특강도 교습과정·교습비 등록 필요</td></tr>
<tr><td>연중 수시</td><td>현금 10만원 이상 받으면 현금영수증 발급</td><td>학원은 의무발행업종. 미발급 시 20% 가산세</td></tr>
<tr><td>보험 만기 전</td><td>학원 배상책임보험 갱신, 교육청에 가입 내역 등록</td><td>미가입 시 행정처분</td></tr>
</table></div>
<h2>우리 학원 메모</h2>
<table><tr><td style="height:90px"></td></tr></table>
""", "국세청 신고 안내, 학원법, 아동복지법 제26조. 세부 기한은 해마다 국세청·교육청 공지로 확인")

for name, html in T.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)

print("written:", sorted(os.listdir(OUT)))
