# ERO Snow-Removal Optimization

Optimisation des opérations de déneigement de la Ville de Montréal dans le cadre du projet **ERO** (Élement — Recherche — Optimisation).

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📌 Objectifs du projet
1. **Tournée drone** : trouver un circuit minimal couvrant toutes les routes de Montréal  
   (problème du facteur chinois / *Chinese Postman*).  
2. **Plan de déneigement** : générer, pour cinq secteurs ciblés, des tournées de véhicules
   avec passage unique et respect du code de la route (VRP avec couverture).  
3. **Modèle de coûts global** : comparer plusieurs scénarios de flotte
   (types I & II, effectifs) en agrégeant coûts fixes, kilométriques et horaires.

---

## 🗂️ Arborescence prévue du dépôt
```plaintext
├── AUTHORS
├── LICENSE
├── README.md
├── data/                  # Jeux de données (raw, processed, figures)
├── notebooks/             # Prototypes et analyses exploratoires
├── src/                   # Code source (modules Python)
├── scripts/               # Scripts shell pour rejouer le pipeline
├── demo/                  # Exemples d’utilisation
├── report/                # PDF de synthèse final
└── .gitignore