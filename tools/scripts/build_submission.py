#!/usr/bin/env python3
"""Reduce the 19-slide master (docs/index.html) to a 9-slide submission deck, in place.

  build_submission.py control   robot arm: overview / pose (ROS2, FK, IK) / position; then mobile robot, PLC
  build_submission.py vision    robot arm: overview / position / inspection + model; then walking aid, knock research

Run on a copy of the master deck.
"""
import re
import sys
VARIANT = sys.argv[1] if len(sys.argv) > 1 else 'control'
assert VARIANT in ('control', 'vision'), VARIANT
from pathlib import Path
P = Path(__file__).resolve().parents[2] / 'docs' / 'index.html'
t = P.read_text()
arts = re.findall(r'<article.*?</article>', t, flags=re.S)
assert len(arts) == 19, len(arts)
head, tail = t[:t.index('<section class="page-shell"')], t[t.rindex('</section></main>'):]
A = {re.search(r' id="([^"]+)"', a).group(1): a for a in arts}

def rep(key, old, new):
    assert A[key].count(old) == 1, (key, old, A[key].count(old))
    A[key] = A[key].replace(old, new)

def body_of(key):
    return re.search(r'<div class="slide-body">.*</div>\s*(?=<footer)', A[key], flags=re.S).group(0)

# --- cover: short introduction only, skills in even rows
rep('profile', '<p class="hero-line">설계부터 구현, 디버깅까지<br/>어느 단계도 가볍게 넘기지 않습니다</p>',
    '<p class="hero-line">펌웨어부터 로봇팔 제어까지<br/>어느 단계도 가볍게 넘기지 않습니다</p>' if VARIANT == 'control' else
    '<p class="hero-line">데이터 준비부터 모델 실행까지<br/>어느 단계도 가볍게 넘기지 않습니다</p>')
# education: status badge first, then the dates
for _old, _st, _dt in [('<time>2026.04 – 2026.11 수료</time>', '수료', '2026.04 – 2026.11'),
                       ('<time>2026.02 졸업</time>', '졸업', '2019.03 – 2026.02'),
                       ('<time>2019.02 졸업</time>', '졸업', '2016.03 – 2019.02')]:
    rep('resume', _old, f'<time><span class="edu-state">{_st}</span>{_dt}</time>')
# submission copy: no contact line on the cover
_c = re.search(r'<div class="contact-links">.*?</div>', A['profile'], flags=re.S).group(0)
A['profile'] = A['profile'].replace(_c, '<p class="site-line"><a href="https://sditr0414.github.io/">포트폴리오 사이트<svg class="site-arrow" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 L12 4 M6 4 H12 V10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a></p>')
assert 'naver.com' not in A['profile']
rep('profile', '<p class="intro-label">로봇 제어 · 비전 · 임베디드 신입</p>',
    '<p class="intro-label">로봇 제어 · 임베디드 신입</p>' if VARIANT == 'control' else '<p class="intro-label">로봇 비전 · 제어 신입</p>')
rep('profile', '<p>C · C++<br/>STM32 · FreeRTOS · PLC</p>', '<p>C · C++ · STM32<br/>FreeRTOS · PLC</p>')
rep('profile', '<p>Python · ROS2<br/>OpenCV · YOLO · TFLite</p>', '<p>Python · ROS2 · OpenCV<br/>YOLO · TFLite</p>')

# --- robot arm (6 -> 3): overview / position / inspection + model
rep('opencv', '<div><dt>진행 상태</dt><dd>프로젝트 진행 중</dd></div>', '<div><dt>인식 대상</dt><dd>부품·지그 13종</dd></div>')
rep('opencv-locate', '>지그·팔레트 위치를 AI와 형상 검증으로 확정</h2>', '>AI 인식과 설계 형상 맞춤으로 지그·팔레트 위치 확정</h2>')
rep('opencv-locate', '<p class="deck">AI가 찾은 영역을 OpenCV·CAD 형상에 다시 맞춰, 위치·방향이 맞을 때만 채택합니다</p>',
    '<p class="deck">외곽선만으로는 가려진 팔레트를 놓쳐, AI가 찾은 영역을 설계 형상에 다시 맞추고 위치·방향이 맞을 때만 채택합니다</p>')
cards = re.search(r'<div class="s26-cards">.*?</div>(?=<table)', A['opencv-inspect'], flags=re.S).group(0)
table = re.search(r'<table class="s26-table">.*?</table>', A['opencv-inspect'], flags=re.S).group(0)
take = re.search(r'<p class="s26-take">.*?</p>', A['opencv-inspect'], flags=re.S).group(0)
guifig = re.search(r'<figure class="system-figure figure-board"><div class="inline-demo">.*?</figure>', A['opencv-inspect'], flags=re.S).group(0)
logfig = re.search(r'<figure class="s26-fig figure-board">.*?</figure>', A['opencv-log'], flags=re.S).group(0)
A['opencv-inspect'] = A['opencv-inspect'].replace(body_of('opencv-inspect'),
    '<div class="slide-body"><div class="s26-two model"><div><p class="s26-dhead">부품 검사</p>' + cards + table + take
    + '</div><div><p class="s26-dhead">오안착 검출 사례</p>' + logfig
    + '<dl class="s26-mini"><div><dt>판정</dt><dd>이탈 7.8mm &gt; 허용 5mm</dd></div><div><dt>처리</dt><dd>안착 불합격 · 작업 중단</dd></div>'
      '<div><dt>기록</dt><dd>판정 영상·오류 기록 저장</dd></div></dl></div></div></div>')
rep('opencv-inspect', '<p class="deck">티칭 GUI에서 기준 설정·스텝 편집과 측정·검사 결과를 함께 관리합니다</p>',
    '<p class="deck">OpenCV만으로 생긴 구분 오류를 없애려고 종류와 안착 검사를 나누고, 제자리를 벗어난 부품은 작업을 멈추게 했습니다</p>')
if VARIANT == 'control':
    # control deck: operator screens instead of the inspection page
    A['opencv-inspect'] = re.sub(r'(<h2 id="opencv-inspect-title">).*?(</h2>)', r'\1티칭 GUI와 Windows 관제 화면\2', A['opencv-inspect'], flags=re.S)
    A['opencv-inspect'] = re.sub(r'<p class="deck">.*?</p>', '<p class="deck">동작을 가르치는 화면과 작업을 요청하는 화면을 만들고, 통신이 끊기면 팔이 멈추게 했습니다</p>', A['opencv-inspect'], count=1, flags=re.S)
    _gui_img = re.search(r'<img[^>]*opencv-gui-poster[^>]*/>', guifig).group(0)
    A['opencv-inspect'] = A['opencv-inspect'].replace(body_of('opencv-inspect'),
        '<div class="slide-body"><div class="gui-page"><div class="gui-shots">'
        '<figure class="figure-board">' + _gui_img + '<figcaption><b class="fig-no">그림 4. </b>티칭 GUI · 스텝 편집·카메라 측정·검사</figcaption></figure>'
        '<figure class="figure-board"><img alt="Windows WPF 작업 관제 화면: 전체 명령, 연결·운전 상태, 최근 명령" decoding="async" loading="lazy" '
        'src="assets/images/opencv-wpf-console.webp" width="1920" height="1008"/>'
        '<figcaption><b class="fig-no">그림 5. </b>Windows 관제 화면 · 명령 요청과 연결·운전 상태</figcaption></figure></div>'
        '<div class="text-stack gui-cards">'
        '<section><h3>티칭 GUI · Python</h3><p>기준 설정과 스텝 편집을 한 화면에서 처리<br/>'
        '지그 측정과 <strong>안착 검사 결과를 함께 표시</strong></p></section>'
        '<section><h3>관제 화면 · WPF</h3><p>조립·적재·정지·재개 명령 요청과 결과 조회<br/>'
        'Ubuntu 중계로 <strong>ROS2 Action 클라이언트와 연결</strong></p></section>'
        '<section><h3>통신 단절과 정지 처리</h3><p>0.25초마다 생존 신호 교환<br/>'
        '<strong>3초간 응답이 없으면 팔 정지·작업 보류</strong></p></section>'
        '</div></div></div>')
rep('opencv-model', '<p class="deck">지그·단품·부분 조립체·완제품 13개 클래스를 구분하고, Raspberry Pi5에서 실행 형식과 모델 크기를 정했습니다</p>',
    '<p class="deck">실물로 반복해 찍기 어려운 장면은 Isaac Sim 가상 작업대에서 만들어 학습하고, Raspberry Pi5에 맞춰 실행 형식과 모델 크기를 정했습니다</p>')
rep('opencv-model', '<div><dt>가상 데이터</dt><dd>오안착 137장·경계 사례 45장 포함, 배치·적재·조명 변화</dd></div>',
    '<div><dt>Isaac Sim 가상 데이터</dt><dd>살짝 벗어난 배치는 실물로 같은 조건을 반복해 찍기 어려워 가상으로 생성<br/>오안착 137장·경계 사례 45장 포함, 배치·적재·조명 변화</dd></div>')
rep('opencv-model', '<p>평균 IoU가 비슷한 혼합·순차 중 편차 0.60으로 가장 안정적</p>',
    '<p>실물·가상을 섞은 학습과 차례로 한 학습을 비교, 편차 0.60으로 가장 안정적</p>')
rep('opencv-model', '<p class="s26-note">실물 31장·169개 · 신뢰도 50% · 처리 시간은 Pi5 중앙값</p>',
    '<p class="s26-note">학습에 넣지 않은 실물 31장·169개로 비교 · 신뢰도 50% · 처리 시간은 Pi5 중앙값</p>')
if VARIANT == 'vision':
    rep('opencv', '학습 데이터·모델 비교와 실행 기준 검증', '실물·Isaac Sim 가상 데이터로 학습, 모델 비교와 실행 기준 검증')
rep('opencv-pose', '지그의 이동·회전만큼 집게 목표와 관절값을 다시 계산합니다</p>', '지그의 이동·회전만큼 집게 목표와 관절값을 다시 계산했습니다</p>')
# real photos of the jig-compensation demo above the diagram
rep('opencv-pose', '<div class="s29-board s29-pose">',
    '<div class="pose-photos">'
    '<figure><img alt="처음 지그 위치에 부품을 올려놓는 로봇팔" src="assets/images/opencv-pose-1.webp" width="636" height="636"/><span>처음 위치</span></figure>'
    '<figure><img alt="지그를 옮긴 뒤 부품을 올려놓는 로봇팔" src="assets/images/opencv-pose-2.webp" width="636" height="636"/><span>지그 이동 후</span></figure>'
    '<figure><img alt="지그를 다시 옮기고 돌린 뒤 부품을 올려놓는 로봇팔" src="assets/images/opencv-pose-3.webp" width="636" height="636"/><span>다시 이동·회전 후</span></figure>'
    '</div><div class="s29-board s29-pose">')
rep('opencv-pose', '</b>지그가 움직인 만큼 집게 작업점을 옮기고, 높이와 벌림은 유지</figcaption>',
    '</b>지그를 옮기고 돌려도 저장한 동작으로 부품을 올려놓는 시연(위)과 목표 보정 방식(아래)</figcaption>')
ARM = ['opencv', 'opencv-pose', 'opencv-locate', 'opencv-inspect'] if VARIANT == 'control' else ['opencv', 'opencv-locate', 'opencv-model', 'opencv-inspect']
for k in ARM + ['plc', 'plc-detail', 'vision', 'vision-detail', 'thesis', 'thesis-results']:
    A[k] = re.sub(r'<nav aria-label="[^"]*" class="stage-nav">.*?</nav>', '', A[k], flags=re.S)
for n, k in enumerate(ARM, 1):
    A[k] = re.sub(r'<span class="part-number">\d / 6</span>', f'<span class="part-number">{n} / {len(ARM)}</span>', A[k])

# --- mobile robot (3 -> 2): structure and fixes on one text slide
stack = re.search(r'<div class="text-stack">.*?</section></div>', A['robot-system'], flags=re.S).group(0)
issues = re.search(r'<table class="issue-table">.*?</table>', A['robot-detail'], flags=re.S).group(0)
def _row(th, why, fix):
    return f'<tr><th scope="row">{th}</th><td class="why">{why}</td><td>{fix}</td></tr>'
issues = ('<table class="issue-table three"><thead><tr><th scope="col">문제</th><th scope="col">원인</th><th scope="col">개선</th></tr></thead><tbody>'
    + _row('부하가 걸릴 때의 떨림', '서보 단자 전압이 순간적으로 낮아짐', '전원 배선 점검, 커패시터 추가, 서보 교체로 <strong>떨림 감소</strong>')
    + _row('관절의 급격한 움직임', '펄스폭이 한 번에 바뀌어 속도가 불연속', '<strong>20ms마다 펄스폭을 단계적으로 바꾸는 S-curve</strong> 적용')
    + _row('관절 원점·가동 범위', '필요한 펄스값이 서보마다 다름', '<strong>−90°·0°·+90° 3점 보정</strong>으로 원점·리미트 설정')
    + _row('고속 주행 시 방향 보정', 'PWM이 최댓값에 닿아 PID 보정이 반영되지 않음', '<strong>최대 출력을 220 PWM으로 제한</strong>')
    + '</tbody></table>')
A['robot-system'] = A['robot-system'].replace(body_of('robot-system'),
    '<div class="slide-body"><div class="split submission-two">' + stack + '<div class="app-cases">' + issues + '</div></div></div>')
rep('robot-system', '>로봇팔 제어와 시스템 통신 구조</h2>', '>16바이트 통신 규격과 구동 문제 개선</h2>')
rep('robot-system', '<p class="deck">16바이트 통신 규격으로 서보 제어·보정·티칭 데이터를 주고받고 저장합니다</p>',
    '<p class="deck">16바이트 규격으로 앱과 펌웨어를 연결하고, 부하 시 떨림과 급격한 움직임을 줄였습니다</p>')
_plc_old = re.search(r'<dl class="process-list">.*?</dl>', A['plc-detail'], flags=re.S).group(0)
_plc_rows = [
 ('문제 1', "병렬 운전 중 '빈 층을 찾았다'는 값과 '그 층에 소재가 있다'는 값이 한 메모리에 섞여<br/><strong>이전 동작의 상태가 다음 시퀀스의 판단에 영향</strong>"),
 ('개선', '<strong>판단용·적재용 메모리 분리</strong><br/>판단값은 적재가 끝나면 초기화하고, 적재값은 소재를 뺄 때까지 유지'),
 ('문제 2', '각자 작성한 코드를 통합하자 <strong>같은 메모리 주소를 서로 다른 용도로 사용</strong>해 시퀀스가 꼬임'),
 ('개선', '사용 중인 주소를 모두 모아 대조하고 <strong>겹치는 주소 정리</strong><br/>코멘트에 사용 주소를 적어 서로 확인'),
 ('배운 점', '코드 통합 전 <strong>메모리 사용 주소 합의</strong>가 중요함<br/>병렬 동작에서는 장치별 동작 조건·완료 조건·인터록을 먼저 정해야 함'),
]
A['plc-detail'] = A['plc-detail'].replace(_plc_old, '<dl class="process-list">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in _plc_rows) + '</dl>')
for k in ['robot', 'robot-system']:
    A[k] = re.sub(r'<nav aria-label="[^"]*" class="stage-nav">.*?</nav>', '', A[k], flags=re.S)
    A[k] = re.sub(r'(<span class="part-number">\d) / 3</span>', r'\1 / 2</span>', A[k])

rep('vision-detail', '<p class="deck">입력 해상도와 모델 형식을 조정하고, 보행 경로와 차량 접근을 판단할 영역을 정했습니다</p>',
    '<p class="deck">Raspberry Pi5 한 대에서 두 모델을 함께 돌리기 위해 입력과 모델을 줄이고, 판단 영역을 보행과 차량으로 나눴습니다</p>')

# --- walking aid: clean ROI picture on the overview, Pi5 run screen on the detail slide
rep('vision', '<img alt="Raspberry Pi5에서 실행한 객체·지면 인식 화면" class="video-poster" decoding="async" height="1068" loading="lazy" src="assets/images/vision-demo.webp" width="1611"/>',
    '<img alt="보행 영역과 차량 영역을 나눠 표시한 인식 화면" class="video-poster" decoding="async" height="483" loading="lazy" src="assets/images/vision-roi.webp" width="719"/>')
rep('vision', '</b>Raspberry Pi5에서 실행한 객체·지면 인식 화면</figcaption>', '</b>객체·지면 인식 화면 · 빨간색: 보행 경로, 주황색: 차량 접근 영역</figcaption>')
rep('vision-detail', '<img alt="보행 영역과 차량 영역을 나눠 표시한 ROI" decoding="async" height="483" loading="lazy" src="assets/images/vision-roi.webp" width="719"/>',
    '<img alt="Raspberry Pi5에서 실행한 객체·지면 인식 화면과 실행 기록" decoding="async" height="1068" loading="lazy" src="assets/images/vision-demo.webp" width="1611"/>')
rep('vision-detail', 'data-caption="빨간색: 보행 경로 · 주황색: 차량 접근 영역" data-image="assets/images/vision-roi.webp"', 'data-caption="Raspberry Pi5에서 실행한 인식 화면과 실행 기록" data-image="assets/images/vision-demo.webp"')
rep('vision-detail', '</b> 빨간색: 보행 경로 · 주황색: 차량 접근 영역</figcaption>', '</b>Raspberry Pi5에서 실행한 인식 화면과 실행 기록</figcaption>')

# --- finished projects: past tense
if VARIANT == 'control':
    rep('opencv', '<p class="deck">Raspberry Pi5에서 AI·OpenCV·CAD로 지그 위치와 부품 상태를 확인합니다</p>',
        '<p class="deck">ROS2 요청을 받아 지그 위치를 다시 재고, 저장한 동작을 그 위치에 맞춰 실행했습니다</p>')
else:
    rep('opencv', '지그 위치와 부품 상태를 확인합니다</p>', '지그 위치와 부품 상태를 확인했습니다</p>')
rep('opencv', '저장한 동작으로 조립·하차 공정을 이어갑니다<br/>', '저장한 동작으로 조립·하차 공정을 이어가게 했습니다<br/>')
rep('opencv', '부품 종류와 안착 상태를 검사합니다</p>', '부품 종류와 안착 상태를 검사했습니다</p>')
rep('opencv-locate', '위치·방향이 맞을 때만 채택합니다</p>', '위치·방향이 맞을 때만 채택했습니다</p>')
rep('robot', '주행과 물품 회수 동작을 제어합니다</p>', '주행과 물품 회수 동작을 제어했습니다</p>')
rep('robot', '물품 회수·운반 시연품입니다<br/>', '물품 회수·운반 시연품을 만들었습니다<br/>')
rep('robot', '저장한 동작을 재생합니다</p>', '저장한 동작을 재생하게 했습니다</p>')
rep('vision', '인도와 차도를 구분합니다<br/>', '인도와 차도를 구분했습니다<br/>')
rep('vision', '음성으로 알려 줍니다</p>', '음성으로 알려 주게 했습니다</p>')
rep('vision', '<span>YOLO26n</span>', '<span>YOLO26n · YOLO26n-seg</span>')

def renumber(k, old, new):
    A[k] = A[k].replace(f'aria-label="프로젝트 {old}" class="project-number">{old}</b>', f'aria-label="프로젝트 {new}" class="project-number">{new}</b>')
    A[k] = A[k].replace(f'data-project-no="{old}"', f'data-project-no="{new}"')

if VARIANT == 'control':
    keep = ['profile', 'resume'] + ARM + ['robot', 'robot-system', 'plc', 'plc-detail']
    renumber('plc', '04', '03'); renumber('plc-detail', '04', '03')
    dropped = ['vision', 'thesis', 'travel']
else:
    keep = ['profile', 'resume'] + ARM + ['vision', 'vision-detail', 'thesis', 'thesis-results']
    for k, old, new in [('vision', '03', '02'), ('vision-detail', '03', '02'), ('thesis', '05', '03'), ('thesis-results', '05', '03')]:
        renumber(k, old, new)
    rep('thesis', '8개의 피에조 센서로 수집합니다<br/>', '8개의 피에조 센서로 수집했습니다<br/>')
    rep('thesis', '노크 위치를 9개 구역으로 구분합니다</p>', '노크 위치를 9개 구역으로 구분했습니다</p>')
    dropped = ['plc', 'robot', 'travel']
    # real-time detection screen on the overview; method and results on the second slide
    summary = re.search(r'<p class="summary">.*?</p>', A['thesis'], flags=re.S).group(0)
    role = re.search(r'<div class="role-block contribution">.*?</div>', A['thesis'], flags=re.S).group(0)
    tags = re.search(r'<div class="tags">.*?</div>', A['thesis'], flags=re.S).group(0)
    specs = re.search(r'<dl class="specs">.*?</dl>', A['thesis'], flags=re.S).group(0)
    A['thesis'] = A['thesis'].replace(body_of('thesis'),
        '<div class="slide-body"><figure class="main-figure figure-board knock-wide"><img alt="실시간 노크 위치 탐지 화면: 센서 신호와 주파수 분석, 예측 구역, 아크릴판을 두드리는 손" '
        'src="assets/images/knock-realtime.webp" width="1436" height="397"/>'
        '<figcaption><b class="fig-no">그림 17. </b>실시간 탐지 화면 · 가운데 구역을 두드리자 시간·주파수 특징 모두 같은 구역으로 예측</figcaption></figure>'
        '<div class="knock-intro text-stack"><section><h3>신호 수집</h3>' + summary.replace('class="summary"','') + '</section><section><h3>모델 선정과 검증</h3><!--K2--></section></div>' + tags + specs + '</div>')
    table = re.search(r'<table class="result-table">.*?</table>', A['thesis-results'], flags=re.S).group(0)
    A['thesis-results'] = A['thesis-results'].replace(body_of('thesis-results'),
        '<div class="slide-body"><div class="split submission-two knock-method"><div class="text-stack">'
        '<section data-step="01"><h3>데이터 수집</h3><p>센서 8개로 9개 위치를 위치당 140회, 총 1,260회 기록<br/>2,500Hz로 0.4초, 트리거 이전 0.05초 포함</p></section>'
        '<section data-step="02"><h3>전처리</h3><p>61Hz 하이패스 필터와 데이터 평탄화 후 정규화</p></section>'
        '<section data-step="03"><h3>특징 선정</h3><p>다중 선형회귀로 중요도를 판단해<br/>시간 영역 4개, 주파수 영역 3개, 센서 간 시간 차 1개 선정</p></section>'
        '<section data-step="04"><h3>모델 선정과 실시간 예측</h3><p>K-NN·SVM·ANN 중 <strong>평균 정확도가 가장 높은 K-NN 선정</strong><br/>학습 70%·검증 30%로 검증하고, 두드린 위치를 실시간 예측</p></section>'
        '</div><div><h3>K-NN 검증 정확도</h3>' + table +
        '<p class="s26-take">센서 간 시간 차만 쓴 방식보다 <b>시간·주파수 영역 특징의 정확도가 더 높음</b></p></div></div></div>')
    rep('thesis-results', '>입력 특징별 K-NN 검증 결과</h2>', '>신호 수집부터 입력 특징별 K-NN 검증까지</h2>')
    rep('thesis-results', '<p class="deck">같은 아크릴판에서 수집한 데이터를 학습 70%, 검증 30%로 무작위 분할해 비교했습니다</p>',
        '<p class="deck">같은 아크릴판에서 수집한 신호를 전처리하고, 입력 특징을 바꿔 가며 위치 분류 정확도를 비교했습니다</p>')
# skills: control | robot·vision | tools; Ansys dropped
_t = re.search(r'<h3>설계·개발 도구</h3><p>.*?</p>', A['profile'], flags=re.S).group(0)
assert 'Ansys' in _t
A['profile'] = A['profile'].replace(_t, '<h3>설계·개발 도구</h3><p>SolidWorks · MATLAB<br/>MuJoCo · Isaac Sim</p>')
# --- one column grid on every project slide; figure on the left, text on the right
rep('plc', '공급·가공·분류·저장 공정을 연결했습니다<br/>여러 장치를 병렬로 운전하고, 수동 모드에서는 개별 제어할 수 있게 했습니다</p>',
    '공급·가공·분류·저장 공정을 연결했습니다<br/>여러 장치를 병렬로 운전하고,<br/>수동 모드에서는 개별 제어할 수 있게 했습니다</p>')
def set_summary(k, paras):
    old = re.search(r'<p class="summary">.*?</p>', A[k], flags=re.S).group(0)
    A[k] = A[k].replace(old, '<div class="text-stack ov-stack">' + ''.join(f'<section><h3>{h}</h3><p>{t}</p></section>' for h, t in paras) + '</div>', 1)
set_summary('opencv', [
    ('프로젝트 개요', '로봇팔 2대가 지그 도착부터 조립, 완제품 하차까지 맡는 작업대를 만들었습니다<br/>정차 위치가 달라지고 부품이 서로 가려도 공정이 이어지게 했습니다'),
    ('핵심 기능', '카메라로 <strong>지그를 다시 측정해 동작 목표를 보정</strong>하고,<br/><strong>부품 종류와 안착 상태를 검사</strong>했습니다'),
    ('제어 방식', '<strong>ROS2 Action</strong>으로 작업 요청을 받고,<br/>순기구학·역기구학으로 집게 목표와 관절값을 계산했습니다') if VARIANT == 'control' else
    ('적용 모델', '지그·팔레트와 부품은 <strong>YOLO26 분할 모델</strong>과 설계 형상 맞춤으로 찾고,<br/>모델은 <strong>Raspberry Pi5</strong>에서 실행했습니다')])
set_summary('robot', [
    ('프로젝트 개요', '이동체와 로봇팔을 결합한 물품 회수·운반 시연품을 만들었습니다<br/>앱으로 주행과 관절을 수동 조작하고, 저장한 동작을 재생하게 했습니다'),
    ('펌웨어·통신', '<strong>STM32F411과 FreeRTOS</strong>로 펌웨어를 작성하고,<br/>앱과는 Bluetooth로 <strong>16바이트 명령·응답</strong>을 주고받았습니다'),
    ('구동·저장', '서보 6개는 PCA9685로 제어하고, 티칭한 동작은 Flash에 저장했습니다')])
set_summary('plc', [
    ('공정 구성', '컨베이어·실린더·서보모터로 공급·가공·분류·저장 공정을 연결했습니다'),
    ('병렬 적재', '금속·비금속을 판별해 <strong>1~4층 창고에 병렬로 적재</strong>하고,<br/>수동 모드에서는 층별로 개별 제어할 수 있게 했습니다'),
    ('HMI 구성', 'HMI 화면에서 가공 횟수와 시간을 지정하고 적재 상태를 확인하게 했습니다')])
set_summary('vision', [
    ('프로젝트 개요', '시각장애인의 보행을 돕는 웨어러블 장치를 만들었습니다<br/>카메라 영상에서 사람·차량·장애물을 탐지하고 인도와 차도를 구분했습니다'),
    ('적용 모델', '객체는 <strong>YOLO26n 객체 검출</strong> 모델로 위치를 찾고,<br/>지면은 <strong>YOLO26n-seg 인스턴스 분할</strong> 모델로 영역을 나눴습니다'),
    ('위험 알림', '보행 경로에 가까운 대상을 판단해 음성으로 알려 주게 했습니다')])
_k2 = '<p><strong>K-NN·SVM·ANN</strong> 중 평균 정확도가 가장 높은 K-NN을 선정했습니다<br/>입력 특징을 <strong>시간 차·시간 영역·주파수 영역</strong>으로 바꿔 정확도를 검증했습니다</p>'
if '<!--K2-->' in A['thesis']:
    A['thesis'] = A['thesis'].replace('<!--K2-->', _k2)
def _specs(k, cells, role):
    old = re.search(r'<dl class="specs">.*?</dl>', A[k], flags=re.S).group(0)
    A[k] = A[k].replace(old, '<dl class="specs with-role">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in cells)
                        + f'<div class="role"><dt>담당 역할</dt><dd>{role}</dd></div></dl>')
_specs('opencv', [('기간', '2026.09 – 2026.11'), ('장비', 'SO-101 2대 · Raspberry Pi5')],
       '비전 보정 · 티칭 GUI · Raspberry Pi5 연동 · 학습 데이터·모델 비교')
_specs('robot', [('수행 시기', '2026.07 · 1주'), ('구동 구성', '4WD · 서보 6개')],
       '프로젝트 리더 · 로봇팔 제작·제어 · STM32 펌웨어 · 통신 규격 설계')
_specs('plc', [('PLC', 'Mitsubishi Q 시리즈'), ('개발 도구', 'GX Works2 · GT Designer3')],
       '병렬 처리 로직 · HMI 화면 작성 · 수동 제어 코드 통합')
_specs('vision', [('수행 시기', '2026.05 · 11일'), ('라벨 통합', '객체 29→10종 · 지면 23→7종')],
       '라벨 통합 · 모델 학습·변환 · ROI·알림 판단 로직 구현')
_specs('thesis', [('논문 제출', '2023.05'), ('수집 데이터', '센서 8개 · 9구역 × 140회')],
       '주제 제안 · MATLAB 전처리·특징 추출 · 모델 비교 · 실시간 탐지 구현')
if 'thesis-results' in A:
    for o, n in [('90.741<span>', '90.7<span>'), ('96.296<span>', '96.3<span>'), ('97.884<span>', '97.9<span>')]:
        if o in A['thesis-results']: A['thesis-results'] = A['thesis-results'].replace(o, n)
# technology tags removed from the overviews (the cards already name what was used)
for k in ['opencv', 'robot', 'vision', 'plc', 'thesis']:
    A[k] = re.sub(r'<div class="tags">.*?</div>', '', A[k], flags=re.S)
    assert 'class="tags"' not in A[k], k
# role blocks removed: every slide already shows only my own work
for k in ['opencv', 'robot', 'vision', 'plc', 'thesis']:
    A[k] = re.sub(r'<div class="role-block contribution">.*?</div>', '', A[k], flags=re.S)
    assert 'role-block' not in A[k], k
m = re.search(r'<div class="split">(<div class="text-stack">.*?</section></div>)(<div><figure class="roi-figure.*?</figure></div>)</div>', A['vision-detail'], flags=re.S)
A['vision-detail'] = A['vision-detail'].replace(m.group(0), '<div class="split">' + m.group(2) + m.group(1) + '</div>')
for k in keep:
    if k in ('profile', 'resume'):
        continue
    A[k], c = re.subn(r'(<div class="slide-body">\s*(?:<figure class="main-figure figure-board knock-wide">.*?</figure>)?<div class=")', r'\1sg ', A[k], count=1, flags=re.S)
    assert c == 1, k
    if k in ('opencv-pose', 'robot-system', 'plc-detail', 'vision-detail', 'thesis-results'):
        A[k] = A[k].replace('<div class="sg ', '<div class="sg fill ', 1)

n = len(keep); out = []; fig = 0
def renum(m):
    global fig
    fig += 1
    return f'{m.group(1)}그림 {fig}. '
for i, k in enumerate(keep, 1):
    a = re.sub(r'(<span class="slide-count">)\d+ / \d+(</span>)', rf'\g<1>{i:02d} / {n:02d}\2', A[k])
    a = re.sub(r'(<b class="fig-no">)그림 \d+\. ', renum, a)
    out.append(f'<section class="page-shell" data-page="{i}">{a}')
html = head + '</section>'.join(out) + tail
html = html.replace('<span id="mobile-count">01 / 19</span>', f'<span id="mobile-count">01 / {n:02d}</span>')
for sec in dropped:
    html, c = re.subn(rf'<a aria-label="[^"]*" data-label="[^"]*" data-section="{sec}".*?</a>', '', html, flags=re.S); assert c == 1, sec
P.write_text(html)
print('slides', n, 'figures', fig)
