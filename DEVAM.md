# DEVAM — Oturum Devir Notu (Türk Dilleri Morfoloji Platformu)

> Yeni oturumda / compact sonrası **İLK BUNU OKU.** Nerede kaldık, sıradaki iş, nasıl sürdürülür — tek kaynak.
> Sonra ihtiyaca göre: `plan/YOLCULUK-VE-VAZGECILENLER.md` (ne bıraktık+neden), `arastirma/*.prompt.md` (3 derin araştırma),
> `platform/NOTLAR.md` (apertium nasıl kullanılır), `plan/PLATFORM-OZELLIKLERI.md`.
> **Güncelleme: 24 Haziran 2026 (2. tur).** §0=güncel durum+sıradaki · §2=VM/apertium ERİŞİMİ (kritik) · §4.6=hatalar/dersler — KAYBOLMASIN · §9=compact sonrası örnek prompt.
> Yol haritası/todolist: [`plan/TODO.md`](plan/TODO.md). Araştırma promptları: `arastirma/1..4-*.prompt.md`.

---

## 0) ŞU AN NEREDE KALDIK — TEK BAKIŞ (24 Haz 2026)

**BÜYÜK PİVOT YAPILDI.** Proje artık: *tek dilli "kendi Python motoru" Çuvaşça analizör* DEĞİL → **~20 Türk dili için Apertium-temelli, öğrenen-odaklı morfoloji + KARŞILAŞTIRMA platformu.**

- **Motor kararı KESİN:** Apertium FST'leri (analiz **ve** üretim), `turkicnlp`+`hfst` ile, **Linux'ta** çalışır. ~20 Türk dili. **KANITLANDI** (VM'de canlı test — §3).
- **Kendi Python motorumuz TERK EDİLDİ** → `arsiv/cuvasca-kendi-motor/` (neden: `plan/YOLCULUK-VE-VAZGECILENLER.md`). Saklanan varlık: **karışık-yazı kirliliği bulgusu %45.85** (sona saklandı, kullanıcı kararı).
- **Klasör YENİDEN DÜZENLENDİ** (24 Haz): `arastirma/` · `plan/` · `platform/` · `arsiv/`. Kök sade.
- **Repo temiz + push'lu:** github.com/muhammedkumcu/cuvas-platform (main). Commit'lerde **yalnız kullanıcı** görünür (Co-Authored-By Claude YOK — §7).

### ★ ÇİFT KİTLE & TAKVİM (24 Haz, 2. tur kararları)
- **İki hedef kitle:** (1) **Öğrenenler** (çocuk/öğrenci/meraklı) + (2) **Araştırmacılar (KRİTİK):** "literatür karşılarındaymış gibi", **Türk dil dünyasının takip edildiği**, araştırmacının **ilk uğrayacağı**, işini gerçekten kolaylaştıran (birleşik arama, karşılaştırmalı sorgu, toplu üretim/analiz, dışa aktarım, açık API, kaynak/literatür hub'ı) **çözüm‑odaklı merkez.**
- **Takvim:** Platformun hakkını ver; **30 Haziran UBMK son tarihine SIKIŞMA** (yetişirsek sunarız). Daha ileri/güçlü venue hedefle. "Tarih yokmuşçasına" sağlam çalış.
- **MVP dilleri (KESİN):** 5-kol 10 dil → **tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah** → sonra 20'ye ölçekle.

### ★ SIRADAKİ İŞ (compact sonrası buradan devam) — bkz. [`plan/TODO.md`](plan/TODO.md)
**ARAŞTIRMA FAZI TAMAM — sırada MİMARİ tasarımı (BİRLİKTE).**
1. **Elde 3 geçerli derleme** (`arastirma/`):
   - `3-turk-dilleri-karsilastirma.pdf` (#3, eşzamanlı dilbilim, 26 sf/108 kaynak: ses denklikleri, paradigmalar, kognatlar, veri envanteri).
   - `3b-karsilastirma-agi-temeli.pdf` (#3'ün 2. motoru — **ÜRÜN/MÜHENDİSLİK odaklı**: 3-katman veri mimarisi, **Apertium FST olgunluk seviyeleri** [prod: tat/sah/kaz/tur/kir/crh/tyv · working: chv/uzb/bak/kaa/uig/krc/gag/kum · proto: aze/tuk/nog/kjh/alt], SavelyevTurkic CLDF + NorthEuraLex veri setleri+lisans, core/extended hal DB tasarımı, önerilen MVP seti).
   - `4-turk-dilleri-tarih-sosyokultur-iliski.pdf` (#4, 24 sf/68 kaynak: tarih, 20-dil profili, alfabe reformu, canlılık/EGIDS+Joshi, Altay tartışması, areal, kültür/destan, genetik-vs-dil, **çok-boyutlu uzaklık matrisleri J.1-3**, araştırmacı ekosistemi, 20-dil profil matrisi).
2. **NOT (misfire):** `4-KONUDISI-derin-arastirma-metodolojisi.pdf` = bir motor promptu YANLIŞ anlayıp "derin araştırma nedir" metodoloji denemesi yazmış (PRISMA/Cochrane/KVKK). İçerik için KULLANILMAZ; kayıt için duruyor.
3. **KARARLAR KİLİTLENDİ:** MVP = 5-kol 10 dil (tur,aze,kaz,kir,uzb,uig,tat,bak,chv,sah) · ilk dilim = morfoloji çekirdeği · FastAPI+SQLite+açık API · **UI'yı kullanıcı veriyor.** Vizyon: `plan/PLATFORM-VIZYON.md`.

### ★★ UI GELDİ — KÖKEN (24 Haz, 3. tur) — ŞİMDİ BURADAN DEVAM
- **UI entegre edildi** → `platform/ui/` ("KÖKEN — Türk dilleri atlası & laboratuvarı"). DesignCanvas prototipi (`Morfoloji Platformu.dc.html` + `support.js` runtime). **Güncel hâl KODDA** (screenshots ESKİ). Tam modül seti + 14 dil profili + öğrenen/uzman modu + Kiril/Latin translit + **yerleşik SOURCES/USAGE kaynak-kütüğü** (her veride lisans, "⚠ örnek/illüstratif" rozeti). Veri şu an **illüstratif**.
- **Kullanıcı ilkesi (KRİTİK):** kaynaklar çok önemli → **doğrudan kaynakları belirt + locale çek + incele**, uydurma yok. → `platform/KAYNAKLAR.md` (provenance defteri) + `platform/ui/README.md` (veri sözleşmesi).
- **İlk kaynak çekildi:** `sources/savelyevturkic` (SavelyevTurkic CLDF, CC BY 4.0): 32 dil (10 MVP'nin hepsi var) + glottocode/ISO/**lat-long** + 254 kavram + 8360 form + 8360 kognat yargısı. → Kognat Ağı + Harita + Uzaklık(leksikal) gerçek veri kaynağı.
### ★★★ VERİ + BACKEND CANLI (24 Haz, 4. tur) — BURADAN DEVAM
- **Kaynak hasadı + ÇIKARIM YAPILDI (hepsi kaynaklı, `_meta` ile):** `platform/data/` →
  - `cognates.json` (SavelyevTurkic CLDF, 254 kavram/905 kognat seti) · `languages.geo.json` (32 dil lat/lon/kol) · `distance.lexical.json` (32×32 derin-kognat mesafe)
  - `profiles.json` (Glottolog, 23 dil + **AES canlılık** EGIDS/UNESCO eşlemeli) · `distance.typological.json` + `features.wals.json` (WALS, 192 özellik)
  - Çıkarım betikleri: `platform/etl/` (savelyev/glottolog/wals). Hasat: `sources/` (savelyevturkic, glottolog-cldf, northeuralex, wals, unimorph×9, UD×4). Defter: `platform/KAYNAKLAR.md`.
- **BACKEND CANLI (VM):** `platform/backend/app.py` (FastAPI) → MVP 10 dil için **apertium analiz + üretim + paradigma**. Host'tan `http://127.0.0.1:8000` (VBox port-forward `koken` 8000 + guest firewalld 8000 açık). Test: tur/chv/kaz/sah analiz, chv üretim (`кӗнеке<n><pl><dat>→кӗнекесене`) + paradigma. Her yanıt `_source` (Apertium GPL-3.0). **Başlat/durdur + erişim: `platform/backend/README.md`.**
  - Hızlı başlat (VM kapanıp açılırsa uvicorn'u tekrar başlat): `ssh ... 'cd /root/koken_api && setsid /root/apv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 < /dev/null &'`
- **SIRADAKİ:** (a) **UI'yı bağla** — Analiz/Paradigma/Üretim → API (`fetch` 127.0.0.1:8000); Kognat/Harita/Uzaklık/Profil/Canlılık → `platform/data/*.json`; bağlanan modülde **"⚠ örnek" rozetini kaldır**. (b) kalan çıkarım: UniMorph→paradigma, UD→analiz bağlamı, #4→filogenetik+anlaşılabilirlik mesafe eksenleri. (c) transliterasyon + araştırmacı uçları (dışa aktarım, API doc).
5. **Sona:** UniMorph/UD/Wiktionary değerlendirme + karışık‑yazı bulgusu + Çuvaşça derin vaka + paper.

> Akademik katkı (gap): **Türk dilleri için çift‑kitleli (öğrenen + araştırmacı), çok‑dilli, çok‑boyutlu morfoloji + karşılaştırma + araştırma merkezi YOK** (apertium=CLI/MT, turkicnlp=dev‑kütüphane). Onu açıyoruz + karşılaştırma/uzaklık ağı + araştırmacı hub'ı + (sona) karışık‑yazı.

---

## 1) PROJE
**Açık kaynak, öğrenen-odaklı Türk dilleri morfoloji + karşılaştırma platformu.** ~20 dil için (Apertium FST): analiz + üretim + paradigma + ICALL (oyunlaştırılmış öğrenme) + **diller arası kognat/ses-denkliği karşılaştırma ağı**. Düşük kaynaklı/tehlikedeki üyelere (Çuvaş, Hakas, Tuva, Saha…) önem. **Hedef:** UBMK 2026 / TurkLang. Repo: `muhammedkumcu/cuvas-platform`.

Diller (apertium morph): **chv tur aze tuk gag crh tat bak kaz kir kaa krc kum nog uzb uig alt kjh tyv sah** (+klj kısmi).

---

## 2) ORTAM — VM/APERTIUM ERİŞİMİ (KRİTİK)
- **Proje kökü (Windows/host):** `C:\Users\Tombulteke\Desktop\cuvas-guncelleme`
- **Windows'ta apertium ÇALIŞMAZ** (`pip install hfst` wheel-build hatası, C++ derleme). **Geliştirme Linux VM'de yapılır.**
- **VM:** VirtualBox `RHEL9-Bootcamp` (RHEL 9.8, Python 3.9, 4 CPU, 7.6GB). Host'tan **SSH ERİŞİMİ KURULU:**
  ```bash
  ssh -i ~/.ssh/cuvas_vm -p 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1
  ```
  - VirtualBox NAT port-yönlendirme (host 2222 → guest 22) host'tan eklenmişti:
    `VBoxManage controlvm "RHEL9-Bootcamp" natpf1 "ssh,tcp,127.0.0.1,2222,,22"` (kalıcı; VM kapanırsa tekrar gerekebilir).
  - Anahtar: `~/.ssh/cuvas_vm` (host). VM'de `/root/.ssh/authorized_keys`. (Kullanıcı isterse anahtarı silip erişimi geri alabilir.)
  - **apertium venv VM'de hazır:** `/root/apv` (`hfst`+`turkicnlp` kurulu). apertium-chv FST indirilmiş.
  - Bağlanamazsan: VM açık mı, port-forward duruyor mu (`VBoxManage showvminfo "RHEL9-Bootcamp" --machinereadable | grep -i forwarding`), sshd çalışıyor mu kontrol et.
- `VBoxManage` host'ta: `/c/Program Files/Oracle/VirtualBox/VBoxManage.exe`.
- **gh** (host) `muhammedkumcu` ile authenticated → repo push/oluşturma çalışır.

---

## 3) APERTIUM — NASIL KULLANILIR (kanıtlanmış, VM'de)
```bash
# VM'de (Linux):
pip install hfst turkicnlp        # hfst Linux'ta hazır wheel (Windows'ta DERLENMEZ)
python3 -c "import turkicnlp; turkicnlp.download('chv')"   # apertium FST indir
```
- FST yolları: `~/.turkicnlp/models/<dil>/<script>/morph/apertium/`
  - `<dil>.automorf.hfst` = **ANALİZ** (yüzey → kök+etiket)
  - `<dil>.autogen.hfst` = **ÜRETİM** (etiket → yüzey)
- **Yüksek seviye (turkicnlp):** `Pipeline("chv", processors=["tokenize","morph"])` → token'lara `.lemma` + `.feats` (UD-tarzı). (`torch yok` uyarıları zararsız — nöral backend atlanır.)
- **Düşük seviye (hfst, üretim için):**
  ```python
  import hfst
  gen = hfst.HfstInputStream(".../chv.autogen.hfst").read()
  gen.lookup("кӗнеке<n><pl><dat>")   # -> [('кӗнекесене', 0.0)]
  ```
- **KANITLANMIŞ çıktılar (chv):**
  - Analiz: `кӗнекесене → кӗнеке<n><pl><dat>`, `вулатӑп → вула<v><...><pres><p1><sg>`
  - Üretim: `кӗнеке<n><pl><dat> → кӗнекесене`, `вула<v><tv><pres><p1><sg> → вулатӑп`

---

## 4) PİVOT GEÇMİŞİ & KARARLAR (kısa)
- **Faz 1 (terk):** Türkmence kendi-motorunu Çuvaşça için tekrarladık → `arsiv/cuvasca-kendi-motor/` (63.5K sözlük, Python motor, %75 kapsam, web/ICALL, 62 test, **karışık-yazı %45.85 bulgusu**). Detay+neden: `plan/YOLCULUK-VE-VAZGECILENLER.md`.
- **Kırılma:** apertium olgun + Linux'ta çalışıyor → kendi motor gereksizdi. Kullanıcı itirazı haklıydı.
- **Pivot:** çok-dilli apertium platformu + **karşılaştırma ağı** (kullanıcı fikri — Türk dillerini birbiriyle karşılaştır).
- **Onaylı kararlar:** çok-dilli yön (Option 1); paper İngilizce; commit'lerde Claude görünmez; karışık-yazı bulgusu **sona**.

## 4.5) FELSEFE & İLKELER (yön bunlardan çıkar)
- **Olgun açık kaynağı yeniden icat etme** → üstüne değer kat (erişilebilirlik, pedagoji, karşılaştırma).
- **Düşük-kaynak/tehlikedeki Türk dilleri için dijital kapsayıcılık** — "dijital uçurum" misyonu (Joshi 2020 Class0-5).
- **Apertium = motor (rakip değil); biz = erişilebilirlik + öğrenme + karşılaştırma katmanı.** Apertium'a hata-düzeltme geri katkısı.
- **Akademik ağırlık = özellikler + değerlendirme** (UniMorph/UD altın standart, ML değil), salt "UI sarmak" değil.
- **Kanıtla, iddia etme** (özellikle "X kullanılamaz" demeden önce empirik test).

## 4.6) HATALAR & DERSLER (tekrar düşmemek için)
- **"Apertium kullanılamaz" yanlışıydı:** Windows'ta hfst derlenmez ≠ apertium kullanılamaz; **deploy/dev ortamı Linux** (VM). Empirik test (VM) her şeyi çözdü. **DERS:** ortam-spesifik engeli genel imkânsızlık sanma.
- **Güvenlik sınıflandırıcısı (classifier) engelleri:** (a) public repo oluşturma — kullanıcı "public" demeden engellenir → açık onay al. (b) dış paste servisi/HTTP-server/SSH-anahtarı-kurma `curl|bash` → "kalıcı uzaktan erişim" diye engellenir. **DERS:** bunları BYPASS etme; kullanıcı açık-rızasıyla yap (anahtarı kullanıcı kendi yapıştırdı).
- **VM kopyala-yapıştır:** VirtualBox host→guest pano **Guest Additions** ister; yoksa çalışmaz. ISO host'tan takıldı (`VBoxManage storageattach ... --medium .../VBoxGuestAdditions.iso`), guest'te `dnf install gcc make kernel-devel-$(uname -r) ... && mount /dev/cdrom /mnt && sh /mnt/VBoxLinuxAdditions.run && reboot`. Terminalde paste = **Ctrl+Shift+V**.
- **SSH anahtarı elle yazılınca base64 BOZULDU** (fingerprint farklı) → pano düzelince doğru yapıştırıldı. **DERS:** uzun base64'ü elle yazdırma.
- **Karışık-yazı tuzağı (önemli bulgu):** Çuvaş Wikipedia'sının %45.85'i Kiril kelimelere **Latin breve** (ă/ĕ/ç U+0103/0115/00E7) karıştırıyor → normalize etmeden hepsi OOV. (arsiv `phonology.py` CHUVASH_LATIN_MAP + `corpus_coverage.py` ölçümü.)
- **Hunspell host down → Wayback Machine** snapshot'ından `.oxt` kurtarıldı (30.494 giriş). **DERS:** ölü host = web.archive.org dene.
- **Windows git CRLF uyarıları** zararsız; görmezden gel.

---

## 5) ARAŞTIRMA TEMELİ (`arastirma/`)
- **1-cuvasca-morfoloji** (prompt.md + pdf): Çuvaş morfolojisi/kaynakları (kendi-motor fazını besledi).
- **2-egitim-platform** (prompt.md + pdf): NLP+eğitim platformu konumlandırma (Joshi dijital uçurum, ICALL, Eryiğit/İTÜRK, MUDT, homoglyph, Hamăr Yal, UniMorph/UD).
- **3-turk-dilleri-karsilastirma** (prompt.md + **pdf GELDİ**): karşılaştırmalı Türk dilbilimi (kollar, ses denklikleri rotasizm/lambdasizm/*d-t-y-z/*h-/*g-v-w, ünlü uyumu tipolojisi, karşılaştırmalı paradigmalar hal/iyelik/çoğul/fiil+morfotaktik, kognat setleri, alıntı katmanları, yazı sistemleri, anlaşılabilirlik %'leri, açık-veri envanteri, 4-modül veri haritası). 26 sf/108 kaynak → **eşzamanlı dilbilim çekirdeği.**
- **4-turk-dilleri-tarih-sosyokultur-iliski** (prompt.md — **PDF BEKLENİYOR**): tarih/sosyokültür/disiplinlerarası ilişki (köken/ana yurt, dönemleşme & yazılı gelenek, 20 dil bireysel profili, alfabe reformları, canlılık/EGIDS, Altay/Transavrasya tartışması, areal/temas Sprachbund, kültür/din/destan, genetik-vs-dil, **çok-boyutlu uzaklık matrisleri**, **araştırmacı ekosistemi+boşluklar+çözüm**) → **artzamanlı tarih/ilişki + araştırmacı-merkezi temeli.** 40-50 sf hedef.

## 6) KLASÖR HARİTASI
```
DEVAM.md · README.md
arastirma/  1-/2-/3- prompt.md (+1-/2- pdf) · _*.txt (gitignored çıkarımlar)
plan/       PLAN.md · PLATFORM-OZELLIKLERI.md · YOLCULUK-VE-VAZGECILENLER.md
platform/   apertium_probe.py (+ inşa edilecek backend/frontend)
arsiv/cuvasca-kendi-motor/  chuvash-fst/ (motor+web+data+tests) · scripts/ · kurallar/ · render.yaml · DEPLOY.md
sources/    (gitignored) apertium-chv · hunspell_cv · cuvasca_old · chv_corpus · _pkgcheck
```

## 7) KONVANSİYONLAR / TUZAKLAR
- **Git commit'lerde Claude GÖRÜNMEZ:** Co-Authored-By Claude **EKLENMEZ** (kullanıcı kararı). Yazar = Muhammed Kumcu <muhammedkumcu@marun.edu.tr> (local config kurulu). Her adımda commit+push.
- **gh** `muhammedkumcu` authenticated. Repo public.
- **Deploy/public/uzaktan-erişim** = classifier engelleyebilir → kullanıcı açık onayı al, bypass etme.
- **Apertium dev = VM'de** (host Windows'ta hfst yok). VM: `/root/apv` venv.
- md'leri güncel tut: iş ilerledikçe DEVAM.md + ilgili plan güncellensin.

## 8) HEMEN BAŞLAMAK İÇİN (yeni oturum)
1. **§0** (güncel durum + sıradaki) + **§2** (VM/apertium erişimi) + **§4.6** (dersler) oku.
2. Karşılaştırma PDF'i geldiyse → `arastirma/3-...prompt.md` + PDF'ten karşılaştırma ağı verisini kur.
3. Platform backend'i **VM'de** kur: `ssh ... root@127.0.0.1`, `/root/apv/bin/python`, apertium analiz+üretim → JSON API.
4. Her adımda commit+push (Claude attribution YOK).

## 9) COMPACT SONRASI — KULLANICININ GÖNDERECEĞİ ÖRNEK PROMPT (şablon)
```
cuvas-guncelleme projesindeyiz (C:\Users\Tombulteke\Desktop\cuvas-guncelleme). Önce DEVAM.md §0 (güncel durum+pivot) +
§2 (VM/apertium SSH erişimi: ssh -i ~/.ssh/cuvas_vm -p 2222 root@127.0.0.1; apertium Windows'ta DEĞİL VM'de çalışır) +
§3 (apertium nasıl kullanılır: automorf/autogen FST) + §4.6 (dersler) oku. Yön: ~20 Türk dili için Apertium-temelli
morfoloji + KARŞILAŞTIRMA platformu; kendi motorumuz arsiv'de. Commit'lerde Claude görünmez. Şimdi: [ÖRNEK]
"karşılaştırma PDF'i hazır, yolu: <path> — karşılaştırma ağını kurmaya başla" / "platform backend'ini VM'de kur" /
"paradigma API'sini yaz".
```
