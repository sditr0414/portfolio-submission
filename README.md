# 정승호 제출용 포트폴리오

로봇 제어 · 비전 · 임베디드

<p>
  <a href="https://sditr0414.github.io/portfolio-submission/"><b>제어형 열기 →</b></a>
  &nbsp;·&nbsp;
  <a href="https://sditr0414.github.io/portfolio-submission/vision.html"><b>비전형 열기 →</b></a>
  &nbsp;·&nbsp;
  <a href="https://sditr0414.github.io/">상세 포트폴리오(시연 영상)</a>
</p>

| 버전 | 슬라이드 PDF (16:9 · 10쪽) | A4 인쇄용 PDF (한 면 2장 · 5쪽) |
| --- | --- | --- |
| 제어형 | [slides.pdf](https://sditr0414.github.io/portfolio-submission/assets/pdf/slides.pdf) | [handout.pdf](https://sditr0414.github.io/portfolio-submission/assets/pdf/handout.pdf) |
| 비전형 | [slides-vision.pdf](https://sditr0414.github.io/portfolio-submission/assets/pdf/slides-vision.pdf) | [handout-vision.pdf](https://sditr0414.github.io/portfolio-submission/assets/pdf/handout-vision.pdf) |

## 구성

| | 제어형 | 비전형 |
| :-: | --- | --- |
| 01 | [비전 기반 로봇팔 조립·검사](https://sditr0414.github.io/portfolio-submission/#opencv) · 동작 보정, 티칭 GUI·관제 화면 | [비전 기반 로봇팔 조립·검사](https://sditr0414.github.io/portfolio-submission/vision.html#opencv) · 위치 확정, 학습·경량화, 검사 |
| 02 | [원격 물품 회수·운반 로봇](https://sditr0414.github.io/portfolio-submission/#robot) · STM32 펌웨어와 통신 규격 | [AI 기반 보행 보조 장치](https://sditr0414.github.io/portfolio-submission/vision.html#vision) · 객체 검출과 지면 분할 |
| 03 | [PLC 기반 창고 적재 제어](https://sditr0414.github.io/portfolio-submission/#plc) · 병렬 적재 공정 | [노크 위치 탐지 연구](https://sditr0414.github.io/portfolio-submission/vision.html#thesis) · 진동 센서로 두드린 위치 판별 |

두 버전은 `tools/source/master.html`에서 `tools/scripts/build_both.sh`로 만듭니다.

## 팔레트 검출 결과

촬영 사진 285장을 사진당 1회 처리했습니다. 외곽선 검출 79.3%(226장), AI+외곽선 80.7%(230장), AI+CAD 정합 99.6%(284장)입니다.
