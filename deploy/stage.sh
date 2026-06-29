#!/usr/bin/env bash
# KÖKEN API — Cloud Run build-context hazırlayıcı.
# app.py + Dockerfile + requirements'i kopyalar, modelleri (~196MB) ve dix'i (~18MB) VM'den indirir.
# Kullanım (repo kökünden):  bash deploy/stage.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CTX="$ROOT/deploy/_ctx"
VM_OPTS="-i $HOME/.ssh/cuvas_vm -P 2222 -o StrictHostKeyChecking=no"
SSH_OPTS="-i $HOME/.ssh/cuvas_vm -p 2222 -o StrictHostKeyChecking=no"
VM="root@127.0.0.1"

echo "[1/5] context temizleniyor: $CTX"
rm -rf "$CTX"; mkdir -p "$CTX"

echo "[2/5] app.py + Dockerfile + requirements + .dockerignore"
cp "$ROOT/platform/backend/app.py"      "$CTX/app.py"
cp "$ROOT/deploy/Dockerfile"            "$CTX/Dockerfile"
cp "$ROOT/deploy/requirements.txt"      "$CTX/requirements.txt"
cp "$ROOT/deploy/.dockerignore"         "$CTX/.dockerignore"
printf '__pycache__/\n*.pyc\n' > "$CTX/.gcloudignore"   # context temiz; her şey yüklensin (modeller dahil)

echo "[3/5] app.py md5 (VM ile eşit olmalı):"
md5sum "$CTX/app.py"

echo "[4/5] modeller (~196MB) VM'den indiriliyor..."
scp $VM_OPTS -q -r "$VM:/root/.turkicnlp/models/." "$CTX/models/"

echo "[5/5] dix (~18MB) VM'den indiriliyor..."
scp $VM_OPTS -q -r "$VM:/root/koken_api/dix/." "$CTX/dix/"

echo "--- context hazır ---"
du -sh "$CTX" "$CTX/models" "$CTX/dix" 2>/dev/null
echo "Sıradaki:  gcloud run deploy ... --source deploy/_ctx   (bkz. deploy/README.md)"
