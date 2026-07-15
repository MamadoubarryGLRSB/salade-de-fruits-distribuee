"""
Étape 2 — Maître (client RPyC)
================================
Le maître distribue les tâches aux esclaves via RPC.
L'accès aux ressources partagées est géré par un verrou.
"""

import time
import threading
import rpyc

# ─── Configuration ──────────────────────────────────────────────────
FRUITS = [
    "pomme", "banane", "kiwi", "mangue",
    "ananas", "orange", "fraise", "poire",
]

PORTS_ESCLAVES = [18861, 18862, 18863]

# ─── Données partagées ──────────────────────────────────────────────
pile_taches = list(FRUITS)       
resultats = []                   

# Verrou (Mutex) pour assurer l'exclusion mutuelle lors de l'accès à la pile
lock = threading.Lock()          

# ─── Fonction exécutée par chaque thread ────────────────────────────
def travailler(port):
    """Gère la connexion à un esclave et l'attribution des tâches."""
    nom = f"Esclave:{port}" 
    
    try:
        conn = rpyc.connect("localhost", port)
        print(f" {nom} connecté.")
    except Exception as e:
        print(f" {nom} — connexion impossible : {e}")
        return 

    while True:
        # ── Section critique : extraction d'une tâche ──
        with lock:
            if len(pile_taches) == 0:
                break
            fruit = pile_taches.pop(0)

        print(f" {nom} ← tâche : {fruit}")

        # ── Appel RPC distant ──
        resultat = conn.root.preparer_fruit(fruit)

        # ── Section critique : stockage du résultat ──
        with lock:
            resultats.append(resultat)
            print(f" {nom} → résultat : {resultat}")

    conn.close()
    print(f" {nom} a terminé (plus de tâches).")

# ─── Programme principal ────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print(" MAÎTRE — DISTRIBUTION DES TÂCHES")
    print("=" * 50)
    
    debut = time.time()
    threads = []
    
    for port in PORTS_ESCLAVES:
        t = threading.Thread(target=travailler, args=(port,))
        threads.append(t) 
        t.start()         

    for t in threads:
        t.join()

    fin = time.time()
    duree = fin - debut 

    print()
    print("=" * 50)
    print(" SALADE TERMINÉE !")
    print("=" * 50)
    print(f"Résultats ({len(resultats)}/{len(FRUITS)}) : {resultats}")
    print(f"  Temps total : {duree:.1f} secondes")
