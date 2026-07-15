"""
Étape 4 — Maître Robuste (Timeout et Déduplication)
=========================================================
Le système gère les pannes franches, redistribue le travail non complété
et garantit l'unicité des résultats grâce à l'idempotence.
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

# Délai maximum avant de considérer l'esclave comme inactif
TIMEOUT = 6  

# ─── Données partagées ──────────────────────────────────────────────
pile_taches = list(FRUITS)       
resultats = []                   

# Ensemble pour mémoriser les tâches complétées (déduplication)
taches_terminees = set()         

lock = threading.Lock()          

def travailler(port):
    """Gère l'attribution des tâches, la détection des pannes et la redistribution."""
    nom = f"Esclave:{port}"

    try:
        conn = rpyc.connect("localhost", port)
        print(f" {nom} connecté.")
    except Exception as e:
        print(f" {nom} — connexion impossible : {e}")
        return

    while True:
        with lock:
            if len(pile_taches) == 0:
                break
            fruit = pile_taches.pop(0)

        print(f" {nom} ← tâche : {fruit}")

        try:
            # ── Appel RPC avec timeout ──
            async_result = rpyc.timed(conn.root.preparer_fruit, TIMEOUT)
            resultat = async_result(fruit)
            resultat = resultat.value  

            with lock:
                # ── Déduplication (garantie at-least-once) ──
                if fruit in taches_terminees:
                    print(f"  {nom} — doublon ignoré pour « {fruit} »")
                else:
                    taches_terminees.add(fruit)
                    resultats.append(resultat) 
                    print(f"  {nom} → résultat : {resultat}")

        except Exception as e:
            # ── Détection de panne ──
            print(f"  {nom} — TIMEOUT / PANNE pendant « {fruit} » : {type(e).__name__}")

            # ── Redistribution de la tâche ──
            with lock:
                if fruit not in taches_terminees:
                    pile_taches.append(fruit)
                    print(f"  « {fruit} » remis dans la pile (redistribution)")

            # Tentative de reconnexion
            try:
                conn = rpyc.connect("localhost", port)
                print(f"  {nom} — reconnexion réussie !")
            except Exception:
                print(f"  {nom} — reconnexion impossible, processus interrompu.")
                break 

    print(f" {nom} a terminé.")

# ─── Programme principal ────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print(" MAÎTRE ROBUSTE — TIMEOUT + DÉDUPLICATION")
    print("=" * 55)
    
    debut = time.time()

    threads = []
    for port in PORTS_ESCLAVES:
        t = threading.Thread(target=travailler, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    fin = time.time()
    
    print()
    print("=" * 55)
    
    if len(resultats) == len(FRUITS):
        print(" SALADE TERMINÉE — TOUTES LES TÂCHES ONT ÉTÉ COMPLÉTÉES")
    else:
        print(f"  ERREUR — {len(resultats)}/{len(FRUITS)} tâches complétées")
    print("=" * 55)
    print(f"Résultats ({len(resultats)}/{len(FRUITS)}) : {resultats}")
    print(f"  Temps total : {fin - debut:.1f} secondes")
