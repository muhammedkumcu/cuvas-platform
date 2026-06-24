# KAYNAK KÜTÜĞÜ — Platform Verisinin Doğrudan Kaynakları
### (Veri Provenance & Lisans Defteri)

> **İlke (kullanıcı kararı):** Platformdaki HER veri **doğrudan bir kaynağa** dayanır. Kaynakları **locale çekeriz** (`sources/`, gitignored), **inceleriz**, veriyi oradan **çıkarırız** — uydurmayız. Gerçek veriyle değişene kadar UI'da **"⚠ örnek/illüstratif"** etiketi kalır. UI'daki `SOURCES` + `USAGE` kütüğü bu defterle **birebir** tutulur.
> Güncelleme: **24 Haziran 2026.**

## Durum lejantı
`✅ çekildi` (locale indirildi+incelendi) · `⏳ bekliyor` · `🖥️ VM` (apertium, Linux'ta) · `📄 makale` (PDF) · `🔒 tescilli` (açık alternatif kullan)

## Kaynak tablosu

| id (UI) | Ad | Tür | Lisans | Yerel yol / çekme | Durum | Beslediği modül / veri |
|---|---|---|---|---|---|---|
| `cldf` | **SavelyevTurkic CLDF** | veri | **CC BY 4.0** | `sources/savelyevturkic` (`git clone github.com/lexibank/savelyevturkic`) | **✅ çekildi** | Kognat Ağı, Karşılaştır, Uzaklık(leksikal), Harita (lat/long). 32 dil · 254 kavram · 8360 form · 8360 kognat yargısı (hizalama+kök). |
| `fst` | **Apertium** morfolojik FST | araç | GPL-3.0 | VM `/root/apv` + `sources/apertium-chv` (diğer diller: `git clone github.com/apertium/apertium-{tur,tat,kaz,kir,uzb,uig,azj,bak,sah}`) | **🖥️ VM** (chv ✅; diğerleri ⏳) | Morfolojik Analiz, Paradigma, Araştırmacı (canlı analiz+üretim). |
| `nel` | **NorthEuraLex** | veri | CC BY 4.0 | `git clone github.com/lexibank/northeuralex` | ⏳ bekliyor | Kognat Ağı (ikincil), yüzey benzerliği. |
| `ud` | **Universal Dependencies** | veri | CC BY-SA 4.0 (ağaçbank bazlı değişir!) | `git clone github.com/UniversalDependencies/UD_Turkish-*` vb. | ⏳ bekliyor | Analiz bağlamı, POS, örnek cümle. **Lisans ağaçbank bazında kaydedilecek.** |
| `unimorph` | **UniMorph** | veri | CC BY 4.0 | `git clone github.com/unimorph/{tur,tat,kaz,...}` | ⏳ bekliyor | Paradigma Gezgini (etiket hizalama). |
| `wals` | **WALS** | veri | CC BY 4.0 | `git clone github.com/cldf-datasets/wals` | ⏳ bekliyor | Uzaklık(tipolojik), özellik matrisi. |
| `glottolog` | **Glottolog** | veri | CC BY 4.0 | `git clone github.com/glottolog/glottolog-cldf` | ⏳ bekliyor | Soy ağacı, sınıflandırma, dil kimliği, profil. |
| `ethnologue` | Ethnologue / EGIDS | veri | **🔒 tescilli** | — (açık alternatif: **Glottolog AES** + **ElCat** + UNESCO Atlas) | ⏳ alternatif | Canlılık/konuşur. *Tescilli → açık AES verisi kullanılacak, EGIDS referans olarak anılacak.* |
| `joshi` | Joshi vd. 2020 | 📄 makale | akademik | `sources/_papers/joshi2020.pdf` (aclanthology.org/2020.acl-main.560) | ⏳ bekliyor | Dijital kaynak sınıfı (0–5), canlılık katmanı. |
| `yunusbayev` | Yunusbayev vd. 2015 | 📄 makale | açık (PLOS Gen.) | `sources/_papers/yunusbayev2015.pdf` (doi 10.1371/journal.pgen.1005068) | ⏳ bekliyor | Genetik-vs-dil mit kırıcı. |
| `kasgari` | Dîvânu Lugâti't-Türk (~1075) | 📄 tarihsel | kamu malı | tarihsel atıf | — referans | Tarih & Köken anlatısı. |
| `arastirma` | **Bizim derlemeler #3/#3b/#4** | sentez | (derleme; kaynakları içinde) | `arastirma/*.pdf` + `_research*.txt` | **✅ elde** | Ses denklikleri, Uzaklık matrisleri (J.1-3), profiller, zaman çizelgesi, areal/temas. |

## Çıkarım kuralları
1. **Çek → incele → çıkar.** Her kaynağı `sources/`'a indir, yapısını incele, UI veri-sözleşmesine (bkz. `platform/ui/README.md`) eşle.
2. **Her veri satırı kaynaklı.** Çıkarılan JSON'da her kayıt `source` + (gerekiyorsa) `license` taşır. UI'daki `SOURCES`/`USAGE` ve sayfa-altı "KAYNAKLAR" şeridi bununla beslenir.
3. **Uydurma yok.** Kaynaktan gelmeyen hiçbir dilsel iddia eklenmez. Henüz gerçek veriye bağlanmamış modül **"⚠ örnek/illüstratif"** kalır.
4. **Lisans uyumu.** CC BY → atıfla kullanılır; CC BY-SA → türev aynı lisansla; GPL araç (apertium) çıktısı veri olarak kullanılır, dağıtımda lisans belirtilir; tescilli (Ethnologue) → açık alternatif.
5. **Erişim tarihi** her çekmede kaydedilir (bugün: 2026-06-24).

> **Not:** `sources/` `.gitignore`'da (büyük 3. parti veri repoya girmez). Bu defter (`platform/KAYNAKLAR.md`) **repoda tutulur** ve provenance'ın tek kaydıdır.
