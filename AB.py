# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as numpy


def AB(x1, y1, x2, y2, h):
    return y2 + (h*(3 * fxy(x2, y2) - 1*fxy(x1, y1))/2)  # adams bashforth

def euler(x0, y0, h):
    return y0 + h * fxy(x0, y0)   # metodo de euler

def rungeKutta(x, y, h):
    m0 = h * fxy(x, y)
    m1 = h * fxy(x + h, y + m0)
    return y + (m0 + m1) / 2

def rungeKutta4o(x, y, h):
    m0 = h * fxy(x, y)
    m1 = h * fxy(x + h/2, y + m0/2)
    m2 = h * fxy(x + h/2, y + m1/2)
    m3 = h * fxy(x + h, y + m2)
    return y + ((m0 + 2*m1 + 2*m2 + m3) / 6)

def PVI(y0, dominio, h):
    y = numpy.zeros(len(dominio))
    y[0] = y0
#     y[1] = euler(dominio[0], y0, h);
    y[1] = rungeKutta(dominio[0], y0, h)
    for i, xi in enumerate(dominio[1:-1], start=1):
        y[i + 1] = AB(dominio[i - 1], y[i - 1], xi, y[i], h) 
    return y

def fxy(x, y):
    return (1/(1+x*x))-(2*y*y)

def know(x):
    return x/(1+pow(x, 2))

def PVIRK(y0, dominio, h):
    y = numpy.zeros(len(dominio))
    for i, xi in enumerate(dominio[0:-1], start = 0):
        y[i+1] = rungeKutta4o(xi, y[i], h)
    return y;

passo = 0.1
x = numpy.arange(0, 5.1, passo)
y = PVI(0., x, passo)
plt.plot(x, y, '-o', label='Passo ' + str(passo))


passo = 0.3
x = numpy.arange(0, 5.1, passo)
y = PVI(0., x, passo)
plt.plot(x, y, '-o', label='Passo ' + str(passo))

plt.xlabel('$x$'), plt.ylabel('$y$')
plt.legend(loc=1)

plt.savefig("temp1.png")
