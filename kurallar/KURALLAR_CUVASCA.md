# ÇUVAŞÇA MORFOLOJİ — KANONİK KURAL SPESİFİKASYONU (motor için)

> Motorun (`chuvash_fst/`) uygulayacağı kuralların tek doğruluk kaynağı (ground truth).
> Kaynaklar: araştırma PDF'leri (`_research_text.txt`, `_research2_text.txt`), **apertium-chv `.twol`/`.lexc`** (sources/apertium-chv) ve referans gramerler (Krueger *Chuvash Manual*; Cambridge *Turkic*; chuvsu.ru).
> Standart dil = **Anatri (Aşağı Çuvaşça)**. Kökler **Kiril (UTF-8)**; Latin çevrim yalnız açıklama.
> ⚠️ "DOĞRULANACAK" etiketli kurallar corpus/gramerle test edilecek.

---

## 1. ALFABE, ÜNLÜ VE ÜNSÜZ SİSTEMİ

37 harfli Kiril + 4 özel harf: **Ӑ ӑ (ă), Ӗ ӗ (ĕ), Ҫ ҫ (ş/ś), Ӳ ӳ (ü)**.

**Ünlüler (8 asıl):**
- Art (back): `а ӑ ы у о` (+ iotated `я ё ю`)
- Ön (front): `е ӗ и ӳ э`
- İndirgenmiş (reduced): `ӑ` (back), `ӗ` (front)

(apertium twol Sets: `BackVow = ӑ а ы о у я ё ю`, `FrontVow = ӗ э и ӳ е`.)

**Ünsüzler (14 temel):** `б в г д ж з й к л м н п р с ҫ т ф х ц ч ш щ`
- Tonsuz (voiceless): `п т к с ç ҫ ş х` → ünlüler arası/sonorant yanında **okunuşta** tonlulaşır ama **yazımda değişmez** (allofonik; FST'de UYGULANMAZ).
- Likit/nazal (т- allomorf tetikleyici): **`р л н`**

**Homoglyph riski:** Latin `a c e o p x y A B C E H K M O P T X Y` ↔ Kiril karşılıkları görsel aynı. Ön işlemede normalize edilmeli.

---

## 2. ÜNLÜ UYUMU (vowel harmony)

- **Yalnız ön/art (palatal) uyum.** Yuvarlaklık uyumu **YOK** (Türkmence'den fark). → Ekler genelde **2 varyantlı** (art/ön), 4 değil.
- Harmoni kelimenin **son ünlüsüne** göre belirlenir; indirgenmiş ünlüler (ă/ĕ) uyuma katılır.
- İstisnalar (uyuma girmez / donmuş): **-сем** çoğul eki, 3. tekil iyelik bazı formları, bileşikler, Rusça alıntılar (son hece ünlüsüne uyar: `Шупашкарта`, `килте`).
- Türkmence'deki **ünsüz yumuşaması (k→g…) YOK** (yazımda). FST'den çıkarıldı.

| Arşifonem (twol) | Art | Ön |
|---|---|---|
| {A} | а (iotated я) | е |
| {Ă} | ӑ | ӗ |
| {U} | у | ӳ |

---

## 3. İSİM — EK SIRASI (slot order)

**KÖK + [İYELİK] + [ÇOĞUL] + [HAL]**  → Türkmence'den (KÖK+ÇOĞ+İYELİK+HAL) **farklı!**
Örn: `кӗнеке-м-сем` (kitap-POSS1sg-PL), `кӗнеке-сен-че` (kitap-PL.obl-LOC).
(apertium lexc: Root→NOMINAL→POSS→PLURAL→CASE.)

---

## 4. HAL (case) SİSTEMİ — 8 hal

Dat ve Acc tarihsel olarak **birleşik** (`<dat-acc>` tek etiket).

| Hal | Ek (art/ön) | Allomorf / koşul |
|---|---|---|
| Yalın (nom) | -∅ | sözlük formu |
| İlgi (gen) | -ӑн / -ӗн | ünsüzden sonra ă/ĕ bağlayıcı; ünlüden sonra -н (DOĞRULANACAK) |
| Yönelme-Belirtme (dat-acc) | -а / -е | ünlüden sonra koruyucu -н- (кӗнеке→кӗнекене) |
| Bulunma (loc) | **-ра/-ре** ↔ **-та/-те** | kök **р/л/н** ile bitiyorsa **т-**, diğerlerinde **р-** (хула-ра, кӗл-те) |
| Ayrılma (abl) | -ран/-рен ↔ -тан/-тен | loc kuralı + sonuna -н |
| Vasıta (ins) | -па / -пе | serbest; çoğulla -семпе |
| Mahrumiyet (abe) | -сӑр / -сӗр | isimden sıfat türetimi olarak da |
| Sebep-amaç (ter/causal) | -шӑн / -шӗн | bazen postpozisyon |

**Çoğul -сем → -сен (oblik):** Nominatif ve enstrümantal DIŞINDA tüm hallerde çoğul **-сен** olur.
- nom: кӗнеке-**сем** · ins: кӗнеке-**сем**-пе · loc: кӗнеке-**сен**-че (т→ч asimilasyon) · dat: кӗнеке-**сен**-е.

---

## 5. İYELİK (possessive) — KÖK ile ÇOĞUL arasına girer

3. şahısta tekil/çoğul ayrımı yok (`<px3sp>`). (apertium: px1sg -{ă}м, px2sg -{U}н, px1pl -{ă}м{Ă}р, px2pl -{Ĕ}р, px3sp -{и}{н}.)

| Şahıs | Ek (art/ön) | Örnek (кӗнеке) |
|---|---|---|
| 1tk | -ӑм / -ӗм (ünlüden sonra -м) | кӗнекем |
| 2tk | -у / -ӳ | кӗнекӳ |
| 3tk/çoğ | -ӗ / -и (-(ш)ӗ) | кӗнеки |
| 1çoğ | -ӑмӑр / -ӗмӗр | кӗнекемӗр |
| 2çoğ | -ӑр / -ӗр | кӗнекӗр |

> Eski repo (sources/cuvasca_old) у/ӳ-sonu için -ӑвӑм vb. ve gemination varyantları çıkarmış — referans, DOĞRULANACAK.

---

## 6. FİİL — EK SIRASI + ZAMAN/KİP/ŞAHIS

**KÖK + [ÇATI] + [OLUMSUZ] + ZAMAN/KİP + [ŞAHIS]** (Türkmence ile paralel — omurga korunur).
Fiil kökleri tek heceli olma eğiliminde (кил- gel, пар- ver, ту- yap).

**Zamanlar:**
| Zaman | Ek (art/ön) | Not |
|---|---|---|
| Şimdiki/geniş (pres/dur) | -ат / -ет | |
| Belirli geçmiş (past) | -р / -т | |
| Öğrenilen geçmiş (nar/ifi) | -нӑ / -нӗ | sıfat-fiil + kopula temelli |
| Gelecek (fut) | -ӑ / -ӗ | + şahıs |
| Emir (imp) | kök (2tk eksiz) | |

**Şahıs ekleri (zamana göre 2 set: pronominal / possessive).** Şimdiki zaman örn (ӗҫле-):
1tk -ӗп · 2tk -ӗн · 3tk/çoğ -∅ (sadece zaman eki) · 1çoğ -пӗр · 2çoğ -ӗр.
(apertium V-PERS-PRES-REG: -{Ă}п, -{Ă}н, -∅, -{Ă}п{Ă}р, -{Ă}р.)

**Olumsuzluk (3 strateji):**
1. **Sentetik:** köke -м / -ма/-ме; şimdiki zamanda kaynaşık **-мас/-мест** (ӗҫле-мест-ӗп). → FST üretir.
2. **Analitik (emir):** fiil önüne **ан** (ан ӗҫле). → bağımsız token, sentaktik/CG katmanı.
3. **Analitik (isim/sıfat/partisip):** **мар** (лайӑх мар). → bağımsız token.

**Non-finite:** mastar -ма/-ме (veya -малли); partisip şimdi -кан/-кен, geçmiş -нӑ/-нӗ, gelecek -ас/-ес; zarf-fiil -са/-се, -сан/-сен, -иччен.
**Çatı:** ettirgen -тар/-тер (~-т); edilgen -л/-н; dönüşlü/işteş -лан/-лен.

---

## 7. MORFOFONOLOJİ KURALLARI (fonoloji motoru)

apertium twol'dan damıtılan, pragmatik Python karşılıkları:

1. **Ön/art allomorf seçimi** (§2) — `V(back, front, word)`.
2. **Ek başı ünsüz asimilasyonu (loc/abl {T}):** kök `р/л/н` → т-allomorf; aksi → р-allomorf. (twol: "{T} after liquids and nasals".)
3. **т→ч palatalizasyon:** н'den sonra {T} bazı bağlamlarda ч (кӗнеке-сен-**че**). (twol: "Palatalisation of {T} after {н}".)
4. **İndirgenmiş ünlü düşmesi:** kök-sonu ӑ/ӗ, ünlüyle başlayan ek (iyelik/gen) öncesi düşebilir. (twol: "Weak/stem vowel deletion".) — DOĞRULANACAK, başta liste/işaret tabanlı.
5. **Bağlayıcı (epentez) ünlü:** ünsüz-sonu köke ünsüz-başı ek gelince hece için ă/ĕ girebilir (gen -ăн/-ĕн). 
6. **Ünsüz ikizleşmesi (gemination):** belirli (CV̆C) köklerde kök-sonu ünsüz, ünlü-başı ek öncesi ikizleşir (ҫын→ҫын{ː}). (twol: "Consonant gemination".) — lexicon özelliğiyle işaretlenir, DOĞRULANACAK.
7. **-сем/-сен** oblik dönüşümü (§4).

> Yuvarlaklık uyumu ve yazımsal ünsüz yumuşaması **YOK** (Türkmence'den silindi).

---

## 8. HOMOGLYPH NORMALİZASYON (UX + analiz öncesi)

Latin→Kiril görsel-aynı eşleme + NFC. Kiril giriş alanında otomatik. (Araştırma #2, D2.)
`a→а c→с e→е o→о p→р x→х y→у` ; `A→А B→В C→С E→Е H→Н K→К M→М O→О P→Р T→Т X→Х Y→У` (+ k→к).

---

## 9. TÜRETİM (öncelikli ekler — MVP)

| Ek | İşlev | Örnek |
|---|---|---|
| -лӑ/-лӗ | isim→sıfat (sahiplik) | вӑй→вӑйлӑ |
| -сӑр/-сӗр | isim→sıfat (yoksunluk) | вӑй→вӑйсӑр |
| -ҫӑ/-ҫӗ | isim→isim (meslek) | патша→патшаҫӑ |
| -лӑх/-лӗх | soyut isim | ҫын→ҫынлӑх |
| -ла/-ле | isim→fiil | пуҫ→пуҫла |
| -мӗш | sıra sayı | иккӗ→иккӗмӗш |

> Tam liste için araştırma PDF Bölüm E (15 ek). MVP'de çekim önceliklidir; bunlar 2. dalga.
