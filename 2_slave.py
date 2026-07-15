"""
Étape 2 — Esclave (serveur RPyC)
==================================
L'esclave agit comme un serveur RPC qui expose la fonction de préparation de fruit.
Il attend passivement les instructions du maître.
"""

import sys
import time
import rpyc
from rpyc.utils.server import ThreadedServer

# ─── Service esclave ────────────────────────────────────────────────
class SlaveService(rpyc.Service):
    """Expose la fonction de préparation d'un fruit via RPC."""

    def on_connect(self, conn):
        print(" Maître connecté.")

    def on_disconnect(self, conn):
        print(" Maître déconnecté.")

    def exposed_preparer_fruit(self, fruit):
        """
        Prépare un fruit (épluchage et découpage).
        Simule 3 secondes de traitement.
        Retourne une chaîne confirmant la fin de la tâche.
        """
        print(f" Préparation de : {fruit} …")
        time.sleep(3)
        print(f" {fruit} prêt !")
        return f"{fruit} prêt"

# ─── Lancement ──────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python3 2_slave.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    print("=" * 50)
    print(f" ESCLAVE — port {port}")
    print("=" * 50)
    print("En attente de tâches du maître…")
    print()

    serveur = ThreadedServer(SlaveService, port=port)
    serveur.start()
