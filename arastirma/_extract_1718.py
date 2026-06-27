# -*- coding: utf-8 -*-
"""ds17 (ses denklikleri) + ds18 (kognat) PDF -> UTF-8 metin + tablo dökümü.
cp1254 konsol çökmesini önlemek için yalnız dosyaya yazar."""
import sys, io, json
import pdfplumber

JOBS = [
    ("17-Türk Dilleri Ses Denklikleri.pdf", "_ses17.txt", "_ses17_tablo.txt"),
    ("18Türk Dilleri Kognat Veritabanı.pdf", "_kognat18.txt", "_kognat18_tablo.txt"),
]

for pdf, txt_out, tbl_out in JOBS:
    txt_chunks, tbl_chunks = [], []
    with pdfplumber.open(pdf) as doc:
        n = len(doc.pages)
        for i, page in enumerate(doc.pages):
            t = page.extract_text() or ""
            txt_chunks.append(f"\n===== SAYFA {i+1}/{n} =====\n{t}")
            for ti, table in enumerate(page.extract_tables()):
                tbl_chunks.append(f"\n--- SAYFA {i+1} TABLO {ti+1} ---")
                for row in table:
                    cells = ["" if c is None else str(c).replace("\n", " ").strip() for c in row]
                    tbl_chunks.append(" | ".join(cells))
    with io.open(txt_out, "w", encoding="utf-8") as f:
        f.write("".join(txt_chunks))
    with io.open(tbl_out, "w", encoding="utf-8") as f:
        f.write("\n".join(tbl_chunks))
    # ASCII-safe stdout
    sys.stdout.write(f"{pdf}: {n} sayfa, metin={len(''.join(txt_chunks))} ch, tablo_satir={len(tbl_chunks)}\n")
