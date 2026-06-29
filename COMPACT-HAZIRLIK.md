# COMPACT-HAZIRLIK — her /compact'tan ÖNCE bakılacak kontrol listesi

> **Amaç:** Bağlam (context) sıfırlanmadan önce projenin temiz, izlenebilir ve devam-edilebilir
> bir noktada olduğundan emin olmak. Compact'tan önce bu dosyayı aç, listeyi geç, sonra compact'la.
> **Güncelleme: 28 Haziran 2026.** Bu dosya R8 fazının kalıcı çıktısıdır (kullanıcı isteği).

---

## 1) COMPACT'TAN ÖNCE — kontrol listesi (hepsi ✓ olmalı)

- [ ] **Tree temiz:** `git status --short` boş. Yarım bırakılmış değişiklik yok.
- [ ] **Her şey push'lu:** `git push` sonrası "Everything up-to-date" / `done=0`.
- [ ] **Build temiz:** `python platform/ui/build.py` hatasız; enjeksiyon sayaçları beklenen değerde
      (uyarı/`Traceback` yok). `dist/index.html` yazıldı.
- [ ] **Preview doğrulandı:** son değişiklikler Claude_Preview'da render oluyor, konsol hatası yok.
- [ ] **MD'ler güncel:** `DEVAM.md` §0 ★★★ (en güncel durum + sıradaki), `platform/GELISTIRME-GUNLUGU.md`
      (yeni devam-N girişi), `platform/KAYNAKLAR.md`, `plan/GELECEK-PLANLAR.md`.
- [ ] **Resume promptu hazır:** aşağıdaki §3'teki prompt güncel (sıradaki işe işaret ediyor).

> Bunlardan biri ✗ ise compact'tan önce tamamla. "Yarım iş + compact" = bağlam kaybı riski.

## 2) KIRMIZI ÇİZGİLER — her oturumda geçerli (compact sonrası da)

1. **UYDURMA YOK.** Kaynak + test + doğruluk her şeyin önünde (DEVAM §4.5 felsefe). Kaynak yoksa
   boş/null bırak. "deepsearch" KAYNAK DEĞİL — PDF içindeki gerçek atıfları yaz.
2. **`.dc.html` ELLE DÜZENLENMEZ.** Tüm UI değişiklikleri `platform/ui/build.py` enjeksiyonuyla →
   `dist/index.html`. Tasarım yeniden export edilirse `python platform/ui/build.py` tekrar çalıştır.
3. **Commit'lerde yalnız Muhammed Kumcu** görünür — **Co-Authored-By Claude YOK.**
4. **Commit + push SIK** — her anlamlı adımda (kolay unutuluyor).
5. **Doğal, insan Türkçesi.** Başlıklar temiz isim tamlaması (talimat değil); robotik kalıp yok.
6. **Konsol cp1254:** `print()` içinde `→` (→) ve Kiril ÇÖKERTİR → `->` kullan ya da dosyaya
   yaz + Read. (Dosya/HTML içeriği UTF-8, sorun değil; yalnız `print` çöker.)
7. **Bash cwd kayabilir** (bir `cd` sonrası): build'i mutlak yolla ya da kök dizinden çalıştır.
8. **VM/backend:** canlı API için VM açık + uvicorn çalışır olmalı (DEVAM §4.6 uvicorn tuzağı).

## 3) İŞ DÖNGÜSÜ (compact sonrası standart akış)

`DEVAM.md §0 ★★★ oku` → `build.py'ye yama` → `python platform/ui/build.py` →
`Claude_Preview'da doğrula (reload + ayrı eval, async)` → `ayrı commit + push` → `MD güncelle`.

## 4) ŞU AN NEREDE KALDIK (29 Haz · YAYIN + MOBİL TAM)

**★ PLATFORM CANLI + MOBİL TAM UYUMLU — BİTTİ** (en güncel tek-bakış: **DEVAM §0 ★★★★★ YAYIN+MOBİL** + GELISTIRME-GUNLUGU **devam-33..38**). Tree temiz, push'lu.
- **CANLI:** UI **https://koken-morfoloji.web.app** (Firebase) · API **https://koken-api-1087019161757.europe-west3.run.app** (Cloud Run, sıfıra-inme, soğuk ~1.4sn).
- **GCP:** proje `koken-morfoloji` · `europe-west3` · billing `01642B-2CB63A-E78542` · hesap ymuhammedk61@gmail.com. **Runbook: `deploy/README.md`.**
- **Güvenlik (canlı doğrulandı):** CORS allowlist (evil engellendi ✓) · **rate-limit 600/dk/IP** (60→600, kullanıcı onayı; Karşılaştır ~20 istek/aksiyon) · girdi sınırları · başlıklar · /docs kapalı (404) · non-root · salt-okunur. Env-güdümlü → VM dev AYNI.
- **MOBİL TAM UYUMLU — BİTTİ (v1→v5, devam-34..38):** hamburger drawer + üst-bar (tıklanabilir→home, "KÖKEN Türk Dilleri Atlası + Laboratuvarı") · `overflow-x:hidden` (sayfa yana kaymaz) + zoom:0.92 · 2-sütun→tek · Kognat 2-graf+Tümü kaldır · Paradigma 3-sütun tablo · morfem orantı + aksiyon butonları · Harita touch-pan. **360px 14/14 sıfır taşma, masaüstü değişmedi.**
- **app.py VM↔repo md5 `e42e88be78b3964c6a8e6f7f424c0f15`** (sertleştirme sonrası, eşit). repo dist=localhost (dev); prod dist Firebase'e ayrı build.
- **YENİDEN DEPLOY:** backend → `bash deploy/stage.sh` + `gcloud run deploy --source deploy/_ctx` (CORS env korunur). UI → `KOKEN_API_URL=<api> python platform/ui/build.py` + `firebase deploy --only hosting --project=koken-morfoloji`.
- **SIRADAKİ (kullanıcı: yayından HEMEN sonra):** **C1 ses motoru** (Piper/MMS/eSpeak) → **C3 Ekosistem CRON**. Sonra tüm-dil güçlendirme, Bölüm D, paper.

---

**[ALT: 29 Haz gece-6 — KAYNAKLAR/STATİK COMPARE/20-DİL]**
**★ TÜM İNCELEME + DERİN MORFOLOJİ ONARIMI + UI CİLA BİTTİ** (en güncel tek-bakış: **DEVAM §0 ★★★★★** + GELISTIRME-GUNLUGU **devam-29..32**). Tree temiz, push'lu. **VM app.py deploy md5 senkron (cac90d4).**
- **gece-6 deltaları:** **STATİK COMPARE KALDIRILDI** (Karşılaştır hep dinamik, okuduk вуларӑмӑр/аахтыбыт doğru) · **Tarih per-olay kaynak GERİ** (Tekin/Arat…) + Tarih/Eko sayfa-altı KAYNAKLAR YOK · **KAYNAKLAR açıklama kutusunun ALTINA** (_psrc PAGE_HELP'ten sonra) · Quality "Motor neyi yapabiliyor" combiner-güncel + 1)/2)/3) düz sayı renksiz · **20-dil doğrulama: ham-etiket 0/20.**
Kullanıcının ~50 maddelik inceleme + 3 tur derin geri bildirim BİTTİ:
- **MORFOLOJİ DERİN ONARIM (en kritik):** ① **fiil segment inceltme** (`_segment_verb_align` kümülatif kök+zaman+kişi: geliyorum→gel·iyor·um). ② **ham etiket** (backend TAG_TR 90+, UI humanBadge → sızıntı yok). ③ **KOPULA-BİRLEŞTİRİCİ** (`_copula_combine`+`_tr_copula`: tur şimdiki/gelecek/geniş kişi-çekimli — geliyorum/geleceğim; yalın gövde FST + ek-fiil eki kod, morfofonoloji; COPULA_RULES={tur} probe-gated). ④ **#54 FEATTENSE** dile-duyarlı zaman gate. ⑤ **#55 crosslang** gold round-trip %97 + dinamik-otorite. ⑥ **#56 humanizer** tam denetim (0 kapsanmayan). ⑦ sıfat/zarf/edat analiz+POS.
- **KAYNAKLAR TEK SİSTEM:** chip-strip (`showSrcStrip:false`) KAPALI; tüm KAYNAKLAR **_psrc ekran-id** (12 sayfa, birebir aynı biçim, çift YOK).
- **HARİTA:** gerçek **GeoJSON** kara+ülke sınırları (Natural Earth 110m, `build_map_geojson.py`→`map_geo.py`); eski elle-süsler kaldırıldı, yalnız 5 bölge adı.
- **YENİ BETİKLER:** capability_probe · tense_probe · humanizer_audit_api · compare_consistency_check · build_map_geojson (+ map_geo.py, raporlar).
- **KALAN:** **yayın** (GELECEK-PLANLAR C4: **Cloud Run min-instance** öneri — HF Space uyur; + Cloudflare) · **tüm-dil güçlendirme** (prototip fiil sözlüğü→apertium katkı, OOV; misyon) · **C1 ses** · **C3 CRON** · **Bölüm D** eğitim portalı · paper.
- **DOKUNULMAZ:** Öğren + Araştırmacı Merkezi · Tarih & Köken UI · `.dc.html` (build.py).
- **DERS:** ① kopula-zamanı = yalın gövde (FST) + şahıs eki (kod, morfofonoloji), probe-gated, uydurmasız. ② KAYNAKLAR tek otorite (_psrc ekran-id; iki footer çakışır). ③ fiil segment kümülatif (kelimeyi kes → kopula da bölünür). ④ gerçek GeoJSON varken elle-süs gereksiz. ⑤ her şeyi 20 dilde test.

---

**[ALT: 29 Haz gece-2 — SAYFA-SAYFA İNCELEME BÜYÜK BATCH]**
- Bug'lar (humanizer sızıntı/Analiz senkron/profil renk şeridi [DesignCanvas border-shorthand ezme]/paradigma feedback/crosslang+segment SONLU fiil chv okuduk→вуларӑмӑр) · menü (Öğren çıkar/Hakkında→ana sayfa/Harita↔Tarih) · #53 master 288 PDF-bozukluk · #39 harita · #31/#51 Kaynaklar · Üreteç zaman fallback · humanizer +24. ~33 commit. DERS: DesignCanvas border shorthand→longhand; apertium zaman etiketi dilden dile farklı; ham etiket→humanizer.

---

**[ALT: 28-29 Haz kaydı — İNCELEME R-fazları + MORFOLOJİ ODAĞI]**
**★ İNCELEME (R1-R8 + R6b) + C2 BİTTİ.** Hepsi push'lu, tree temiz.
İnceleme: R5b-2 (47-dil kaynaklı demografi) · R5b-3 (Tarih ds20) · R-AÇIKLAMA (10 sayfa doğal copy) ·
R6/R6b (gerçek atıflar + 50 künye) · R7 (analiz MD) · R8.
**C2 (28 Haz, commit c33ef49): Morfolojik ÜRETEÇ** — analizin tersi (kök+öznitelik→`/generate`→yüzey+`/segment`
morfem dökümü; isim her dilde, fiil tv→iv; üretilemeyende dürüst boş). **+ KRİTİK REGRESYON ONARILDI:**
HERO akıllı-arama runSearch'i değiştirince runParadigm/runCompare/applySegment TANIMSIZ kalmıştı (Paradigma/
Karşılaştır çöküyordu) → anchor'lar kararlı noktalara taşındı, hepsi düzeldi (Preview'da doğrulandı).

**★★ MORFOLOJİ ODAĞI (28-29 Haz, kullanıcı kararı: C1/C3'ten ÖNCE) — TAMAMLANDI.** "en güçlü yerimiz; ölç+genişlet+göster." Plan E/T/G/U (todolist #16-29) BİTTİ:
- **Dil kapsamı 10→20** (B1 bug + E1/E2/E4): tüm apertium Türk dilleri Analiz+Üreteç+Paradigma'da canlı.
- **Ölçüm (T):** E5 round-trip (align %100, recon %92-95) · T1 UniMorph doğruluk (lemma %91-100) · T2 UD ikinci gold (uig "yazı uyumsuz" çözüldü) · T3 sözlük kök sayısı türüne göre (continuation-sınıfı, 20 dil kesin) · **T4 korpus kapsamı 20/20** (FLORES 10 + HF/fineweb-2 10; chv %88, sah %80, alt %33/kjh %29 = dijital yoksulluk).
- **Gösterim (G):** G1 "Kalite & Kapsam" 5-eksen sayfası (Sözlük tıkla-aç POS dökümü · Tutarlılık · Doğruluk UniMorph+UD · Olgunluk · Kapsam 20/20) + G2 sayfa-içi mini rozetler.
- **Entegrasyon (U):** U1 Üreteç dile-duyarlı hâller (Çuvaşça acc yok → soluk) · U2 round-trip köprüsü (Üreteç→"bu biçimi analiz et").
- **DERS/uyarı:** ① VM uvicorn flaky olabilir (10054 connection reset → `bash /root/koken_api/start.sh` ile restart, §4.6). ② **Leipzig bu ortamdan bloke (host timeout/VM refused) → korpus için HF/fineweb-2 kullan** (1000+ dil; düşük-kaynaklılar dahil). ③ Büyük korpus/parquet host'ta (pyarrow var) indir → scp → VM'de FST-direct ölç (HTTP'den hızlı; uvicorn'u yormaz).

**SIRADAKİ:**
- **Kullanıcı siteyi kendi test edip sayfa-sayfa yorum yapacak** → geri bildirim bekle.
- **★ BÖLÜM C:** C1 gerçek ses motoru (Piper/MMS/eSpeak+FastAPI; VM; en büyük lokma) · C3 Ekosistem HfApi-CRON. **Bölüm D — EN SON** (eğitim portalı + Saha/Şor "Dilin Kalbi" şablonu).
- **GELECEK-PLANLAR'da (ne+ne zaman):** OOV→CC0 açık veri · tam-etiket doğruluğu (T5) · apertium'a geri katkı · paper (20 FST birleşik değerlendirme).
- **ÇERÇEVE (DEĞİŞMEZ):** 3 eksen AYRI (tutarlılık≠doğruluk≠kapsam); prototip FST düşük skor=olgunluk, hata değil; her metrik commit'li betik+tarih+kaynak; boşluk gizlenmez işaretlenir.
- **NOT:** VM uvicorn 20 dil FST canlı; `/generate` host'tan çalışır; doğrulama için açık+restart-edilebilir olmalı (§2/§4.6). repo↔VM app.py md5 eşit tut (deploy: scp + start.sh).

## 5) COMPACT SONRASI YAZILACAK RESUME PROMPTU

> **DEVAM.md §0'daki ★★★★★ YAYIN+MOBİL (en üst) bloğunu oku — PLATFORM CANLI + MOBİL TAM UYUMLU: UI
> https://koken-morfoloji.web.app (Firebase) + API https://koken-api-1087019161757.europe-west3.run.app (Cloud
> Run, sıfıra-inme, soğuk ~1.4sn). Tree temiz, push'lu. Detay: GELISTIRME-GUNLUGU devam-33..38, runbook
> deploy/README.md. GCP proje koken-morfoloji / europe-west3 / billing 01642B-2CB63A-E78542. Güvenlik canlı
> doğrulandı: CORS allowlist, rate-limit 600/dk, girdi sınırları, başlıklar, /docs kapalı, non-root, salt-okunur
> — hepsi env-güdümlü (VM dev AYNI). MOBİL (v1→v5): hamburger drawer, overflow-x:hidden (sayfa yana kaymaz),
> Kognat 2-graf+Tümü-kaldır, Paradigma 3-sütun tablo, üst-bar tıklanabilir→home, aksiyon butonları, Harita
> touch-pan — 360px 14/14 sıfır taşma, masaüstü korundu.
> app.py VM↔repo md5 e42e88be (eşit). YENİDEN DEPLOY: backend→`bash deploy/stage.sh`+`gcloud run deploy --source
> deploy/_ctx` (CORS env korunur); UI→`KOKEN_API_URL=<api> python platform/ui/build.py`+`firebase deploy --only
> hosting --project=koken-morfoloji`. repo dist=localhost(dev), prod dist Firebase'e ayrı build.
> **SIRADAKİ (kullanıcı: yayından HEMEN sonra): C1 gerçek ses motoru (Piper/MMS/eSpeak — en büyük lokma) → C3
> Ekosistem HfApi-CRON (küçük).** Sonra: tüm-dil güçlendirme (prototip fiil sözlüğü→apertium katkı/OOV), Bölüm D
> eğitim portalı, paper. DOKUNULMAZ: Öğren+Araştırmacı Merkezi · Tarih UI · .dc.html (build.py). Backend
> değişikliğinde VM'e de scp+start.sh, md5 senkron tut. Önce DEVAM §0 ★★★★★ YAYIN'ı oku, sonra C1'i öner+onayla.**
