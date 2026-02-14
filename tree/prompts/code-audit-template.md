# Prompt d'audit de code

## Utilisation
Coller ce prompt à Claude avec le code source ou le nom du repo.

## Prompt

> Audite ce code. Pour CHAQUE problème trouvé :
> 1. Ligne exacte
> 2. Sévérité (CRITIQUE / MOYEN / FAIBLE)
> 3. Fix proposé (code, pas de blabla)
>
> Je ne veux pas :
> - "Le code est bien structuré" → je m'en fous
> - "Vous pourriez considérer" → dis-moi quoi faire
>
> Je veux :
> - L1234: BUG — variable non initialisée → fix: ajouter `x = 0`
> - L5678: PERF — boucle O(n²) → fix: utiliser dict lookup
>
> Format de sortie :
> ```
> [CRITIQUE] L1234 — description → fix
> [MOYEN]    L5678 — description → fix
> [FAIBLE]   L9012 — description → fix
> ```
>
> Trie par sévérité. CRITIQUE d'abord.
