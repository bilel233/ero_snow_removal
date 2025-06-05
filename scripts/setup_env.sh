#!/usr/bin/env bash
set -e

# on cree l'environnement venv
python3 -m venv .venv
source .venv/bin/activate

# On fait la mise à jour de pip et  wheel
python -m pip install --upgrade pip wheel

# Installation des dépendances a partir du fichier requirements
pip install -r ./requirements.txt