#!/bin/bash
# Lance 3 esclaves de base (étape 2) en parallèle
echo " Lancement de 3 esclaves sur les ports 18861, 18862, 18863…"
python3 2_slave.py 18861 &
python3 2_slave.py 18862 &
python3 2_slave.py 18863 &
echo "✅ Esclaves lancés. Vous pouvez maintenant lancer le maître :"
echo "   python3 3_master.py"
echo ""
echo "Pour tout arrêter : kill %1 %2 %3  ou  pkill -f 2_slave.py"
wait
