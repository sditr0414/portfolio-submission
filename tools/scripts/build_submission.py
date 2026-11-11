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
    '<p class="hero-line">ROS2로 로봇팔 동작을 제어하고,<br/>STM32 펌웨어와 통신 규격을 만들었습니다</p>' if VARIANT == 'control' else
    '<p class="hero-line">비전으로 로봇팔 동작을 보정하고,<br/>그 모델을 Raspberry Pi5에 올렸습니다</p>')
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
decisions = re.search(r'<div class="s26-decisions">.*?</div><p class="s26-note">.*?</p>', A['opencv-model'], flags=re.S).group(0)
A['opencv-inspect'] = A['opencv-inspect'].replace(body_of('opencv-inspect'),
    '<div class="slide-body"><div class="s26-two model"><div><p class="s26-dhead">부품 검사</p>' + cards + table + take
    + '<dl class="s26-mini"><div><dt>오안착 검출 사례</dt><dd>이탈 7.8mm &gt; 허용 5mm</dd></div><div><dt>처리</dt><dd>안착 불합격 · 작업 중단</dd></div>'
      '<div><dt>기록</dt><dd>판정 영상·오류 기록 저장</dd></div></dl></div><div>' + decisions + '</div></div></div>')
rep('opencv-inspect', '>부품 종류와 제자리 안착을 따로 확인</h2>', '>부품 종류·안착 검사와 Raspberry Pi5 경량화</h2>')
rep('opencv-inspect', '<p class="deck">티칭 GUI에서 기준 설정·스텝 편집과 측정·검사 결과를 함께 관리합니다</p>',
    '<p class="deck">OpenCV만으로 생긴 구분 오류를 없애려고 종류와 안착 검사를 나누고, Raspberry Pi5에 맞춰 실행 형식과 모델 크기를 정했습니다</p>')
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
ARM = ['opencv', 'opencv-pose', 'opencv-locate'] if VARIANT == 'control' else ['opencv', 'opencv-locate', 'opencv-inspect']
for k in ARM + ['plc', 'plc-detail', 'vision', 'vision-detail', 'thesis', 'thesis-results']:
    A[k] = re.sub(r'<nav aria-label="[^"]*" class="stage-nav">.*?</nav>', '', A[k], flags=re.S)
for n, k in enumerate(ARM, 1):
    A[k] = re.sub(r'<span class="part-number">\d / 6</span>', f'<span class="part-number">{n} / 3</span>', A[k])

# --- mobile robot (3 -> 2): structure and fixes on one text slide
stack = re.search(r'<div class="text-stack">.*?</section></div>', A['robot-system'], flags=re.S).group(0)
issues = re.search(r'<table class="issue-table">.*?</table>', A['robot-detail'], flags=re.S).group(0)
A['robot-system'] = A['robot-system'].replace(body_of('robot-system'),
    '<div class="slide-body"><div class="split submission-two">' + stack + '<div class="app-cases">' + issues + '</div></div></div>')
rep('robot-system', '>로봇팔 제어와 시스템 통신 구조</h2>', '>16바이트 통신 규격과 구동 문제 개선</h2>')
rep('robot-system', '<p class="deck">16바이트 통신 규격으로 서보 제어·보정·티칭 데이터를 주고받고 저장합니다</p>',
    '<p class="deck">16바이트 규격으로 앱과 펌웨어를 연결하고, 부하 시 떨림과 급격한 움직임을 줄였습니다</p>')
for k in ['robot', 'robot-system']:
    A[k] = re.sub(r'<nav aria-label="[^"]*" class="stage-nav">.*?</nav>', '', A[k], flags=re.S)
    A[k] = re.sub(r'(<span class="part-number">\d) / 3</span>', r'\1 / 2</span>', A[k])

rep('vision-detail', '<p class="deck">입력 해상도와 모델 형식을 조정하고, 보행 경로와 차량 접근을 판단할 영역을 정했습니다</p>',
    '<p class="deck">Raspberry Pi5 한 대에서 두 모델을 함께 돌리기 위해 입력과 모델을 줄이고, 판단 영역을 보행과 차량으로 나눴습니다</p>')

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
    skills = re.findall(r'<section><span aria-hidden="true" class="skill-index">\d\d</span>.*?</section>', A['profile'], flags=re.S)
    assert len(skills) == 3
    order = [skills[1], skills[0], skills[2]]
    order = [re.sub(r'class="skill-index">\d\d<', f'class="skill-index">{i:02d}<', s) for i, s in enumerate(order, 1)]
    A['profile'] = A['profile'].replace(''.join(skills), ''.join(order))
    dropped = ['plc', 'robot', 'travel']
    # real-time detection screen full width, accuracies in a strip below
    A['thesis-results'] = A['thesis-results'].replace(body_of('thesis-results'),
        '<div class="slide-body"><figure class="main-figure figure-board knock-wide"><img alt="실시간 노크 위치 탐지 화면: 센서 신호와 주파수 분석, 예측 구역, 아크릴판을 두드리는 손" '
        'src="assets/images/knock-realtime.webp" width="1436" height="397"/>'
        '<figcaption><b class="fig-no">그림 18. </b>실시간 탐지 화면 · 가운데 구역을 두드리자 시간·주파수 특징 모두 같은 구역으로 예측</figcaption></figure>'
        '<dl class="specs"><div><dt>전처리</dt><dd>61Hz 하이패스 필터 · 평탄화 · 정규화</dd></div>'
        '<div><dt>K-NN 정확도 · 센서 간 피크 시간 차</dt><dd>90.741%</dd></div>'
        '<div><dt>K-NN 정확도 · 시간 영역 특징</dt><dd>96.296%</dd></div>'
        '<div><dt>K-NN 정확도 · 주파수 영역 특징</dt><dd>97.884%</dd></div></dl></div>')
    rep('thesis-results', '>입력 특징별 K-NN 검증 결과</h2>', '>실시간 탐지와 입력 특징별 K-NN 검증 결과</h2>')
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
