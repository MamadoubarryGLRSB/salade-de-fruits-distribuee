"""
Étape 4 — Esclave avec simulation de panne (fail-stop)
======================================================
Cet esclave peut s'arrêter brutalement pour tester la résilience du maître.
"""

import os
import sys
import time
import random
import rpyc
from rpyc.utils.server import ThreadedServer

# Probabilité d'échec
PROBA_CRASH = 0.3  

class SlaveTimeoutService(rpyc.Service):
    def on_connect(self, conn):
        print(" Maître connecté.")

    def on_disconnect(self, conn):
        print(" Maître déconnecté.")

    def exposed_preparer_fruit(self, fruit):
        """Simule la préparation d'un fruit avec possibilité de panne franche."""
        
        # ── Simulation de crash ──
        if random.random() < PROBA_CRASH:
            print(f" CRASH pendant : {fruit}")
            os._exit(1)

        print(f" Préparation de : {fruit} …")
        time.sleep(3)
        print(f" {fruit} prêt !")
        return f"{fruit} prêt"

# ─── Lancement ──────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python3 6_slave_timeout.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    print("=" * 50)
    print(f" ESCLAVE (TIMEOUT) — port {port}")
    print("=" * 50)
    print(f"  Probabilité de crash : {PROBA_CRASH*100:.0f}%")
    print("En attente de tâches…")
    print()

    serveur = ThreadedServer(SlaveTimeoutService, port=port)
    serveur.start()
