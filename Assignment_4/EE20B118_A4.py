"""
   EE2703 Applied Programming Lab - 2022
        Assignment 4 by EE20B118
"""
from matplotlib.pyplot import *
import numpy as np
from scipy import integrate
# Declaring all the required functions necessary for the program.
def exponential(x):
        return np.exp(x)

def coscos(x):
        return np.cos(np.cos(x))

def u_exponential(x,k):
	return exponential(x)*np.cos(k*x)

def u_coscos(x,k):
	return coscos(x)*np.cos(k*x)

def v_exponential(x,k):
	return exponential(x)*np.sin(k*x)

def v_coscos(x,k):
	return coscos(x)*np.sin(k*x)
# Creating a range of x values from -2π to 4π.
x = np.linspace(-2*np.pi,4*np.pi,300)
# Creating a range from 0 to 2π with periodicity 2π.
x1 = np.linspace(0,2*np.pi,100)
x_per = np.tile(x1,3)

exp_x = exponential(x)
coscos_x = coscos(x)

figure(1)
semilogy(x,exp_x,'r',label='True value')
semilogy(x,exponential(x_per),'b',label='Periodic extension')
xlabel(r'x$\rightarrow$',fontsize=15)
ylabel(r'$e^{x}\rightarrow$',fontsize=15)
title('Semilog plot of $e^{x}$',fontsize=15)
grid()
legend()
show()

figure(2)
plot(x,coscos_x,'r',label='True value')
plot(x,coscos(x_per),'b',label='Periodic extension')
xlabel(r'x$\rightarrow$',fontsize=15)
ylabel(r'$cos(cos(x))\rightarrow$',fontsize=15)
title('Plot of $cos(cos(x))$',fontsize=15)
grid()
legend(loc = 'upper right')
show()

# Initializing all the required variables.
c_exp = np.empty((51,1))
c_coscos = np.empty((51,1))
sum_exp = 0
sum_coscos = 0
p=0

for k in range(26):

# The function integrate.quad() is used to find the value of the Fourier coefficients.
	a_exp = integrate.quad(u_exponential,0,2*np.pi,args=(k))[0]/np.pi
	b_exp = integrate.quad(v_exponential,0,2*np.pi,args=(k))[0]/np.pi
	a_coscos = integrate.quad(u_coscos,0,2*np.pi,args=(k))[0]/np.pi
	b_coscos = integrate.quad(v_coscos,0,2*np.pi,args=(k))[0]/np.pi

# The corresponding Fourier series and coefficients are calculated and stored.
	if k==0:
		sum_exp += a_exp/2
		sum_coscos += a_coscos/2
		c_exp[p][0]  = a_exp/2
		c_coscos[p][0] = a_coscos/2
		p = p + 1

	else:
		sum_exp += a_exp*np.cos(k*x) + b_exp*np.sin(k*x)
		sum_coscos += a_coscos*np.cos(k*x) + b_coscos*np.sin(k*x)
		c_exp[p][0] = a_exp
		c_coscos[p][0] = a_coscos
		c_exp[p+1][0] = b_exp
		c_coscos[p+1][0] = b_coscos
		p = p + 2

figure(3)
semilogy(abs(c_exp),'or')
title(r"Semilog plot for coefficients of $e^{x}$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
show()

figure(4)
loglog(abs(c_exp),'or')
title(r"loglog plot for coefficients of $e^{x}$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
show()

figure(5)
semilogy(abs(c_coscos),'or')
title(r"Semilog plot for coefficients of $cos(cos(x))$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
show()

figure(6)
loglog(abs(c_coscos),'or')
title(r"loglog plot for coefficients of $cos(cos(x))$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
show()

# The below set of codes will find the values of the Fourier coefficients using the lstsq() function.
xl=np.linspace(0,2*np.pi,401)
xl=xl[:-1] # drop last term to have a proper periodic integral

B_exp = exponential(xl)
B_coscos = coscos(xl)

A = np.zeros((400,51))
A[:,0] = 1
for k in range(1,26):
	A[:,2*k-1] = np.cos(k*xl)
	A[:,2*k] = np.sin(k*xl)

cl_exp = np.linalg.lstsq(A,B_exp,rcond = -1)[0]
cl_coscos = np.linalg.lstsq(A,B_coscos,rcond = -1)[0]
# The difference and deviation between the actual and predicted values are calculated.
c_expt = c_exp.T
c_coscost = c_coscos.T
diff_exp = np.abs(cl_exp - c_expt)
diff_coscos = np.abs(cl_coscos - c_coscost)
# print(diff_exp)
dev_exp = np.max(diff_exp)
dev_coscos = np.max(diff_coscos)
# print(c_exp)
print(cl_exp)
# print(c_coscos)
print(cl_coscos)

figure(7)
semilogy(np.abs(cl_exp),'og',label='lsq approach')
semilogy(np.abs(c_exp),'or',label='True')
title(r"Semilog plot for coefficients of $e^{x}$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
legend()
show()

figure(8)
loglog(np.abs(cl_exp),'og',label='lsq approach')
loglog(np.abs(c_exp),'or',label='True')
title(r"loglog plot for coefficients of $e^{x}$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
legend()
show()

figure(9)
semilogy(np.abs(cl_coscos),'og',label = 'lsq approach')
semilogy(np.abs(c_coscos),'or',label = 'True')
title(r"Semilog plot for coefficients of $cos(cos(x))$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
legend()
show()

figure(10)
loglog(np.abs(cl_coscos),'og',label='lsq approach')
loglog(np.abs(c_coscos),'or',label='True')
title(r"loglog plot for coefficients of $cos(cos(x))$")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid()
legend()
show()

print("The deviation between coefficients for exp() is ",dev_exp)
print("The deviation between coefficients for coscos() is ",dev_coscos)

approx_exp = np.matmul(A,c_exp)
approx_coscos = np.matmul(A,c_coscos)

figure(11)
semilogy(xl,approx_exp,'go',label="Function Approximation")
semilogy(xl,exponential(xl),'-r',label='True value')
grid()
xlabel(r'n$\rightarrow$',fontsize=15)
ylabel(r'$f(x)\rightarrow$',fontsize=15)
title('Plot of $e^{x}$ and its Fourier series approximation',fontsize=15)
legend(loc='upper left')
show()

figure(12)
plot(xl,approx_coscos,'go',label="Function Approximation")
plot(xl,coscos(xl),'-r',label='True value')
grid()
xlabel(r'n$\rightarrow$',fontsize=15)
ylabel(r'$f(x)\rightarrow$',fontsize=15)
title('Plot of $cos(cos(x))$ and its Fourier series approximation',fontsize=15)
legend(loc='upper right')
show()

