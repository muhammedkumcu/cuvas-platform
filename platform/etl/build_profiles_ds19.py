# -*- coding: utf-8 -*-
"""build_profiles_ds19.py — ds19 (Az Belgeli/Tarihsel Türk Dilleri) → profiles_deep.json

9 yaşayan az-belgeli lehçe (derin profili YOKtu) + 8 tarihsel dil (ince profili yenilenir).
4 bölüm: Tarih / Yapı & özgünlük / İlişkiler / Dijital güç. Faithful + GERÇEK kaynaklı (ds19'un
'Alıntılanan çalışmalar' bölümündeki atıflar: Wikipedia/Glottolog/Ethnologue/Apertium/HF +
Dolatkhah, Csató, Erdal, Tekin, Schluessel, Ercilasun, Röhrborn, Grönbech, Harrison vb.).
İdempotent: deep[code]'u ekler/değiştirir.
"""
import json
import io
import os

S = ("Tarih", "Yapı & özgünlük", "İlişkiler", "Dijital güç")


def prof(t, y, i, d):
    return [{"label": S[0], "body": t}, {"label": S[1], "body": y},
            {"label": S[2], "body": i}, {"label": S[3], "body": d}]


DEEP = {
    # ---- 9 YAŞAYAN AZ-BELGELİ LEHÇE ----
    "bgx": prof(
        "11. yy'da Balkanlar'a göçüp Ortodoks Hristiyanlığı benimseyen Peçenek-Kuman boylarının mirasçısı. Osmanlı garnizon şehirlerinde bir koiné (ortak dil) olarak şekillendi; edebî Gagavuzcadan bağımsız gelişti. [Balkan Turkish, Wikipedia; Grokipedia]",
        "Oğuz şemsiyesini (eklemeli yapı, ünlü uyumu) korur; ama söz başı ötümsüz gırtlak sızıcısının düşmesi (hazır→azır) ve batı varyantlarında ö/ü'nün artdamaksıllaşması (gün→gʉn) özgün izoglosslarıdır. [Grokipedia]",
        "En yakın akrabası standart Gagavuzca ve Türkiye Türkçesi (yüksek anlaşılırlık). Yüzyıllarca Slavca/Yunanca temasıyla ağır Balkan Sprachbund substratı: sözdizim kopyaları ve areal alıntılar. [Wikipedia]",
        "Joshi taksonomisinde 'Left-Behind'. HuggingFace'te tek dilli veri/model yok; Apertium morfolojik analizörü yok; standart dijital korpuslardan yoksun. [HF; Apertium]"),
    "qxq": prof(
        "Kökleri 11. yy Selçuklu göçlerine dayanan, Zagros çevresinde yarı göçebe Kaşkay konfederasyonunun Güney Oğuz dili. Uzun süre salt sözlü kaldı; Farsça konuşan devlet içinde izole bir Oğuz adası olarak yaşadı. [Qashqai, Wikipedia; Grokipedia]",
        "Türk ünlü uyumunu taşır ama yoğun Farsça temasıyla sapar; uvular /q/ ve /ɢ/ ayırt edici. Analitik ettirgenlik (qoy-/ver-), Farsça şablonlu modalite ve iyelik düşmesi morfosentaktik kopyalardır. [Lrr.modares; Dolatkhah]",
        "Genetik en yakın akraba Azerbaycan Türkçesi (çoğu kez diyalekti sayılır); Şeşbeyli gibi boylar Anadolu Türkçesine yakındır. Farsça/Arapçadan masif alıntı + kısıtlı ezafe (tamlama) yapısı. [Wikipedia]",
        "Joshi 'Scraping-By'. Dolatkhah'ın corpus-tabanlı dilbilgisi (2016) dijital analizi başlattı; HF'te Helsinki-NLP opus-mt çok-dilli modelinde qxq kodu + deneysel ASR temsili var. [Dolatkhah; HF]"),
    "uum": prof(
        "Kökeni KD Anadolu'nun (Trabzon/Kars) Türkçe konuşmaya başlayıp Ortodoksluğu koruyan Pontus Rumları. 18. yy'da II. Katerina döneminde Kırım'dan Azak'a (Mariupol) sürülünce dil Kıpçakça unsurlarla izole gelişti. [Urum, Wikipedia; Ethnologue]",
        "Söz başı /r/ için ünlü türemesi (protez): 'Rum'→'Urum' adı bizzat bu kuraldan doğar. Arkaik Kıpçak ekleri + ünlü uyumu sapmaları + /k/→/h/ sızıcılaşması; 2. çoğul -sis/-siz asimilasyonu yeniliktir. [Glottolog]",
        "Kırım Tatarcasının etno-diyalekti / çok yakın akrabası; erken Kafkasya Oğuz ağız izleri. Hristiyanlık terimleri Yunancadan (Noel→hristugin); modern çağda ağır Rusça baskısı. [Wikipedia]",
        "Joshi 'Scraping-By'. Skopteteas'ın 'Urum DoReCo' projesi fonetik-hizalı ses/metin korpusu (TLA arşivi); Apertium'da morfolojik dönüştürücü + kod-değişimli ASR çalışmaları. [DoReCo; Apertium; ACL 2025]"),
    "kdr": prof(
        "13.-14. yy'da Kırım'dan Litvanya (Trakai), Polonya ve Ukrayna'ya yerleşen Karaizm (Musevilik) inançlı Türk boylarının dili. Codex Cumanicus Kıpçakçasına dayanır; İbrani alfabesiyle kutsal metin çevirisi geleneği zengin yazılı tarih bıraktı. [Karaim, Wikipedia; Csató/DergiPark]",
        "Kuzeybatı (Trakai) diyalekti ünlü uyumunu büyük ölçüde yitirip yerine Slav etkili bir 'ünsüz uyumu' (palatalizasyon) geliştirdi: kelimedeki ünsüzler ya tümüyle damaksıl ya değil olmak zorundadır. [Csató]",
        "Kırım Tatarcası/Kıpçak dalında; din ekseninde İbranice sözdizim kopyaları. Asıl yıkıcı temas Slavca: Lehçe/Ukraynaca/Rusça ile uzun aradalık, fonoloji ve morfosentaksı dilin omurgasına işledi. [pressto.amu; Vilnius UP]",
        "Joshi 'Scraping-By'. HF'te düşük-kaynaklı mmBERT (Fill-Mask) temsili; GlotLID tanır ama Apertium/Stanza'da yapılandırılmış morfolojik analizörü yok. [HF mmBERT; GlotLID]"),
    "jct": prof(
        "Kırım'a göçen Sefarad/Aşkenaz kökenli Rabban Yahudilerinin 15. yy'dan Kırım Tatarcasını benimsemesiyle doğan etno-diyalekt. 1930'larda Latin (Yañalif) ile standartlaştırıldı; Holokost ve Sovyet sürgünleriyle nüfus yok oldu, aktarım kesildi. [Krymchak, Glottolog]",
        "Diğer Kıpçak varyantlarının aksine yalnızca beş kısa ünlü; en büyük sapma ön-arka dudaksıl ünlü ayrımının (o/ö, u/ü) tümden kaybıdır. İbranice sözcükler özgün Kıpçak/Oğuz karma fonolojisiyle telaffuz edilir. [Wikipedia]",
        "Kırım Tatarcasının Orta diyalektiyle aşırı geçişken. İbranice söz varlığının ~%5'i (din/günlük); eski metinlerde Arapça/Farsça yüksek üslup, modern metinlerde ağır Rusça substratı. [Glottolog]",
        "Joshi 'Left-Behind'; dijital izi neredeyse yok. HF'te yalnız ~38 satırlık çok sığ bir veri seti (Frank535/JCT); ne Apertium morfolojisi ne NLLB karşılığı var. [HF; Apertium]"),
    "sty": prof(
        "11.-14. yy Moğol istilaları ve Altın Orda'nın parçalanmasında Deşt-i Kıpçak kabilelerinin (Kanglı vb.) hareketiyle şekillenen kadim dil. Uzun süre İdil Tatarcasının diyalekti sanıldı; bağımsız bir Kuzey Kıpçak dalı kabul edilir. [Wikipedia; Glottolog]",
        "İdil Tatarcasından leksik/fonolojik sapma: söz başı b- düşmesi, /ç/→[ts], /c/→[j]; su→sıu diftonglaşması ve doğu Türk ünlü uyumu farkları tipiktir. [Wikipedia]",
        "Üç diyalekt sürekliliği: Tobol-İrtiş, Baraba, Tom. Baraba/Tom Kırgız-Kıpçak'a, Tobol-İrtiş Kıpçak-Nogay'a yakın. 16. yy'dan ağır Rusça kopyalama + Altay/Hakas/Şor areal substratı. [Glottolog]",
        "Joshi 'Scraping-By'. HF'te Qwen2.5 deneme adaptörleri (andreas-sty) ve veri setleri; TurkicNLP'de temel tokenizasyon var ama Apertium/Stanza derin morfoloji + ağaçbank henüz yok. [HF; TurkicNLP]"),
    "kim": prof(
        "Önceleri Karagas denen, Sayan dağlarında ren geyiği çobanlığı/avcılıkla yaşayan Tofa halkının dili. Proto-Sibirya Sayan alt grubundan Tuvaca ile erken koptu, coğrafi yalıtımda evrildi; bugün terminal nesle hapsoldu. [Glottolog; ELP]",
        "Proto-Türkçe köklere sadık; sekizli kısa + uzun ünlü zıtlığı. En eşsiz yanı hem damaksıl hem dudaksıl uyumu kökten eke iki boyutlu (double vowel harmony) işletmesidir; tayga/avcılık üzerine arkaik kökler. [ELP/Harrison]",
        "Tuvaca ve Dukha ile doğrudan akraba. Geçmişte Moğolca ve yok olmuş Yenisey/Samoyed dilleriyle substrat; 20. yy Sovyet iskânıyla Rusça hegemonyası altında asimile. [Glottolog]",
        "Joshi 'Left-Behind'. Harrison & Anderson'ın belgeleme projeleri olmasa dijital verisi olmayacaktı; Apertium/HF'te model, korpus veya çeviri aracı yok. [Living Tongues; HF]"),
    "clw": prof(
        "Sibirya ormanlarında balıkçılık/toplayıcılıkla yaşayan Yenisey/Ob-Ugor/Samoyed halklarının Türkleşmesiyle doğan otokton dil. Sovyet yatılı okulları + dil yasağı + itibarsızlaştırma ile ölüm döşeğine geldi; 1959 sonrası ayrı halk sayılmadı. [Glottolog; ELP]",
        "Orta Çulım (Ös) ve Aşağı Çulım (neredeyse ölü) diyalektleri. Orta Çulım'da ž→z (kiži→kizi), č→š/s (çäl→šäl) belirgin ses olaylarıdır. Yenisey substratı + Kıpçak leksiği Sibirya fonolojisinde harmanlanır. [Glottolog/Lemskaya]",
        "Şor, Hakas ve Altay ile doğrudan genetik bağ. Temel söz dağarcığı yüksek oranda Kıpçak özelliği korur (Leipzig-Jakarta). Hem Rusça yutması hem tarihsel Tatarlaşma baskısı altında. [Glottolog]",
        "Joshi 'Left-Behind'. 'The Linguists' (2008) kayıtları ve Tomsk arşivlerindeki Lemskaya derlemeleri dışında korpus yok; Apertium/HF için temel veriden yoksun. [ELP; Tomsk DPÜ]"),
    "ili": prof(
        "19. yy'da Tarım/Fergana'dan (muhtemelen Dungan İsyanı'ndan kaçarak) Kuzey Sincan İli Vadisi'ne göçen küçük topluluk. Çin'de bağımsız etnik grup sayılmaz, Kazak/Uygur olarak asimile edilir; dil yalnız kırsalda yaşlı nesilde sözlü yaşar. [Glottolog/Hahn]",
        "Karluk şemsiyesinde ama güçlü Kıpçak substratlı: arkaik *G yuvarlak ünlüden sonra w'ye dönüp eridi (dağ→taw, sarığ→sarıq); ikiz ünsüzleri (sekkiz) korur — izole muhafazakârlık. [Zhao & Hahn 1989]",
        "En yakın akraba modern Uygurca (İli diyalekti) ve Özbekçe. Çevredeki Kazak (Kıpçak) + egemen Uygur kültürü ağır leksik baskı yaratır; genç nesil Uygurca/Kazakçaya geçmiştir. [Glottolog]",
        "Joshi 'Left-Behind', dijital uçurumun dibinde. Yazılı edebî gelenek yok; internette metin verisi, Apertium çözümleyici veya HF modeli bulunmaz. [Apertium; HF]"),
    # ---- 8 TARİHSEL / ÖLÜ DİL (ince profil yenilenir) ----
    "otk": prof(
        "Türkçenin gramer/söz varlığı doğrudan izlenebilen ilk standart edebî formu. II. Göktürk ve erken Uygur kağanlıklarının bengü taşları (Kül Tigin, Bilge Kağan) ile ulaştı; 1893'te Thomsen çözdü ve Türkolojinin temel taşı oldu. [Erdal 2004; Johanson 2021]",
        "Katı fonotaktik: söz başı yalnız /b,t,k,s/ (nadiren ç,y,l). Modern dillerde eriyen /d/ ve damaksıl /ñ/ (adaq, qoyñ) korunur. -gU kollektif sayı eki, lokatif -dA'nın aynı anda ablatif görevi arkaik özelliklerdir. [Erdal 2004]",
        "Çuvaşça (Oğur) hariç tüm modern Türk dillerinin (Şaz kolu) ortak edebî atası. Yalnız idare/askerlik/ticarette Çince ve Soğdcadan alıntı; geri kalanı oldukça saftır. [Johanson 2021]",
        "Ölü ama dijitalleşiyor: Universal Dependencies'te Orhun ağaçbankası (sözdizim etiketli); TurkicNLP'de Runik-Latin çift yönlü transliterasyon + tokenizasyon. [UD; TurkicNLP]"),
    "oui": prof(
        "Göktürk yıkılışı sonrası Ötüken'den Turfan/Tarım'a göçen Uygurların yerleşik hayatla ürettiği klasik yazı dili (8.-14. yy). Budizm, Maniheizm ve Nasturi Hristiyanlık etrafında muazzam bir çeviri edebiyatı bıraktı. [Röhrborn]",
        "Runik metinlerin sentaktik katılığından ayrılıp soyut/felsefi kavramlara esnek bir morfosentaks geliştirdi; yoğun ikilemeler (bilip katıp) ve yardımcı fiilli karmaşık analitik eylemler. [Röhrborn 1977-1998]",
        "Karahanlıcanın sözdizimsel altyapısını hazırlar. Budizm/Maniheizm üzerinden Sanskritçe, Toharca, Soğdca ve Çinceden devasa leksik/kavramsal kopyalama (bakçan, toyın). [Wilkens]",
        "Akademik dijitalleşme güçlü (Wilkens/Röhrborn sözlükleri dijital tabanlara aktarılıyor); ama heterojen alfabe (Soğd/Brahmi/Maniheist) makine öğrenmesi ve standart HF entegrasyonunu çok zorlaştırır. [HF]"),
    "xqa": prof(
        "Türklerin İslam dairesine girmesiyle Maveraünnehir/Kaşgar merkezli doğan ilk standart İslamî edebî dil (11.-13. yy). Kâşgarlı Mahmud'un Dîvânu Lugâti't-Türk'ü (1072) ve Yusuf Has Hâcib'in Kutadgu Bilig'i başyapıtlarıdır. [Ercilasun 2014]",
        "Eski Uygurca morfolojisini korur, İslamî kavramlara yeni yapılar ekler. Kâşgarlı'ya göre Arapçada bulunmayan ötümlü dudak-diş /v/ için üç noktalı özel bir 'fa' (ڤ) harfi icat edilmiştir. [Ercilasun 2014]",
        "Karluk boylarının (Çiğil, Yağma) diyalektleri etrafında; Arapça-Farsça masif adstrat. Türk şiirinin Fars aruzuyla ilk melezlendiği, arkaik Türk + Semitik din terminolojisi sentezidir. [Ercilasun]",
        "Filolojik transkripsiyon (TDK veritabanları) zengindir; ama xqa koduyla doğrudan eğitilmiş açık LLM veya Apertium/Stanza entegrasyonu dijital platformlarda yoktur. [TDK; Apertium]"),
    "xzm": prof(
        "Moğol istilaları ve Altın Orda hegemonyasında Harezm'de Karluk/Kıpçak/Oğuz kabilelerinin harmanlanmasıyla doğan bir Orta Türkçe koiné (13.-14. yy). Nehcü'l-Ferâdîs, Kısasü'l-Enbiyâ gibi dinî-didaktik metinlerle var oldu. [Kurtulmuş 2025]",
        "Geçiş evresinin işareti heterojen eklerdir: aynı metinde Kıpçakça ve Oğuzca ekler yan yana bulunabilir. Eski Türkçe /d/~/ð/ sesinin /z/'ye dönüşü (adak→azak) karakteristik ses değişimidir. [Kurtulmuş 2025]",
        "Karahanlıcanın edebî mirasını alıp Çağataycaya zemin hazırlar. Suvar/Yemek boy diyalektleriyle temas etmiş, Farsçanın yoğun edebî kopyalarını barındırır. [DergiPark]",
        "Joshi 'Left-Behind'. Akademik çevriyazı dışında dijital morfoloji motoru yok; metinler yalnız spesifik corpus çalışmalarında (Tugantel vb.) kısıtlı referanslar olarak taranır. [DergiPark]"),
    "qwm": prof(
        "İpek Yolu'nda Cenevizli/Venedikli tüccarlar ve Fransisken misyonerlerin derlediği çok dilli el yazması (sözlük/gramer) üzerinden ulaşan Kuman-Kıpçak lingua francası (13. yy sonu-14. yy başı). [Grönbech]",
        "Arap yerine Latin alfabesinin kullanımı, dönemin ünlü değerlerini fonetik muazzam bir doğrulukla saptadı. Söz ortası *ğ'nin v'ye sızıcılaşması (oğul→ovul) gibi Kuzeybatı Kıpçak özelliklerini ilk kez belgeler. [Grönbech]",
        "Kırım Tatarcası, Karayca ve Urumcanın doğrudan atası konumunda. Çok dilli yapısı, Kumanların Farsça/Latince/İtalyanca/Moğolca adstrat ortamında yaşadığını net gösterir. [Kuun]",
        "Kuun ve Grönbech endekslemeleri dijital filolojik taramalarda kullanılır; ama makine çevirisi, ağaçbank (Treebank) veya herhangi bir Apertium/HF modeli söz konusu değildir. [filolojik]"),
    "xbo": prof(
        "İdil (Volga) Bulgar Devleti'nin resmî dili (9.-14. yy); kitabeler, sikkeler ve İbn Fazlan raporlarından bilinir. Altın Orda sonrası Kıpçak Tatarcaya asimile oldu ama Çuvaşçaya evrilerek mirasını sürdürdü. [Tekin 1988]",
        "Şaz şemsiyesinden radikal sapan Oğur (Lir) grubunun klasik örneği. Rotasizm (z>r) ve lambdasizm (ş>l) kritik izoglosu: 'sekiz' ve 'yedi yüz', mezar taşlarına 'sekir' ve 'jeti yir' olarak kazınmıştır. [Tekin 1988]",
        "Modern Çuvaşçanın tek ve edebî atası. Fin-Ugor (Ural) ve Slav dilleriyle, yerini aldığı Kıpçak diyalektleriyle güçlü tarihsel temas ve substrat ilişkisi vardır. [Erdal]",
        "Talat Tekin'in (1988) İdil Bulgar kitabe okumaları dışında dijital bir NLP varlığı söz konusu değildir; 'Left-Behind' statüsünde. [Tekin 1988]"),
    "zkz": prof(
        "Ortaçağ'da Kafkaslar/Doğu Avrupa'da hüküm süren, elitleri Museviliği benimseyen Hazar Kağanlığı'nın dili (7.-10. yy). Ticaret yollarında lingua franca; 13. yy'da Kıpçak dilleri içinde asimile olup yok oldu. [Erdal 2007]",
        "Dünyada en az belge bırakan dillerden: iki isim, birkaç unvan (Kağan, Tudun, Şad) ve Kiev Mektubu'ndaki 'HWQWRWM' (okudum). Bu tek kök, dilin Oğur mu Şaz mı olduğu tartışmasının tam merkezindedir. [Erdal 2007]",
        "Çok dilli/çok dinli Hazar Devleti'nde Slav, İrani, Kafkas ve İbrani dilleriyle bir arada var oldu; özellikle elit düzeyde Musevi kültüründen dinî/politik substrat aldı. [Glottolog]",
        "Literatürü olmayan, yalnız epigrafik ve spekülatif bir ölü dil olduğu için dijital gücü veya doğal dil işleme (NLP) varlığı bulunmamaktadır. [Glottolog]"),
    "chg": prof(
        "Karahanlı/Harezm mirasını alan, Timur ve Babür saraylarında standartlaşan, Ali Şir Nevâî'yle Hint altkıtasından Çin'e uzanan coğrafyada prestij dili olan muazzam edebî dil (15.-20. yy, 1921'e dek). [Schluessel 2018]",
        "Karluk omurgası üzerine oturur ama ünlü uyumunda zayıflama görülür. Şairlerin aruza uymak için ünlüleri keyfî değiştirmesi, Kıpçak/Oğuz eklerinin karışık (heterojen) kullanımı dönem karakteristiğidir. [Schluessel 2018]",
        "Modern Özbekçe ve Yeni Uygurcanın doğrudan edebî/genetik atası. Farsça (Hint-İran edebiyatı) ve Arapça ile entelektüel yarış, söz varlığına ve sözdizimine devasa adstrat yığdı. [Schluessel]",
        "Joshi 'Scraping-By'. Özbekistan/Çin'de el yazması dijitalleşmesi (OCR) hızlı; ama chg koduna adanmış açık sinirsel çeviri modelleri (NLLB, mBART) henüz yeterli olgunluğa erişmedi. [HF]"),
}


def main():
    p = os.path.join(os.path.dirname(__file__), "..", "data", "profiles_deep.json")
    d = json.load(io.open(p, encoding="utf-8"))
    deep = d["deep"]
    added, repl = [], []
    for code, sec in DEEP.items():
        (repl if code in deep else added).append(code)
        deep[code] = sec
    d["_meta"]["source"] = d["_meta"].get("source", "") + " | +ds19 (Az Belgeli/Tarihsel Diller): 9 yaşayan lehçe + 8 tarihsel, gerçek kaynaklı (Erdal/Tekin/Dolatkhah/Csató/Schluessel/Ercilasun/Röhrborn/Grönbech/Harrison + Glottolog/Ethnologue/UNESCO/Apertium/HF)."
    with io.open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("profiles_deep.json: +%d yeni, %d yenilendi (toplam deep=%d)" % (len(added), len(repl), len(deep)))
    print("  yeni:", ",".join(sorted(added)))
    print("  yenilenen:", ",".join(sorted(repl)))


if __name__ == "__main__":
    main()
