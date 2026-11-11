#!/bin/sh
# Build both submission versions: docs/index.html (control) and docs/vision.html (vision), with their PDFs.
set -e
cd "$(dirname "$0")/../.."
python3 tools/scripts/build_submission.py vision
python3 tools/scripts/export_pdf.py
cp docs/index.html docs/vision.html
mv docs/assets/pdf/slides.pdf docs/assets/pdf/slides-vision.pdf
mv docs/assets/pdf/handout.pdf docs/assets/pdf/handout-vision.pdf
python3 tools/scripts/build_submission.py control
python3 tools/scripts/export_pdf.py
python3 tools/scripts/add_site_link.py docs/assets/pdf/slides.pdf docs/assets/pdf/slides-vision.pdf
