"""
Étape 3 — Maître SANS protection contre les pannes
=====================================================
Identique à 3_master.py, mais les esclaves peuvent crasher.
Le maître n'a AUCUN mécanisme de récupération :
  → si un esclave meurt, le fruit qu'il préparait est perdu.
  → la salade est incomplète.

Prérequis : lancer les esclaves crash :
    python3 4_slave_crash.py 18861 &
    python3 4_slave_crash.py 18862 &
    python3 4_slave_crash.py 18863 &

Puis :
    python3 5_master_crash.py
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

# ─── Données partagées ─────────────────────────────────────────────
pile_taches = list(FRUITS)
resultats = []
lock = threading.Lock()

# ─── Fonction exécutée par chaque thread ────────────────────────────
def travailler(port):
    """
    Se connecte à l'esclave et distribue des tâches.
    Si l'esclave crashe, l'exception est attrapée mais le fruit
    est PERDU — pas de redistribution.
    """
    nom = f"Esclave:{port}"
    try:
        conn = rpyc.connect("localhost", port)
        print(f" {nom} connecté.")
    except Exception as e:
        print(f"❌ {nom} — connexion impossible : {e}")
        return

    while True:
        # ── Prendre un fruit ──
        with lock:
            if len(pile_taches) == 0:
                break
            fruit = pile_taches.pop(0)

        print(f" {nom} ← tâche : {fruit}")

        try:
            # ── Appel RPC ──
            resultat = conn.root.preparer_fruit(fruit)

            with lock:
                resultats.append(resultat)
                print(f" {nom} → résultat : {resultat}")

        except Exception as e:
            # L'esclave a crashé !
            print(f" {nom} — PANNE pendant « {fruit} » : {e}")
            print(f"   ⚠️  Le fruit « {fruit} » est PERDU.")
            print(f"   L'esclave {port} ne répond plus.")
            break  # on sort de la boucle, cet esclave est mort

    print(f" {nom} a terminé.")

# ─── Programme principal ────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("‍ MAÎTRE (SANS PROTECTION) — PANNES POSSIBLES")
    print("=" * 50)
    print(f"Fruits : {FRUITS}")
    print(f"Esclaves : {PORTS_ESCLAVES}")
    print(f"⚠️  Pas de timeout, pas de redistribution !")
    print()

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
    if len(resultats) == len(FRUITS):
        print(" SALADE TERMINÉE (chanceux, aucun crash !)")
    else:
        print("⚠️  SALADE INCOMPLÈTE !")
    print("=" * 50)
    print(f"Résultats ({len(resultats)}/{len(FRUITS)}) : {resultats}")
    print(f"Fruits manquants : {len(FRUITS) - len(resultats)}")
    print(f"⏱  Temps total : {duree:.1f} secondes")
