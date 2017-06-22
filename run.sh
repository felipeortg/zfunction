
CONFIG="config_files/config_l_0_d_000.txt"

#python create_triplets.py $CONFIG

python zdlm.py $CONFIG

python plotzdlm.py $CONFIG
