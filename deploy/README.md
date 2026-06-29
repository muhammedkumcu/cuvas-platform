# KÖKEN — Yayın Runbook'u (API: Cloud Run · UI: Firebase Hosting)

> Mimari: **ayrı**. API Cloud Run'da (sıfıra-inme, bedava kota), UI Firebase Hosting'de
> (always-on CDN, anında, bedava). UI cross-origin API'ye bağlanır → CORS allowlist ile kilitli.
> **Salt-okunur API** (veri yazmaz/silmez). Tüm güvenlik env-güdümlü (bkz. `platform/backend/app.py`).

## ✅ CANLI (29 Haz 2026 deploy edildi)
- **UI:** https://koken-morfoloji.web.app  (Firebase Hosting)
- **API:** https://koken-api-1087019161757.europe-west3.run.app  (Cloud Run `koken-api`, sıfıra-inme)
- Yeniden deploy için aşağıdaki adımlar (ilk kurulum adım 1-2 atlanır; backend→3-4, UI→5).

## 0) Değişkenler (tek yerde)
```
PROJ=koken-morfoloji          # globalde benzersiz olmalı; alınmışsa -1, -tr vb. ekle
REGION=europe-west3           # Frankfurt — Türkiye'ye en yakın Cloud Run bölgesi
BILLING=01642B-2CB63A-E78542  # "Firebase Payment" (açık)
SVC=koken-api
```

## 1) Kullanıcının yapacağı TEK interaktif adım
```bash
firebase login        # tarayıcıda Google ile oturum (yalnız bir kez)
```
gcloud zaten yetkili (`gcloud auth list`). Başka interaktif adım yok.

## 2) Proje + faturalandırma + API'ler  (otomatik)
```bash
gcloud projects create $PROJ --name="KOKEN"
gcloud billing projects link $PROJ --billing-account=$BILLING
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
    artifactregistry.googleapis.com firebasehosting.googleapis.com --project=$PROJ
firebase projects:addfirebase $PROJ        # GCP projesine Firebase'i ekle (Hosting için)
```

## 3) Build context'i hazırla (modeller+dix VM'den)  (otomatik)
```bash
bash deploy/stage.sh          # deploy/_ctx/ → app.py + models/ + dix/ (~213MB)
```

## 4) API'yi Cloud Run'a deploy et  (otomatik; ilk build ~3-5 dk, Cloud Build)
```bash
gcloud run deploy $SVC --source deploy/_ctx --project=$PROJ --region=$REGION \
  --allow-unauthenticated \
  --min-instances=0 --max-instances=3 --concurrency=20 \
  --cpu=1 --memory=1Gi --timeout=30 \
  --set-env-vars=KOKEN_ENV=prod
# Çıktıdaki Service URL'yi NOT AL:
API_URL=$(gcloud run services describe $SVC --project=$PROJ --region=$REGION --format='value(status.url)')
echo "$API_URL"
```

## 5) UI'yi API'ye bağlayıp Firebase'e deploy et  (otomatik)
```bash
KOKEN_API_URL="$API_URL" python platform/ui/build.py     # dist/index.html prod API ile
firebase use $PROJ
firebase deploy --only hosting --project=$PROJ
# UI URL: https://$PROJ.web.app  (ve https://$PROJ.firebaseapp.com)
```

## 6) API CORS'unu UI origin'ine kilitle  (otomatik; en son)
```bash
gcloud run services update $SVC --project=$PROJ --region=$REGION \
  --set-env-vars=KOKEN_ENV=prod,KOKEN_RATE_LIMIT=60/minute,\
KOKEN_ALLOWED_ORIGINS=https://$PROJ.web.app,https://$PROJ.firebaseapp.com
```

## 7) Doğrulama
```bash
curl -s $API_URL/health                                   # {"ok":true,...}
curl -s -X POST $API_URL/analyze -H 'Content-Type: application/json' \
     -d '{"lang":"tur","word":"evler"}'                   # 3 çözüm
curl -s -o /dev/null -w '%{http_code}\n' $API_URL/docs     # 404 (prod'da kapalı)
# Tarayıcı: https://$PROJ.web.app → Analiz "geliyorum" → canlı sonuç (ilk istek ~3-8 sn soğuk).
```

## Güvenlik özeti (uygulanan)
- CORS yalnız UI origin'leri (env); salt GET/POST. Rate-limit 60/dk/IP (X-Forwarded-For).
- Girdi sınırları: kelime ≤80, sorgu ≤200, gövde ≤8KB. Güvenlik başlıkları (nosniff/DENY/no-referrer).
- `/docs`+`/openapi` prod'da kapalı. Root-olmayan konteyner kullanıcısı. Salt-okunur API.
- min/max-instances + concurrency → maliyet+kötüye-kullanım tavanı. `*.run.app` → otomatik HTTPS.

## Maliyet (demo trafiği)
- Cloud Run sıfıra-inme: ~**0₺** (aylık 2M istek bedava kotası). Firebase Hosting: **bedava**.
- Cloud Build: ~3-5 dk/build (günlük 120 dk bedava). Artifact Registry imaj depolama: ~**0.01$/ay**.
- Sürekli-sıcak istenirse: `--min-instances=1` (aylık ~10-30$). Özel alan adı (ops.): ~yıllık 10-15$.

## Güncelleme (sonraki deploy'lar)
- **Backend değişti:** `bash deploy/stage.sh` → adım 4 (CORS env korunur, --set-env-vars tekrar verme). VM↔repo md5 senkron tut.
- **UI değişti:** adım 5 (KOKEN_API_URL = mevcut $API_URL ile build → firebase deploy).
