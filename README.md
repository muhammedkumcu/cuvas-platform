# Türk Dilleri Morfoloji Platformu (çalışma adı)

> **Yeni oturum / compact sonrası: önce [`DEVAM.md`](DEVAM.md)'i oku.** Nerede kaldık, ne yapıyoruz, nasıl sürdürülür — tek kaynak.

Açık kaynak, **çift kitleli** bir **Türk dilleri morfoloji + karşılaştırma + araştırma platformu**. ~20 Türk dili için (Apertium FST'leri üzerinden) **morfolojik analiz + üretim + paradigma tabloları + ICALL (oyunlaştırılmış öğrenme)**, diller arası **kognat/ses-denkliği/çok-boyutlu uzaklık ağı**, **dil profilleri + tarih haritası/zaman çizelgesi**. Düşük kaynaklı / tehlikedeki üyelere (Çuvaş, Hakas, Tuva, Saha…) özel önem.

**İki kitle:** (1) **öğrenenler** (çocuk/öğrenci/meraklı) ve (2) **araştırmacılar** — Türk dil dünyasının takip edildiği, "literatür karşınızdaymış gibi" ilk başvuru noktası (birleşik arama, karşılaştırmalı sorgu, dışa aktarım, açık API, kaynak/literatür hub'ı).

**Hedef yayın:** ileri/güçlü bir venue (UBMK/TurkLang dahil; takvime sıkışmadan). **Repo:** github.com/muhammedkumcu/cuvas-platform · **Yol haritası:** [`plan/TODO.md`](plan/TODO.md)

## Klasör yapısı
```
.
├── DEVAM.md                  ← oturum devir notu (ÖNCE BUNU OKU)
├── README.md
├── arastirma/                ← derin araştırma promptları + PDF sonuçları
│   ├── 1-cuvasca-morfoloji.(prompt.md|pdf)
│   ├── 2-egitim-platform.(prompt.md|pdf)
│   ├── 3-turk-dilleri-karsilastirma.(prompt.md|pdf)        (eşzamanlı dilbilim — GELDİ)
│   └── 4-turk-dilleri-tarih-sosyokultur-iliski.prompt.md   (tarih/ilişki + araştırmacı — PDF bekleniyor)
├── plan/
│   ├── TODO.md                       (YOL HARİTASI / canlı todolist)
│   ├── PLATFORM-VIZYON.md            (vizyon/misyon/modüller/ekran haritası — UI için)
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
