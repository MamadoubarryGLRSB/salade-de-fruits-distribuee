"""
Étape 2 — Maître (client RPyC)
================================
Le maître distribue les fruits aux esclaves via RPC.
"""

# 'time' pour chronométrer la durée totale
import time
# 'threading' pour exécuter du code en parallèle (un thread par esclave)
import threading
# 'rpyc' pour communiquer avec les esclaves
import rpyc

# ─── Configuration ──────────────────────────────────────────────────
# La liste de tous les fruits qu'on veut préparer
FRUITS = [
    "pomme", "banane", "kiwi", "mangue",
    "ananas", "orange", "fraise", "poire",
]

# Les ports sur lesquels nos 3 esclaves écoutent
PORTS_ESCLAVES = [18861, 18862, 18863]

# ─── Données partagées (protégées par verrou) ───────────────────────
# On convertit la liste FRUITS en une nouvelle liste "pile_taches".
# Cette pile va se vider au fur et à mesure.
pile_taches = list(FRUITS)       

# Une liste vide pour stocker les fruits une fois qu'ils sont préparés
resultats = []                   

# TRÈS IMPORTANT : Le Verrou (Mutex). 
# Comme on a 3 threads qui tournent en même temps, s'ils essaient de prendre 
# un fruit dans 'pile_taches' exactement à la même milliseconde, ça va planter.
# Le 'lock' garantit qu'un seul thread à la fois peut toucher à la pile.
lock = threading.Lock()          

# ─── Fonction exécutée par chaque thread ────────────────────────────
# Cette fonction est le "cerveau" qui gère un seul esclave.
def travailler(port):
    """Se connecte à l'esclave et lui donne du travail en boucle."""
    nom = f"Esclave:{port}" # Juste pour faire des jolis prints (ex: "Esclave:18861")
    
    try:
        # On se connecte à l'esclave. "localhost" veut dire que l'esclave est sur le même ordinateur.
        conn = rpyc.connect("localhost", port)
        print(f"📡 {nom} connecté.")
    except Exception as e:
        # Si on n'arrive pas à se connecter (par exemple si on a oublié de lancer l'esclave)
        print(f"❌ {nom} — connexion impossible : {e}")
        return # On arrête cette fonction

    # Boucle infinie : on donne du travail tant qu'il y en a
    while True:
        
        # ── Section critique : prendre un fruit dans la pile ──
        # Le "with lock:" active le verrou. Les autres threads sont bloqués à cette ligne
        # jusqu'à ce que ce thread finisse et relâche le verrou.
        with lock:
            # S'il n'y a plus de fruits dans la pile, on arrête (break sort du 'while True')
            if len(pile_taches) == 0:
                break
            # pop(0) enlève le 1er élément de la liste et nous le donne. 
            fruit = pile_taches.pop(0)
            # Fin de l'indentation 'with lock' : le verrou est automatiquement relâché ici !

        print(f"📤 {nom} ← tâche : {fruit}")

        # ── Appel RPC distant ──
        # Note qu'on est EN DEHORS du verrou. C'est crucial : on ne veut pas bloquer 
        # les autres threads pendant les 3 secondes où l'esclave prépare le fruit !
        # L'appel réseau : conn.root permet d'accéder aux méthodes "exposed_" de l'esclave.
        resultat = conn.root.preparer_fruit(fruit)

        # ── Section critique : stocker le résultat ──
        # Le fruit est prêt. Il faut l'ajouter à la liste 'resultats'.
        # Comme c'est une liste partagée, on doit remettre le verrou.
        with lock:
            resultats.append(resultat)
            print(f"📥 {nom} → résultat : {resultat}")

    # On ferme proprement la connexion quand il n'y a plus de fruits
    conn.close()
    print(f"🏁 {nom} a fini (plus de tâches).")

# ─── Programme principal ────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("👨‍🍳 MAÎTRE — DISTRIBUTION DES TÂCHES")
    print("=" * 50)
    
    # On mémorise l'heure de départ
    debut = time.time()

    # On crée une liste pour garder une trace de nos threads
    threads = []
    
    # Pour chaque port (18861, 18862, 18863)...
    for port in PORTS_ESCLAVES:
        # On crée un Thread. On lui dit "exécute la fonction 'travailler' avec l'argument 'port'"
        t = threading.Thread(target=travailler, args=(port,))
        threads.append(t) # On l'ajoute à notre liste
        t.start()         # On DÉMARRE le thread. Il part faire sa vie en parallèle !

    # À ce stade, le programme principal continue instantanément, 
    # mais nos 3 threads tournent en tâche de fond.
    
    # Il faut DIRE au programme principal d'attendre que les threads aient fini !
    for t in threads:
        # .join() bloque le programme jusqu'à ce que le thread 't' se termine
        t.join()

    # Quand on arrive ici, tous les threads ont terminé.
    fin = time.time()
    duree = fin - debut # On calcule le temps écoulé

    print()
    print("=" * 50)
    print("🥗 SALADE TERMINÉE !")
    print("=" * 50)
    print(f"Résultats ({len(resultats)}/{len(FRUITS)}) : {resultats}")
    print(f"⏱  Temps total : {duree:.1f} secondes")
