"""
Étape 4 — Esclave avec crash (pour le test timeout)
======================================================
Identique à 4_slave_crash.py.
L'esclave peut crasher — c'est le MAÎTRE qui devient plus intelligent.
"""

import os
import sys
import time
import random
import rpyc
from rpyc.utils.server import ThreadedServer

# Probabilité de crash (0.3 = 30%)
PROBA_CRASH = 0.3  

class SlaveTimeoutService(rpyc.Service):
    def on_connect(self, conn):
        print("📡 Maître connecté.")

    def on_disconnect(self, conn):
        print("📴 Maître déconnecté.")

    def exposed_preparer_fruit(self, fruit):
        """Prépare un fruit ou crashe en essayant."""
        
        # ── Crash aléatoire ──
        # random.random() donne un nombre entre 0 et 1.
        # Si c'est < 0.3 (30% des cas), on déclenche un crash.
        if random.random() < PROBA_CRASH:
            print(f"💀 CRASH pendant : {fruit}")
            # os._exit(1) tue instantanément le processus Python. 
            # C'est une PANNE FRANCHE (fail-stop). 
            # Le maître ne reçoit même pas de message d'erreur, 
            # la connexion est juste coupée brutalement.
            os._exit(1)

        # Si on survit au crash, on prépare le fruit normalement
        print(f"🔪 Préparation de : {fruit} …")
        time.sleep(3)
        print(f"✅ {fruit} prêt !")
        return f"{fruit} prêt"

# ─── Lancement (classique) ──────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python3 6_slave_timeout.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    print("=" * 50)
    print(f"🧑‍🍳 ESCLAVE (TIMEOUT) — port {port}")
    print("=" * 50)
    print(f"⚠️  Probabilité de crash : {PROBA_CRASH*100:.0f}%")
    print(f"En attente de tâches…")
    print()

    serveur = ThreadedServer(SlaveTimeoutService, port=port)
    serveur.start()
