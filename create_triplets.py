import sys
import pickle
import os

# -----------------
# Config file:
config_file = str(sys.argv[1])

with open(config_file, 'r') as f:
	for line in f:
		if line[0:9] == 'cube num ':
			cube_num = int(line[9:-1])
			print 'Triplets max value:' + str(cube_num)

trip_folder = '../felipe_results/'
n_list = []
w_list = []

for x_coord in range(-cube_num,cube_num+1):
		for y_coord in range(-cube_num,cube_num+1):
			for z_coord in range(-cube_num,cube_num+1):
				triplet = [x_coord,y_coord,z_coord]
				norm = 0
				for el in triplet: norm += el**2
				if norm < cube_num**2:
					n_list.append(triplet)
					if norm != 0:
						w_list.append(triplet)
					

folder = trip_folder +'triplets/'

filename = folder + 'n_list_r<' + str(cube_num) + '.txt'

if not os.path.exists(folder):
	os.makedirs(folder)

f = open(filename, 'w')

pickle.dump(n_list,f)

f.close()

filename = folder + 'w_list_r<' + str(cube_num) + '.txt'

g = open(filename, 'w')

pickle.dump(w_list,g)

g.close()