# Projet : Salade de Fruits Distribuée

Ce projet illustre la création d'un système distribué en Python (architecture Maître-Esclave) avec la bibliothèque RPyC. Il aborde le parallélisme, la gestion des accès concurrents et la tolérance aux pannes.

## Installation

```bash
pip3 install rpyc
```

## Utilisation

Le projet est conçu pour être testé étape par étape.

### Étape 0 : Mode Séquentiel (Référence)
Exécute le programme de manière classique (un seul processus).
```bash
python3 0_seq.py
```
*Temps estimé : ~24 secondes.*

### Étape 1 : Test RPC
Vérifie la communication réseau de base.
- Terminal 1 (Serveur) : `python3 1_server.py`
- Terminal 2 (Client) : `python3 -c "import rpyc; print(rpyc.connect('localhost', 18861).root.repondre())"`

### Étape 2 : Système Distribué (Maître-Esclave)
Exécute le programme en parallèle sur 3 esclaves.
- Terminal 1 (Esclaves) : `bash start_slaves.sh`
- Terminal 2 (Maître) : `python3 3_master.py`
*Temps estimé : ~9 secondes.*
*(Nettoyage : `pkill -f 2_slave.py`)*

### Étape 3 : Simulation de Pannes
Montre l'échec du système lorsqu'un esclave s'arrête brutalement (crash).
- Terminal 1 : `python3 4_slave_crash.py 18861 & python3 4_slave_crash.py 18862 & python3 4_slave_crash.py 18863 &`
- Terminal 2 : `python3 5_master_crash.py`
*Résultat attendu : Traitement incomplet (perte de données).*
*(Nettoyage : `pkill -f 4_slave_crash.py`)*

### Étape 4 : Système Robuste (Timeout et Redistribution)
Montre le système final capable de survivre aux pannes grâce à un mécanisme de timeout et de déduplication.
- Terminal 1 : `bash start_slaves_crash.sh`
- Terminal 2 : `python3 7_master_timeout.py`
*Résultat attendu : Traitement terminé avec succès malgré les crashs.*
*(Nettoyage : `pkill -f 6_slave_timeout.py`)*
