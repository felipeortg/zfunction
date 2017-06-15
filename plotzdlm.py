import os
import sys
import pylab as pl
import numpy as np
import datetime as dt

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

filename = 'Z_' + str(l) +'_' + str(m)+ '_d(' + str(d) +')'

# For plotting a specific data set use the following format:
# folder = 'Z_values_'+'2017-mm-dd'+'/'

folder = '../'+folder+'Z_values_'+str(dt.datetime.now())[:-16]+'/'

y = np.load(folder+filename+'.npy')

filename = 'x2-'+filename 

x = np.load(folder+filename+'.npy')


y_re = np.real(y)
y_im = np.imag(y)

fig = pl.figure()

pl.plot(x, y_re,label='Real part')
pl.plot(x, y_im, label='Imaginary part')

# tidy up the figure
pl.grid(True)
pl.legend(loc='upper right')
pl.title('Z(l = ' + str(l) + ', m = '+ str(m) +', d = ' + str(d) +')')
pl.xlabel('x^2')

# show the plot on the screen

folder = '../felipe_results/Plots/'

if not os.path.exists(folder):
	os.makedirs(folder)

figname = folder + filename[3:] + '--' + str(dt.datetime.now())[:-16]+'.pdf'

pl.show()

fig.savefig(figname)