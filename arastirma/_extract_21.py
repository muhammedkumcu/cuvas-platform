# -*- coding: utf-8 -*-
"""ds21 (korpus kaynak haritasi) PDF -> UTF-8 metin."""
import io
import pdfplumber

JOBS = [("21-Türk Dilleri Korpus Kaynak Haritası.pdf", "_korpus21.txt")]
for pdf, out in JOBS:
    chunks = []
    with pdfplumber.open(pdf) as doc:
        n = len(doc.pages)
        for i, page in enumerate(doc.pages):
            chunks.append(f"\n===== SAYFA {i+1}/{n} =====\n{page.extract_text() or ''}")
    io.open(out, "w", encoding="utf-8").write("".join(chunks))
    print("%s: %d sayfa, %d ch" % (pdf[:20], n, len("".join(chunks))))
