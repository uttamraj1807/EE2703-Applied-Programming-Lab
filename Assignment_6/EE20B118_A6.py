"""
   EE2703 Applied Programming Lab - 2022
        Assignment 6 by EE20B118
"""
import scipy.signal as sp
import numpy as np
import matplotlib.pyplot as pl

# Question 1
num1 = np.poly1d([1,0.5])
den1 = np.polymul([1,1,2.5],[1,0,2.25])
X1 = sp.lti(num1,den1)
t1,x1 = sp.impulse(X1,None,np.linspace(0,50,500))
pl.figure(1)
pl.plot(t1, x1)
pl.xlabel(r'$t$')
pl.ylabel(r'$x(t)$')
pl.show()

# Question 2
num2 = np.poly1d([1,0.05])
den2 = np.polymul([1,0.1,2.2525],[1,0,2.25])
X2 = sp.lti(num2,den2)
t2,x2 = sp.impulse(X2,None,np.linspace(0,50,500))
pl.figure(2)
pl.plot(t2, x2)
pl.xlabel(r'$t$')
pl.ylabel(r'$x(t)$')
pl.show()

# Question 3
H1 = sp.lti([1],[1,0,2.25])
for w in np.arange(1.4,1.65,0.05):
	t = np.linspace(0,50,500)
	f = np.cos(w*t)*np.exp(-0.05*t)
	t,x,svec = sp.lsim(H1,f,t)
	pl.figure(3)
	pl.plot(t,x,label='w = ' + str(w))
	pl.title("x(t) for different frequencies")
	pl.xlabel(r'$t\rightarrow$')
	pl.ylabel(r'$x(t)\rightarrow$')
	pl.legend(loc = 'upper left')
	pl.grid(True)

# Question 4
t = np.linspace(0,20,1000)
H_x = sp.lti([1,0,2],[1,0,3,0])
t3,x = sp.impulse(H_x,T=t)
H_y = sp.lti([2],[1,0,3,0])
t4,y = sp.impulse(H_y,T=t)
pl.figure(4)
pl.plot(t3, x)
pl.plot(t4, y)
pl.legend([r'$x(t)$', r'$y(t)$'])
pl.xlabel(r'$t$')
pl.show()

# Question 5
L = 1e-6; R = 100; C = 1e-6
H2 = sp.lti([1], [L*C, R*C, 1])
w,S,phi = H2.bode()
pl.figure(5)
pl.subplot(2, 1, 1)
pl.semilogx(w,S)
pl.xlabel(r'$\omega$')
pl.legend(['Magnitude Response'])
pl.subplot(2, 1, 2)
pl.semilogx(w, phi)
pl.xlabel(r'$\omega$')
pl.legend(['Phase Response'])
pl.show()

# Question 6
time = np.linspace(0, 10e-3, 10001)
vi = np.cos(1e3*time) - np.cos(1e6*time)
time, vo, svec = sp.lsim(H2, vi, time)
pl.figure(6)
pl.plot(time, vo)
pl.xlabel(r'$t$')
pl.savefig('fig10.jpeg')
pl.figure()
pl.plot(time[:30], vo[:30])
pl.title(r'Plot for t < 30$\mu$s')
pl.show()

