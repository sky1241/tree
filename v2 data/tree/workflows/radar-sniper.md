# Workflow Radar / Sniper

## Principe
- Deep Research = RADAR (prompt large, récolte les noms, URLs, termes)
- Claude web search = SNIPER (un par un, extraire les données précises)

## Étape 1 — Radar (Deep Research)
Prompt type :
> "Liste-moi TOUS les papers, outils, libs, blogs, auteurs qui traitent de [SUJET].
> Je veux les NOMS et RÉFÉRENCES uniquement — pas de résumé, pas d'analyse.
> Format : une ligne par référence avec auteur, année, titre, URL si dispo."

But : obtenir la CARTE (les branches à explorer). Accepter le bruit.

## Étape 2 — Triage
Parmi les résultats, marquer :
- ★ = critique (données chiffrées attendues)
- ○ = utile (contexte)
- ✗ = poubelle

## Étape 3 — Sniper (Claude web search)
Pour chaque ★, donner à Claude :
> "Cherche [Auteur Année Titre exact]. Je veux :
> 1. [question précise 1]
> 2. [question précise 2]
> Pas de résumé. Juste les données."

## Règles d'or
- Radar = large, on accepte le bruit
- Sniper = chirurgical, une cible à la fois
- JAMAIS les deux dans le même prompt
- Le radar donne la carte, le sniper explore le territoire
