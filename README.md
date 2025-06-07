# ERO – Optimisation des tournées de déneigement

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Licence](https://img.shields.io/badge/Licence-MIT-green)

> **ERO** (Engineering Route Optimiser) est une boîte à outils **open‑source** pour planifier et simuler les opérations de déneigement à Montréal à l’aide de flottes mixtes : camions, pick‑ups et drones épandeurs de saumure.
>
> Elle combine théorie des graphes (postier chinois, VRP), programmation linéaire en nombres entiers et animation temps réel afin de comparer plusieurs scénarios d’équipement.

---

## ✨ Fonctionnalités principales

| Dossier / Fichier                           | Rôle                                                               | Statut        |
| ------------------------------------------- | ------------------------------------------------------------------ | ------------- |
| `src/drone/model.py` & `src/drone/solve.py` | Formulation et résolution du sous‑problème drone (postier chinois) | ✅ Fonctionnel |
| `src/carp_mvp.py`                           | Prototype VRP / CARP pour camions & pick‑ups                       | 🚧 En cours   |
| `src/data/prepare_data.py`                  | Nettoyage & conversion des réseaux via GeoPandas                   | ✅ Basique     |
| `demo/demo_live.py`                         | **NOUVEAU** : animation Matplotlib temps réel d’une tournée        | ✅ Prêt        |

---

## 🏁 Démarrage rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/bilel233/ero_snow_removal.git
cd ero_snow_removal

# 2. Créer & activer l’environnement virtuel
python -m venv .venv && source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt   # networkx, geopandas, ortools, matplotlib, pandas…

# 4. Lancer la démonstration live (secteur d’Outremont)
python demo/demo_live.py --sector Outremont
```

> **Astuce :** changez `--sector` (Anjou, Verdun, Plateau‑Mont‑Royal…) ou passez un pickle NetworkX via `--graph data/processed/graph_sector_Anjou.pkl`.

---

## 📂 Organisation du dépôt (simplifiée)

```
├── README.md
├── pyproject.toml / requirements.txt
├── AUTHORS
├── data/                     ← données brutes & pré‑traitées
│   ├── raw/                  # shapefiles OSM + secteurs
│   ├── processed/            # graphes pickle ready‑to‑use
│   └── figures/              # images pour le rapport
├── src/
│   ├── drone/                ← modèle & solveur pour drones
│   ├── carp_mvp.py           ← prototype VRP véhicules
│   └── ...
├── demo/
│   ├── demo_live.py          ← animation temps réel
│   └── demo.py               ← script statique (figures)
├── scripts/                  ← CLI utilitaires (setup, run_demo, etc.)
├── notebooks/                ← analyses Jupyter
├── docs/                     ← documentation (modèle math., etc.)
└── tests/                    ← tests unitaires pytest
```

---

## 🧠 Méthodologie

1. **Modélisation du graphe** – Les rues sont des arêtes, les intersections des nœuds. Chaque arête porte une hauteur de neige et une priorité.
2. **Sous‑problèmes**
   a. *Drones* → Arc‑routing (postier chinois) pour l’épandage ciblé.
   b. *Véhicules* → VRP/CARP capacitaire avec fenêtres temporelles pour chasse‑neige.
   c. *Coûts* → Combinaison linéaire (coûts fixes, distances, main‑d’œuvre, émissions).
3. **Comparaison de scénarios** – KPI (coût total, longueur de tournée, GES, temps de service) calculés pour différentes tailles de flotte (cf. `notebooks/cost_benchmark.ipynb`).
4. **Simulation** – `demo/demo_live.py` anime la progression sur le graphe en temps réel.

---

## 🚧 Feuille de route

* [ ] Animation multi‑agents (couleurs & vitesses distinctes)
* [ ] Intégration complète du VRP OR‑Tools dans la boucle de simulation
* [ ] Tableau de bord Dash/Streamlit pour les KPI de scénarios
* [ ] CI automatisée (pytest + coverage GitHub Actions)

---

## 🤝 Contribuer

1. Forkez le dépôt et créez votre branche (`git checkout -b feat/maFonction`).
2. Activez les hooks `pre‑commit` pour lint & formatage.
3. Ajoutez des tests (`pytest`).
4. Ouvrez une Pull Request.



---

## 📜 Licence

Ce projet est distribué sous licence **MIT** – voir le fichier [LICENSE](LICENSE).

---

## 📣 Remerciements

* OR‑Tools (Google) – solveur en nombres entiers
* NetworkX & GeoPandas – algorithmes de graphes & traitement SIG
* Données ouvertes de la Ville de Montréal – réseaux routiers
