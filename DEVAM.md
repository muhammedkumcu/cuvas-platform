# DEVAM — Oturum Devir Notu (KÖKEN · Türk Dilleri Morfoloji Platformu)

> **Compact sonrası / yeni oturumda İLK BUNU OKU.** Bu §0 = güncel tek-bakış. Sonra: §2 (VM erişimi), §3 (apertium), §4.5 (FELSEFE), §4.6 (HATALAR+ÇÖZÜMLER), §7 (konvansiyonlar).
> **Güncelleme: 24 Haziran 2026.** Repo: github.com/muhammedkumcu/cuvas-platform (main, push'lu).

---

## 0) ŞU AN NEREDE KALDIK — TEK BAKIŞ

### NE YAPIYORUZ — amaç
**KÖKEN** — "Türk dilleri atlası & laboratuvarı." ~20 Türk dili için Apertium FST'leriyle çalışan, **çift kitleli** açık kaynak **morfoloji + karşılaştırma + araştırma platformu**:
analiz · üretim · paradigma · kognat ağı · ses denkliği · çok-boyutlu uzaklık · dil profilleri · harita · tarih · ICALL.
- **İki kitle:** (1) **öğrenenler** (çocuk/öğrenci) + (2) **araştırmacılar (KRİTİK)** — "literatür karşısındaymış gibi", Türk dil dünyasının takip edildiği, araştırmacının **ilk uğrağı**, işini kolaylaştıran (birleşik sorgu, toplu analiz, dışa aktarım, açık API) merkez.
- Düşük-kaynaklı/**tehlikedeki** üyelere (Çuvaş, Saha, Tuva, Hakas, Şor, Halaç) özel önem (dijital kapsayıcılık misyonu).
- **Felsefe/ilkeler: §4.5 — MUTLAKA OKU.** Akademik hedef: çift-kitleli çok-dilli çok-boyutlu böyle bir platform YOK (apertium=CLI/MT, turkicnlp=dev-kütüphane). Venue: UBMK/TurkLang ya da daha güçlüsü (tarihe sıkışma).

### MİMARİ — 3 katman
1. **Backend (VM/Linux)** — `platform/backend/app.py` (FastAPI), apertium FST sarıcı. Uçlar: `/health /languages /analyze {lang,word} /analyze_all {word} /generate {lang,query} /paradigm/{lang}/{lemma}`. 10 MVP dil FST'si indirilmiş. Host'tan `http://127.0.0.1:8000` (VBox port-forward `koken`:8000 + guest firewalld 8000). **Başlat/durdur + ⚠ uvicorn restart tuzağı: §4.6 + `platform/backend/README.md`.**
2. **Veri (gerçek, locale çekilmiş, kaynaklı)** — `platform/data/*.json` (her dosya `_meta`+lisans):
   `cognates.json` · `languages.geo.json` · `distance.lexical.json` · `distance.typological.json` · `features.wals.json` · `profiles.json` (+AES canlılık) · `intelligibility.json` (Lindsay) · `lang_extra.json` (Wikipedia, 14 dil).
   Çıkarım betikleri: `platform/etl/` (savelyev/glottolog/wals). Ham kaynaklar: `sources/` (gitignored: savelyevturkic, glottolog-cldf, wals, northeuralex, unimorph×9, UD×4). **Provenance defteri: `platform/KAYNAKLAR.md`.**
3. **UI (KÖKEN)** — `platform/ui/`. ⚠⚠ **KURAL: kullanıcının tasarım export'u `Morfoloji Platformu.dc.html` (DesignCanvas; `support.js`=runtime) ELLE DÜZENLENMEZ.** Tüm değişiklikler **`platform/ui/build.py`** ile enjekte edilir → **`dist/index.html`** (çalıştırılabilir). Kullanıcı tasarımı tekrar export edince → `python platform/ui/build.py` tekrar çalıştır. Veri sözleşmesi + modül haritası: `platform/ui/README.md`.

### MODÜL DURUMU (hepsi build.py ile enjekte, Claude_Preview'da doğrulandı)
- ✅ **Dil Profilleri + Canlılık** — Glottolog AES + 14/14 dil Wikipedia zengin metin (çapraz-kontrollü, atıflı). Harita düğümü → profil.
- ✅ **Harita** — 14 dil Glottolog koordinat (şematik projeksiyon).
- ✅ **Uzaklık Gezgini** — **5/5 eksen kaynaklı**: leksikal+filogenetik (Savelyev), tipolojik (WALS), coğrafi (koordinat), anlaşılabilirlik (Lindsay).
- ✅ **Kognat Ağı** — 14 kavram, gerçek kognat setleri+boşluklar (Savelyev). NOT: formlar **karşılaştırmalı transkripsiyon** (kuś, χaraχ); yerel ortografi = **C planı**.
- ✅ **Analiz + Paradigma → CANLI API, herhangi kelime/dil** — bağlam çubuğunda **10-dil seçici** (`searchLang`); Analiz seçili dilde herhangi kelimeyi `/analyze`; Paradigma'da **serbest kök girişi** (örneklerin üstünde) → `/paradigm/<dil>/<kök>`. Graceful fallback (VM kapalıysa illüstratif).
- ✅ **öğrenen/uzman KALDIRILDI** (her şey hep görünür, `isExpert=true`); **script toggle (Кир/Lat) KALDI**. Paradigma başlığı **dinamik** (sabit "Çuvaşça" bug'ı düzeldi).

### ★★ SIRADAKİ İŞ — A→F PLANI (compact sonrası TEK PATCHTE; her adımda commit+push+kontrol)
**Kullanıcı bu planı ve sırayı ONAYLADI.** "tek patchte bitir, aralarda commit atıp kontrolleri yap."
- **A) Multi-dil OTOMATİK analiz** — backend `/analyze_all` ✅ YAZILDI+COMMIT (`c0efe60`) **ama ⚠ VM uvicorn ESKİ kodu servis ediyordu → ÖNCE temiz restart + `/analyze_all` doğrula (§4.6).** UI YAPILACAK: dil seçicide **"⚡ Otomatik (tüm diller)"** seçeneği → `runSearch` otomatik dalı → `/analyze_all` → ilk eşleşen dil aktif + Analiz görünümünde **"bu kelime şu dillerde:"** çip satırı (tıkla → o dile geç). State: `apiMatches`. (FST kök+etiket verir, yüzey-segmentasyon değil — kabul.)
- **B) Araştırmacı Merkezi'ni CANLIYA bağla** — şu an küratörlü WORDS. Serbest kelime girişi + seçili dil → canlı `/analyze` → **gerçek CSV/JSON/CoNLL-U dışa aktarım**.
- **C) Kognat yerel ortografi** — Savelyev formları Latin transkripsiyon (kuś, χaraχ). Doğru yerel-script türetmek zor (kaynak vermiyor) → **okunur transkripsiyon temizliği** (χ→h, ɕ→ś, ŋ→ñ, ʃ→ş, ɣ→ğ, ɯ→ı …) + "karşılaştırmalı biçim" etiketi (dürüst).
- **D) Karşılaştır "dizilim" sekmesi canlı** — aranan kelimeyi diller-arası analiz (`analyze_all`). Sınırlı (FST kök+etiket).
- **E) Tarih & Köken kaynaklı genişletme** — `#4`/Glottolog'dan kaynaklı zaman çizelgesi olayları/profil notları.
- **F) Kaynaklar 'demo' temizliği** — kullanılmayan 'demo' SOURCES kaydını çıkar.

> Her adım döngüsü: `build.py`'ye yama → `python platform/ui/build.py` → Claude_Preview'da doğrula → commit+push. **Preview: reload/click sonrası eval ASYNC — bir tık sonra tekrar oku.**

### OKUNMASI GEREKEN MD'LER (sırayla)
1. **Bu DEVAM.md** — özellikle §0, §2 (VM), §3 (apertium), §4.5 (felsefe), §4.6 (hatalar), §7.
2. `platform/ui/README.md` — UI veri sözleşmesi + **build.py workflow** (kritik: .dc.html elle düzenlenmez).
3. `platform/KAYNAKLAR.md` — kaynak/lisans defteri (provenance).
4. `platform/backend/README.md` — API başlat/durdur/erişim.
5. `plan/TODO.md` (yol haritası, A→F işli) · `plan/PLATFORM-VIZYON.md` (vizyon/modüller/ekran haritası) · `plan/GELECEK-PLANLAR.md` (çocuk eğitim portalı — onaylı, yatay ölçek sonrası) · `plan/YOLCULUK-VE-VAZGECILENLER.md` (ne bıraktık+neden).

### KRİTİK HATIRLATMALAR
- Commit'lerde **yalnız kullanıcı (Muhammed Kumcu)** görünür — **Co-Authored-By Claude YOK**.
- **`.dc.html` ELLE DÜZENLENMEZ** → her şey `build.py`. Siteyi BOZMA (güzel tasarım); değişiklikleri abartma, net olanları yap.
- **Kaynak ilkesi:** PDF doğrudan veri değil; işaret ettiği veri setini locale çek, çapraz-kontrol et (özellikle Wikipedia), atıf+lisans ver, **uydurma yok** (kaynak yoksa null/boş bırak).
- **Önce dikey (MVP sağlam+kaliteli), SONRA yatay (tüm Türk dillerine ölçek).** Yatay ölçek EN SON.
- Canlı API için **VM açık + uvicorn çalışır** olmalı.

---

## 1) PROJE (özet)
Açık kaynak, çift-kitleli (öğrenen+araştırmacı) **Türk dilleri morfoloji + karşılaştırma + araştırma platformu**. Diller (apertium morph backend): **chv tur aze tuk gag crh tat bak kaz kir kaa krc kum nog uzb uig alt kjh tyv sah** (+klj kısmi). MVP 10: tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah.

---

## 2) ORTAM — VM/APERTIUM ERİŞİMİ (KRİTİK)
- **Proje kökü (Windows/host):** `C:\Users\Tombulteke\Desktop\cuvas-guncelleme`
- **Windows'ta apertium ÇALIŞMAZ** (`pip install hfst` derlenmez). **Geliştirme/canlı API Linux VM'de.**
- **VM:** VirtualBox `RHEL9-Bootcamp` (RHEL 9.8, Python 3.9). Host'tan SSH:
  ```bash
  ssh -i ~/.ssh/cuvas_vm -p 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1
  ```
  - NAT port-forward (host 2222→guest 22) + (host 8000→guest 8000, adı `koken`). VM kapanırsa tekrar gerekebilir:
    `VBoxManage controlvm "RHEL9-Bootcamp" natpf1 "ssh,tcp,127.0.0.1,2222,,22"` / `... "koken,tcp,127.0.0.1,8000,,8000"`.
  - venv: `/root/apv` (hfst+turkicnlp+fastapi+uvicorn). FST'ler `/root/.turkicnlp/models/`. API kodu: `/root/koken_api/app.py`.
  - guest firewalld'de 8000 açık (`firewall-cmd --add-port=8000/tcp --permanent`).
- `VBoxManage` host'ta: `/c/Program Files/Oracle/VirtualBox/VBoxManage.exe`. `gh` (host) `muhammedkumcu` authenticated.

---

## 3) APERTIUM / BACKEND — NASIL ÇALIŞIR (kanıtlanmış)
- FST yolları: `~/.turkicnlp/models/<dil>/<script>/morph/apertium/<dil>.{automorf|autogen}.hfst` (analiz | üretim).
- İndirme (yalnız morph, nöral modeller DEĞİL): `turkicnlp.download(lang, processors=['morph'], script=<Latn|Cyrl|Arab>)`.
- Düşük seviye: `hfst.HfstInputStream(path).read().lookup("кӗнеке<n><pl><dat>")` → `[('кӗнекесене',0.0)]`.
- **API başlat (VM'de) — TEMİZ restart (§4.6'daki tuzağa dikkat):**
  ```bash
  ssh ... 'pkill -9 -f "uvicorn app:app"; sleep 2; cd /root/koken_api && setsid /root/apv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 >uvicorn.log 2>&1 </dev/null & '
  # SONRA VM-İÇİ doğrula: ssh ... 'curl -s http://127.0.0.1:8000/health'  (host'tan önce!)
  ```

---

## 4) PİVOT GEÇMİŞİ (kısa)
- **Faz 1 (terk):** Türkmence kendi-motorunu Çuvaşça için tekrarladık → `arsiv/cuvasca-kendi-motor/` (Python motor, %75 kapsam, **karışık-yazı %45.85 bulgusu** — sona saklandı). Detay: `plan/YOLCULUK-VE-VAZGECILENLER.md`.
- **Kırılma:** apertium olgun + Linux'ta çalışıyor → kendi motor gereksizdi (kullanıcı haklıydı).
- **Pivot:** çok-dilli apertium platformu + karşılaştırma ağı (kullanıcı fikri).

## 4.5) FELSEFE & İLKELER (yön bunlardan çıkar)
- **Olgun açık kaynağı yeniden icat etme** → üstüne değer kat (erişilebilirlik, pedagoji, karşılaştırma).
- **Düşük-kaynak/tehlikedeki Türk dilleri için dijital kapsayıcılık.**
- **Apertium = motor (rakip değil); biz = erişilebilirlik + öğrenme + karşılaştırma + araştırma katmanı.** Hatalar yüzeye çıkınca apertium'a geri katkı.
- **Gerçek kaynak, locale çek, çapraz-kontrol, atıf+lisans, UYDURMA YOK.** PDF'ler pusula; veri PDF'in işaret ettiği setlerden.
- **Kanıtla, iddia etme** (empirik test).
- **Önce dikey (MVP sağlam), sonra yatay (ölçek).** Siteyi bozma; değişiklik abartma.

## 4.6) HATALAR & ÇÖZÜMLER (tekrar düşmemek için)
- **Apertium "kullanılamaz" YANLIŞTI** → Windows'ta hfst yok ≠ apertium yok; **Linux VM**. DERS: ortam-engelini genel imkânsızlık sanma.
- **⚠ uvicorn ESKİ kod tuzağı (YENİ):** Çok önceki bir turda `setsid uvicorn ... &` bir SSH komutunda başlatıldı ve harness o kanalı **uzun süre arka planda tuttu** (pid 6157/6159); app.py değişince **eski uvicorn ESKİ kodu servis etmeye devam etti** (404 /analyze_all). ÇÖZÜM: `pkill -9 -f "uvicorn app:app"; sleep 2; setsid ... uvicorn ... </dev/null &` → **VM-İÇİ `curl localhost:8000/health` ile doğrula, SONRA host'tan test et.** Host'tan "connection reset/10054" = uvicorn down. DERS: kanalı tutan uvicorn-start komutları sorun; her zaman temiz pkill+restart+VM-içi doğrula.
- **build.py string-yama yaklaşımı:** `.dc.html` elle düzenlenmez; build.py'de **birebir string** eşleşmesi gerekir. Apostrof: tasarımcı **kıvrık ' (U+2019)** kullanmış → ASCII ' ile eşleşmez. Apostrof içeren metni JS'e enjekte ederken **`json.dumps`** kullan (çift tırnak, güvenli). Eşleşme tutmazsa build.py uyarı basar.
- **Claude_Preview async:** `location.reload()`/`click()` sonrası eval HEMEN okursa boş döner (render async) → bir eval sonra tekrar oku. `<select>`/`<input>` simülasyonu: `el.value=...; el.dispatchEvent(new Event('input',{bubbles:true}))` (+ Enter için `KeyboardEvent('keydown',{key:'Enter',bubbles:true})`).
- **Windows konsol (cp1254) Türkçe ı/ş + Kiril'i bozar** → dosyaya UTF-8 yaz, `Read`/python (`sys.stdout.reconfigure(encoding='utf-8')`) ile doğrula; konsola güvenme.
- **Güvenlik classifier:** public repo / kalıcı-uzaktan-erişim engellenebilir → kullanıcı açık onayıyla yap, BYPASS etme.
- **Ölü host → Wayback Machine** (web.archive.org) dene. **Windows git CRLF uyarıları** zararsız.

---

## 5) ARAŞTIRMA TEMELİ (`arastirma/`) — HEPSİ ELDE
- **1-cuvasca-morfoloji**, **2-egitim-platform** (prompt+pdf) — eski faz/konumlandırma.
- **3-turk-dilleri-karsilastirma** (+pdf) — eşzamanlı dilbilim çekirdeği (ses denklikleri, paradigmalar, kognatlar, veri envanteri).
- **3b-karsilastirma-agi-temeli** (pdf) — ÜRÜN/MÜHENDİSLİK (3-katman veri mimarisi, **FST olgunluk seviyeleri**, MVP seti, veri setleri+lisans).
- **4-turk-dilleri-tarih-sosyokultur-iliski** (+pdf) — tarih/sosyokültür/ilişki (profiller, AES, **uzaklık matrisleri J.1-3**, areal, genetik-vs-dil, araştırmacı ekosistemi).
- **4-KONUDISI-...pdf** = misfire (metodoloji denemesi), içerik için KULLANILMAZ.
- Çıkarılmış metinler `_research*_text.txt` (gitignored).

## 6) KLASÖR HARİTASI
```
DEVAM.md · README.md
arastirma/   1..4 prompt.md + pdf'ler · _*.txt (gitignored)
plan/        TODO.md · PLATFORM-VIZYON.md · GELECEK-PLANLAR.md · YOLCULUK-VE-VAZGECILENLER.md · PLAN.md · PLATFORM-OZELLIKLERI.md
platform/
  backend/   app.py (FastAPI) · README.md · requirements.txt
  ui/        Morfoloji Platformu.dc.html (TASARIM, elle düzenleme!) · support.js (runtime) · build.py (ENJEKSİYON) · dist/index.html (çalışır) · README.md · screenshots/(eski)
  data/      *.json (çıkarılmış kaynaklı veri)
  etl/       savelyev_extract.py · glottolog_extract.py · wals_extract.py
  KAYNAKLAR.md · NOTLAR.md · apertium_probe.py
arsiv/cuvasca-kendi-motor/   (terk edilen Python motor)
sources/     (gitignored) savelyevturkic · glottolog-cldf · wals · northeuralex · unimorph* · UD_* · apertium-chv · hunspell_cv …
.claude/launch.json   (Claude_Preview "koken" :8090)
```

## 7) KONVANSİYONLAR / TUZAKLAR
- **Commit'lerde Claude GÖRÜNMEZ** (Co-Authored-By YOK). Yazar = Muhammed Kumcu. Her adımda commit+push.
- **`.dc.html` elle düzenlenmez** → build.py. Önizleme: `python -m http.server 8080` (repo kökü) → `http://127.0.0.1:8080/platform/ui/dist/index.html`.
- **gh** `muhammedkumcu` authenticated. Repo public. Deploy/uzaktan-erişim = classifier engelleyebilir → açık onay.
- Türkmence klasörü (`Desktop/turkmence-guncelleme`) = kullanıcının AYRI projesi; DOKUNMA (push yetkisi de yok, 403).
- md'leri güncel tut (iş ilerledikçe DEVAM.md + plan/TODO.md).

## 8) HEMEN BAŞLAMAK İÇİN (yeni oturum)
1. §0 (A→F planı) + §2 (VM) + §3 (API restart) + §4.5 (felsefe) + §4.6 (hatalar, özellikle uvicorn) oku.
2. **VM'i kontrol et + uvicorn temiz restart + `/analyze_all` doğrula** (A planının ön şartı).
3. A→F'yi sırayla uygula: her adım build.py → `python platform/ui/build.py` → Claude_Preview doğrula → commit+push.
4. Yatay ölçek YOK (MVP bitene kadar).

## 9) COMPACT SONRASI — KULLANICININ GÖNDERECEĞİ ÖRNEK PROMPT
```
cuvas-guncelleme projesindeyiz. Önce DEVAM.md'yi oku (§0 A→F planı + §2 VM + §3 API restart + §4.5 felsefe + §4.6 hatalar).
KÖKEN = ~20 Türk dili morfoloji+karşılaştırma+araştırma platformu; backend VM'de canlı (apertium), UI build.py ile
dist/index.html'e enjekte (.dc.html ELLE DÜZENLENMEZ). Şimdi: A→F planını TEK PATCHTE, aralarda commit+kontrol ile bitir.
Önce VM uvicorn'u temiz restart edip /analyze_all'ı doğrula, sonra A (multi-dil otomatik) UI'sini yap. Commit'lerde Claude görünmesin.
```
