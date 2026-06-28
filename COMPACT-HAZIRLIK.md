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

**★ MORFOLOJİ ODAĞI (28 Haz, kullanıcı kararı: C1/C3'ten ÖNCE):** "en güçlü yerimiz; ölç+genişlet+göster." Plan E/T/G/U (todolist #16-29). **YAPILDI:** B1 (Analiz "ev"→Kognat bug'ı; 0d92be3) · E1 (10 yeni FST indi → 20 dil) · E2 (backend 20 dil + QUALITY tier, VM deploy; 4800da1) · E4 (UI 20 dil + Türkmen nom bare-retry; a0ab150). **20 dil Analiz+Üreteç+Paradigma'da canlı.** Round-trip ölçüldü: align %100, yeniden-üretim ~%95.

**SIRADAKİ = morfoloji planı devam:**
- **E3** dil-bazlı özellik envanteri (FST'den) · **E5** round-trip eval 20 dil+fiil.
- **T1** UniMorph DOĞRULUK (öncelik) · **T2** UD kapsam · **T3** lexicon · **T4** korpus *(kaynak Wikipedia DEĞİL → resmi haber/akademik; indirmeden önce kullanıcıya sun)*.
- **G1** Kalite & Kapsam sayfası + **G2** mini rozetler · **U1** Üreteç dile-duyarlı + **U2** çapraz-link/round-trip köprüsü.
- **ÇERÇEVE:** 3 eksen AYRI (tutarlılık≠doğruluk≠kapsam); prototype FST düşük=olgunluk değil hata değil; her metrik commit'li betik+tarih+kaynak; diller-özelinde test.
- **SONRA Bölüm C:** C1 ses motoru (en büyük) · C3 Ekosistem CRON. **Bölüm D — EN SON.**
- **NOT:** VM uvicorn canlı (20 dil FST), `/generate` host'tan çalışıyor; doğrulama için açık kalmalı (§2/§4.6). repo↔VM app.py md5 eşit tutulmalı (deploy: scp + start.sh).

## 5) COMPACT SONRASI YAZILACAK RESUME PROMPTU

> **DEVAM.md §0 ★★★'ı oku (önce `COMPACT-HAZIRLIK.md`'ye de bak). İNCELEME + C2 + morfoloji-odağı B1/E1/E2/E4
> (20 dile genişleme) bitti; morfoloji planından devam — E3/E5 (özellik envanteri + round-trip 20 dil),
> sonra T1 (UniMorph doğruluk) / T2-T4 / G1-G2 / U1-U2. C1/C3 bunlardan SONRA. Önce DEVAM §0'daki YAPILDI'yı
> oku, kaldığımız yeri özetle, plan öner, onayımla devam et.**
