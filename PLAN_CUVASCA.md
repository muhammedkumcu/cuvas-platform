# ÇUVAŞÇA MORFOLOJİK ANALİZ & ÜRETİM SİSTEMİ — KAPSAMLI PLAN
### Hedef: UBMK 2026 (TurkLang track) bildirisi · Son gönderim: **30 Haziran 2026**

> Bu plan üç girdiyi sentezler: (1) Türkmence projesi (TurkmenFST) mimarisi ve metodolojisi, (2) TurkLang 2026 bildirisi, (3) Çuvaşça derin araştırma raporu (`Çuvaşça Morfolojik Sistem Araştırması.pdf`). Tüm çalışma `C:\Users\Tombulteke\Desktop\cuvas-guncelleme\` içinde yürütülecek.

---

## 🔄 PIVOT (v2) — ANALİZÖR DEĞİL, ICALL ÖĞRENME PLATFORMU

> İkinci araştırma (`Çuvaşça NLP ve Eğitim Platformu.pdf`) sonrası konumlandırma kesinleşti. Aşağıdaki §0–§10 hâlâ geçerli (motor mühendisliği, sözlük, Çuvaş morfolojisi); ama **bildirinin ana katkısı ve ürünün kalbi** değişti. Bu bölüm önceliklidir.

**Yeni katkı cümlesi:** apertium-chv analizör olarak olgun (kapsam Turku %89.2 / Chuvash.org %83.6 / İncil %90.3; 10.267 kök) ama MT için tasarlanmış, son-kullanıcıya paketlenmemiş. Bizim katkımız *"yeni bir analizör"* değil → **FST'nin çift-yönlü ÜRETİM (generation) gücünü kullanarak dinamik çekim paradigmaları üreten, oyunlaştırılmış akıllı egzersizler (ICALL) sunan ve homoglyph-korumalı Kiril arayüzle buluşturan, Çuvaşça için ilk açık kaynak öğrenme platformu.**

**Üç teorik çerçeve (paper'ı "app" olmaktan çıkaran):**
1. **FST'nin ICALL için yeniden kullanımı (repurposing):** MT modülünü paradigma üretimi + boşluk-doldurma + çeldirici (distractor) üretimine dönüştürme metodolojisi.
2. **Homoglyph/Kiril metin normalizasyonu** düşük-kaynak NLP UX'inde (Latin↔Kiril çakışması filtresi).
3. **Tehlikedeki dil canlandırmasında oyunlaştırma:** Türkmence "kural-tabanlı analiz" → Çuvaşça "oyunlaştırılmış ICALL + toplumsal fayda" geçişi.

**Mimari (pivota göre revize):**
- **Motor (backend):** Pedagojik olarak merkezî paradigmalar (isim hal/iyelik/çoğul, fiil zaman/şahıs/olumsuz) için **kendi Python üretim çekirdeğimiz** — kontrol + kural hâkimiyeti + temiz paradigma tabloları. Genişlik/analiz için apertium-chv hasadı (sözlük) ve gerekirse **turkicnlp/hfst** (erken denenecek spike: Python'dan Çuvaşça FST çalışıyor mu?).
- **Platform (yıldız):** ICALL web uygulaması.

**Platform özellik seti (araştırmadan):** renklendirilmiş paradigma ağaçları (kök/zaman/şahıs farklı renk), Aralıklı Tekrar (SRS), boşluk-doldurma + FST-üretimli çeldiriciler, **Ӑ Ӗ Ҫ Ӳ sanal klavyesi**, **homoglyph normalizer**, seri/rozet/liderlik, mikro-etkileşimler, PWA + hafif (kırsal düşük bant), React/Vue/Next + FastAPI/Flask.

**Revize bildiri yapısı (6 sayfa IEEE, İngilizce):** I. Giriş (dijital uçurum — Joshi Class 0-5, %88 Class 0; Çuvaşça UNESCO Vulnerable 1M→700k) · II. Related Work (2 tablo: morfoloji araçları + edtech platformları; Hamăr Yal, İTÜRK, MUDT, apertium-chv) · III. Çuvaş morfolojisi (öz) · IV. Sistem (üretim motoru + ICALL platform + homoglyph katmanı) · V. Pedagoji & oyunlaştırma (SRS, distractor) · VI. Değerlendirme (kapsam + mümkünse küçük uzman/öğrenci değerlendirmesi) · VII. Sonuç.

**Venue:** UBMK 2026/TurkLang (birincil); ileride ComputEL, NLP4CALL.

**Anahtar atıflar:** Joshi 2020 (ACL); Eryiğit vd. "Gamification of complex morphology learning: Turkish" + patent WO2023063907A1; MUDT Uyghur ICALL (arXiv 2507.21536); apertium-chv/stats; "Correcting Keyboard Layout Errors and Homoglyphs" (D14-1068); Hamăr Yal (hamoryal.org); Çuvaşça MAIN.

---

## 0. YÖNETİCİ ÖZETİ & FİZİBİLİTE KARARI

**Bugün 23 Haziran 2026. UBMK son gönderim 30 Haziran 2026 → elimizde tam 7 gün var.** "1 hafta yoğun çalışma" hedefiniz bu takvimle birebir örtüşüyor.

**Verdict (gerçekçi):** ✅ **Yapılabilir** — ama Türkmence'deki %96,37 / 32.738 girişlik seviyeyi 7 günde yakalayamayız. Bunun yerine **savunulabilir, "ilk" niteliğinde bir MVP** hedefliyoruz:
- **Bağımsız (standalone), açık kaynaklı, kural tabanlı bir Çuvaşça morfolojik analiz + ÜRETİM sistemi** — Python, Türkmence mimarisini Çuvaşça'ya uyarlayarak.
- Mevcut `apertium-chv` (HFST) **analiz yapar ama ÜRETİM (generation) sunmaz** ve standalone bir araç/web/API değildir. Bizim katkımız: **üretim + analiz + REST API + web + corpus değerlendirmesi + Türkmence ile karşılaştırmalı Oğur-kolu morfolojisi.**
- **Gerçekçi kapsam hedefi:** ~15.000–30.000 kök sözlük, **≥%85 token kapsamı** (apertium-chv ~%85'i yakala/aş), stretch %90+.

**Konuyu reframe etmeye gerek YOK.** Morfolojik analizör/üreteç teması UBMK'nin **TurkLang özel track'ine** birebir oturuyor. Tek değişiklik: Türkmence'ye göre **daha kısa (6 sayfa IEEE)** ve **Çuvaşça'nın dilbilimsel farklılıklarına** odaklı bir anlatı.

---

## 1. NE İNŞA EDİYORUZ — SİSTEM & BİLDİRİ AÇISI

**Çalışma adı (öneri):** `ChuvashFST` / Türkçe başlık: *"ÇuvaşFST: Çuvaş Türkçesi için Kural Tabanlı Morfolojik Çözümleme ve Üretim Sistemi"* (İngilizce alt başlıkla).

**Bildiri açısı (one-liner):** *Türk dillerinin tek yaşayan Oğur (Bulgar) kolu üyesi olan, kritik düzeyde düşük kaynaklı Çuvaşça için, üretim yeteneğine sahip ilk bağımsız açık kaynak kural tabanlı morfolojik analiz sistemi.*

**Katkı iddiaları (paper "Contributions"):**
1. **Üretim + analiz birlikte:** apertium-chv yalnız analiz; biz kök+özellik → yüzey biçimi üretimi de sunuyoruz (paradigma tabloları, yazım denetimi, eğitim aracı).
2. **Sözlük derlemesi:** apertium-chv (~10,3K) + Hunspell-cv + Wiktionary'den derlenmiş, temizlenmiş, POS+özellik etiketli birleşik sözlük (hedef 15–30K kök).
3. **Corpus tabanlı değerlendirme:** Çuvaş Ulusal Korpusu üzerinde token kapsama ölçümü + apertium-chv ile karşılaştırma.
4. **Oğur-kolu morfolojisinin formal modeli:** Kiril normalizasyonu, indirgenmiş ünlü (ă/ĕ) epentezi, KÖK+İYELİK+ÇOĞUL+HAL slot sırası, -сем/-сен dönüşümü, üç-stratejili olumsuzluk.

---

## 2. MİMARİ KARARI (en kritik karar)

İki yol var:

| | **A) Python mimarisini yeniden kullan** (ÖNERİLEN) | **B) apertium-chv'yi (HFST/lexc/twolc) genişlet** |
|---|---|---|
| Temel | Türkmence'deki 5 bileşenli Python motoru uyarlanır | Mevcut lexc/twolc dosyaları üzerine inşa |
| Sözlük | apertium-chv + Hunspell + Wiktionary **hasat edilip** Python sözlük formatına aktarılır | Zaten lexc'te |
| Artılar | Ekip bu mimariyi biliyor; tam kontrol; **üretim** kolay; kanıtlanmış paper anlatısı; bağımsız araç/web/API | ~10K kök + kurallar hazır; hızlı yüksek kapsam |
| Eksiler | Morfotaktik + fonoloji Çuvaşça'ya yeniden yazılır | HFST/lexc/twolc öğrenme eğrisi (7 günde riskli); üretim/araç katmanı yine yazılır; "apertium uzantısı" daha az özgün; GPLv3 |
| Lisans | Kod MIT; veri kaynaklarına göre (aşağıya bk.) | Tümü GPLv3 |

**ÖNERİM: A (hibrit).** Türkmence'nin kazandığı oyun planını tekrarla: motoru Python'da yaz, ama **apertium-chv'nin kök envanterini seed olarak hasat et.** Bu hem hızlı (lexicon hazır) hem özgün (bağımsız üretim+analiz sistemi) hem de ekibin bildiği teknoloji. apertium-chv bizim **karşılaştırma temelimiz** olur (tıpkı Türkmence'de Apertium-tuk gibi).

---

## 3. TÜRKMENCE → ÇUVAŞÇA YENİDEN TASARIM HARİTASI

Araştırma raporunun H bölümünü mühendislik diline çevirdik. Türkmence kod tabanından neyi koruyacağımız, neyi sileceğimiz, neyi sıfırdan yazacağımız:

### 3.1 Fonoloji motoru (`phonology.py`)
| Kural | Karar |
|---|---|
| Ön/Art (palatal) ünlü uyumu | ✅ **Koru** — mantık aynı (e,i,ü,ĕ ↔ a,y,u,ă). Allomorflar **2 varyantlı** (ön/art) — Türkmence'deki 4 varyant basitleşir. |
| Yuvarlaklık uyumu | ❌ **Sil** — Çuvaşça'da yok. |
| Kök sonu ünsüz yumuşaması (k→g, p→b…) | ❌ **Sil** — Çuvaşça yazımında yok (tonlulaşma sadece okunuşta, yazıda değil). Bu büyük bir basitleşme. |
| İndirgenmiş ünlü (ă/ĕ) epentezi & düşmesi | 🆕 **Sıfırdan yaz** — (C)VC(C)ă/ĕ köklerde ek alınca ünlü düşmesi; ünsüz kümesini bozmamak için bağlayıcı ă/ĕ epentezi. |
| Ek başı ünsüz asimilasyonu | 🆕 **Yeni koşul** — kök r/l/n ile bitiyorsa hal eki **t-** ile başlar (хула-**ра** ama кӗл-**те**). |
| Ünsüz ikizleşmesi (gemination) | 🆕 **Destekle** — morfem sınırlarında. |
| **Kiril normalizasyon katmanı** | 🆕 **Yeni & zorunlu** — homoglyph denetimi (Rus Kirili а/е/с/р/о/х ≠ Latin), Ӑ/Ӗ/Ҫ/Ӳ birleşik karakter zorlaması, NFC. |

### 3.2 İsim morfolojisi (`morphotactics.py` + `generator.py`)
| Öğe | Karar |
|---|---|
| **Slot sırası** | 🆕 **Tamamen değiş:** Türkmence `KÖK+ÇOĞUL+İYELİK+HAL` → Çuvaşça **`KÖK+İYELİK+ÇOĞUL+HAL`** (кӗнеке-м-сем). Continuation class'lar baştan çizilir. |
| Hal sistemi | 🆕 8 hal: Nom(-∅), Gen(-(ă)n/-(ĕ)n), **Dat-Acc birleşik**(-(n)a/-(n)e), Loc(-ра/-ре~-та/-те), Abl(-ран/-рен~-тан/-тен), Instr(-па/-пе), Abessive(-сăр/-сĕр), Causal(-шăн/-шĕн). |
| Çoğul | 🆕 -сем; **oblik hallerde -сен'e döner** (deterministik kural). Lokatifte -сен-че (т→ч asimilasyonu). |
| İyelik | 🆕 6 şahıs; KÖK ile ÇOĞUL arasına girer. 3. şahıs tekil/çoğul ayrımı yok. |
| Sıfat | ✅ Çekimsiz (isimden önce, hal/çoğul almaz) — kolay. |
| Zamir | 🆕 Suppletive kökler (эпӗ→мана) düzensiz lemma olarak sözlükte. |

### 3.3 Fiil morfolojisi
| Öğe | Karar |
|---|---|
| **Slot sırası** | ✅ **Koru:** `KÖK+ÇATI+OLUMSUZ+ZAMAN+ŞAHIS` — Türkmence omurgası büyük ölçüde kalır. |
| Zamanlar | 🆕 Ek envanteri değişir: Şimdiki/geniş -ат/-ет, Belirli geçmiş -р/-т, Öğrenilen geçmiş -нă/-нĕ (sıfat-fiil+kopula), Gelecek -ă/-ĕ. |
| Şahıs ekleri | 🆕 Pronominal vs possessive iki set; zamana göre seçilir (ör. şimdiki: -ӗп/-ӗн/-∅/-пӗр/-ӗр). |
| Olumsuzluk | 🆕 **Üç strateji:** sentetik -м/-ма/-ме (şimdiki kaynaşık -мас/-мест) → **FST üretir**; analitik ан (emir) ve мар (isim/sıfat) → **bağımsız token, sentaktik/CG katmanına bırak.** |
| Non-finite | 🆕 Mastar -ма/-ме; partisip -кан/-кен (şimdi), -нă/-нĕ (geçmiş), -ас/-ес (gelecek); zarf-fiil -са/-се, -сан/-сен, -иччен. Partisip→isim yoluna bağlanır. |
| Çatı | 🆕 Ettirgen -тар/-тер/-т, Edilgen -л/-н, Dönüşlü/işteş -лан/-лен. |

### 3.4 Türetim
15 türetim eki araştırma raporunda hazır (Bölüm E). MVP'de **çekim öncelikli**; yüksek getirili 3-5 türetim eki (-лӑ/-лӗ, -сӑр/-сӗр, -ҫӑ/-ҫӗ, -лӑх/-лӗх, -ла/-ле) eklenir, gerisi ertelenir.

---

## 4. SÖZLÜK DERLEME PLANI

**Kaynaklar (hepsi araştırma raporunda doğrulandı):**

| Kaynak | URL | Boyut | Lisans | Rol |
|---|---|---|---|---|
| **apertium-chv** | github.com/apertium/apertium-chv | ~10.267 kök | GPLv3 | Ana seed sözlük + karşılaştırma temeli |
| **Hunspell-cv 1.06** | hunspell.chv.su (.oxt) | geniş | GPL/LGPL/MPL | Eksik kökleri tamamla |
| **Wiktionary (chv)** | en.wiktionary.org/Category:Chuvash_lemmas | binlerce | CC BY-SA | POS + altın standart çekim örnekleri |
| **samah.chv.su / chuvash.org** | samah.chv.su | çok geniş (Aşmarin+Skvortsov) | Eğitim/Free | **enedilim.com muadili** → çapraz doğrulama |
| **Krylov DB** | ru.corpus.chv.su | etiketli | Kısmi açık | Tagset uyumu referansı |

**Pipeline (Türkmence'nin 9 aşamalı hattının sadeleştirilmiş hali):**
1. apertium-chv `.lexc` / `.dix` parse → kök + POS çıkar.
2. Kiril normalizasyonu (homoglyph temizliği) tüm girişlere.
3. Hunspell-cv `.dic` ekle → eksik kökler.
4. Wiktionary MediaWiki API → POS doğrulama + ek kökler.
5. POS sınıflandır (n/v/adj/np), tek-harf ve çekimli form temizliği.
6. Morfolojik özellik etiketleri (reduced-vowel-drop, gemination, loanword/no-harmony) ekle.
7. samah.chv.su örneklemiyle çapraz doğrulama.

**Sözlük formatı (Türkmence formatını koru):** `kelime<TAB>%<pos%>[<TAB>özellikler]`. **Kökler Kiril (UTF-8) tutulur**; Latin çevrim yalnız yorum.

**⚠️ Lisans kararı:** apertium-chv GPLv3 olduğundan, onun verisini hasat eden sözlüğümüz/repomuz büyük olasılıkla **GPLv3** olur (Türkmence'deki MIT yerine). Alternatif: birincil kaynağı Wiktionary (CC BY-SA) + Hunspell yapıp apertium-chv'yi yalnız doğrulamada kullanmak → daha esnek lisans. **Karar verilmeli** (bkz. §9).

---

## 5. DEĞERLENDİRME PLANI

1. **Corpus kapsamı (ana metrik):** `github.com/AlAntonov/chv_corpus` (Çuvaş Ulusal Korpusu, ~1M cümle Çuv-Rus) → temiz Çuvaşça tarafını tokenize et → analizörün ≥1 geçerli çözüm verdiği token oranı = **token coverage**. Türkmence'deki gibi tür (type) kapsamı da raporla.
2. **Karşılaştırma:** apertium-chv (~%85 naïve coverage) vs bizim sistem. Tablo: teknoloji, lexicon, çekim kodu, kapsam, üretim desteği, durum.
3. **Çapraz doğrulama:** samah.chv.su'dan örneklem headword/paradigma kontrolü (enedilim.com rolü).
4. **İç tutarlılık:** round-trip testi (üret→çözümle→aynı spec) + birim testleri (Türkmence'deki pytest altyapısını uyarla).
5. **Aşamalı kapsam grafiği:** seed → +fonoloji → +isim → +fiil → +rafine (Türkmence makaledeki gibi).

---

## 6. 7 GÜNLÜK SPRINT (23–29 Haziran, 30'da gönderim)

| Gün | Tarih | İş | Çıktı |
|---|---|---|---|
| **1** | 23 Haz | Workspace; eski cuvas repo + apertium-chv + Hunspell klonla; Python iskeleti (Türkmence'den kopya); **Kiril normalizasyon katmanı**; apertium-chv'den seed sözlük çıkar + POS böl | Çalışan seed sözlük (~10K), normalize edilmiş |
| **2** | 24 Haz | **Fonoloji motoru:** 2-varyant ön/art uyum, ă/ĕ epentez/düşme, r/l/n→t asimilasyon (yuvarlaklık+yumuşama SİL); birim testler; Hunspell+Wiktionary ile sözlük zenginleştir | phonology.py + testler, ~15K+ sözlük |
| **3** | 25 Haz | **İsim morfotaktik + üretim:** yeni slot (KÖK+İYELİK+ÇOĞ+HAL), 8 hal, iyelik 6, -сем/-сен; paradigma üretimi; Wiktionary formlarıyla test | İsim üretimi + paradigma |
| **4** | 26 Haz | **Fiil morfotaktik + üretim:** şimdiki/geçmiş/gelecek/öğrenilen + 6 şahıs + sentetik olumsuzluk + mastar + temel partisip/zarf-fiil | Fiil üretimi |
| **5** | 27 Haz | **Analiz motoru** (generate-and-verify), dedup, kopula/partisip soyma; round-trip testler; **REST API + minimal web** (Türkmence Flask'ı uyarla) | Çalışan analiz + API + web |
| **6** | 28 Haz | **Değerlendirme:** chv_corpus indir, tokenize, kapsam ölç, gap analizi, allomorf/sözlük yamala, yeniden ölç; samah.chv.su çapraz doğrulama; karşılaştırma tablosu | Coverage sonuçları + tablolar |
| **7** | 29 Haz | **6 sayfa IEEE bildiriyi yaz** (yapı §7), şekiller, **benzerlik <%25** kontrolü (özellikle Türkmence makaleye karşı!); web'i deploy (vercel/render); GitHub repo | Bildiri PDF + repo + demo |
| **+** | 30 Haz | Tampon + **gönderim** | UBMK submission |

> Not: Yazma günü (7) hızlıdır çünkü bildiri yapısı Türkmence makaleyi izler — ama **metni yeniden yazmak zorundayız** (self-plagiarism / %25 benzerlik sınırı).

---

## 7. BİLDİRİ PLANI (UBMK, 6 sayfa IEEE)

**Yapı (Türkmence makaleyi izler ama sıkıştırılmış + Çuvaşça'ya özgü):**
1. **Abstract + Keywords** (Chuvash, morphological analysis, rule-based, Oghur/Bulgar branch, low-resource).
2. **I. Introduction** — Çuvaşça'nın Oğur kolu benzersizliği, kritik düşük kaynak, çapraz-dilli aktarımın neden başarısız olduğu, katkılar.
3. **II. Related Work** — apertium-chv (Tyers/HFST), Krylov (Markov+semantic), NLLB-200 (neural, kara kutu); Türkik FST geleneği (Oflazer, Washington). **Karşılaştırma tablosu.**
4. **III. Morphological Structure of Chuvash** *(en özgün bölüm)* — Kiril yazı + 4 özel harf, rotasizm/lambdasizm, ön/art uyum (yuvarlaklık yok), 8 hal + Dat-Acc birleşmesi, KÖK+İYELİK+ÇOĞ slot sırası, -сем/-сен, üç-stratejili olumsuzluk.
5. **IV. System Architecture** — 5 bileşen + **Kiril normalizasyon katmanı** (Türkmence'de olmayan yeni bileşen). Şekil 1 (mimari diyagram).
6. **V. Lexicon Compilation** — kaynak tablosu + sadeleştirilmiş pipeline + boyut/POS dağılımı.
7. **VI. Evaluation** — corpus kapsamı, apertium-chv karşılaştırması, çapraz doğrulama, round-trip testler, aşamalı kapsam grafiği.
8. **VII. Conclusion + Future Work** — gold-standard annotated corpus, türetim genişletme, analitik olumsuzluk için CG katmanı, Hunspell export.
9. **References** (apertium-chv, Krylov, NLLB, Krueger Chuvash Manual, Cambridge Turkic, Savelyev, vb. — araştırma raporundaki 46 kaynaktan seç).

**Şekiller/tablolar:** mimari diyagram, isim paradigma örneği (кӗнеке), fiil paradigma örneği (кил-), kaynak tablosu, karşılaştırma tablosu, kapsam sonuç tablosu.

---

## 8. UBMK ↔ TurkLang FARKLARI (dikkat!)

| Konu | TurkLang 2026 (önceki) | **UBMK 2026 (şimdi)** |
|---|---|---|
| Son gönderim | — | **30 Haziran 2026** (7 gün!) |
| Konferans | 13–15 Mayıs, Astana | 16–18 Eylül, İstanbul Beykent |
| Sayfa limiti | uzun olabiliyordu | **maks 6 sayfa A4** |
| Format | — | **IEEE standartları** (Word/LaTeX şablon) |
| Dil | İngilizce | İngilizce **veya** Türkçe (TR ise İngilizce özet zorunlu) |
| Benzerlik | — | **maks %25** (kaynakça hariç) |
| İndeksleme | — | **IEEE Xplore** |
| İlgili track | (ana konferans) | **TurkLang özel track'i var** → morfoloji bildirisine ideal |
| Camera-ready / bildirim | — | Camera-ready 11 Ağu, bildirim 18 Ağu, ücret 24 Ağu |

**Kritik uyarılar:**
- **6 sayfa** = Türkmence makalesi kadar uzun yazamayız; sert sıkıştırma.
- **%25 benzerlik** = Türkmence makalemiz IEEE/indeksli olduğundan, mimari/metodoloji paragrafları **kelime kelime kopyalanamaz**; yeniden yazılmalı. Çuvaşça-özgü içerik bizi korur.
- **IEEE şablonu** baştan kullanılmalı (LaTeX öneririm).

---

## 9. KARAR GEREKEN NOKTALAR

1. **Mimari:** A (Python yeniden kullanım + apertium-chv hasat) — önerim. Onaylıyor musunuz?
2. **Bildiri dili:** İngilizce (Xplore görünürlüğü, Türkmence ile tutarlı) mi, Türkçe (TurkLang track, İngilizce özetle) mi?
3. **Lisans:** apertium-chv hasat → GPLv3 kabul mü, yoksa Wiktionary/Hunspell birincil + apertium yalnız doğrulama (esnek lisans) mı?
4. **Yazarlık & demo:** Türkmence'deki gibi Esma Aydın + Muhammed Kumcu mu? Web demo (vercel/render) ve GitHub repo açılsın mı?

## 10. HEMEN SONRAKİ ADIMLAR (onay sonrası)
1. Eski cuvas reposunu + apertium-chv + Hunspell-cv'yi `cuvas-guncelleme/` altına klonla.
2. Türkmence Python iskeletini kopyalayıp Çuvaşça'ya göre boşalt (phonology/morphotactics/generator/analyzer/lexicon).
3. Kiril normalizasyon katmanı + apertium-chv seed sözlük çıkarımı (Gün 1).
