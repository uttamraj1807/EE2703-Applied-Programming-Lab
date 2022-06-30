"""
   EE2703 Applied Programming Lab - 2022
        Assignment 3 by EE20B118
"""
from numpy import *
from matplotlib.pyplot import *
import scipy.special as sp

Input = loadtxt("fitting.dat")
Samples = len(Input[0])
Time = Input[:,0]
Noises = []
for j in range(1,Samples):
    Noises.append(Input[:,j])

Noise_1 = Noises[0] #Storing first dataset because its often used
sigma = logspace(-1,-3,9) #9 values

def g(t,A,B):                  # Defining the actual function.
    return A*sp.jn(2,t)+B*t

figure(0)

for i in range(9):
    plot(Time,Noises[i],label=r'$\sigma_{noise}$=%.3f'%sigma[i])

xlabel(r'$Time$',size=20)                        #labeling x-axis
ylabel(r'$f(t)+n(t)$',size=20)                   #labeling y-axis
title("A Plot of various Noise Levels")          #Title of the plot
grid()                                           #grid behind the graph
legend()                                         #Place legend on the axes
show()                                           #Show the plot

figure(1)

plot(Time,g(Time,1.05,-0.105),label='f(t)')
errorbar(Time[::5],Noise_1[::5],sigma[0],fmt='ro',label='Errorbar')   #plotting every 5th element of 1st data column
xlabel(r'$t$')
ylabel(r'f(t)')
title("Data points for $\sigma$ = 0.10 with error bars")
grid()
legend()
show()
# Calculation of M matrix
def error_matrix(X,Y,A,B):
    M = c_[X,Y]
    p = [[A],[B]]
    return dot(M,p)

y = error_matrix(Noise_1,Time,1.05,-0.105)
z = g(Time,1.05,-0.105)
if array_equal(y,z):
    print("Both vectors are equal.")
else:
    print("Both vectors are not equal.")

figure(2)

A = linspace(0,2,21)
B = linspace(-0.2,0,21)
Epsilon = zeros((len(A), len(B)))
#calculation of the mean squared error for different values of A and B.
for i in range(len(A)):
    for j in range(len(B)):
            Epsilon[i][j] = mean(square(g(Time,1.05,-0.105) - g(Time, A[i], B[j])))
# This will plot the contour of mean squared error for different values of A and B.
Contour_plot = contour(A, B, Epsilon, levels=20)
clabel(Contour_plot,Contour_plot.levels[:5],inline = 1,fontsize = 10)
plot([1.05], [-0.105], 'ro')
xlabel("A")
ylabel("B")
title("Contour plots")
grid()
show()

def estimateAB(M, b ):
    return linalg.lstsq(M,b,rcond=None)

M = c_[sp.jn(2,Time),Time]
b = Input[:,1:10]
# This will plot the variation of error in the estimate of A and B with respect to noise.
figure(3)

A,B = estimateAB(M,b)[0]
A_error = abs(A - 1.05)
B_error = abs(B + 0.105)
plot(sigma,A_error,'o--', label='$A_{error}$')
plot(sigma,B_error,'o--', label='$B_{error}$')
title("Variation of Error with Noise",size=20)	
xlabel('Noise standard deviation',size=20)
ylabel('MS error',size=20)
grid()
legend()
show()
# This will plot the variation of error in the estimate of A and B with respect to noise in loglog scale
figure(4)

loglog(sigma, A_error, 'ro', label="$A_{error}$")
loglog(sigma, B_error, 'bo', label="$B_{error}$")
errorbar(sigma, A_error, std(A_error), fmt='ro')
errorbar(sigma, B_error, std(B_error), fmt='bo')
title("Variation of Error with Noise(loglog scale)",size=20)	
xlabel('Noise standard deviation',size=20)
ylabel('MS error',size=20)
grid()
legend()
show()










