# Türk Dilleri Morfoloji Platformu (çalışma adı)

> **Yeni oturum / compact sonrası: önce [`DEVAM.md`](DEVAM.md)'i oku.** Nerede kaldık, ne yapıyoruz, nasıl sürdürülür — tek kaynak.

Açık kaynak, **öğrenen-odaklı** bir **Türk dilleri morfoloji + karşılaştırma platformu**. ~20 Türk dili için (Apertium FST'leri üzerinden) **morfolojik analiz + üretim + paradigma tabloları + ICALL (oyunlaştırılmış öğrenme)** ve diller arası **kognat/ses-denkliği karşılaştırma ağı**. Düşük kaynaklı / tehlikedeki üyelere (Çuvaş, Hakas, Tuva, Saha…) özel önem.

**Hedef yayın:** UBMK 2026 (TurkLang track). **Repo:** github.com/muhammedkumcu/cuvas-platform

## Klasör yapısı
```
.
├── DEVAM.md                  ← oturum devir notu (ÖNCE BUNU OKU)
├── README.md
├── arastirma/                ← derin araştırma promptları + PDF sonuçları
│   ├── 1-cuvasca-morfoloji.(prompt.md|pdf)
│   ├── 2-egitim-platform.(prompt.md|pdf)
│   └── 3-turk-dilleri-karsilastirma.prompt.md   (PDF bekleniyor)
├── plan/
│   ├── PLAN.md                       (sprint/plan — kısmen eski, DEVAM güncel)
│   ├── PLATFORM-OZELLIKLERI.md       (özellik listesi)
│   └── YOLCULUK-VE-VAZGECILENLER.md  (ne yaptık, neyden vazgeçtik, NEDEN)
├── platform/                 ← YENİ yön: apertium-temelli çok-dilli platform (inşa edilecek)
│   └── apertium_probe.py             (Linux'ta apertium-chv'yi kanıtlayan probe)
├── arsiv/
│   └── cuvasca-kendi-motor/   ← TERK EDİLEN prototip (kendi Python motorumuz; bkz. YOLCULUK)
└── sources/                  ← klonlanan referans repolar + Hunspell (gitignored)
```

## Mevcut yön (özet)
- **Motor:** Apertium FST'leri (analiz **ve** üretim), turkicnlp + hfst ile, **Linux'ta** çalışır. ~20 Türk dili. (Kanıtlandı — bkz. DEVAM §apertium.)
- **Bizim katman:** öğrenen platformu (paradigma + ICALL) + **karşılaştırma ağı** (kognat/ses-denkliği) + Çuvaşça derin vaka + (sona saklanan) karışık-yazı bulgusu.
- **Önceki kendi-motor prototipi** `arsiv/`'de — neden bıraktığımız `plan/YOLCULUK-VE-VAZGECILENLER.md`'de.
