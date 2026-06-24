#!/usr/bin/env bash
# KÖKEN diller-arası motoru için apertium iki-dilli sözlükleri (.dix) indirir (GPL-3.0).
# VM'de çalıştır: bash fetch_dix.sh   → /root/koken_api/dix/ altına indirir (gitignored, ~MB).
# /crosslang bunları lemma→lemma grafiğine yükler (BFS pivot). Yeni pair = listeye ekle.
set -e
DIR="${1:-$HOME/koken_api/dix}"
mkdir -p "$DIR"; cd "$DIR"
PAIRS="tur-aze tur-kir tur-tat tur-uzb kaz-tat kaz-kir tat-bak chv-tat kaz-uig"
for p in $PAIRS; do
  url="https://raw.githubusercontent.com/apertium/apertium-$p/master/apertium-$p.$p.dix"
  code=$(curl -s -o "$p.dix" -w "%{http_code}" "$url")
  if [ "$code" = "200" ]; then echo "$p.dix ($(grep -c '<e>' "$p.dix") giriş)"; else echo "$p -> HTTP $code (atlandı)"; rm -f "$p.dix"; fi
done
echo "Bağlanan diller: tur aze kir tat uzb kaz bak chv uig (sah: pair yok → cross-lang dışı)"
