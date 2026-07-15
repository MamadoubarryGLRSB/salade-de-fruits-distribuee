# 🍉 Aide-mémoire : Comment tester

Voici la version ultra-simple pour lancer les 4 étapes de ton projet.

---

### Étape 0 : Le mode lent (séquentiel)
*Un seul cuisinier fait tout.*
1. Ouvre un terminal et tape :
   `python3 0_seq.py`
2. Attends... ça prend environ 24 secondes.

---

### Étape 1 : Le test du serveur (RPC)
*Vérifie que les machines peuvent se parler.*
1. Ouvre le terminal A et lance le serveur :
   `python3 1_server.py`
2. Ouvre le terminal B et teste s'il répond bien "42" :
   `python3 -c "import rpyc; print(rpyc.connect('localhost', 18861).root.repondre())"`
3. Coupe le serveur (Ctrl+C).

---

### Étape 2 : Le système distribué (Rapide !)
*1 maître distribue le travail à 3 esclaves.*
1. Ouvre le terminal A et lance les 3 esclaves en même temps :
   `bash start_slaves.sh`
2. Ouvre le terminal B et lance le maître :
   `python3 3_master.py`
3. Regarde la magie : c'est 3x plus rapide ! (~9 secondes)
4. Nettoie tout en tapant : `pkill -f 2_slave.py`

---

### Étape 3 : Le problème (Les pannes)
*Que se passe-t-il si un esclave meurt en plein travail ?*
1. Ouvre le terminal A et lance les esclaves "fragiles" (qui peuvent planter) :
   `python3 4_slave_crash.py 18861 & python3 4_slave_crash.py 18862 & python3 4_slave_crash.py 18863 &`
2. Ouvre le terminal B et lance le maître (qui n'est pas protégé) :
   `python3 5_master_crash.py`
3. Oups... des fruits manquent à la fin, la salade est gâchée.
4. Nettoie tout en tapant : `pkill -f 4_slave_crash.py`

---

### Étape 4 : La solution (Le Timeout)
*Le maître devient intelligent : s'il n'a pas de réponse, il redonne le fruit à un autre.*
1. Ouvre le terminal A et lance les esclaves "fragiles" (avec le script) :
   `bash start_slaves_crash.sh`
2. Ouvre le terminal B et lance le maître "robuste" :
   `python3 7_master_timeout.py`
3. Même s'il y a des crashs, tous les fruits sont finalement préparés !
4. Nettoie tout en tapant : `pkill -f 6_slave_timeout.py`
