#!/usr/bin/env bash
set -e
echo "▶ Phase 2 : préparation des données"
python3 -m src.data.prepare_data
echo "✔ Données prêtes (raw & processed)"