"""Add a clickable link over the cover's portfolio-site label (Chromium drops it in this layout)."""
import sys
import fitz

URL = "https://sditr0414.github.io/"
for path in sys.argv[1:]:
    doc = fitz.open(path)
    page = doc[0]
    rects = page.search_for("포트폴리오 사이트")
    assert len(rects) == 1, (path, rects)
    r = rects[0] + (-2, -3, 16, 3)
    page.insert_link({"kind": fitz.LINK_URI, "from": r, "uri": URL})
    doc.save(path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    print(path, [l["uri"] for l in fitz.open(path)[0].get_links()])
