"""
Étape 1 — Test RPC minimal
============================
Un serveur RPyC expose une seule fonction qui renvoie 42.
Objectif : vérifier que RPyC fonctionne avant de construire le reste.

Lancer le serveur :
    python3 1_server.py

Tester depuis un autre terminal :
    python3 -c "import rpyc; print(rpyc.connect('localhost', 18861).root.repondre())"
    → doit afficher : 42
"""

import rpyc
from rpyc.utils.server import ThreadedServer

# ─── Service RPC minimal ────────────────────────────────────────────
class MonService(rpyc.Service):
    """Service de test : expose une seule méthode qui renvoie 42."""

    def on_connect(self, conn):
        print("📡 Un client s'est connecté.")

    def on_disconnect(self, conn):
        print("📴 Un client s'est déconnecté.")

    def exposed_repondre(self):
        """Méthode exposée au réseau — renvoie 42."""
        print("📨 Requête reçue → je renvoie 42")
        return 42

# ─── Lancement du serveur ───────────────────────────────────────────
if __name__ == "__main__":
    PORT = 18861

    print("=" * 50)
    print("🖥  SERVEUR RPC MINIMAL")
    print("=" * 50)
    print(f"En écoute sur le port {PORT}…")
    print(f"Testez avec :")
    print(f"  python3 -c \"import rpyc; print(rpyc.connect('localhost', {PORT}).root.repondre())\"")
    print()

    serveur = ThreadedServer(MonService, port=PORT)
    serveur.start()
