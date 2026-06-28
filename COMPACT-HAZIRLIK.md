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

## 4) ŞU AN NEREDE KALDIK (28 Haz)

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

> **DEVAM.md §0 ★★★'ı oku (önce `COMPACT-HAZIRLIK.md`'ye de bak). MORFOLOJİ ODAĞI (dil kapsamı 10→20 + T/G/U
> ölçüm-gösterim-entegrasyon) BİTTİ; site "Kalite & Kapsam" sayfasıyla 20 dilde ölçülü+dürüst. Kullanıcı
> siteyi kendi test edip yorum yapacak — onun geri bildirimini bekle. Sıradaki potansiyel: T4-kalanı (8 dil
> Leipzig, ayrı ortam) ya da Bölüm C (C1 ses motoru / C3 CRON). Önce DEVAM §0'daki YAPILDI'yı oku, kaldığımız
> yeri özetle, kullanıcının test yorumlarını al, plan öner, onayıyla devam et. C1/C3 kullanıcı onayıyla.**
