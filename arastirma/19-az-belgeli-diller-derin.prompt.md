# DEEPSEARCH 19 — Az Belgeli / Tarihsel Türk Dilleri: Derin Profil + Kaynaklı Veri

## Bağlam
KÖKEN, ~20 Türk dili için açık kaynak **morfoloji + karşılaştırma + araştırma** platformudur (çift kitle:
araştırmacı + öğrenci). "Dil Profilleri" sayfasında her dil için **derin profil** (4 bölüm) + kimlik verisi
gösteriyoruz. Aşağıdaki dillerde profilimiz **YOK ya da çok zayıf**. Bunları, **akademik kaynaklara
dayanarak ve her iddiayı atıflandırarak** doldurmak istiyoruz.

## ⚠ KIRMIZI ÇİZGİLER (kesinlikle uy)
1. **Uydurma yok.** Kaynaktan gelmeyen hiçbir dilsel/tarihsel iddia yazma. Bir bilgi yoksa açıkça **"güvenilir
   kaynak bulunamadı"** yaz — boş geç, doldurmaya çalışma.
2. **Her kayıt atıflı.** Her bölümün/sayının yanında **gerçek kaynak** ver: makale (yazar, yıl, başlık, DOI/URL),
   kitap (Johanson & Csató *The Turkic Languages*; Cambridge *The Turkic Languages* 2021), Glottolog/ELP/UNESCO
   sayfası, Ethnologue, dilbilgisi monografisi, vb. **"deepsearch" ya da "genel bilgi" KAYNAK DEĞİLDİR.**
3. **Konuşur sayısı + yıl + kaynak.** Mümkünse "X (YYYY sayımı/ tahmini, Kaynak)" formatında; sayım yoksa
   "tahmin, kaynak yok" diye işaretle.
4. **Tutarlı terminoloji.** Kol adları: Oğuz / Kıpçak / Karluk / Sibirya / Oğur / Argu. Canlılık için **EGIDS**
   (Lewis & Simons 2010) derecesi + UNESCO/ELP durumu.

## HEDEF DİLLER

### A) Yaşayan ama derin profili olmayan 7 lehçe (ÖNCELİK)
| Dil | ISO 639-3 | Kol | Bölge |
|---|---|---|---|
| Balkan Gagavuzcası | bgx | Oğuz | Balkanlar (Bulgaristan/Yunanistan/Makedonya) |
| Kaşkayca | qxq | Oğuz | İran (Fars eyaleti) |
| Urumca | uum | Kıpçak | Ukrayna (Azak) / Gürcistan |
| Karayca (Karaim) | kdr | Kıpçak | Litvanya/Polonya/Ukrayna (Kırım) |
| Kırımçak | jct | Kıpçak | Kırım |
| Sibirya Tatarcası | sty | Kıpçak | Batı Sibirya (Tümen/Omsk) |
| Tofaca (Tofalar) | kim | Sibirya | Doğu Sibirya (İrkutsk) |

*(Varsa Çulımca [clw] ve İli Türki [ili] için de aynı veriyi ekle.)*

### B) Tarihsel / ölü diller — mevcut profilimiz çok ince, derinleştir (8)
| Dil | ISO | Kol | Dönem |
|---|---|---|---|
| Eski Türkçe (Orhun/Göktürk) | otk | (Ortak ata) | 8. yy |
| Eski Uygurca | oui | Karluk | 8.–14. yy |
| Karahanlı Türkçesi | xqa | Karluk | 11.–13. yy |
| Harezm Türkçesi | xzm | Kıpçak-Karluk geçiş | 13.–14. yy |
| Codex Cumanicus Kıpçakçası | qwm | Kıpçak | 14. yy |
| İdil Bulgarcası | xbo | Oğur | 9.–14. yy |
| Hazarca | zkz | Oğur (tartışmalı) | 7.–10. yy |
| Çağatayca | chg | Karluk | 15.–20. yy |

## HER DİL İÇİN İSTENEN ÇIKTI (yapılandırılmış)

```
### <Dil adı> [<ISO>]
- Kol: <…>
- Bölge / konuşulduğu yer: <…> [Kaynak]
- Konuşur sayısı: <sayı> (<yıl, sayım/tahmin>) [Kaynak]   ← yoksa "kaynak yok"
- Canlılık (EGIDS): <derece + etiket> [Kaynak: Glottolog AES / UNESCO / ELP]
- Yazı sistemi: <Latin/Kiril/Arap/İbrani… tarih boyunca> [Kaynak]

**Tarih** (~200–280 karakter): kökeni, ne zaman/nereden ayrıldığı, kritik tarihsel dönemler, yazılı
kaynaklar/ilk metinler. [Kaynak(lar)]

**Yapı & özgünlük** (~200–280): ayırt edici fonoloji/morfoloji; bu dili özel kılan ses olayları/izoglosslar
(ör. rotasizm, *h- korunumu, ünlü uyumu kaybı, substrat etkisi). [Kaynak(lar)]

**İlişkiler** (~200–280): en yakın akraba diller; temas/substrat (Farsça, Slavca, Moğolca, Fin-Ugor,
Yunanca, İbranice…); diyalekt konumu; geçişkenlik. [Kaynak(lar)]

**Dijital güç** (~150–250): NLP/dijital kaynak durumu (Joshi sınıfı varsa); açık veri/araç (Apertium, HF,
korpus) var mı; yoksa "dijital kaynak yok" diye dürüstçe yaz. [Kaynak(lar)]
```

## EK İSTEK — Tüm 47 dile kaynaklı konuşur/canlılık tablosu
Yukarıdaki 15'in dışında, platformdaki **tüm yaşayan Türk dilleri** için de (Türkçe, Azerice, Kazakça,
Özbekçe, Tatarca, Başkurtça, Kırgızca, Türkmence, Uygurca, Çuvaşça, Yakutça, Tuvaca, Hakasça, Şorca,
Nogayca, Kumukça, Karaçay-Balkarca, Karakalpakça, Gagavuzca, Kırım Tatarcası, Altayca, Salarca, Sarı
Uygurca, Dolganca, Eynuca vb.) **konuşur sayısı (yıl + kaynak)** ve **EGIDS canlılık (kaynak)** sütunlu
bir tablo ver. Amaç: profillerdeki tahmini sayıları kaynaklı + yıllı hale getirmek.

## Önerilen kaynak türleri (gerçek, atıflandırılacak)
Johanson & Csató (ed.) *The Turkic Languages* (Routledge); Cambridge *The Turkic Languages* (2021,
ed. Bowern vd. — Diachrony/Lexicon bölümleri); Glottolog (glottolog.org); UNESCO Atlas of the World's
Languages in Danger / ELP (endangeredlanguages.com); Ethnologue; Savelyev & Robbeets (2020, *Journal of
Language Evolution*); Doerfer (Halaçça/Argu); Erdal (*Old Turkic Word Formation*, İdil Bulgar yazıtları);
Clauson (*Etymological Dictionary of Pre-13th-C Turkish*); dil-özel dilbilgisi monografileri; DergiPark /
TDK Belleten makaleleri; Wikipedia/Grokipedia yalnız ÇAPRAZ-KONTROL için (birincil kaynak değil).
