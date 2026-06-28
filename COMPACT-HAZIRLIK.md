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

**★ TÜM İNCELEME (R1-R8 + R6b) BİTTİ.** İnceleme notlarından doğan tüm fazlar tamam, push'lu, tree temiz:
R5b-2 (47-dil kaynaklı demografi) · R5b-3 (Tarih ds20 zenginleştirme) · R-AÇIKLAMA (9 sayfa) ·
R6 (Kaynaklar gerçek atıflar) · R6b (Tam kaynakça 50 künye + link) · R7 (analiz MD'leri) · R8 (bu dosya).

**SIRADAKİ = asıl mühendislik (Bölüm C):**
- **C1** gerçek ses motoru (Piper/MMS/eSpeak + FastAPI router; VM gerekir)
- **C2** morfolojik üretim arayüzü (`/generate` backend'de var, UI yok)
- **C3** ekosistem HfApi-CRON (metrik tazeleme)
- Sonra **Bölüm D** (eğitim portalı + Saha/Şor "Dilin Kalbi" şablonu).
- İnce iyileştirmeler: `platform/inceleme/sayfa-sayfa-analiz.md` öncelik özetinde.

## 5) COMPACT SONRASI YAZILACAK RESUME PROMPTU

> **DEVAM.md §0 ★★★'ı oku (önce `COMPACT-HAZIRLIK.md`'ye de bak). İNCELEME (R1-R8) bitti; Bölüm C'den
> başlıyoruz — C1 (gerçek ses motoru) / C2 (morfolojik üretim arayüzü) / C3 (ekosistem CRON) içinden
> hangisinden başlayacağımızı planla, dürüstçe anlat ve onayımla devam et.**
