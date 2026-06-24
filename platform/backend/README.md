# platform/backend — KÖKEN Morfoloji API (FastAPI, VM'de)

> Apertium FST'lerini saran canlı morfoloji servisi. **Linux VM'de çalışır** (apertium/hfst Windows'ta derlenmez — bkz. `DEVAM.md` §2). Host'tan (ve UI'dan) `http://127.0.0.1:8000` üzerinden erişilir.

## Durum
**CANLI** — MVP 10 dil (tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah), analiz + üretim + paradigma. Her yanıt `_source` (Apertium, GPL-3.0) taşır.

## Uç noktalar
| Yöntem | Yol | Açıklama |
|---|---|---|
| GET | `/health` | sağlık + dil listesi |
| GET | `/languages` | dil + script + analyzer/generator var mı |
| POST | `/analyze` | `{lang, word}` → `analyses[{raw, lemma, tags[], weight}]` |
| POST | `/generate` | `{lang, query}` (ör. `хӗр<n><pl><dat>`) → `forms[{surface, weight}]` |
| GET | `/paradigm/{lang}/{lemma}?pos=n` | isim çekim tablosu (hâl × sayı) |

Örnek: `POST /analyze {"lang":"chv","word":"хӗрсем"}` → `хӗр<n><pl><nom>`.
`GET /paradigm/chv/хӗр` → Yalın хӗр/хӗрсем · İlgi хӗррӗн/хӗрсен · Yönelme хӗрре/хӗрсене · Bulunma хӗрре/хӗрсенче · Ayrılma хӗррен/хӗрсенчен · Araç хӗрпе/хӗрсемпе.

## Kurulum / dağıtım (VM)
```bash
# host -> VM kopyala
scp -i ~/.ssh/cuvas_vm -P 2222 platform/backend/app.py root@127.0.0.1:/root/koken_api/app.py
# VM'de bağımlılıklar (bir kez): /root/apv/bin/pip install fastapi "uvicorn[standard]"  (hfst+turkicnlp zaten kurulu)
# başlat (arka plan, ssh kapansa da sürer):
ssh ... root@127.0.0.1 'cd /root/koken_api && setsid /root/apv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 < /dev/null &'
```

## Host erişimi (port-forward + firewall) — BİR KEZ
```bash
# VirtualBox NAT port-forward (host 8000 -> guest 8000):
"/c/Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "RHEL9-Bootcamp" natpf1 "koken,tcp,127.0.0.1,8000,,8000"
# guest firewalld'de portu aç:
ssh ... root@127.0.0.1 'firewall-cmd --add-port=8000/tcp --permanent && firewall-cmd --reload'
```
Sonra host'tan: `curl http://127.0.0.1:8000/health`.

## Yeniden başlatma / durdurma
```bash
ssh ... 'pkill -f "uvicorn app:app"'                       # durdur
ssh ... 'cd /root/koken_api && setsid /root/apv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 < /dev/null &'  # başlat
```
> Not: dev launch (nohup/setsid). VM yeniden başlarsa port-forward kalıcı, firewalld kalıcı; uvicorn'u tekrar başlat (sonradan systemd unit eklenebilir).

## UI bağlantısı
KÖKEN arayüzü (`platform/ui/`) bu API'ye `fetch('http://127.0.0.1:8000/analyze', …)` ile bağlanacak; Analiz/Paradigma/Üretim modüllerinin illüstratif verisi bununla değişecek (uzman modda `fstSource`/`fstLicense` zaten yerinde).
