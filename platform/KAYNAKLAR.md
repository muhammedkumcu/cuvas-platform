# KAYNAK KÜTÜĞÜ — Platform Verisinin Doğrudan Kaynakları
### (Veri Provenance & Lisans Defteri)

> **İlke (kullanıcı kararı):** Platformdaki HER veri **doğrudan bir kaynağa** dayanır. Kaynakları **locale çekeriz** (`sources/`, gitignored), **inceleriz**, veriyi oradan **çıkarırız** — uydurmayız. Gerçek veriyle değişene kadar UI'da **"⚠ örnek/illüstratif"** etiketi kalır. UI'daki `SOURCES` + `USAGE` kütüğü bu defterle **birebir** tutulur.
> Güncelleme: **25 Haziran 2026** (deepsearch 5–9 işlendi; `bayes`/`hf`/`deepds` + `profiles_deep`/`profiles_tts`/`ecosystem` eklendi).

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
| `deepds-yatay` | **Yatay ölçek deepsearch promptları (11–18)** | prompt | — | `arastirma/11..18*.prompt.md` (envanter, 5 kol-profil, ses denklikleri, kognat) | ⏳ **kullanıcı çalıştıracak** | Yatay ölçek (tüm Türk dilleri+lehçeleri): profiller/kognat/uzaklık/harita/ses-denklikleri tüm dillere. Sonuçlar gelince locale çek + işle. |

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
| `languages.geo.json` | 32 dil: glottocode/iso/lat-lon/kol (10 MVP işaretli) | SavelyevTurkic | Harita, dil kimliği |
| `cognates.json` | 254 kavram → 905 kognat seti (üye diller+biçim+segment+kök) | SavelyevTurkic | Kognat Ağı (kognat boşlukları görünür: ör. "göz" *gȫrs vs Sibirya *Karak) |
| `distance.lexical.json` | 32×32 leksikostatistik mesafe (derin kognat paylaşımı) | SavelyevTurkic | Uzaklık Gezgini (leksikal eksen) |
| `profiles.json` | 23 dil profili: kimlik/koordinat/ülke/kol + **AES canlılık** (EGIDS/UNESCO eşlemeli) | Glottolog | Dil Profilleri, Canlılık ısı-haritası |
| `distance.typological.json` | 23×23 tipolojik mesafe (WALS özniteliklerinde farklılık; her hücre `shared` sayısı taşır) | WALS | Uzaklık Gezgini (tipolojik eksen) |
| `features.wals.json` | dil → 192 WALS özniteliği (değer etiketleriyle) | WALS | Özellik Matrisi |
| `profiles_deep.json` | 14 dil × 4 bölüm derin profil (Tarih / Yapı-özgünlük / İlişkiler / Dijital güç), atıflı | deepsearch 9.1-9.5 (`deepds`) + Glottolog/Ethnologue/UNESCO çapraz-kontrol | Dil Profilleri (derin bölümler) |
| `profiles_tts.json` | 14 dil × Seslendirme (TTS/ASR) durum + açık model/lisans/boşluk | deepsearch 6 (`hf`/`deepds`) | Dil Profilleri (5. bölüm) |
| `ecosystem.json` | **Ekosistem sayfası** — 8 kategori (LLM/Encoder/ASR/TTS/Veri/Benchmark/Araçlar/Org) × dil × **doğrudan bağlantı** (101 link: HF model/veri, GitHub, leaderboard, Zemberek/TRmorph/Apertium…). NÖTR launchpad, olgunluk yargısı yok | deepsearch 7 + **kendi web araştırması** (`hf`/`deepds`) | **Ekosistem** sayfası (ARAŞTIR) |

> *Not (yöntem):* `distance.lexical.json` **derin kognat paylaşımı** ölçer (uzman kognat yargıları, 254 kavram) — #4'teki yüzey-Swadesh/anlaşılabilirlik yüzdelerinden farklı, tamamlayıcı bir sinyaldir; UI'da ayrı eksen olarak sunulabilir.

> **Not:** `sources/` `.gitignore`'da (büyük 3. parti veri repoya girmez). Bu defter (`platform/KAYNAKLAR.md`) + `platform/data/` + `platform/etl/` **repoda tutulur** ve provenance'ın kaydıdır.
