#!/usr/bin/env bash
set -euo pipefail

GRAPH_DIR="data/processed"
OUT_DIR="data/figures"
mkdir -p "${OUT_DIR}"

if [[ $# -gt 0 ]]; then
  graphs=("graph_sector_$1.pkl")
else
  graphs=(graph_sector_*.pkl)
fi

for g in "${graphs[@]}"; do
  graphfile="${GRAPH_DIR}/${g}"
  [[ -f "$graphfile" ]] || { echo "Fichier $graphfile absent"; continue; }
  sector="${g#graph_sector_}"
  sector="${sector%.pkl}"
  out_png="${OUT_DIR}/${sector}_drone.png"

  echo "Secteur : $sector"
  python -m src.drone.solve --graph "$graphfile" --out "$out_png"
done

echo "Terminé. PNG dans ${OUT_DIR}"
