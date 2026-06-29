# KÖKEN Morfoloji API — Cloud Run konteyneri (YALNIZ API; UI ayrı, Firebase Hosting'de).
# Temel: python:3.11-slim-bookworm (glibc 2.36 → hfst manylinux_2_28 wheel'i ile uyumlu).
# Build context'i `deploy/stage.sh` hazırlar (app.py + models/ + dix/ VM'den toplanır).
FROM python:3.11-slim-bookworm

# Bağımlılıklar — ince: fastapi/uvicorn/pydantic/hfst/slowapi. (numpy/turkicnlp/regex GEREKMEZ.)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Root-olmayan çalışma kullanıcısı (güvenlik)
RUN useradd -m -u 10001 koken
WORKDIR /app

# Modeller (~196MB) + iki-dilli sözlükler (~18MB): nadiren değişir → app.py'den ÖNCE (katman önbelleği).
COPY --chown=koken:koken models/ /app/models/
COPY --chown=koken:koken dix/ /app/dix/
COPY --chown=koken:koken app.py /app/app.py

# Prod ortamı: /docs+/openapi kapalı, rate-limit açık, CORS allowlist deploy'da --set-env-vars ile verilir.
ENV KOKEN_ENV=prod \
    KOKEN_MODELS_DIR=/app/models \
    KOKEN_DIX_DIR=/app/dix \
    PORT=8080 \
    PYTHONUNBUFFERED=1

USER koken
EXPOSE 8080
# Cloud Run $PORT enjekte eder → shell formuyla genişlet. Tek worker (FST'ler süreç-belleğinde).
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT} --workers 1
