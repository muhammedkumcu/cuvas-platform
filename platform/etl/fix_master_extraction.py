#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
languages.master.json — deepsearch11 PDF çıkarımının soktuğu SİSTEMİK boşluk-bölme bozukluklarını
düzeltir (curated, kullanıcı onaylı; #53). Ham metin replace: bozuk parçalar YALNIZ değerlerde geçer
(anahtar/yapı değil) → format korunur. Idempotent: düzeltilmiş biçimler bozuk parçayı içermez.
Sıra önemli (uzun/çok-kelimeli önce). Geri kalan TRUNCATION (eksik metin) ayrı ele alınır — bu betik
yalnız boşluk-bölmeyi onarır.
"""
import io, os, sys

PATH = os.path.join(os.path.dirname(__file__), "..", "data", "languages.master.json")

# (bozuk -> doğru) — uzun/çok-kelimeli önce gelir ki kısa kalıplar parçalamasın.
REPS = [
    # --- İngilizce canlılık terimleri (UNESCO/EGIDS etiketi) ---
    ("Nearl y Extin ct", "Nearly Extinct"),
    ("Threa tene d", "Threatened"),
    ("Defini tely", "Definitely"),
    ("Vulne rable", "Vulnerable"),
    ("Shifti ng", "Shifting"),
    ("Sever ely", "Severely"),
    ("Critic ally", "Critically"),
    ("Extin ct", "Extinct"),
    # --- Türkçe bileşik/çok-kelime ---
    ("veri setin de", "veri setinde"),
    ("Stand art", "Standart"),
    ("mevc ut", "mevcut"),
    ("Tarihi -Ölü", "Tarihî · Ölü"),
    ("Tarih i", "Tarihî"),
    ("Lehç e", "Lehçe"),
    ("Tehlik ede", "Tehlikede"),
    ("Para filetik", "Parafiletik"),
    ("Kıpça k", "Kıpçak"),
    ("Kıpç ak", "Kıpçak"),
    ("Noga y", "Nogay"),
    ("Gün ey", "Güney"),
    ("Doğ u", "Doğu"),
    ("Volg a", "Volga"),
    ("Kuze y", "Kuzey"),
    ("Kuma n", "Kuman"),
    ("Kafk as", "Kafkas"),
    ("Sibiry a", "Sibirya"),
    ("Saya n", "Sayan"),
    ("Yenis ey", "Yenisey"),
    ("Karlu k", "Karluk"),
    ("Karl uk", "Karluk"),
    ("Bulg ar", "Bulgar"),
    ("Kript olekt", "Kriptolekt"),
    ("Bölge sel", "Bölgesel"),
    ("Yuna n", "Yunan"),
    ("Çoğu nlukla", "Çoğunlukla"),
    ("Ağırlı klı", "Ağırlıklı"),
    ("Sözl ü", "Sözlü"),
    ("Eski Uygu r", "Eski Uygur"),
    ("Uyg ur", "Uygur"),
    ("Uygu r", "Uygur"),
    ("Orhu n", "Orhun"),
    ("Runi k", "Runik"),
    ("Köke ni", "Kökeni"),
    ("Köke n", "Köken"),
    ("Türkç e", "Türkçe"),
    ("Gene l", "Genel"),
    ("ayrıl ma", "ayrılma"),
    ("düğü mü", "düğümü"),
    ("düğü m", "düğüm"),
    ("varya nt", "varyant"),
    ("Özb ek", "Özbek"),
    ("birleş ik", "birleşik"),
    ("mod el", "model"),
    ("Gag avuz", "Gagavuz"),
    ("Geçi şken", "Geçişken"),
    ("Tartı şmalı", "Tartışmalı"),
    ("metin sel", "metinsel"),
    ("olara k", "olarak"),
    ("Pers- Arap", "Pers-Arap"),
    ("Altay/ Yenisey", "Altay/Yenisey"),
    ("İbrani ,", "İbrani,"),
    ("Azeri )", "Azeri)"),
    # --- 2. batch: büyük-harf/işaret-boşluğu kalanları + dangling ayraç temizliği (truncation'ı
    # FABRİKE ETMEZ; yalnız asılı kalmış " -" / " /" ayraçlarını ve apostrof/parantez boşluğunu temizler) ---
    ("Veri setin de", "Veri setinde"),
    ("2020' de", "2020'de"),
    ("temel ;", "temel;"),
    ("Parafiletik )", "Parafiletik)"),
    ('Shifting / 7 /"', 'Shifting / 7"'),
    ('Oğuz -"', 'Oğuz"'),
    ('Lehçe /"', 'Lehçe"'),
    ('Shifting /"', 'Shifting"'),
    ('Pers-"', 'Pers-Arap"'),
    # --- 3. batch: belirsiz OLMAYAN kesik-kelime tamamlamaları (kaynağın yarıda kestiği kelimeyi
    # bitirir; yeni olgu iddia ETMEZ). Bare "S&R 2020 veri" / "geçiş keni" gibi belirsizler bırakılır. ---
    ('setinde mevc"', 'setinde mevcut."'),
    ('(Geçi"', '(Geçiş)"'),
    ('Türkçe gövd"', 'Türkçe gövdesi."'),
]


def main():
    with io.open(PATH, encoding="utf-8") as f:
        txt = f.read()
    n = 0
    for bad, good in REPS:
        c = txt.count(bad)
        if c:
            txt = txt.replace(bad, good)
            n += c
    with io.open(PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    out = ["fix_master_extraction: {} bosluk-bolme onarildi".format(n)]
    sys.stdout.reconfigure(encoding="utf-8")
    print(out[0])


if __name__ == "__main__":
    main()
