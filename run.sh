
CONFIG="config_files/config_l_2.txt"

python create_triplets.py $CONFIG

python zdlm.py $CONFIG

python plotzdlm.py $CONFIG
