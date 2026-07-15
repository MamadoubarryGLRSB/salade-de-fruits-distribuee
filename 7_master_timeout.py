"""
Étape 4 — Maître ROBUSTE avec timeout et déduplication
=========================================================
Le chef-d'œuvre du système distribué. 
Le maître gère les pannes, redistribue le travail, et s'assure qu'aucun fruit
n'est préparé en double.
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

# ── LE TIMEOUT ──
# On sait que la préparation d'un fruit prend 3 secondes.
# Si au bout de 6 secondes l'esclave n'a toujours pas répondu, 
# on DÉCIDE qu'il est en panne. 
TIMEOUT = 6  

# ─── Données partagées (protégées par verrou) ───────────────────────
pile_taches = list(FRUITS)       
resultats = []                   

# ── LA DÉDUPLICATION ──
# Un "set()" en Python est une collection mathématique d'éléments UNIQUES.
# Si on ajoute "pomme" deux fois dans un set, il n'y sera qu'une seule fois.
# On va s'en servir pour retenir quels fruits ont DÉJÀ été préparés, 
# au cas où un esclave lent renvoie un fruit qui avait été redistribué.
taches_terminees = set()         

lock = threading.Lock()          

def travailler(port):
    nom = f"Esclave:{port}"

    try:
        conn = rpyc.connect("localhost", port)
        print(f"📡 {nom} connecté.")
    except Exception as e:
        print(f"❌ {nom} — connexion impossible : {e}")
        return

    while True:
        # Prendre un fruit dans la pile (sécurisé par le verrou)
        with lock:
            if len(pile_taches) == 0:
                break
            fruit = pile_taches.pop(0)

        print(f"📤 {nom} ← tâche : {fruit}")

        try:
            # ── APPEL RPC AVEC TIMEOUT ──
            # rpyc.timed "emballe" notre fonction. 
            # Ça crée un 'async_result' qui va attendre au maximum TIMEOUT (6) secondes.
            async_result = rpyc.timed(conn.root.preparer_fruit, TIMEOUT)
            
            # On lance l'appel réseau
            resultat = async_result(fruit)
            
            # .value est bloquant : il attend la réponse du serveur.
            # S'il reçoit une réponse dans les 6 secondes, tout va bien.
            # Si le délai de 6 secondes est dépassé, ou si la connexion coupe (crash), 
            # ça lève une ERREUR (Exception) qu'on va attraper dans le 'except' en dessous !
            resultat = resultat.value  

            # ── Si on arrive ici, l'appel a RÉUSSI ──
            with lock:
                # ── DÉDUPLICATION ──
                # On vérifie si ce fruit n'est pas DEJA dans notre liste de fruits terminés
                if fruit in taches_terminees:
                    print(f"🔁 {nom} — doublon ignoré pour « {fruit} »")
                else:
                    # C'est la première fois qu'on termine ce fruit. On l'ajoute au set.
                    taches_terminees.add(fruit)
                    resultats.append(resultat) # Et on garde le vrai résultat
                    print(f"📥 {nom} → résultat : {resultat}")

        except Exception as e:
            # ── Si on arrive ici, l'appel a ÉCHOUÉ (Crash ou Timeout) ──
            print(f"⏰ {nom} — TIMEOUT / PANNE pendant « {fruit} » : {type(e).__name__}")

            # ── REDISTRIBUTION ──
            # Le fruit n'a pas été fini ! Il faut le redonner à un autre.
            with lock:
                # On vérifie quand même qu'un autre esclave (plus rapide) ne l'a pas déjà fini
                if fruit not in taches_terminees:
                    # On le REMET DANS LA PILE à la fin. Un autre thread/esclave le prendra.
                    pile_taches.append(fruit)
                    print(f"🔄 « {fruit} » remis dans la pile (redistribution)")

            # L'esclave a planté. On essaie de se reconnecter à lui (peut-être qu'il a redémarré ?)
            try:
                conn = rpyc.connect("localhost", port)
                print(f"🔌 {nom} — reconnexion réussie !")
            except Exception:
                # Si on ne peut pas se reconnecter, c'est qu'il est bien mort.
                print(f"💀 {nom} — reconnexion impossible, esclave mort.")
                break  # Le 'break' sort du While True, le Thread meurt.

    print(f"🏁 {nom} a terminé.")

# ─── Programme principal ────────────────────────────────────────────
if __name__ == "__main__":
    # Le démarrage est identique au maître précédent
    print("=" * 55)
    print("👨‍🍳 MAÎTRE ROBUSTE — TIMEOUT + DÉDUPLICATION")
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
    
    # ─── Bilan final ───
    print()
    print("=" * 55)
    
    # Grâce à la redistribution, on a la GARANTIE que la liste de résultats est complète,
    # sauf si TOUS les esclaves sont morts avant d'avoir fini.
    if len(resultats) == len(FRUITS):
        print("🥗 SALADE TERMINÉE — TOUS LES FRUITS PRÉPARÉS !")
    else:
        print(f"⚠️  SALADE INCOMPLÈTE — {len(resultats)}/{len(FRUITS)} fruits")
        print(f"   (tous les esclaves sont morts avant de finir)")
    print("=" * 55)
    print(f"Résultats ({len(resultats)}/{len(FRUITS)}) : {resultats}")
    print(f"⏱  Temps total : {fin - debut:.1f} secondes")
