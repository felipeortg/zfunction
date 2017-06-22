import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

# -----------------
# Matplotlib param
plt.rc('text', usetex=True)
plt.rc('font', size=12)
#plt.rc('font', family='serif')
plt.rc('axes.formatter', useoffset = False)

# -----------------
# Config file:
config_file = str(sys.argv[1])

with open(config_file, 'r') as f:
	for line in f:
		if line[0:6] == 'folder':
			folder = line[7:-1]
		if line[0] == 'l':
			l = int(line[2:])
		if line[0] == 'm':
			m = int(line[2:])
		if line[0:2] == 'dx':
			dx = int(line[2:])
		if line[0:2] == 'dy':
			dy = int(line[2:])
		if line[0:2] == 'dz':
			dz = int(line[2:])


d = [dx,dy,dz]

save_folder = '../'+folder+'Plots/'

filename = 'Z_' + str(l) +'_' + str(m)+ '_d(' + str(d) +')'

# For plotting a specific data set use the following format:
# folder = 'Z_values_'+'2017-mm-dd'+'/'

folder = '../'+folder+'Z_values_'+str(dt.datetime.now())[:-16]+'/'

y = np.load(folder+filename+'.npy')

filename = 'x2-'+filename 

x = np.load(folder+filename+'.npy')


y_re = np.real(y)
y_im = np.imag(y)

fig = plt.figure()

plt.plot(x, y_re,label='Real part')
plt.plot(x, y_im, label='Imaginary part')

# tidy up the figure
plt.grid(True)
plt.legend(loc='upper right')
plt.title(r'$Z_{' + str(l) + str(m) +'}^{' + str(d) +'}[1;x^2]$')
plt.xlabel(r'$x^2$')

# show the plot on the screen

if not os.path.exists(save_folder):
	os.makedirs(save_folder)

figname = save_folder + filename[3:] + '--' + str(dt.datetime.now())[:-16]+'.pdf'

plt.show()

fig.savefig(figname)