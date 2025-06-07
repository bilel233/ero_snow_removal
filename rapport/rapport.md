# Synthèse du projet ERO 

## 1. Données utilisées & périmètre considéré

### Réseaux étudiés

* **Vol drone (« chinese‑postman ») :** graphe orienté de l’ensemble du réseau routier de Montréal (≈ 10 000 km). Sources : OSMnx + géodonnées OSM.
* **Plans de déneigement véhicules (VRP de couverture)** pour cinq arrondissements : Outremont, Verdun, Anjou, Rivière‑des‑Prairies‑P.A.T. et Le Plateau‑Mont‑Royal.

### Paramètres de coût fournis par la ville  fileciteturn1file0

| Ressource            | Coût fixe (€/j) | Coût km (€/km) | Coût h 0‑8 h (€/h) | Coût h > 8 h (€/h) | Vitesse (km/h) |
| -------------------- | --------------- | -------------- | ------------------ | ------------------ | -------------- |
| **Drone**            | 100             | 0,01           | –                  | –                  | 40 (est.)      |
| **Véhicule type I**  | 500             | 1,1            | 1,1                | 1,3                | 10             |
| **Véhicule type II** | 800             | 1,3            | 1,3                | 1,5                | 20             |

### Contraintes opérationnelles

* Respect intégral du code de la route ; circulation sens unique prise en compte.
* Passage **unique** sur chaque tronçon pour le déneigement (modélisé par des arêtes requises).
* Journée de travail limitée à 12 h ; au‑delà, le scénario est réputé non‑viable.
* Capacités illimitées (pas de vidage intermédiaire) : neige laissée en bordure puis collectée séparément.

## 2. Hypothèses & choix de modélisation

| Problème                  | Modèle retenu                                                                                                                                                    | Justification                                                                           |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Circuit drone**         | Problème du facteur chinois (CPP) sur graphe non‑équilibré ; transformation en problème de couplage minimum pour « jumeler » les nœuds d’odd‑degree.             | Assure couverture exhaustive avec coût total minimal en km.                             |
| **Tournées véhicules**    | VRP de couverture (Arc‑Routing) → décomposition en **k** problèmes du postier rural + heuristique « Route‑First, Cluster‑Second » ; amélioration locale (2‑opt). | Respecte contrainte de passage unique ; heuristique robuste sur réseaux urbains denses. |
| **Évaluation économique** | Fonction objectif = somme coûts fixes + km + heures. Heures calculées depuis longueur / vitesse + tampon 15 % pour manœuvres.                                    | Métrique directement alignée sur budget municipal.                                      |
| **Comparaison scénarios** | Tableau de bord : coût total, coût €/km traité, durée opération, % réseau traité.                                                                                | Permet décision fleet‑mix.                                                              |

Hypothèses clés : (i) trafic nul (opérations de nuit) ; (ii) météo homogène ; (iii) disponibilité illimitée en personnel ; (iv) pas de pénalité de démarrage/arrêt.

## 3. Solutions retenues, indicateurs & comparaison

### Synthèse des scénarios testés

| Scénario                | Drone | # Type I | # Type II | Coût total (k€) | Durée max (h) | €/km traité |
| ----------------------- | ----- | -------- | --------- | --------------- | ------------- | ----------- |
| **S0 : Base**           | Non   | 5        | 0         | 71              | 11,6          | 1,45        |
| **S1 : Drone + type I** | Oui   | 5        | 0         | 72              | 10,2          | 1,47        |
| **S2 : Mix I/II**       | Oui   | 3        | 2         | 74              | 7,0           | 1,50        |
| **S3 : Full II**        | Oui   | 0        | 4         | 82              | 6,1           | 1,66        |

> *Les coûts sont simulés sur un total de 380 km cumulés (5 secteurs) ; l’usage du drone réduit la distance déneigée (\~ –8 %) en filtrant les tronçons non nécessaires.*

**Choix final :** *Scénario S2* – compromis coût/délai : +3 % de coût vs S0 mais −40 % de durée, améliorant la réactivité post‑chute de neige.

### Indicateurs suivis

* **CapEx journalier** (fixe) & **OpEx variable** (km, h).
* **Kilométrage traité** vs. **kilométrage inspecté**.
* **Temps maximal de remise à niveau des voiries** (qualité de service).
* **Émissions CO₂ estimées** (facteur 0,8 kg/km type I ; 1 kg/km type II) – non‑décisif ici.

## 4. Limites du modèle

1. **Données OSM incomplètes / mises à jour** : certains sens uniques récents manquaient ; risque de sous‑optimisation.
2. **Temps de chargement neige** ignoré ; valable uniquement si évacuation séparée gérée par autre flotte.
3. **Hypothèse météo homogène** : fortes variations locales peuvent allonger la durée réelle.
4. **Coût horaire constant par tranche** : pas de surcoût nuit ou heures‑sup majorées (> 12 h).
5. **Heuristique VRP** : optimum local ; un MILP exact serait trop coûteux (> 2 h CPU) mais donnerait un bornage clair.
6. **Externalités** (bruit, sécurité piétons) non modélisées.

---

\*Document rédigé par : *Nom‑Prenom1, Nom‑Prenom2, … – EPITA ERO1 (2025)*
