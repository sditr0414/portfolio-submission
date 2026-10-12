# 포트폴리오 관리 안내

## 로컬 실행

저장소 루트에서 실행합니다. 웹사이트 실행에는 npm 설치나 빌드가 필요하지 않습니다.

```sh
python3 -m http.server 8000 --directory docs
```

브라우저에서 `http://localhost:8000`을 엽니다. `docs/index.html`을 직접 열어도 됩니다.

## 파일 수정과 배포

- 내용: `docs/index.html`
- 스타일: `docs/assets/css/styles.css`
- 목차·이미지 확대·출력 동작: `docs/assets/js/app.js`
- 사진·화면 캡처: `docs/assets/images/`
- 시연 영상: `docs/assets/videos/`
- 다운로드용 PDF: `docs/assets/pdf/`
- 사이트 접속 QR: `docs/assets/qr/`

GitHub Pages의 배포 소스는 `main` 브랜치의 `/docs` 폴더입니다. `docs/.nojekyll`을 유지하며 파일 경로는 대소문자를 구분합니다.

`docs/`에는 공개할 사이트 파일만 두고, 관리 문서와 출력 도구는 `tools/`에 둡니다. 저장소 최상위에는 두 폴더와 `README.md`, `.gitignore`만 둡니다.

사이트 주소는 `https://sditr0414.github.io/`입니다. QR은 이 주소로 연결되므로 파일 위치나 포트폴리오 내용이 바뀌어도 다시 만들 필요가 없습니다.

## PDF와 인쇄

상단 ‘PDF 저장’을 누르면 형식을 고르는 메뉴가 열립니다. ‘슬라이드형 · 1장씩’은 `slides.pdf`(16:9, 16쪽), ‘A4 인쇄형 · 2장씩’은 `handout.pdf`(A4 세로, 8쪽)를 내려받습니다. 16:9 PDF는 배경을 투명하게 출력하고 표지 색을 페이지 밖까지 칠해 뷰어에서 가장자리 흰 선이 생기지 않게 합니다.

Ctrl/Cmd+P는 A4 세로 두 슬라이드 출력을 준비합니다. **A4 / 세로 / 용지당 1페이지 / 배율 100%**로 설정합니다. 한 페이지에 두 슬라이드가 이미 배치되어 있으므로 용지당 2페이지를 다시 선택하지 않습니다.

다운로드용 PDF는 `docs/assets/pdf/`에 보관합니다. 본문이나 슬라이드 디자인을 수정하면 보관용 PDF도 다시 생성하고, `index.html`의 PDF 링크 `?v=` 값을 바꿔 브라우저에 남은 이전 파일이 내려받아지지 않게 합니다. A4 인쇄형은 상단에 이름만 두고, 슬라이드마다 네 변이 같은 테두리를 그립니다(네이비 표지는 테두리 없음).

## 출력 파일 생성

Python, Chromium, 한국어 표시가 가능한 글꼴이 필요합니다. 저장소 루트에서 가상 환경을 만든 뒤 실행합니다.

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/scripts/requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tools/scripts/export_pdf.py
.venv/bin/python tools/scripts/make_preview.py preview.html
```

설치된 Chromium을 지정하려면 `export_pdf.py --browser /path/to/chromium`을 사용합니다. PDF는 `docs/assets/pdf/`에, 검사 결과는 `work/qa/`에 저장됩니다. `preview.html`은 이미지·영상과 현재 화면 동작을 포함한 단일 HTML입니다. 임시 출력과 가상 환경은 Git에서 제외합니다.

## 변경 확인

PC와 모바일에서 내용 넘침, 목차 이동, 이미지 확대, 갤러리, 시연 영상의 자동 재생·화면 밖 정지와 상단 PDF 저장 메뉴의 두 파일 다운로드를 확인합니다. 공개 사이트의 사진과 문서는 누구나 접근할 수 있으므로 공개할 자료만 포함합니다.

## 2026-10-12 추가 자료

- OpenCV 티칭 3장: 사용자가 제공한 Canva 발표 「OpenCV 티칭 — 시각 설명과 실물·GUI 시연」와 ‘OpenCV 티칭’·‘계획 및 의견’ 대화, SO101_teach의 지그 보정 구현 문서를 근거로 작성했습니다.
- 첫 장 영상은 발표에 사용한 편집본에서 시연 영역만 분리했습니다. 편집본의 속도·구간을 유지했으므로 실제 작업 시간의 근거로 사용하지 않습니다. GUI 이미지는 발표용 저장 영상·시연 데이터를 사용한 화면입니다.
- 16개 프레임 중 9→15개는 같은 저장 영상의 팔레트 검출 결과이며, 실물 작업 성공률이나 반복 정밀도가 아닙니다. 반복 도킹·보정 오차·전체 공정 시험은 남은 검증으로 표시합니다.
- Travel Visualizer의 `travel-route.mp4`·`travel-photos.mp4`는 [원본 저장소](https://github.com/sditr0414/Travel-Visualizer/tree/main/docs/assets/demos)의 두 MP4를 그대로 사용했습니다. ‘사진 여정’ 영상의 한 프레임을 첫 장 포스터로 사용합니다.

프로젝트 첫 장의 영상은 `data-src`를 사용해 보이는 시점에 불러옵니다. `poster`와 `.video-poster`는 동일한 대표 장면이며 PDF에서도 같은 배치를 유지합니다. Travel Visualizer의 두 영상은 PC에서 나란히, 모바일에서 세로로 배치합니다.
