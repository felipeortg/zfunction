# -----------------
# Import packages
import pickle
import os
import sys
import numpy as np
import datetime as dt
from scipy import special
from scipy import integrate

# -----------------
# Config file:
config_file = str(sys.argv[1])

quick_ev = False
with open(config_file, 'r') as f:
	for line in f:
		if line[0:6] == 'folder':
			folder = line[7:-1]
		if line[0:9] == 'cube num ':
			cube_num = int(line[9:])
		if line[0] == 'L':
			L_lattice_size = float(line[2:]) # fermis
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
		if line[0:5] == 'x2max':
			x2max = float(line[6:])
		if line[0:5] == 'x2min':
			x2min = float(line[6:])
		if line[0:3] == 'x2q':
			x2q = float(line[3:])
			quick_ev = True
		if line[0:6] == 'points':
			points = int(line[7:])


d = [dx,dy,dz]

print 'Lattice size: ' +str(L_lattice_size) + ' fm' 
print 'Z function with (l,m) = (' + str(l) + ','+ str(m) +')\n d = ' + str(d) 
print 'Shells (nmax) = ' +str(cube_num)
# -----------------
# Location to get triplets from:
trip_folder = 'felipe_results/'

# -----------------
# Define constants
I = complex(0.0,1.0)
hbar = 197.3269718 # MeV fm when speed of ligth is 1


# -----------------
# Define variables of the Z function
# d= [1.0,1.0,0]
# L_lattice_size = 10.0 # fermis
L = L_lattice_size/hbar # MeV^-1
lab_moment = (2*np.pi/L)*np.array(d)
lab_moment2 = np.dot(lab_moment,lab_moment)
m1 = 146.0 # MeV
m2 = 146.0 # MeV


# -----------------
# Define integrands functions for second and third term calculation
def integr_second_term(t,x2):
	return 2.0*np.exp((t**2)*x2)
	#return np.exp(t*x2)/np.sqrt(t)

def integr_third_term_r(t,l,gw2,x2,coef):
	integr = np.power(np.pi/t,3.0/2.0+l)*np.exp(t*x2-np.square(np.pi)*gw2/t)
	return np.real(sum(coef*integr))

def integr_third_term_i(t,l,gw2,x2,coef):
	integr = np.power(np.pi/t,3.0/2.0+l)*np.exp(t*x2-np.square(np.pi)*gw2/t)
	return np.imag(sum(coef*integr))

# -----------------
# Calculate triplets used in the sums of the first and third term

# ---- First term triplets -----
# Get the array of n triplets
filename = '../' + trip_folder + 'triplets/n_list_r<' + str(cube_num) + '.txt'
f = open(filename, 'r')
n_list = pickle.load(f)
n_arr = np.array(n_list)

# Create an array of d vector copies, and calculate its magnitude
d_arr = np.repeat([np.array(d)],len(n_arr),axis=0)
d2 = float(d[0]**2+d[1]**2+d[2]**2)

# Dot product of vector d with n triplets
if d2 == 0:
	d_n_dot = np.inner(d,n_arr)
else:
	d_n_dot = np.inner(d,n_arr)/d2

# Create array of the parallel component of the n triplets [(d dot n) / (d2) * d]
n_par_arr = np.transpose(np.append([d_n_dot],[d_n_dot,d_n_dot],axis=0)) * d_arr

# Create array of the perpendicular component
n_perp_arr = n_arr - n_par_arr

# ---- Third term triplets -----
# Get the array of w triplets
filename = '../' + trip_folder + 'triplets/w_list_r<' + str(cube_num) + '.txt'
f = open(filename, 'r')
w_list = pickle.load(f)
w_arr = np.array(w_list)

# Take out one element, summation not in w=0
d_arr_for_w = np.delete(d_arr, 0,0)

# Dot product / d2, of vector d with w triplets
if d2 == 0:
	d_w_dot = np.inner(d,w_arr)
else:
	d_w_dot = np.inner(d,w_arr)/d2

# Create array of the paralel component of the w triplets [(d dot w) / (d2) * d]
w_par_arr = np.transpose(np.append([d_w_dot],[d_w_dot,d_w_dot],axis=0)) * d_arr_for_w

# Create array of the perpendicular component
w_perp_arr = w_arr - w_par_arr

# Define r^l times spherical harmonic (Laplace spherical solution)

def lap_sol(m,l,x,y,z,r2):
	# Receive azimutal m and polar l numbers
	# x,y,z components of the vector
	# r^2 squared magnitude of the vector
	if m>l:
		raise NameError('Azimutal number m bigger than l')
	lm = 'l' +str(int(l))+'m' +str(int(m))
	#print lm

	r2_sph = r2 + (r2==0) # Last part to avoid division by zero

	sph_dict = {
		'l0m0': 0.5*np.sqrt(1./np.pi),

		'l1m-1': 0.5*np.sqrt(3./(2*np.pi))*(x-I*y)/np.sqrt(r2_sph),

		'l1m0': 0.5*np.sqrt(3./np.pi)*z/np.sqrt(r2_sph),

		'l1m1': -0.5*np.sqrt(3./(2*np.pi))*(x+I*y)/np.sqrt(r2_sph),

		'l2m-2': 0.25*np.sqrt(15./(2*np.pi))*(x-I*y)**2/(r2_sph),

		'l2m-1': 0.5*np.sqrt(15./(2*np.pi))*z*(x-I*y)/(r2_sph),

		'l2m0': 0.25*np.sqrt(5./(np.pi))*(3*z**2/(r2_sph)-1),

		'l2m1': -0.5*np.sqrt(15./(2*np.pi))*z*(x+I*y)/(r2_sph),

		'l2m2': 0.25*np.sqrt(15./(2*np.pi))*(x+I*y)**2/(r2_sph),
	}

	val = np.power(r2,l/2.0)*sph_dict[lm]
	
	return val

# -----------------
# Calculate the zeta function

def zdlm(l,m,x2):
	if l < m:
		print 'Error:\nabs(m) must be equal or less than l'
		return None
	else:

		# Kinematics
		q2 = ((2*np.pi/L)**2)*x2
		cm_energy = np.sqrt(q2 + m1**2) + np.sqrt(q2 + m2**2)
		lab_energy = np.sqrt(cm_energy**2+lab_moment2)
		alpha = 1.0/2.0*(1.0+(np.square(m1)-np.square(m2))/np.square(cm_energy))
		gamma = lab_energy/cm_energy

		# -----------------
		# Finish triplets calculation (gamma dependent part)
		# rn triplets
		# Calculate array of r vectors
		r_arr = (1.0/gamma)*(n_par_arr-alpha*d_arr)+n_perp_arr

		# Spherical and cartesian components of r
		rx = r_arr[:,0]
		ry = r_arr[:,1]
		rz = r_arr[:,2]
		r2_array = np.sum(r_arr*r_arr, axis = 1)
		# r_azimuthal = np.arctan2(ry,rx)
		# r_polar = np.arctan2(np.sqrt(rx**2 + ry**2),rz)		

		# gw triplets
		# Calculate array of gw vectors
		gw_arr = gamma*w_par_arr+w_perp_arr

		# Calculate array with square of the magnitude of gw, the azimuthal and polar angle
		gwx = gw_arr[:,0]
		gwy = gw_arr[:,1]
		gwz = gw_arr[:,2]
		gw2_array = np.sum(gw_arr*gw_arr, axis = 1)
		# gw_azimuthal = np.arctan2(gwy,gwx)
		# gw_polar = np.arctan2(np.sqrt(gwy**2 + gwx**2),gwz)

		# Calculate the first term of the Z function
		#first_term = sum(np.exp(-r2_array+x2)*(1.0/(r2_array-x2))*(r2_array**(l/2.0))*special.sph_harm(m,l,r_azimuthal,r_polar))
		first_term = sum(np.exp(-r2_array+x2)*(1.0/(r2_array-x2))*lap_sol(m,l,rx,ry,rz,r2_array))
		
		# print first_term

		# Calculate the second term
		if l == 0:
			second_term = special.sph_harm(0,0,0.0,0.0)*gamma*np.power(np.pi,3.0/2.0)
			second_term_bracket = 2 * x2 * integrate.quad(integr_second_term,0,1, args = (x2))[0] - 2 * np.exp(x2)
			second_term *= second_term_bracket
		else:
			second_term = 0

		# print second_term

		# Calculate the third term
		wd = np.inner(w_arr,d)
		t1 = np.exp(I*2*np.pi*alpha*wd)
		t2 = lap_sol(m,l,gwx,gwy,gwz,gw2_array)
		coef_third_term = t1*t2
		# t2 = np.power(gw2_array,l/2.0)
		# t3 = special.sph_harm(m,l,gw_azimuthal,gw_polar)
		# coef_third_term = t1*t2*t3

		third_term_r = integrate.quad(integr_third_term_r,0,1, args = (l,gw2_array,x2,coef_third_term))[0]

		third_term_i = integrate.quad(integr_third_term_i,0,1, args = (l,gw2_array,x2,coef_third_term))[0]

		third_term = gamma*np.power(I,l)* (third_term_r + I*third_term_i)

		# print third_term

		total = first_term + second_term + third_term

		return total

if quick_ev == True:
	print 'At ' +str(x2q)
	# ---------
	# One point evaluation	
	print zdlm(l,m,x2q)
else:
	if x2min < -(m1*L/(2*np.pi))**2:
		x2min = -(m1*L/(2*np.pi))**2 + .01

	print 'From '+str(x2min)+ ' to ' +str(x2max)+ ' ' +str(points)+' points'
	# ---------
	# Several point calculation		

	x = np.zeros(points)
	y = np.zeros(points) + I*np.zeros(points)

	# for l in xrange(0,1):
	# 	for m in xrange(-l,l+1):

	for ii in xrange(0,points):
		x[ii] = ii/(points-1.0)*(x2max-x2min) + x2min
		y[ii] = zdlm(l,m,x[ii])
		if ii % 10 == 0:
			print ii

	filename = 'Z_' + str(l) +'_' + str(m)+ '_d(' + str(d) +')'

	folder = '../'+folder+'Z_values_' + str(dt.datetime.now())[:-16] +'/'

	if not os.path.exists(folder):
		os.makedirs(folder)

	np.save(folder+filename,y)

	filename = 'x2-'+filename 

	np.save(folder+filename,x)
