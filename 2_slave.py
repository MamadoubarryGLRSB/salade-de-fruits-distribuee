"""
Étape 2 — Esclave (serveur RPyC)
==================================
L'esclave est un serveur RPC qui expose la fonction de préparation de fruit.
Il attend passivement que le maître l'appelle.

Lancer un esclave :
    python3 2_slave.py 18861
"""

# 'sys' permet d'interagir avec le système (ex: récupérer les arguments de la ligne de commande)
import sys
import time
# 'rpyc' est la bibliothèque qui permet de faire des appels de fonctions à distance via le réseau
import rpyc
# 'ThreadedServer' est un type de serveur RPyC qui crée un nouveau "thread" pour chaque client qui se connecte.
# Cela lui permet de gérer plusieurs maîtres en même temps si besoin.
from rpyc.utils.server import ThreadedServer

# ─── Service esclave ────────────────────────────────────────────────
# En RPyC, on crée toujours une classe qui hérite de "rpyc.Service". 
# C'est ce qui définit ce que le serveur accepte de faire.
class SlaveService(rpyc.Service):
    """Expose la préparation d'un fruit via RPC."""

    # Cette méthode est appelée automatiquement quand un client (le maître) se connecte
    def on_connect(self, conn):
        print(" Maître connecté.")

    # Cette méthode est appelée automatiquement quand le client se déconnecte
    def on_disconnect(self, conn):
        print(" Maître déconnecté.")

    # TRÈS IMPORTANT : Le préfixe "exposed_" indique à RPyC que cette méthode 
    # a le droit d'être appelée à travers le réseau. 
    # Si on appelait la méthode juste "preparer_fruit", le maître n'y aurait pas accès.
    def exposed_preparer_fruit(self, fruit):
        """
        Prépare un fruit (épluchage + découpage).
        Simule ~3 secondes de travail.
        Renvoie une chaîne confirmant que le fruit est prêt.
        """
        print(f" Préparation de : {fruit} …")
        
        # On simule un travail qui prend 3 secondes
        time.sleep(3)
        
        print(f"✅ {fruit} prêt !")
        
        # Ce return sera renvoyé au travers du réseau jusqu'au maître
        return f"{fruit} prêt"

# ─── Lancement ──────────────────────────────────────────────────────
# Cette condition vérifie si le script est exécuté directement 
# (et non pas importé comme un module dans un autre fichier)
if __name__ == "__main__":
    
    # sys.argv contient les arguments tapés dans la console. 
    # argv[0] c'est "2_slave.py". argv[1] c'est le port (ex: 18861)
    # S'il y a moins de 2 arguments, l'utilisateur a oublié de mettre le port.
    if len(sys.argv) < 2:
        print("Usage : python3 2_slave.py <port>")
        print("Exemple : python3 2_slave.py 18861")
        sys.exit(1) # Arrête le programme avec un code d'erreur 1

    # On convertit le port (qui est du texte) en nombre entier (int)
    port = int(sys.argv[1])

    print("=" * 50)
    print(f"‍ ESCLAVE — port {port}")
    print("=" * 50)
    print(f"En attente de tâches du maître…")
    print()

    # On crée le serveur. On lui donne notre classe SlaveService et le port sur lequel écouter.
    serveur = ThreadedServer(SlaveService, port=port)
    
    # On démarre le serveur. Cette ligne "bloque" le programme : 
    # le serveur tourne à l'infini et écoute les requêtes.
    serveur.start()
