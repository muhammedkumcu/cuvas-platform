# KAYNAK KÜTÜĞÜ — Platform Verisinin Doğrudan Kaynakları
### (Veri Provenance & Lisans Defteri)

> **İlke (kullanıcı kararı):** Platformdaki HER veri **doğrudan bir kaynağa** dayanır. Kaynakları **locale çekeriz** (`sources/`, gitignored), **inceleriz**, veriyi oradan **çıkarırız** — uydurmayız. Gerçek veriyle değişene kadar UI'da **"⚠ örnek/illüstratif"** etiketi kalır. UI'daki `SOURCES` + `USAGE` kütüğü bu defterle **birebir** tutulur.
> Güncelleme: **28 Haziran 2026** (deepsearch 5–20 işlendi; **ds19 → 47-dil kaynaklı demografi master'a** [R5b-2] + **ds20 → Tarih sayfası Bayes açıklama + kaynaklı timeline** [R5b-3]; `bayes`/`tarih20` satırları + master demografi alanları eklendi).

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
| `bayes` | **Savelyev & Robbeets 2020** (JoLE, DOI:10.1093/jole/lzz010) + Johanson tasnifi | 📄 makale | akademik (CC BY) | `arastirma/8-*siniflandirma*.pdf` → `_siniflandirma.txt`; **ds20 `_tarih20.txt`** | **✅ çekildi + çıkarıldı** | Tarih & Köken: altı kol açıklayıcı + Bayes soy ağacı + **R5b-3 Bayes açıklama bloğu** (254 kavram/32 varyete/8.360 sözcük/905 kognat; düğümler ~MÖ66/~MS474/~MS650 + %95 GA; sığ-ayrışma içgörüsü). |
| `tarih20` | **Türk dilleri tarihi (ds20)** — 6 kol ses-yasaları + 15-satır zaman çizelgesi atıfları | 📄 derleme (PDF içi gerçek kaynaklar) | akademik atıf | `arastirma/20-*.pdf` → **`_tarih20.txt`** (14 sf, sonunda "Alıntılanan çalışmalar") | **✅ çekildi + işlendi (R5b-3)** | Tarih & Köken timeline + kol kartları. **Gerçek kaynaklar:** Tekin (1968), Arat (1947), Dankoff & Kelly (1982), Drimba (2000), Boeschoten (1998), Laitin (1998), Bacon (1966), Golden (1992/2011), Róna-Tas (1999), Johanson (2021), Johanson & Csató (1998), Erdal (1993), Doerfer (Argu). |
| `hf` | **HuggingFace ekosistemi** | veri/araç | model bazında (CC/Apache/MIT…) | `arastirma/6,7-*.pdf` → `_tts_asr.txt`, `_llm_hf_ekosistem.txt` | **✅ çekildi + çıkarıldı** | Dil Profilleri (Seslendirme TTS/ASR), Araştırmacı Merkezi (ekosistem matrisi). |
| `deepds` | **KÖKEN derin araştırmalar (deepsearch 5–10)** | sentez | (derleme; her kayıt kaynağına atıflı) | `arastirma/_*.txt` (5/5b/5c/6/7/8/9.1-9.5/10) | **✅ elde + işlendi** | Derin dil profilleri, seslendirme, ekosistem (+metrik, ds10), sınıflandırma. Çapraz-kontrol: Glottolog/Ethnologue/UNESCO + Wikipedia/Grokipedia/ACL/apertium-wiki/HF/GitHub. |
| `deepds-yatay` | **Yatay ölçek + inceleme deepsearch (11–20)** | sentez/prompt | — | `arastirma/11..20*.pdf` + `_envanter11.json`, `_profil_*.txt`, `_kognat18.txt`/`_ses17.txt`, **`_prof19.txt`/`_tarih20.txt`** | **✅ 11–20 İŞLENDİ** | **11 ✅ → `languages.master.json`** (47 dil). **12-16 ✅ → `profiles_deep.json` (46 dil)** + Uzaklık 32 + harita/atlas 47. **18 ✅ → `cognates_deep.json`** (Kognat 18-dil). **17 ✅ → ses denklikleri 7 kol-izoglosu**. **19 ✅ → R5b-1 (17 derin profil) + R5b-2 (Bölüm 3 tablosu = 47-dil KAYNAKLI konuşur/yıl/EGIDS/UNESCO → master)**. **20 ✅ → R5b-3 (Tarih sayfası: Bayes açıklama + 6 kol detay + 15-satır kaynaklı timeline; bkz `tarih20`)**. |

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
| `languages.master.json` ★ | **47 dil/lehçe/tarihsel form** (39 canlı+7 tarihsel+1 proto): iso/glottocode/ad/kol/lat-lon/era/canlılık/not + **R5b-2 sourced demografi** (`speakers`/`speakers_year`/`speakers_source`/`egids`/`egids_label`/`unesco`). **Tüm konuşur/EGIDS gösteriminin TEK kaynağı.** Koordinat/ad canlıda Glottolog. | **deepsearch 11 + Glottolog CLDF** (`build_master.py`) + **ds19 Bölüm 3 demografi tablosu** (Ethnologue/UNESCO/Glottolog/Campbell/Rus sayımı; `apply_demographics_ds19.py`) | **Harita (47 dil)** + **Dil Profilleri (konuşur·yıl·kaynak·EGIDS·UNESCO, SPKMETA)** + Uzaklık |
| `languages.geo.json` | 32 dil: glottocode/iso/lat-lon/kol (10 MVP işaretli) | SavelyevTurkic | (eski harita; master'a devrediliyor), dil kimliği |
| `cognates.json` | 254 kavram → 905 kognat seti · 32 dil (üye diller+biçim+segment+kök) | SavelyevTurkic | Ses denklikleri kanıt sayısı (`sound_evidence`: rot 36 / lam 29 / y 14) + **`cognates_broad.json`'un kaynağı** |
| `cognates_deep.json` ★ | **11 kavram × 18 dil** (Vücut/Doğa/Sayılar/Eylem/Temel-Kültür): her hücre yerel yazı/Latin/IPA/morfem/**kognat-ID** (boşluk)/uygulanan ses kuralı | **deepsearch 18** (Savelyev 2020 + Cambridge Turkic + Wiktionary çapraz-atıf; `platform/etl/build_cognates_deep.py`) | **Kognat Ağı DERİN mod** (18-dil radyal graf + "Dil dil ses kuralı" dökümü); A1 kategori seçici |
| `cognates_broad.json` ★ | **254 kavram × ≤32 dil** (GENİŞ tarama): TR gloss (254/254) + 10 kategori + cogid boşluk + akademik yazım. **DÜRÜST: yerel yazı/IPA/ses-kuralı YOK** (yalnız derin sette). 937KB → lazy-fetch (dist'e kopya, index.html'e gömülmez) | **SavelyevTurkic CLDF** (CC BY 4.0; `platform/etl/build_cognates_broad.py`) | **Kognat Ağı GENİŞ mod** (Derin/Geniş toggle; 254 kavram radyal graf + "biçim & segment" dökümü) |
| `distance.lexical.json` | 32×32 leksikostatistik mesafe (derin kognat paylaşımı) | SavelyevTurkic | Uzaklık Gezgini (leksikal eksen) |
| `profiles.json` | 23 dil profili: kimlik/koordinat/ülke/kol + **AES canlılık** (EGIDS/UNESCO eşlemeli) | Glottolog | Dil Profilleri, Canlılık ısı-haritası |
| `distance.typological.json` | 23×23 tipolojik mesafe (WALS özniteliklerinde farklılık; her hücre `shared` sayısı taşır) | WALS | Uzaklık Gezgini (tipolojik eksen) |
| `features.wals.json` | dil → 192 WALS özniteliği (değer etiketleriyle) | WALS | Özellik Matrisi |
| `profiles_deep.json` | **46 dil** × 4 bölüm derin profil (Tarih / Yapı-özgünlük / İlişkiler / Dijital güç), faithful+atıflı. ds19 ile +7 yaşayan az-belgeli lehçe (Balkan Gagavuz/Kaşkay/Urum/Karay/Kırımçak/Sibirya Tatar/Tofa) + 8 tarihsel yenilendi (Orhun/Çağatay/Karahanlı/Eski Uygur/İdil Bulgar/Hazar/Harezm/Codex) | deepsearch 9/13/14/16 + **19 (az-belgeli/tarihsel: Erdal/Tekin/Dolatkhah/Csató/Schluessel/Ercilasun/Röhrborn/Grönbech/Harrison; `build_profiles_ds19.py`)** + Glottolog/Ethnologue/UNESCO | Dil Profilleri (derin bölümler) |
| `profiles_tts.json` | **14 → 39 dil** × Seslendirme (TTS/ASR) durum. Gerçek model uzn/azb/crh/nog (MMS-TTS/eSpeak/wav2vec2); küçük yaşayan diller "açık model yok + yakın-dil/eSpeak"; tarihsel diller "uygulanamaz" | deepsearch 6 (`_tts_asr.txt`; `platform/etl/expand_tts_47.py`) | Dil Profilleri (5. bölüm — tüm derin profillerde) |
| `distance.lexical.json` (kullanım) | Uzaklık Gezgini **10 → 32 dil** açıldı (Savelyev tam leksikal/filogenetik matris; `build.py` DIST_ROWS, koordinat master'dan) | SavelyevTurkic | Uzaklık Gezgini |
| `ecosystem.json` | **Ekosistem sayfası** — 8 kategori (LLM/Encoder/ASR/TTS/Veri/Benchmark/Araçlar/Org) × dil × **doğrudan bağlantı** (101 link: HF model/veri, GitHub, leaderboard, Zemberek/TRmorph/Apertium…). NÖTR launchpad, olgunluk yargısı yok | deepsearch 7 + **kendi web araştırması** (`hf`/`deepds`) | **Ekosistem** sayfası (ARAŞTIR) |

> *Not (yöntem):* `distance.lexical.json` **derin kognat paylaşımı** ölçer (uzman kognat yargıları, 254 kavram) — #4'teki yüzey-Swadesh/anlaşılabilirlik yüzdelerinden farklı, tamamlayıcı bir sinyaldir; UI'da ayrı eksen olarak sunulabilir.

> **Not:** `sources/` `.gitignore`'da (büyük 3. parti veri repoya girmez). Bu defter (`platform/KAYNAKLAR.md`) + `platform/data/` + `platform/etl/` **repoda tutulur** ve provenance'ın kaydıdır.
