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
<tr><th>학생 연락처</th><td colspan="3"></td></tr>
<tr><th>학교·학년</th><td colspan="3">________ 학교 ____학년</td></tr>
<tr><th>주소</th><td colspan="3"></td></tr>
<tr><th>보호자 연락처</th><td colspan="3"></td></tr>
<tr><th>알게 된 경로</th><td colspan="3">□ 지인 □ 블로그 □ 지도 □ 전단 □ 기타</td></tr>
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

# 9. 강사 계약서 (근로계약서 + 프리랜서 위촉계약서)
CONTRACT_CSS = """
<style>
.art { margin:10px 0; }
.art b { display:block; margin-bottom:2px; }
.art p { margin:2px 0 2px 1em; }
.pb { page-break-before: always; break-before: page; margin-top:28px; border-top:2px dashed var(--line); padding-top:20px; }
.parties { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:18px; }
.parties table th { width:30%; }
.tip { background:var(--soft); padding:8px 10px; font-size:12px; color:var(--muted); margin:10px 0; }
@media print { .pb { border-top:none; margin-top:0; padding-top:0; } .tip { display:none; } }
@media (max-width:640px) { .parties { grid-template-columns:1fr; } }
</style>
"""

PARTIES = lambda a, b: f"""
<div class="parties">
<table><tr><th colspan="2">{a}</th></tr>
<tr><th>학원명</th><td></td></tr><tr><th>주소</th><td></td></tr><tr><th>대표자</th><td style="text-align:right">(서명)</td></tr><tr><th>연락처</th><td></td></tr></table>
<table><tr><th colspan="2">{b}</th></tr>
<tr><th>성명</th><td></td></tr><tr><th>주소</th><td></td></tr><tr><th>연락처</th><td></td></tr><tr><th>서명</th><td style="text-align:right">(서명)</td></tr></table>
</div>"""

T["teacher-contract.html"] = page("학원 강사 계약서", CONTRACT_CSS + """
<p class="tip">이 파일에는 두 가지 계약서가 들어 있습니다. 출퇴근 시간과 업무를 학원이 정하고 지시하면 <b>① 근로계약서</b>, 강사가 수업 방식과 시간을 스스로 정하고 강의료를 받는 경우 <b>② 프리랜서(위촉) 계약서</b>를 씁니다. 이름만 프리랜서여도 실제로 출퇴근·업무 지시를 받으면 근로자로 판단되어 퇴직금·4대보험 의무가 생길 수 있습니다. 필요 없는 쪽은 인쇄 범위에서 빼세요.</p>

<h1>강사 근로계약서</h1>
<p class="sub">고용노동부 표준근로계약서(근로기준법 제17조 필수 기재사항) 기준 · 학원 강사용</p>
<p>________________ 학원(이하 "학원")과 ________________ (이하 "강사")은 다음과 같이 근로계약을 맺는다.</p>

<div class="art"><b>제1조 (근로계약기간)</b>
<p>20___년 ___월 ___일부터 20___년 ___월 ___일까지 (기간을 정하지 않는 경우 근로개시일만 적음)</p>
<p>수습기간: □ 없음 □ ___개월 (수습기간 중 임금은 ________)</p></div>

<div class="art"><b>제2조 (근무 장소와 업무)</b>
<p>근무 장소: ________________ 학원</p>
<p>업무 내용: ________ 과목 수업, 수업 준비, 학생 학습 관리 및 상담, 그 밖에 이에 딸린 업무</p></div>

<div class="art"><b>제3조 (근로시간과 휴게)</b>
<p>근로시간: ___시 ___분 ~ ___시 ___분 (1일 ___시간, 1주 ___시간)</p>
<p>휴게시간: ___시 ___분 ~ ___시 ___분 (4시간마다 30분 이상)</p>
<p>근무 요일: 매주 □월 □화 □수 □목 □금 □토 □일</p>
<p>시험 기간 보강 등으로 연장근로가 필요한 경우 강사와 합의하여 정하며, 연장·야간·휴일근로는 근로기준법에 따라 가산하여 지급한다. (상시 5명 이상 사업장)</p></div>

<div class="art"><b>제4조 (휴일)</b>
<p>주휴일: 매주 ___요일 (1주 소정근로일을 개근하고 1주 15시간 이상 근무한 경우 유급)</p></div>

<div class="art"><b>제5조 (임금)</b>
<p>□ 월급 ____________원 □ 시급 ____________원 (최저임금 이상)</p>
<p>수당: ________________ (항목과 금액) &nbsp; 상여금: □ 없음 □ 있음 ________</p>
<p>임금 지급일: 매월 ___일 (휴일인 경우 전날 지급)</p>
<p>지급 방법: □ 강사 명의 예금통장 입금 □ 직접 지급</p></div>

<div class="art"><b>제6조 (연차유급휴가)</b>
<p>근로기준법에 따라 부여한다. (상시 5명 이상 사업장. 학원 방학 기간 등에 사용 시기를 협의할 수 있다)</p></div>

<div class="art"><b>제7조 (사회보험)</b>
<p>□ 고용보험 □ 산재보험 □ 국민연금 □ 건강보험</p></div>

<div class="art"><b>제8조 (채용 서류와 범죄경력 조회)</b>
<p>강사는 최종학력증명서를 제출하고, 학원이 「아동·청소년의 성보호에 관한 법률」과 「아동복지법」에 따라 성범죄경력 및 아동학대 범죄전력을 조회하는 데 동의한다.</p></div>

<div class="art"><b>제9조 (학생 정보 보호)</b>
<p>강사는 업무 중 알게 된 학생·보호자의 개인정보와 성적을 업무 외 목적으로 쓰거나 다른 사람에게 알리지 않으며, 퇴직할 때 관련 자료를 학원에 돌려준다.</p></div>

<div class="art"><b>제10조 (퇴직)</b>
<p>강사가 퇴직하려는 경우 수업 인수인계를 위해 30일 전까지 학원에 알리도록 노력한다. 1년 이상 근무하고 4주 평균 1주 15시간 이상 일한 경우 퇴직금을 퇴직일부터 14일 이내 지급한다.</p></div>

<div class="art"><b>제11조 (계약서 교부와 기타)</b>
<p>학원은 이 계약을 맺을 때 계약서 사본을 강사에게 준다. 이 계약에 정하지 않은 사항은 근로기준법과 학원 취업규칙에 따른다.</p>
<p class="note">위약금이나 손해배상액을 미리 정하는 조항(예: "중도 퇴사 시 ○개월분 배상")은 근로기준법 제20조에 따라 넣을 수 없습니다.</p></div>

<p style="text-align:right;margin-top:14px">20___년 ___월 ___일</p>
""" + PARTIES("학원 (사용자)", "강사 (근로자)") + """

<div class="pb">
<h1>프리랜서 강사 위촉 계약서</h1>
<p class="sub">사업소득(3.3% 원천징수) 강사용</p>
<p>________________ 학원(이하 "학원")과 ________________ (이하 "강사")은 다음과 같이 강의 위촉 계약을 맺는다.</p>

<div class="art"><b>제1조 (위촉 업무)</b>
<p>강사는 학원의 ________ 과목 (대상: ________ 반) 강의를 맡는다. 강의 내용과 진행 방식은 학원의 교육과정 범위 안에서 강사가 정한다.</p></div>

<div class="art"><b>제2조 (계약기간)</b>
<p>20___년 ___월 ___일부터 20___년 ___월 ___일까지. 기간이 끝나기 30일 전까지 어느 쪽도 해지 의사를 밝히지 않으면 같은 조건으로 ___개월 연장된 것으로 본다.</p></div>

<div class="art"><b>제3조 (강의 일정)</b>
<p>강의 요일과 시간은 학원과 강사가 협의하여 정한다: ________________</p></div>

<div class="art"><b>제4조 (강의료)</b>
<p>□ 시간당 ____________원 × 실제 강의 시간</p>
<p>□ 수강료 수입의 ____% (산정 기준: 해당 월 실제 수납액)</p>
<p>□ 월 고정 ____________원</p>
<p>지급일: 매월 ___일, 강사 명의 계좌로 지급한다. 학원은 소득세법에 따라 사업소득세 3%와 지방소득세 0.3%를 원천징수하여 신고·납부한다.</p></div>

<div class="art"><b>제5조 (보강과 휴강)</b>
<p>강사 사정으로 휴강하는 경우 미리 학원에 알리고 보강 일정을 협의한다. 학원 사정으로 휴강한 경우의 강의료 처리: ________________</p></div>

<div class="art"><b>제6조 (채용 서류와 범죄경력 조회)</b>
<p>강사는 최종학력증명서를 제출하고, 학원이 관계 법령에 따라 성범죄경력 및 아동학대 범죄전력을 조회하는 데 동의한다. 학원은 위촉일부터 15일 이내 교육지원청에 강사로 등록한다.</p></div>

<div class="art"><b>제7조 (학생 정보 보호)</b>
<p>강사는 업무 중 알게 된 학생·보호자의 개인정보와 성적을 강의 외 목적으로 쓰거나 다른 사람에게 알리지 않으며, 계약이 끝나면 관련 자료를 학원에 돌려준다.</p></div>

<div class="art"><b>제8조 (계약 해지)</b>
<p>어느 한쪽이 계약을 끝내려면 수업 인수인계를 위해 30일 전까지 상대방에게 알린다. 다만 상대방이 이 계약을 중대하게 위반한 경우에는 바로 해지할 수 있다.</p></div>

<div class="art"><b>제9조 (기타)</b>
<p>이 계약에 정하지 않은 사항은 학원과 강사가 협의하여 정하고, 협의가 안 되면 관계 법령과 일반 관례에 따른다.</p></div>

<p style="text-align:right;margin-top:14px">20___년 ___월 ___일</p>
""" + PARTIES("학원 (위촉인)", "강사 (수탁인)") + """
</div>
""", "근로기준법 제17조·제20조, 고용노동부 표준근로계약서(2025), 소득세법 제127조, 아동·청소년의 성보호에 관한 법률 제56조, 아동복지법 제29조의3")


for name, html in T.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)

print("written:", sorted(os.listdir(OUT)))
