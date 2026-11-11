#!/usr/bin/env python3
"""Reduce the 19-slide master (docs/index.html) to the 11-slide submission deck, in place.

Run on a branch cut from the master deck. Keeps: cover, education, robot arm (5), mobile robot (2),
walking aid (2). Drops PLC, knock research, Travel Visualizer. Titles become result sentences.
"""
import re
from pathlib import Path
P = Path(__file__).resolve().parents[2] / 'docs' / 'index.html'
t = P.read_text()
arts = re.findall(r'<article.*?</article>', t, flags=re.S)
assert len(arts) == 19, len(arts)
head, tail = t[:t.index('<section class="page-shell"')], t[t.rindex('</section></main>'):]
A = {re.search(r' id="([^"]+)"', a).group(1): a for a in arts}

def rep(key, old, new, count=1):
    assert A[key].count(old) == count, (key, old, A[key].count(old))
    A[key] = A[key].replace(old, new)

# --- cover: role line, representative results, contact
rep('profile', '<p class="hero-line">설계부터 구현, 디버깅까지<br/>어느 단계도 가볍게 넘기지 않습니다</p>',
    '<p class="hero-line">비전으로 로봇팔 동작을 보정하고,<br/>그 모델을 Raspberry Pi5에 올렸습니다</p>'
    '<ul class="hero-facts"><li><b>팔레트 위치 검출</b>79.3% → 99.6% <small>촬영 285장</small></li>'
    '<li><b>부품 구분</b>247개 → 249개 전부 <small>검사 249개</small></li>'
    '<li><b>Pi5 처리 시간</b>1.341초 → 0.523초 <small>FP16 변환</small></li></ul>')

# --- robot arm (6 -> 5): log slide folded into the inspection slide
rep('opencv', '<div><dt>진행 상태</dt><dd>프로젝트 진행 중</dd></div>', '<div><dt>팀 구성</dt><dd>○명 (확인 필요)</dd></div>')
rep('opencv-pose', '>작업 요청부터 관절 목표까지 연결</h2>', '>지그가 움직인 만큼 집게 목표를 다시 계산합니다</h2>')
rep('opencv-pose', '<p class="deck">ROS2 요청을 받아 지그를 측정하고, 지그의 이동·회전만큼 집게 목표와 관절값을 다시 계산합니다</p>',
    '<p class="deck">ROS2 요청을 받아 지그를 측정하고, 저장한 동작을 지그의 이동·회전만큼 옮겨 관절값을 계산합니다</p>')
rep('opencv-locate', '>지그·팔레트 위치를 AI와 형상 검증으로 확정</h2>', '>설계 형상을 맞춰 팔레트 검출을 79.3%에서 99.6%로 높였습니다</h2>')
rep('opencv-inspect', '>부품 종류와 제자리 안착을 따로 확인</h2>', '>종류와 안착을 나눠 검사해 249개를 모두 맞게 구분했습니다</h2>')
rep('opencv-inspect', '<p class="deck">티칭 GUI에서 기준 설정·스텝 편집과 측정·검사 결과를 함께 관리합니다</p>',
    '<p class="deck">AI 라벨로 부품 종류를, 설계 형상으로 안착 위치를 확인하고, 제자리를 벗어난 부품은 작업을 멈춥니다</p>')
rep('opencv-inspect', '<div><dt>기준 설정</dt><dd>원점·TCP·카메라 좌표 기준</dd></div><div><dt>스텝 편집</dt><dd>고정 자세·지그 기준 보정 자세</dd></div><div><dt>측정·검사</dt><dd>지그 채택·부품 안착 결과</dd></div>',
    '<div><dt>오안착 검출 사례</dt><dd>이탈 7.8mm &gt; 허용 5mm</dd></div><div><dt>처리</dt><dd>안착 불합격 · 작업 중단</dd></div><div><dt>기록</dt><dd>판정 영상·오류 기록 저장</dd></div>')
rep('opencv-model', '>실물·가상 데이터로 학습하고 Pi에 맞게 경량화</h2>', '>실물·가상 데이터로 학습하고, Pi5 처리 시간을 61% 줄였습니다</h2>')
for k in ['opencv', 'opencv-pose', 'opencv-locate', 'opencv-inspect', 'opencv-model']:
    rep(k, '<a href="#opencv-log">6. 로그</a>', '')
    A[k] = re.sub(r'(<span class="part-number">\d) / 6</span>', r'\1 / 5</span>', A[k])

# --- mobile robot (3 -> 2): structure and fixes on one text slide, wiring diagram and app screens dropped
rep('robot', '<div><dt>제어 보드</dt><dd>STM32F411</dd></div>', '<div><dt>팀 구성</dt><dd>○명 (확인 필요)</dd></div>')
stack = re.search(r'<div class="text-stack">.*?</section></div>', A['robot-system'], flags=re.S).group(0)
table = re.search(r'<table class="issue-table">.*?</table>', A['robot-detail'], flags=re.S).group(0)
body = re.search(r'<div class="slide-body">.*?</div>\s*<footer', A['robot-system'], flags=re.S).group(0)
A['robot-system'] = A['robot-system'].replace(body,
    '<div class="slide-body"><div class="split submission-two"><div class="text-stack">' + stack[len('<div class="text-stack">'):]
    + '<div class="app-cases">' + table + '</div></div></div><footer')
rep('robot-system', '>로봇팔 제어와 시스템 통신 구조</h2>', '>통신 규격을 먼저 정하고, 구동 문제는 원인을 나눠 고쳤습니다</h2>')
rep('robot-system', '<p class="deck">16바이트 통신 규격으로 서보 제어·보정·티칭 데이터를 주고받고 저장합니다</p>',
    '<p class="deck">16바이트 규격으로 앱과 펌웨어를 연결하고, 부하 시 떨림과 급격한 움직임을 각각 개선했습니다</p>')
for k in ['robot', 'robot-system']:
    A[k] = A[k].replace('2. 구조·통신</a>', '2. 통신·문제 개선</a>')
    A[k] = re.sub(r'<a class="" href="#robot-detail">3\. 문제 개선</a>', '', A[k])
    A[k] = re.sub(r'(<span class="part-number">\d) / 3</span>', r'\1 / 2</span>', A[k])

# --- walking aid
rep('vision', '<div><dt>실행 장치</dt><dd>Raspberry Pi5</dd></div>', '<div><dt>팀 구성</dt><dd>○명 (확인 필요)</dd></div>')
rep('vision-detail', '>Raspberry Pi5 실행 환경에 맞춘 조정</h2>', '>Pi5 한 대에서 두 모델이 돌도록 입력과 모델을 줄였습니다</h2>')

keep = ['profile', 'resume', 'opencv', 'opencv-pose', 'opencv-locate', 'opencv-inspect', 'opencv-model',
        'robot', 'robot-system', 'vision', 'vision-detail']
n = len(keep); out = []; fig = 0
for i, k in enumerate(keep, 1):
    a = re.sub(r'(<span class="slide-count">)\d+ / \d+(</span>)', rf'\g<1>{i:02d} / {n}\2', A[k])
    def renum(m):
        global fig; fig += 1; return f'{m.group(1)}그림 {fig}. '
    a = re.sub(r'(<b class="fig-no">)그림 \d+\. ', renum, a)
    out.append(f'<section class="page-shell" data-page="{i}">{a}')
html = head + '</section>'.join(out) + tail
html = html.replace('<span id="mobile-count">01 / 19</span>', f'<span id="mobile-count">01 / {n}</span>')
for sec in ['plc', 'thesis', 'travel']:
    html, c = re.subn(rf'<a aria-label="[^"]*" data-label="[^"]*" data-section="{sec}".*?</a>', '', html, flags=re.S); assert c == 1, sec
P.write_text(html)
print('slides', n, 'figures', fig)
