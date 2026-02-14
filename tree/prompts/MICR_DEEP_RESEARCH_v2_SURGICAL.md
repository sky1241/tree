# MICR Deep Research v2 — Prompt Chirurgical

## Contexte
MICR = Moteur Inverse de Contraintes Réelles. Solveur inverse pour automates à cames.
Au lieu de : figurine → mécanisme → vérifier collisions
On fait : figurine + mouvement souhaité → calculer mécanisme optimal → garantir zéro collision

## Prompt pour Deep Research

> Je développe un solveur inverse pour automates mécaniques à cames imprimés en 3D (FDM/PLA).
> Le solveur part de la forme de la figurine + le mouvement désiré et calcule le mécanisme optimal.
>
> J'ai besoin de données CONCRÈTES (pas de résumés) sur ces 7 questions :
>
> 1. **Swept volume** : Quelle formule pour calculer le pas angulaire Δθ d'un swept volume
>    en fonction du rayon R et de la taille de voxel ? (chercher Song 2017, Coros 2013)
>
> 2. **Clearances FDM** : Données mesurées de jeu radial pour PLA imprimé en FDM pour :
>    pin-pivot, shaft-bearing (4mm et 6mm), cam-on-shaft (press-fit),
>    follower-guide, pushrod-socket, gear backlash. (chercher CNCKitchen, Maker's Muse)
>
> 3. **Optimisation** : Quel solveur scipy pour 20 variables avec contraintes non-linéaires
>    et variables mixtes (continues + discrètes) ? SLSQP vs COBYLA vs differential_evolution.
>    Budget : 30 secondes max.
>
> 4. **Collision formulation** : Comment formuler g(x) ≥ 0 pour 3 catégories :
>    Contact intentionnel (cam-shaft), Proximité structurelle (wall-bracket),
>    Collision interdite (pushrod-through-figurine).
>
> 5. **Pushrod routing** : Algorithme pour router un pushrod autour d'un obstacle (figurine AABB).
>    Rayon de courbure minimum pour fil acier Ø1.5mm. (chercher A*, bend radius formula)
>
> 6. **Tolerance stack-up** : Formule RSS pour chaîne de 6 interfaces à ±0.25mm.
>    Compensation recommandée sur amplitude de came.
>
> 7. **Shaft deflection** : Formule de flèche pour arbre Ø6mm acier, L=180mm,
>    5 charges ponctuelles réparties. Limite acceptable pour automate jouet.
>
> FORMAT : Pour chaque question, je veux :
> - La formule exacte avec les variables
> - Les valeurs numériques mesurées si disponibles
> - La référence (auteur, année, titre)
> - PAS de résumé, PAS d'introduction, JUSTE les données
