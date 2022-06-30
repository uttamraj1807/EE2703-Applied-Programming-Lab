"""
   EE2703 Applied Programming Lab - 2022
        Assignment 5 by EE20B118
"""
from sys import *
from matplotlib.pyplot import *
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np

#get user inputs
if(len(argv) == 5):
    Nx = int(argv[1])
    Ny = int(argv[2])
    radius = int(argv[3])  
    Niter = int(argv[4])

else:
    Nx = 25 # size along x
    Ny = 25 # size along y
    radius = 8 #radius of central lead
    Niter = 1500 #number of iterations to perform

phi = np.zeros((Ny,Nx))
x = np.linspace(-0.5,0.5,Nx)
y = np.linspace(-0.5,0.5,Ny)
Y,X = np.meshgrid(y,x)

ii = np.where(X**2+Y**2<(0.35)**2)
# Setting the value of Phi as 1.0 at those coordinates.
phi[ii] = 1.0

#plot potential
figure(1)
contourf(X,Y,phi)
plot(ii[0]/Nx-0.48,ii[1]/Ny-0.48,'ro',label="V = 1")
xlabel(r'$X\rightarrow$')
ylabel(r'$Y\rightarrow$')
title("Contour plot of potential")
colorbar()
grid(True)
legend()
show()

#Function to update phi using a finite differentation approximation

def phi_update(phi,oldphi):
    phi[1:-1,1:-1] = 0.25*(oldphi[1:-1,0:-2]+oldphi[1:-1,2:]+oldphi[0:-2,1:-1]+oldphi[2:,1:-1]) 
    return phi

#Function to enforce appropriate boundary conditions

def boundary_conditions(phi,inds):
    phi[1:-1,0] = phi[1:-1,1]
    phi[0,1:-1] = phi[1,1:-1]
    phi[1:-1,-1] = phi[1:-1,-2]
    phi[-1,1:-1] = 0
    phi[inds] = 1.0
    return phi
error = np.zeros(Niter)
#Function to obtain an exponential
def fit_exp(x,A,B):
    return A*np.exp(B*x)
    
#Evaluates the parameters of an exponent. x is the data vector, y is the vector of true values
def get_fit(x,y):
    logy=np.log(y)
    xvec=np.zeros((len(x),2))
    xvec[:,0]=x
    xvec[:,1]=1
    B,logA=np.linalg.lstsq(xvec, np.transpose(logy),rcond = -1)[0]
    return (np.exp(logA),B)

# Evaluating the potential 
for i in range(Niter):
    oldphi = phi.copy()
    phi = phi_update(phi,oldphi)
    phi = boundary_conditions(phi,ii)
    error[i] = (abs(phi-oldphi)).max()

# Fitting an exponential to the error data
A,B = get_fit(range(Niter),error) # fit1
A_500,B_500 = get_fit(range(Niter)[500:],error[500:]) # fit2

# Evolution of the error function 
figure(2)
plot(range(Niter),error,'-r',markersize=3,label='original')
xlabel(r'Niter$\rightarrow$')
ylabel(r'Error$\rightarrow$')
title('Plot of Error vs number of iterations')
show()

# Plotting of error vs iteration in semilog.
figure(3)
semilogy(range(Niter),error,'-r',markersize=3,label='original')
title("Plotting of error vs iteration in semilog")
xlabel(r'$Iteration\rightarrow$',size=15)
ylabel(r'$Error\rightarrow$',size=15)
grid(True)
show()

# Plotting of error vs iteration in loglog.
figure(4)
loglog(range(Niter),error,'-r',label='original')
title("Plotting of error vs iteration in loglog")
xlabel(r'$Iteration\rightarrow$',size=15)
ylabel(r'$Error\rightarrow$',size=15)
grid(True)
show()

# Error, fit1 and fit2 in a semilog plot 
figure(5)
semilogy(range(Niter),error,'-r',label='original')
semilogy(range(Niter)[::50],fit_exp(range(Niter)[::50],A,B),'go',label='fit1')
semilogy(range(Niter)[::50],fit_exp(range(Niter)[::50],A_500,B_500),'bo',label='fit2')
legend(loc='upper right')
xlabel(r'Niter$\rightarrow$')
ylabel(r'Error$\rightarrow$')
title('Semilog plot of original, fit1, fit2')
show()

#Finds an upper bound for the error
def max_error(A,B,N):
    return -A*(np.exp(B*(N+0.5)))/B

# Upper bound on the error
figure(6)
semilogy(range(Niter)[::50],max_error(A,B,np.arange(0,Niter,50)),'ro',markersize=3)
xlabel(r'Niter$\rightarrow$')
ylabel(r'Error$\rightarrow$')
title('Semilog plot of Cumulative Error vs number of iterations')
show()

# 3-D plot of potential
fig1 = figure(7)
ax = p3.Axes3D(fig1) 
title('The 3-D surface plot of the potential')
surf = ax.plot_surface(Y, X, phi.T, rstride=1, cstride=1,cmap=cm.jet)
xlabel(r'x$\rightarrow$',fontsize=15)
ylabel(r'y$\rightarrow$',fontsize=15)
ax.set_zlabel(r'$\phi\rightarrow$',fontsize=15)
show()

# Contour plot of the potential
figure(8)
contourf(Y,X[::-1],phi)
plot(ii[0]/Nx-0.48,ii[1]/Ny-0.48,'ro',label="V = 1")
title("2D Contour plot of potential")
xlabel(r"x$\rightarrow$")
ylabel(r'y$\rightarrow$')
colorbar()
show()

#finding Current density
Jx,Jy = (1/2*(phi[1:-1,0:-2]-phi[1:-1,2:]),1/2*(phi[:-2,1:-1]-phi[2:,1:-1]))
#plotting current density
figure(9)
title("Vector plot of current flow")
quiver(Y[1:-1,1:-1],-X[1:-1,1:-1],-Jx[:,::-1],-Jy)
x_c,y_c=np.where(X**2+Y**2<(0.35)**2)
plot((x_c-Nx/2)/Nx,(y_c-Ny/2)/Ny,'ro')
xlabel(r"x$\rightarrow$")
ylabel(r'y$\rightarrow$')
show()
