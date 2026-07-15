"""
Étape 3 — Esclave avec crash (panne franche)
===============================================
Identique à 2_slave.py, mais avec une probabilité de crash aléatoire.
Simule une panne franche (fail-stop) : l'esclave meurt brutalement.

Lancer :
    python3 4_slave_crash.py 18861
    python3 4_slave_crash.py 18862
    python3 4_slave_crash.py 18863
"""

import os
import sys
import time
import random
import rpyc
from rpyc.utils.server import ThreadedServer

# Probabilité de crash pendant la préparation d'un fruit
PROBA_CRASH = 0.3  # 30 %

# ─── Service esclave (avec crash possible) ──────────────────────────
class SlaveCrashService(rpyc.Service):
    """Expose la préparation d'un fruit, mais peut crasher."""

    def on_connect(self, conn):
        print("📡 Maître connecté.")

    def on_disconnect(self, conn):
        print("📴 Maître déconnecté.")

    def exposed_preparer_fruit(self, fruit):
        """
        Prépare un fruit… ou meurt en essayant.
        Panne franche : os._exit() = mort immédiate, pas d'exception.
        """
        # ── Crash aléatoire ──
        if random.random() < PROBA_CRASH:
            print(f"💀 CRASH pendant la préparation de : {fruit}")
            print(f"   L'esclave meurt brutalement (panne franche).")
            os._exit(1)  # mort immédiate — le processus disparaît

        # ── Préparation normale ──
        print(f"🔪 Préparation de : {fruit} …")
        time.sleep(3)
        print(f"✅ {fruit} prêt !")
        return f"{fruit} prêt"

# ─── Lancement ──────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python3 4_slave_crash.py <port>")
        print("Exemple : python3 4_slave_crash.py 18861")
        sys.exit(1)

    port = int(sys.argv[1])

    print("=" * 50)
    print(f"🧑‍🍳 ESCLAVE (CRASH) — port {port}")
    print("=" * 50)
    print(f"⚠️  Probabilité de crash : {PROBA_CRASH*100:.0f}%")
    print(f"En attente de tâches du maître…")
    print()

    serveur = ThreadedServer(SlaveCrashService, port=port)
    serveur.start()
