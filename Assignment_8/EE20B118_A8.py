"""
   EE2703 Applied Programming Lab - 2022
        Assignment 8 by EE20B118
"""
import matplotlib.pyplot as plt
import numpy as np

#------------------------------------Defining the functions-----------------------------------------------------------------

def magphaplot(x,y,Y,Magtitle):
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(abs(Y),lw=2)
    plt.ylabel(r"$|Y|$",size=16)
    plt.title(Magtitle)
    plt.grid(True)
    plt.subplot(2,1,2)
    plt.plot(np.unwrap(np.angle(Y)),lw=2)
    plt.ylabel(r"Phase of $Y$",size=16)
    plt.xlabel(r"$k$",size=16)
    plt.grid(True)
    plt.show()

def magphaplot1(Y,w,Magtitle,xlim,phas = True):
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(w,abs(Y),lw=2)
    plt.xlim(xlim)
    plt.ylabel(r"$|Y|$",size=16)
    plt.title(Magtitle)
    plt.grid(True)
    plt.subplot(2,1,2)
    if(phas):
        plt.plot(w,np.angle(Y),'ro',lw=2)
    ii = np.where(abs(Y)>1e-3)
    plt.plot(w[ii],np.angle(Y[ii]),'go',lw=2)
    plt.xlim(xlim)
    plt.ylim([-4,4])
    plt.ylabel(r"Phase of $Y$",size=16)
    plt.xlabel(r"$k$",size=16)
    plt.grid(True)
    plt.show()
    #plt.savefig("fig9-2.png")

#------------------------------------Main Program Code----------------------------------------------------------------------

#------------------------------------example1:sin(5x)----------------------------------------------------------------------
x1=np.linspace(0,2*np.pi,128)
y1=np.sin(5*x1)
Y1=np.fft.fft(y1)

magphaplot(x1,y1,Y1,r"Spectrum of $\sin(5t)$")

#------------------------------------example2:sin(5x)----------------------------------------------------------------------

x2=np.linspace(0,2*np.pi,129);x2=x2[:-1]
y2=np.sin(5*x2)
Y2=np.fft.fftshift(np.fft.fft(y2))/128.0
w2=np.linspace(-64,63,128)
xlim2 = [-10,10]

magphaplot1(Y2,w2,r"Spectrum of $\sin(5t)$",xlim2)

#------------------------------------example3:(1+0.1cost)*cos(10t)----------------------------------------------------------------------

t=np.linspace(0,2*np.pi,129);t=t[:-1]
y3=(1+0.1*np.cos(t))*np.cos(10*t)
Y3=np.fft.fftshift(np.fft.fft(y3))/128.0
w3=np.linspace(-64,63,128)

xlim3 = [-15,15]
magphaplot1(Y3,w3,r"Spectrum of $\left(1+0.1\cos\left(t\right)\right)\cos\left(10t\right)$",xlim3)

#------------------------------------example4:(1+0.1cost)*cos(10t)----------------------------------------------------------------------

t1=np.linspace(-4*np.pi,4*np.pi,513);t1=t1[:-1]

y4=(1+0.1*np.cos(t1))*np.cos(10*t1)
Y4=np.fft.fftshift(np.fft.fft(y4))/512.0

w4=np.linspace(-64,64,513);w4=w4[:-1]

magphaplot1(Y4,w4,r"Corrected Spectrum of $\left(1+0.1\cos\left(t\right)\right)\cos\left(10t\right)$",xlim3)

#------------------------------------Question2:(cost)^3----------------------------------------------------------------------


y5=(np.cos(t1))**3
Y5=np.fft.fftshift(np.fft.fft(y5))/512.0
w5=np.linspace(-64,64,513);w5=w5[:-1]

magphaplot1(Y5,w4,r"Spectrum of $cos^3\left(t\right)$",xlim3,False)

#------------------------------------Question2:(sint)^3----------------------------------------------------------------------


y6=(np.sin(t1))**3
Y6=np.fft.fftshift(np.fft.fft(y6))/512.0

magphaplot1(Y6,w4,r"Spectrum of $sin^3\left(t\right)$",xlim3,False)

#------------------------------------Question3:cos(20t)+5cost----------------------------------------------------------------------

y7=np.cos((20*t1)+(5*np.cos(t1)))
Y7=np.fft.fftshift(np.fft.fft(y7))/512.0

xlim4 = [-35,35]

magphaplot1(Y7,w4,r"Spectrum of $cos(20t + 5cos(10t))$",xlim4,False)

#------------------------------------Question4:e^(t^2)/2)----------------------------------------------------------------------

# To plot FFT of gaussian signal
T = 8*np.pi  #Time period
N = 128   # Samples
Yold=0
tolerance=1e-6   #Accuracy
err=tolerance+1
iters = 0
#iterative loop to find window size
while err>tolerance:
    x = np.linspace(-T/2,T/2,N+1)[:-1]
    w = np.linspace(-N*np.pi/T,N*np.pi/T,N+1)[:-1]
    y = np.exp(-0.5*x**2)
    Y = np.fft.ifftshift(np.fft.fft(np.fft.fftshift(y)))*T/(2*np.pi*N)
    err = sum(abs(Y[::2]-Yold))
    Yold = Y
    print(err)
    iters+=1
    T*=2
    N*=2

#The DTF of gaussian
Y_exp = 1/np.sqrt(2*np.pi)*np.exp(-w*2/2)

#calculating error
true_error = sum(abs(Y-Y_exp))
print("True error: ",true_error)
print("samples = "+str(N)+" time period = "+str(T/np.pi)+"*pi")

#Expected output
xlim6 = [-15,15]
magphaplot1(Y_exp,w,r"Expected Spectrum of $e^{\frac{t^{2}}{2}}$",xlim6)


#Estimated output
magphaplot1(Y,w,r"Estimated Spectrum of $e^{\frac{t^{2}}{2}}$",xlim6)