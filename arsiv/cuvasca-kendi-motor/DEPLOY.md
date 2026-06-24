# Platformu Canlıya Alma (Deploy)

Çuvaşça ICALL platformu (`chuvash-fst/web/app.py`) — Flask REST API + tek-sayfa öğrenme arayüzü.

## Yerel (hemen test)
```bash
cd chuvash-fst
pip install -r requirements.txt
python web/app.py
# -> http://localhost:5000
```

## Canlı: Render.com (önerilen — depodaki `render.yaml` hazır)
1. [render.com](https://render.com) → hesabınla giriş yap → **New → Blueprint**
2. GitHub'ı bağla → **muhammedkumcu/cuvas-platform** reposunu seç
3. Render `render.yaml`'ı otomatik okur → **Apply** → birkaç dakikada canlı URL
4. URL'yi paper'a ve repoya ekle (Türkmence'deki Vercel demosu gibi)

> Free tier yeterli (sözlük ~63K giriş belleğe yükleniyor, ~tens of MB). Tek worker.

## Alternatif: Vercel
Türkmence projesi Vercel'de. Flask için Vercel serverless biraz uğraştırır
(soğuk başlangıçta 63K sözlük yükleme yavaş). Render bu uygulama için daha uygun.

## Demo özellikleri (canlı arayüzde)
- **İsim paradigması** — renkli morfemli tam çekim tablosu
- **Fiil çekimi** — şimdiki/geçmiş/gelecek/emir + olumsuz
- **Analiz** — "bu kelimeyi açıkla" (kök + ek + anlam)
- **Yazım denetimi**
- **Alıştırma (ICALL)** — FST-üretimli çeldiricili boşluk-doldurma
- **Sanal Kiril klavyesi** (Ӑ Ӗ Ҫ Ӳ) + homoglyph otomatik düzeltme
