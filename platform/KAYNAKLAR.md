# KAYNAK KÜTÜĞÜ — Platform Verisinin Doğrudan Kaynakları
### (Veri Provenance & Lisans Defteri)

> **İlke (kullanıcı kararı):** Platformdaki HER veri **doğrudan bir kaynağa** dayanır. Kaynakları **locale çekeriz** (`sources/`, gitignored), **inceleriz**, veriyi oradan **çıkarırız** — uydurmayız. Gerçek veriyle değişene kadar UI'da **"⚠ örnek/illüstratif"** etiketi kalır. UI'daki `SOURCES` + `USAGE` kütüğü bu defterle **birebir** tutulur.
> Güncelleme: **27 Haziran 2026** (deepsearch 5–18 işlendi; `cognates_deep.json` [ds18 Kognat 18-dil] + ses denklikleri 7 kol-izoglosu [ds17] eklendi).

## Durum lejantı
`✅ çekildi` (locale indirildi+incelendi) · `⏳ bekliyor` · `🖥️ VM` (apertium, Linux'ta) · `📄 makale` (PDF) · `🔒 tescilli` (açık alternatif kullan)

## Kaynak tablosu

| id (UI) | Ad | Tür | Lisans | Yerel yol / çekme | Durum | Beslediği modül / veri |
|---|---|---|---|---|---|---|
| `cldf` | **SavelyevTurkic CLDF** | veri | **CC BY 4.0** | `sources/savelyevturkic` (`git clone github.com/lexibank/savelyevturkic`) | **✅ çekildi + çıkarıldı** | Kognat Ağı, Karşılaştır, Uzaklık(leksikal), Harita (lat/long). 32 dil · 254 kavram · 8360 form · 905 kognat seti (uzman yargısı). → `platform/data/*` (aşağıda). |
| `fst` | **Apertium** morfolojik FST | araç | GPL-3.0 | VM `/root/.turkicnlp/models/<dil>` (turkicnlp ile indirildi, `processors=['morph']`) | **🖥️ CANLI** (10/10 MVP dil; FastAPI `platform/backend/app.py`, host:8000) | Morfolojik Analiz, Paradigma, Üretim, Araştırmacı (canlı). |
| `nel` | **NorthEuraLex** | veri | CC BY 4.0 | `sources/northeuralex` | **✅ çekildi** (çıkarım ⏳) | Kognat Ağı (ikincil), yüzey benzerliği. |
| `ud` | **Universal Dependencies** | veri | CC BY-SA 4.0 (ağaçbank bazlı değişir!) | `sources/UD_Turkish-IMST,-BOUN,UD_Kazakh-KTB,UD_Uyghur-UDT` | **✅ çekildi** (çıkarım ⏳) | Analiz bağlamı, POS, örnek cümle. **Lisans ağaçbank bazında kaydedilecek.** |
| `unimorph` | **UniMorph** | veri | CC BY 4.0 | `sources/{tur,tat,kaz,kir,uzb,uig,bak,sah,aze}` (chv yok) | **✅ çekildi** (çıkarım ⏳) | Paradigma Gezgini (`lemma⇥form⇥öznitelik`). |
| `wals` | **WALS** | veri | CC BY 4.0 | `sources/wals` (192 tipolojik özellik) | **✅ çekildi + çıkarıldı** | Uzaklık(tipolojik), özellik matrisi. → `distance.typological.json`, `features.wals.json`. |
| `glottolog` | **Glottolog 5.x** | veri | CC BY 4.0 | `sources/glottolog-cldf` | **✅ çekildi + çıkarıldı** | Soy ağacı, sınıflandırma, dil kimliği, **AES canlılık** (açık; EGIDS/UNESCO eşlemeli). → `profiles.json`. |
| `ethnologue` | Ethnologue / EGIDS | veri | **🔒 tescilli** | — (açık alternatif: **Glottolog AES** + **ElCat** + UNESCO Atlas) | ⏳ alternatif | Canlılık/konuşur. *Tescilli → açık AES verisi kullanılacak, EGIDS referans olarak anılacak.* |
| `joshi` | Joshi vd. 2020 | 📄 makale | akademik | `sources/_papers/joshi2020.pdf` (aclanthology.org/2020.acl-main.560) | ⏳ bekliyor | Dijital kaynak sınıfı (0–5), canlılık katmanı. |
| `yunusbayev` | Yunusbayev vd. 2015 | 📄 makale | açık (PLOS Gen.) | `sources/_papers/yunusbayev2015.pdf` (doi 10.1371/journal.pgen.1005068) | ⏳ bekliyor | Genetik-vs-dil mit kırıcı. |
| `kasgari` | Dîvânu Lugâti't-Türk (~1075) | 📄 tarihsel | kamu malı | tarihsel atıf | — referans | Tarih & Köken anlatısı. |
| `arastirma` | **Bizim derlemeler #3/#3b/#4** | sentez | (derleme; kaynakları içinde) | `arastirma/*.pdf` + `_research*.txt` | **✅ elde** | Ses denklikleri, Uzaklık matrisleri (J.1-3), profiller, zaman çizelgesi, areal/temas. |
| `bayes` | **Savelyev & Robbeets 2020** + Johanson tasnifi | 📄 makale | akademik | `arastirma/8-*siniflandirma*.pdf` → `_siniflandirma.txt` | **✅ çekildi + çıkarıldı** | Tarih & Köken: altı kol açıklayıcı + Bayes soy ağacı (zaman derinliği ~MÖ 66 / ~MS 474). |
| `hf` | **HuggingFace ekosistemi** | veri/araç | model bazında (CC/Apache/MIT…) | `arastirma/6,7-*.pdf` → `_tts_asr.txt`, `_llm_hf_ekosistem.txt` | **✅ çekildi + çıkarıldı** | Dil Profilleri (Seslendirme TTS/ASR), Araştırmacı Merkezi (ekosistem matrisi). |
| `deepds` | **KÖKEN derin araştırmalar (deepsearch 5–10)** | sentez | (derleme; her kayıt kaynağına atıflı) | `arastirma/_*.txt` (5/5b/5c/6/7/8/9.1-9.5/10) | **✅ elde + işlendi** | Derin dil profilleri, seslendirme, ekosistem (+metrik, ds10), sınıflandırma. Çapraz-kontrol: Glottolog/Ethnologue/UNESCO + Wikipedia/Grokipedia/ACL/apertium-wiki/HF/GitHub. |
| `deepds-yatay` | **Yatay ölçek deepsearch (11–18)** | sentez/prompt | — | `arastirma/11..18*.pdf` + `_envanter11.json`, `_profil_*.txt` (ds9 kol), `_profil14.txt`, `_profil16_ogur_argu.txt`, `_profil13.txt`, **`_kognat18.txt`/`_ses17.txt`** (ds17/18 faithful transcript) | **✅ 11–18 İŞLENDİ** | **11 ✅ → `languages.master.json`** (47 dil). **12-16 ✅ → `profiles_deep.json` (39 dil)** + Uzaklık 32 + harita/atlas 47. **18 ✅ → `cognates_deep.json`** (Kognat Ağı 7→18 dil, 11 kavram, kognat-ID+ses-kuralı). **17 ✅ → ses denklikleri 4→7 kol-izoglosu** (`build_sound_laws`, çok-kollu refleks, Savelyev kanıt 36/29/14). |

## Çıkarım kuralları
1. **Çek → incele → çıkar.** Her kaynağı `sources/`'a indir, yapısını incele, UI veri-sözleşmesine (bkz. `platform/ui/README.md`) eşle.
2. **Her veri satırı kaynaklı.** Çıkarılan JSON'da her kayıt `source` + (gerekiyorsa) `license` taşır. UI'daki `SOURCES`/`USAGE` ve sayfa-altı "KAYNAKLAR" şeridi bununla beslenir.
3. **Uydurma yok.** Kaynaktan gelmeyen hiçbir dilsel iddia eklenmez. Henüz gerçek veriye bağlanmamış modül **"⚠ örnek/illüstratif"** kalır.
4. **Lisans uyumu.** CC BY → atıfla kullanılır; CC BY-SA → türev aynı lisansla; GPL araç (apertium) çıktısı veri olarak kullanılır, dağıtımda lisans belirtilir; tescilli (Ethnologue) → açık alternatif.
5. **Erişim tarihi** her çekmede kaydedilir (bugün: 2026-06-24).

## Çıkarılan veri ürünleri (`platform/data/`, repoda tutulur)
> Çıkarım betikleri: `platform/etl/`. Her JSON `_meta` ile kaynak+lisans+yöntem taşır.

| Dosya | İçerik | Kaynak | Besler |
|---|---|---|---|
| `languages.master.json` ★ | **47 dil/lehçe/tarihsel form** (39 canlı+7 tarihsel+1 proto): iso/glottocode/ad/kol/lat-lon/era/konuşur/canlılık/not. **Yatay ölçek temeli.** Koordinat/ad canlıda Glottolog (otorite), tarihselde ds11 (Glottolog yanlış). | **deepsearch 11 + Glottolog CLDF çapraz-kontrol** (`platform/etl/build_master.py`) | **Harita (47 dil, açgözlü etiket+era stili)**; sıradaki: profiller/kognat/uzaklık ölçeği |
| `languages.geo.json` | 32 dil: glottocode/iso/lat-lon/kol (10 MVP işaretli) | SavelyevTurkic | (eski harita; master'a devrediliyor), dil kimliği |
| `cognates.json` | 254 kavram → 905 kognat seti · 32 dil (üye diller+biçim+segment+kök) | SavelyevTurkic | Ses denklikleri kanıt sayısı (`sound_evidence`: rot 36 / lam 29 / y 14) + **`cognates_broad.json`'un kaynağı** |
| `cognates_deep.json` ★ | **11 kavram × 18 dil** (Vücut/Doğa/Sayılar/Eylem/Temel-Kültür): her hücre yerel yazı/Latin/IPA/morfem/**kognat-ID** (boşluk)/uygulanan ses kuralı | **deepsearch 18** (Savelyev 2020 + Cambridge Turkic + Wiktionary çapraz-atıf; `platform/etl/build_cognates_deep.py`) | **Kognat Ağı DERİN mod** (18-dil radyal graf + "Dil dil ses kuralı" dökümü); A1 kategori seçici |
| `cognates_broad.json` ★ | **254 kavram × ≤32 dil** (GENİŞ tarama): TR gloss (254/254) + 10 kategori + cogid boşluk + akademik yazım. **DÜRÜST: yerel yazı/IPA/ses-kuralı YOK** (yalnız derin sette). 937KB → lazy-fetch (dist'e kopya, index.html'e gömülmez) | **SavelyevTurkic CLDF** (CC BY 4.0; `platform/etl/build_cognates_broad.py`) | **Kognat Ağı GENİŞ mod** (Derin/Geniş toggle; 254 kavram radyal graf + "biçim & segment" dökümü) |
| `distance.lexical.json` | 32×32 leksikostatistik mesafe (derin kognat paylaşımı) | SavelyevTurkic | Uzaklık Gezgini (leksikal eksen) |
| `profiles.json` | 23 dil profili: kimlik/koordinat/ülke/kol + **AES canlılık** (EGIDS/UNESCO eşlemeli) | Glottolog | Dil Profilleri, Canlılık ısı-haritası |
| `distance.typological.json` | 23×23 tipolojik mesafe (WALS özniteliklerinde farklılık; her hücre `shared` sayısı taşır) | WALS | Uzaklık Gezgini (tipolojik eksen) |
| `features.wals.json` | dil → 192 WALS özniteliği (değer etiketleriyle) | WALS | Özellik Matrisi |
| `profiles_deep.json` | **39 dil** × 4 bölüm derin profil (Tarih / Yapı-özgünlük / İlişkiler / Dijital güç), faithful+atıflı (tüm büyük canlı + 8 tarihsel dil) | deepsearch 9 (kol-profil) + 14 (Karluk) + 16 (Ogur-Argu) + 13 (Kıpçak) + Glottolog/Ethnologue/UNESCO çapraz-kontrol | Dil Profilleri (derin bölümler) |
| `profiles_tts.json` | **14 → 39 dil** × Seslendirme (TTS/ASR) durum. Gerçek model uzn/azb/crh/nog (MMS-TTS/eSpeak/wav2vec2); küçük yaşayan diller "açık model yok + yakın-dil/eSpeak"; tarihsel diller "uygulanamaz" | deepsearch 6 (`_tts_asr.txt`; `platform/etl/expand_tts_47.py`) | Dil Profilleri (5. bölüm — tüm derin profillerde) |
| `distance.lexical.json` (kullanım) | Uzaklık Gezgini **10 → 32 dil** açıldı (Savelyev tam leksikal/filogenetik matris; `build.py` DIST_ROWS, koordinat master'dan) | SavelyevTurkic | Uzaklık Gezgini |
| `ecosystem.json` | **Ekosistem sayfası** — 8 kategori (LLM/Encoder/ASR/TTS/Veri/Benchmark/Araçlar/Org) × dil × **doğrudan bağlantı** (101 link: HF model/veri, GitHub, leaderboard, Zemberek/TRmorph/Apertium…). NÖTR launchpad, olgunluk yargısı yok | deepsearch 7 + **kendi web araştırması** (`hf`/`deepds`) | **Ekosistem** sayfası (ARAŞTIR) |

> *Not (yöntem):* `distance.lexical.json` **derin kognat paylaşımı** ölçer (uzman kognat yargıları, 254 kavram) — #4'teki yüzey-Swadesh/anlaşılabilirlik yüzdelerinden farklı, tamamlayıcı bir sinyaldir; UI'da ayrı eksen olarak sunulabilir.

> **Not:** `sources/` `.gitignore`'da (büyük 3. parti veri repoya girmez). Bu defter (`platform/KAYNAKLAR.md`) + `platform/data/` + `platform/etl/` **repoda tutulur** ve provenance'ın kaydıdır.
