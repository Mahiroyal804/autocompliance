"""Minimal PDF generator — stdlib only.

Writes simple single-column PDFs (Helvetica) from plain text or markdown.
No external dependencies: builds the PDF file structure by hand.
"""

from __future__ import annotations

import re


def _escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap(text: str, width: int = 95) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def markdown_to_pdf_lines(md: str) -> list[tuple[str, int]]:
    """Convert markdown to a list of (text, style) tuples.

    style: 0 = heading1, 1 = heading2, 2 = heading3, 3 = body, 4 = bullet
    """
    out = []
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            out.append(("", 3))
            continue
        if line.startswith("# "):
            out.append((line[2:].strip(), 0))
        elif line.startswith("## "):
            out.append((line[3:].strip(), 1))
        elif line.startswith("### "):
            out.append((line[4:].strip(), 2))
        elif line.startswith(("- ", "* ")):
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", line[2:]).strip()
            out.append(("\u2022 " + text, 4))
        elif re.match(r"^\d+\.\s", line):
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", re.sub(r"^\d+\.\s", "", line)).strip()
            out.append(("\u2022 " + text, 4))
        elif line.startswith("|"):
            continue  # skip tables in PDF
        else:
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
            text = re.sub(r"`(.+?)`", r"\1", text)
            out.append((text, 3))
    return out


def write_pdf(path: str, title: str, lines: list[tuple[str, int]]) -> str:
    """Write lines to a PDF file. Returns path."""
    SIZES = {0: 20, 1: 15, 2: 12, 3: 10, 4: 10}
    LEAD = {0: 26, 1: 20, 2: 16, 3: 14, 4: 14}
    PAGE_W, PAGE_H, MARGIN = 595, 842, 56
    usable = PAGE_W - 2 * MARGIN

    pages: list[list[tuple[str, int, int]]] = [[]]
    y = PAGE_H - MARGIN
    for text, style in lines:
        size = SIZES[style]
        for chunk in _wrap(text, int(usable / (size * 0.55))):
            if y - LEAD[style] < MARGIN:
                pages.append([])
                y = PAGE_H - MARGIN
            pages[-1].append((chunk, style, int(y)))
            y -= LEAD[style]
        if style in (0, 1):
            y -= 6

    objects = []
    # 1: catalog, 2: pages, then page + content pairs, then font
    n_pages = len(pages)
    font_obj = 3 + 2 * n_pages
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(n_pages))
    objects.append(f"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {n_pages} >>")
    for i, page in enumerate(pages):
        content = []
        for text, style, yy in page:
            size = SIZES[style]
            op = "BT /F1 %d Tf %d %d Td (%s) Tj ET" % (size, MARGIN, yy, _escape(text[:400]))
            content.append(op)
        stream = "\n".join(content).encode("latin-1", "replace")
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
            f"/Resources << /Font << /F1 {font_obj} 0 R >> >> /Contents {4 + 2 * i} 0 R >>"
        )
        objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    # info with title
    info_obj = len(objects) + 1
    objects.append(f"<< /Title ({_escape(title[:200])}) /Producer (AutoCompliance) >>")

    out = [b"%PDF-1.4\n"]
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(b"".join(out)))
        body = obj if isinstance(obj, bytes) else obj.encode("latin-1", "replace")
        out.append(f"{i} 0 obj\n".encode() + body + b"\nendobj\n")
    xref_pos = len(b"".join(out))
    out.append(f"xref\n0 {len(objects) + 1}\n".encode())
    out.append(b"0000000000 65535 f \n")
    for off in offsets:
        out.append(f"{off:010d} 00000 n \n".encode())
    out.append(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info {info_obj} 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF".encode()
    )
    with open(path, "wb") as f:
        f.write(b"".join(out))
    return path


def markdown_to_pdf(md: str, path: str, title: str = "Document") -> str:
    """Convert a markdown string to a PDF file. Returns path."""
    return write_pdf(path, title, markdown_to_pdf_lines(md))
