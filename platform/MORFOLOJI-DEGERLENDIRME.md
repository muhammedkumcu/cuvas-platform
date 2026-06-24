# Morfoloji / Yüzey Bölümleme — Değerlendirme & Kararlar

> Apertium FST'leri **lemma + etiket** verir (ses olayında bile doğru: `kitabımızda → kitap<n><px1pl><loc>`), ama **yüzey hece sınırını** (kitab|ımız|da) vermez. Bu katmanı biz ekliyoruz. Bu belge: yöntem + 10-dil testi + deepsearch kararları + sıradaki işler. İlgili: `arastirma/5*.prompt.md` (deepsearch promptları) + `arastirma/_nlp_araclari.txt`, `_nlp_envanteri.txt` (deepsearch çıktıları).

## Yöntem — Needleman-Wunsch hizalama (deepsearch önerisi, kullanıcı fikrinin matematikselleştirilmişi)
`platform/backend/app.py` → `/segment`:
1. **Tüm analizleri** al; **ALIGN EDEN İSİM** analizini seç (analyses[0] çoğu zaman yanlış POS/fiil verir — bu seçim kritikti).
2. Kümülatif üretim: `lemma<n><nom>` → `<pl><nom>` → `<px><nom>` → `<...><case>` (her biri üretilebilir ara biçim).
3. Ardışık biçimleri **Needleman-Wunsch** ile hizala; **fonolojik puanlama**: aynı=+3, yumuşama çifti (p~b, k~ğ, q~ғ, п~б…)=+2, sesli~sesli=+1, uyumsuz/boşluk=−2.
4. Ek = cur'un, prev'e **önden-çapalı** (k≈len(prev)) en iyi oturan ön-ekinden sonrası → tekrar-altdizi (балалар) ve ünlü düşmesine dayanıklı.
5. **Kök kutusu = SÖZLÜK biçimi (lemma: "kitap")**; ses olayı ayrı **SES OLAYI rozetinde** (`p → b · ünsüz yumuşaması`).
6. **Fallback güvenlik ağı:** hizalama tutmazsa kümülatif/kök+kalan'a düşer → asla çökmez.

**Önemli:** el-yazımı allomorf tablosu GEREKMEZ; tek dil-özel şey fonolojik denklik puanlaması (Türk dilleri geneli, Latin+Kiril+Arap).

## Test — round-trip (`platform/backend/segment_eval.py`, VM'de çalışır)
Bilinen etiketlerden form ÜRET (gold) → `/segment` ile çöz → **yeniden-üretim** (morfemler kelimeyi oluşturuyor mu = GERÇEK doğruluk) + ek-sayısı (etiket sayısına eşit mi = proxy). **10 MVP dili, 1700+ form.**

| dil | form | align% | **yeniden-üretim%** (asıl) | ek-sayı% (proxy) | not |
|----|----:|----:|----:|----:|----|
| aze, kaz, kir, uzb, tat, bak | 105–210 | 100 | ~95 | **100** | tam ayrışım |
| tur | 252 | 100 | 94.8 | 98.8 | çok iyi |
| uig | 189 | 100 | 94.2 | 90.5 | çoğul+iyelik allomorfisinde füzyon |
| sah | 108 | 100 | 92.6 | 82.4 | bazı biçimlerde füzyon |
| chv | 162 | 100 | 93.2 | 75.3 | iyelik+hâl KAYNAŞIK (не) |

> **İki metrik, neden farklı:** `ek-sayı` her çekim etiketi için bir ek bekler (tam ayrışım varsayar). Ama Çuvaşça iyelik+hâl (ҫурт**не**) ve Uygurca çoğul+iyelik (köz**lىrى**m) **gerçekten kaynaşık/allomorfik** → doğru cevap TEK ek. Bu yüzden **yeniden-üretim asıl doğruluk ölçütüdür** ve %92–95'tir. `align%`: analiz-seçimi düzeltmesinden önce kaz %73/tat-bak %88 idi → hepsi %100.
> **chv cila (kaynaşık çöküş):** önce ҫуртне→ҫурт+**чӗ** (sayı tutar ama YANLIŞ, yeniden-üretmez); chain-check eklendikten sonra ҫурт+**не** (DOĞRU, yeniden-üretir). Yani chv yeniden-üretim %72→**93**; ek-sayısı düştü çünkü kaynaşık biçim 2 değil 1 ek (dürüst). Basit çoğul/hâl hâlâ tam ayrışır (хӗр+сем).
> **Fiil bölümleme** (`_segment_verb_align`): kök + kaynaşık zaman·kişi eki + ses olayı (git→gid t→d). Türk dillerinde zaman+kişi portmanteau olduğundan 2-katman dürüst seçim. ("Sadece isimde çalışıyor" sorunu giderildi.)

## Hangi dilde NİYE zorlandık (uzun kuyruk, ~%1–8)
- **uig:** apertium-uig **Arap yazısı** bekler; Latin seed → "0". Arapça girdiyle sorunsuz (`كىتاب+لار+دا`). Test artefaktıydı; gerçek boşluk değil.
- **chv (en zayıf, %7):** Çuvaşça iyelik (px3sp) ve bazı hâl ekleri farklı morfotaktik; kümülatif ara biçimler her zaman temiz hizalanmıyor (`кӗнеки`/`ҫуртне`). Çuvaş-özel ince ayar gerek (çekirdek dilimiz — öncelik).
- **tur (~%1):** **ünlü düşmesi + iyelik** sınıfı (burun→burn, `burnunda` 2 yerine 1 ek). Küçük özel sınıf.
- **sah (~%1):** birkaç kök (`оҕо`) kenar durumu.

## Deepsearch KARARLARI (arastirma/_nlp_araclari.txt + _nlp_envanteri.txt)
- **Yüzey bölümleme:** Türkçe için **Zemberek** altın standart (doğrudan yüzey morfem, Apache-2.0, **JPype** ile; zemberek-python overflow bug'lı) — opsiyonel üst-kalite. Bizim **NW-hizalama** apertium-yerel + **10 dile birden** çalışır → çekirdek yöntem bu. (Morfessor/BPE = uygunsuz; gramer sınırına saygısız.)
- **Diller-arası eşdeğer (★ sıradaki):** **Apertium `.dix` iki-dilli sözlükler** (tur-aze, kaz-tat, tat-bak, tur-kir/tat/uzb, tuk-tur…) GPL-3.0 → boru hattı: `analiz → .dix kök eşle → hedefte AYNI etiketlerle üret`. Deterministik, morfolojik sadık. Doğrudan çift yoksa `networkx` ile pivot (tur→tat→bak). **Savelyev CLDF** (254 kavram, bizde var) = altın-standart fallback. **NLLB/OPUS = RED** (CC-BY-NC + morfoloji kaybı). PanLex/Wiktionary = gürültülü/araştırma.
- **Joshi kaynak sınıfı (0–5)** dil profillerine eklenmeli (misyon: eksik/gelişmişlik): Türkçe 4-5; Kazakça/Özbekçe/Tatarca/Uygurca 2-3; Çuvaşça/Azerice/Türkmence/Başkurtça/Saha 1; çoğu 0.

## SIRADAKİ İŞLER (öncelik)
1. **★ Diller-arası `.dix` karşılaştırma motoru** — en yüksek değer; aranan kelimeyi tüm Türk dillerinde (statik "okuduk" gibi) canlı üret. Parçalar hazır (apertium .dix + Savelyev).
2. **Joshi kaynak sınıfı** → dil profillerine rozet (hızlı, envanter PDF'inden).
3. **Cila:** Çuvaş iyelik morfotaktiği (chv %92→); tur ünlü-düşmesi+iyelik sınıfı; dil-başına fonolojik ince ayar JSON'u.
4. (Opsiyonel) Türkçe **Zemberek** entegrasyonu (JPype) — üst-kalite Türkçe; NW zaten %98.8 verdiği için acil değil.
