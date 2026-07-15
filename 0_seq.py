"""
Étape 0 — Version séquentielle
================================
Un seul « cuisinier » prépare tous les fruits, l'un après l'autre.
C'est la référence : on mesure combien de temps cela prend (~26 s).
"""

import time

# ─── Liste des fruits à préparer ────────────────────────────────────
FRUITS = [
    "pomme", "banane", "kiwi", "mangue",
    "ananas", "orange", "fraise", "poire",
]

# ─── Fonction de préparation d'un fruit ─────────────────────────────
def preparer_fruit(fruit):
    """Simule l'épluchage + découpage d'un fruit (~3 secondes)."""
    print(f" Préparation de : {fruit} …")
    time.sleep(3)  # simule le travail
    print(f"✅ {fruit} prêt !")
    return f"{fruit} prêt"

# ─── Programme principal ────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print(" SALADE DE FRUITS — VERSION SÉQUENTIELLE")
    print("=" * 50)
    print(f"Fruits à préparer : {FRUITS}")
    print(f"Nombre de fruits  : {len(FRUITS)}")
    print()

    debut = time.time()

    resultats = []
    for fruit in FRUITS:
        resultat = preparer_fruit(fruit)
        resultats.append(resultat)

    fin = time.time()
    duree = fin - debut

    print()
    print("=" * 50)
    print(" SALADE TERMINÉE !")
    print("=" * 50)
    print(f"Résultats : {resultats}")
    print(f"⏱  Temps total : {duree:.1f} secondes")
    print(f"   (référence séquentielle)")
