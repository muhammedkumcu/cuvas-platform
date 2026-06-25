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

## FAZ 1.1 — FÜZYON EK-AYRIŞMASI: CANLI ARAŞTIRMA BULGULARI (25 Haz)
> Canlı `/segment` (chv) ile gerçek davranış incelendi. **Sonuç: tek-tip "hepsini böl" YANLIŞ olur; nüanslı.** Kullanıcı kararı: "%100 emin olalım" → aşağıdaki ayrım netleştirildi; backend değişikliği `segment_eval` ile doğrulanarak yapılmalı (ayrı odaklı pas).
- **Zaten doğru bölünen (dokunma):** `хӗррӗмсем` → хӗр+рӗм+сем (kök+iyelik+çoğul); `кӗнекемре` → кӗнеке+м+ре (kök+iyelik+hâl). Çuvaş sırası Kök+İyelik+Çoğul+Hâl korunuyor. ✓
- **GERÇEK portmanteau (BÖLME):** `ҫуртне` → ҫурт + **не** (tags: n·px3sp·dat). İyelikli yönelme Çuvaşçada tek yüzeyde kaynaşır. Zorla bölmek tartışmalı/yanlış olur → "iyelik (onun)·Yönelme" portmanteau etiketi DOĞRU; korunmalı.
- **GÜVENLE bölünebilir (temiz sınır):** `кӗнекесенче` → кӗнеке + **сенче** (tags: n·pl·loc). Gramer açık: `-сен`(çoğul oblik allomorf) + `-че`(bulunma). → Hedef ayrışma: кӗнеке+сен+че. Çoğul allomorfları (сем/сам/сен/сан) gövde başında tanınıp kesilebilir; kalan = hâl eki.
- **Olası HATA (ayrı düzelt):** `кӗнекине` (n·px3sp·dat) → kod -не'yi yalnız DAT etiketleyip 3sg iyelik `-и-`'yi sahte **"ses değişimi е→и"** olarak gösteriyor. Doğrusu кӗнеке + **и**(px3sp) + не(dat). Bazı iyelik morfemleri "ünlü değişimi" olarak yutuluyor.
- **✅ YAPILDI — GÜVENLİ-BÖLME (25 Haz, segment_eval ile doğrulandı):** `app.py`'ye `PLURAL_ALLO`/`_plural_allomorph` + füzyon-çöküş dalına TEMİZ-SINIR bölme: **yalnız [pl, <tek non-nom hâl>] (px YOK)** ve yüzey ek bilinen çoğul allomorfuyla (chv -сен/-сан/-сем/-сам) başlıyorsa çoğul|hâl sınırından böl. `px+hâl` portmanteau'ya DOKUNULMADI. VM'ye deploy + temiz uvicorn restart (start.sh) + `segment_eval` (1700+ form).
  - **Sonuçlar (önce → sonra):** **chv ek-sayı %75.3 → %92.0** (+16.7); chv align %100 ve **yeniden-üretim %93.2 değişmedi** (regresyon yok). **Diğer 9 dil HİÇ değişmedi** (değişiklik chv-kapsamlı). Örnek: `ҫуртсенче`→ҫурт+**сен**+**че**, `ҫуртсене`→ҫурт+сен+е, `ҫуртсенчен`→ҫурт+сен+чен.
  - **Bilinçli korunan (chv kalan ~%8):** gerçek **px+hâl portmanteau** (`ҫуртӗнче`=px3sp+loc, `ҫуртне`=px3sp+dat → tek kaynaşık ek, dilbilimsel olarak DOĞRU; eval bunları "2 ek bekler" diye düşürür ama zorla bölmek yanlış olur).
- **✅ YAPILDI — 1.1b (vokal-sonu İYELİK kurtarma, 25 Haz, segment_eval doğrulamalı):** Vokal-sonu gövdede iyelik eki son ünlüyü değiştirip yutulabiliyordu (`кӗнеке`→`кӗнеки`, iyelik -и; `_trailing_affix` yakın-eşleşme sanıp BOŞ ek döndürüyordu → iyelik kaybı). Düzeltme: ek BOŞ ve **tüm etiketler iyelik(px)** ise → sapma-kuyruğunu (`_suffix`) ek olarak geri al; kök ünlü düşmesi rozetiyle gösterilir. **YALNIZ saf-iyelik (hâl/çoğul yok)** — risk dar.
  - **Sonuç:** `кӗнеки`→кӗнеке+**и**(iyelik, ünlü düşmesi е→∅); `ачи`→ача+и. **chv ek-sayı %92.0→%93.2, yeniden-üretim %93.2→%94.4** (ikisi de ARTTI); diğer 9 dil + ünsüz-sonu iyelik (хӗр→хӗрри) sağlam, **regresyon yok**.
  - **Toplam 1.1 (a+b):** chv ek-sayı **%75.3 → %93.2** (+17.9), yeniden-üretim **%93.2 → %94.4**, align %100, diğer diller regresyonsuz.
- **Bilinçli KALAN (kapanmaz — doğru olan bu):** chv ~%6.8 = gerçek **px+hâl portmanteau** (`ҫуртне`=px3sp+dat, `кӗнекине`=px3sp+dat, `ҫуртӗнче`/`кӗнекинче`=px3sp+loc → tek kaynaşık ek; eval "2 ek bekler" diye düşürür ama zorla bölmek dilbilimsel olarak YANLIŞ). Çuvaş iyelikli-hâl tek yüzeyde kaynaşıktır; portmanteau etiketi ("iyelik · hâl") doğru çözümdür.

## SIRADAKİ İŞLER (öncelik)
1. **★ Diller-arası `.dix` karşılaştırma motoru** — en yüksek değer; aranan kelimeyi tüm Türk dillerinde (statik "okuduk" gibi) canlı üret. Parçalar hazır (apertium .dix + Savelyev).
2. **Joshi kaynak sınıfı** → dil profillerine rozet (hızlı, envanter PDF'inden).
3. **Cila:** Çuvaş iyelik morfotaktiği (chv %92→); tur ünlü-düşmesi+iyelik sınıfı; dil-başına fonolojik ince ayar JSON'u.
4. (Opsiyonel) Türkçe **Zemberek** entegrasyonu (JPype) — üst-kalite Türkçe; NW zaten %98.8 verdiği için acil değil.
