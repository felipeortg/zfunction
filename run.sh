
CONFIG="config_files/config_scrat.txt"

python create_triplets.py $CONFIG

python zdlm.py $CONFIG

python plotzdlm.py $CONFIG
