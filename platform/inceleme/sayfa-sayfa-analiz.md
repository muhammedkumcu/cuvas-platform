# Sayfa-Sayfa Analiz — KÖKEN platformu

> R7 (28 Haz). Her sayfa için: **ne yapıyor · güçlü yön · zayıf yön · iyileştirme önerisi**.
> Kullanıcının incelediği sayfalarda mevcut durum + kalan fikirler; **Morfoloji Analiz** ve
> **Paradigma Gezgini** kullanıcı tarafından İNCELENMEDİ → bunları kendim analiz ettim (★ işaretli).
> İyileştirmeler öneri niteliğindedir; uygulama ayrı turlarda + onayla yapılır.

---

## Ana Sayfa
- **Ne yapıyor:** HERO + akıllı arama (dil→profil, kavram→kognat, kelime→analiz) + 4 hızlı çip + "Dilin Kalbi" vitrini.
- **Güçlü:** tek arama kutusu tüm girişleri doğru modüle yönlendiriyor; net giriş noktası.
- **Zayıf:** arama "ne yazabilirim" konusunda örnek vermiyor; ilk gelen kullanıcı boş kutuya bakıyor.
- **Öneri:** arama altına tıklanabilir 3-4 örnek sorgu (göz · Çuvaşça · вуларăмăр) + "şunları deneyin" rotasyonu.

## Dil Profilleri
- **Ne yapıyor:** 47 dil künyesi (konuşur·yıl·kaynak·EGIDS·UNESCO·yazı·kol·Joshi sınıfı) + derin bölümler; arama + kol süzme.
- **Güçlü:** R5b-2 ile demografi tek kaynaklı + kaynaklı; canlılık rengi tutarlı; derin profiller atıflı.
- **Zayıf:** liste sıralaması `vit` (Glottolog AES) ile, gösterilen EGIDS (Ethnologue) sourced — ikisi nadiren ufak ayrışır (liste yeşil, detay turuncu olabilir). 8 küçük lehçede derin profil yok (kaynak yok — dürüst boşluk).
- **Öneri:** liste rengini de sourced EGIDS'e bağla (tam tutarlılık); küçük lehçeler için kaynak çıkarsa derin profil ekle.

## Harita (Atlas)
- **Ne yapıyor:** 47 dilin coğrafi atlası; zoom/sürükle-pan; nokta→inline kart; kol renkleri; ölü diller gri.
- **Güçlü:** tek-ekran (R1-R4 sonrası), tek nokta standardı, gerçek-çizim arka plan (deniz/dağ/Boğaz/Kıbrıs).
- **Zayıf:** inline kartın canlılık satırı hâlâ ham `vitality` stringi ("Safe / 2 / Vulnerable") — İngilizce/teknik. Etiket çakışması yoğun bölgelerde (Kafkasya) zoom gerektiriyor.
- **Öneri:** kart canlılık satırını master'ın sourced EGIDS/UNESCO TR'siyle değiştir (profil ile aynı dil); yoğun bölgeye otomatik "kümele" rozeti.

## Tarih & Köken
- **Ne yapıyor:** Bayes açıklama bloğu (R5b-3) + 6 kol detaylı izogloss + 15-satır kaynaklı kronolojik timeline.
- **Güçlü:** artık "çok özet" değil; renkler zaman-fazlı (karmaşık tip-renkleri kalktı); her satır akademik atıflı.
- **Zayıf:** soy ağacının görseli (FAMILY) hâlâ Karşılaştır sekmesinde — Tarih sayfasında metin var ama ağacın kendisi başka sayfada.
- **Öneri:** FAMILY ağacını Tarih sayfasına da göm (ya da Bayes bloğundan o sekmeye net bağlantı).

## Dilin Kalbi (Çuvaşça)
- **Ne yapıyor:** Çuvaşçaya adanmış anlatı: sesler, özgün yapılar, hayatta kalma; CTA'larla diğer modüllere köprü.
- **Güçlü:** projenin duygusal/misyon merkezi; 740 bin/2020 anlatısı R5b-2 ile veriyle tutarlı.
- **Zayıf:** "Seslendir" hâlâ tarayıcı Web Speech'e düşüyor (gerçek TTS değil — Bölüm C1 işi).
- **Öneri:** Saha/Şor için aynı "Kalbi" şablonu (Bölüm D); gerçek ses motoru gelince güncelle.

## ★ Morfoloji Analiz (kullanıcı incelemedi)
- **Ne yapıyor:** kelimeyi canlı çözer (Apertium FST + `/segment`): renk-kodlu morfem kartları (kök/zaman/şahıs…), satır-arası glossing (vula- -ră- -măr / oku GEÇ 1çğ), FST çözümlemesi, **katman ağacı** (kümülatif yüzey biçimler: вула→вуларă→вуларăмăр), seçili-morfem detay paneli. Otomatik dil algılama + "bu kelime şu dillerde" çipleri.
- **Güçlü:** **ürünün teknik kalbi ve en etkileyici sayfası.** Gerçek yüzey ekleri (etiket değil) + ses olayları otomatik; katman ağacı eklemeli dilin mantığını görselleştiriyor; çok-dil otomatik çözüm güçlü.
- **Zayıf:**
  - Çözülemeyen kelimede geri bildirim zayıf ("Apertium bu biçimi tanımadı") — öneri/ benzer kelime yok.
  - "Ağaç / Ek soy" toggle'ının ne yaptığı ilk bakışta belirsiz (etiketler kısa).
  - Yalnız 10 MVP dilinde canlı FST var; diğer 37 dilde analiz yok ama bu sayfada bu sınır görünmüyor (kullanıcı Nogayca yazınca sessiz boş kalabilir).
  - "Seslendir" Web Speech (gerçek değil).
- **Öneri:** ① çözülemeyince "şunu mu demek istediniz / bu dilde henüz FST yok" bilgilendirmesi + hangi 10 dilin canlı olduğunu gösteren rozet. ② toggle etiketlerini aç ("Katman ağacı" / "Ek kökeni"). ③ R-AÇIKLAMA bloğu eklendi (✅) — iyi. ④ örnek kelime çipleri (her dilden) ekле.

## ★ Paradigma Gezgini (kullanıcı incelemedi)
- **Ne yapıyor:** bir kökün tüm çekim tablosu (isim hâl×sayı; fiil zaman×kişi) canlı üretilir; her hücrede renk-kodlu morfem ayrışması (хӗр + ён → kızın) + tam biçim; çok-dilli örnek kökler; "Tabloyu kopyala".
- **Güçlü:** hücre-içi morfem ayrışması mükemmel pedagojik araç; isim/fiil ayrımı; kopyalama araştırmacı-dostu; örnekler dil-dengeli (Çuvaşça varsayılan).
- **Zayıf:**
  - İsim ve fiil arasında geçiş (sekme) bazı köklerde görünür, bazılarında değil — keşfedilebilirlik düşük.
  - Tablo uzun; mobilde yatay taşma riski (test edilmedi).
  - Renk lejantı en altta — kullanıcı renkleri görüp aşağı kaydırana dek anlamını bilmiyor.
  - Yine yalnız canlı-FST dillerinde dolu.
- **Öneri:** ① lejantı tablonun ÜSTÜne taşı (renkleri görmeden önce anlam). ② isim/fiil sekmesini her zaman göster (boşsa "bu kök fiil değil" de). ③ R-AÇIKLAMA bloğu eklendi (✅). ④ mobilde tabloyu kart-yığınına çevir.

## Kognat Ağı
- **Ne yapıyor:** 18-dil (Derin) / 254-kavram (Geniş) radyal kognat grafiği + "dil dil ses kuralı" dökümü + boşluk tespiti.
- **Güçlü:** R1-R4 sonrası alfabetik, büyük graf/merkez, tek-halka (çakışma minimal); açıklama deseninin doğduğu yer.
- **Zayıf:** Geniş modda 254 kavram çok; gezinme/arama tek kavrama kilitli; 32 düğümde 2-halka hâlâ ~10 çakışma.
- **Öneri:** Geniş modda kavram kategorisi filtresi + "çakışan düğümleri aç" hover; düğüm sayısı yüksekken liste-görünüm alternatifi.

## Karşılaştır
- **Ne yapıyor:** kelime/kavramın diller arası karşılaştırması (Dizilim / Ses denklikleri / Soy ağacı).
- **Güçlü:** üç bakış net; ses denklikleri kanıt-destekli; harita sekmesi kaldırıldı (tek-ekran).
- **Zayıf:** soy ağacı sekmesi + Tarih sayfası içerik olarak örtüşüyor (FAMILY iki yerde mantığı net değil).
- **Öneri:** soy ağacını tek yerde otorite yap (Tarih), Karşılaştır'dan oraya bağla; ya da Karşılaştır'da yalnız "bu iki dil ağacın neresinde" mini-vurgu.

## Uzaklık Gezgini
- **Ne yapıyor:** çok eksenli uzaklık (leksikal/filogenetik/tipolojik/coğrafi/anlaşılabilirlik) radarı; taban + karşılaştırılan diller yan yana kaydırmalı.
- **Güçlü:** 5/5 eksen kaynaklı; OKUMA kutusu yorumu insanca; R-AÇIKLAMA eklendi.
- **Zayıf:** radar tek karşılaştırma çiftinde en okunur; çok dil seçilince çizgiler iç içe.
- **Öneri:** çok-dil modunda radar yerine sıralı çubuk/ısı-haritası alternatifi.

## Ekosistem
- **Ne yapıyor:** Türk dilleri dil-teknolojisi launchpad'i (8 kategori × dil × doğrudan link; Apertium/Zemberek dahil).
- **Güçlü:** araştırmacının ilk uğrağı vizyonuna uygun; nötr, link doğrulanmış.
- **Zayıf:** metrikler (indirme/yıldız) statik (CRON yok — Bölüm C3); bazı düşük-kaynak dilde yalnız HF arama hub'ı.
- **Öneri:** HfApi-CRON ile metrik tazeleme; "son güncelleme" tarihi göster.

## Araştırmacı Merkezi
- **Ne yapıyor:** serbest sözcük + dil → canlı `/analyze` → JSON/CoNLL-U/CSV + indir/kopyala.
- **Güçlü:** gerçek dışa aktarım; araştırmacı-dostu.
- **Zayıf:** "Açık API · planlanan" — gerçek genel API yok (VM uç); toplu (batch) analiz yok.
- **Öneri:** dosya yükle→toplu analiz; gerçek genel API + dokümantasyon (sonraki faz).

## Hakkında / Kaynaklar
- **Ne yapıyor:** misyon + kaynak kütüğü (R6 ile katmanlı: araç/veri/akademik literatür, gerçek atıflar).
- **Güçlü:** R6 sonrası "deepsearch" yok; her kaynak adıyla + KULLANIM; akademik dürüstlük görünür.
- **Zayıf:** linkler düz metin (tıklanmıyor); makale DOI'leri kısmen.
- **Öneri:** linkleri gerçek `<a>` yap; her literatür kaynağına DOI/URL; GitHub/HF repo linkleri.

## Çuvaşça Atölyesi (Öğren)
- **Ne yapıyor:** üniteli öğrenme iskeleti (SRS kartları, rozetler, zayıf nokta) — çoğu "yakında".
- **Güçlü:** eğitim portalı vizyonunun yer tutucusu; SRS/rozet altyapısı tasarlanmış.
- **Zayıf:** içerik büyük ölçüde placeholder; gerçek alıştırma/ünite akışı yok (Bölüm D).
- **Öneri:** Bölüm D'de gerçek ünite içeriği + Saha/Şor şablonu.

---

## Öncelik özeti (kalan iş için sinyal)
1. **Tutarlılık:** harita inline kartı + profil listesi renklerini sourced EGIDS/UNESCO'ya tam bağla.
2. **Morfoloji/Paradigma cilası:** çözülemeyen/FST-yok durumları, lejant konumu, toggle etiketleri.
3. **Soy ağacı tek otorite:** Tarih vs Karşılaştır örtüşmesini çöz.
4. **Erişilebilirlik + mobil:** ayrı bir tur (incelemede hiç bakılmadı).
5. **Altyapı (Bölüm C):** gerçek TTS, ekosistem CRON, genel API — bunlar UI değil mühendislik.
