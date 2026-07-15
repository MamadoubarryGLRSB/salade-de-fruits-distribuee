#!/bin/bash
# Lance 3 esclaves CRASH (étape 3 & 4) en parallèle
echo " Lancement de 3 esclaves (CRASH) sur les ports 18861, 18862, 18863…"
echo "⚠️  Ces esclaves ont 30% de chance de crasher pendant une tâche."
echo ""

# Pour l'étape 3 (sans protection) :
#   python3 4_slave_crash.py 18861 &
#   python3 4_slave_crash.py 18862 &
#   python3 4_slave_crash.py 18863 &

# Pour l'étape 4 (avec timeout) :
python3 6_slave_timeout.py 18861 &
python3 6_slave_timeout.py 18862 &
python3 6_slave_timeout.py 18863 &

echo "✅ Esclaves crash lancés. Lancer le maître :"
echo "   Étape 3 : python3 5_master_crash.py"
echo "   Étape 4 : python3 7_master_timeout.py"
echo ""
echo "Pour tout arrêter : pkill -f slave"
wait
