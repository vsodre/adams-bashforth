# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as numpy
from math import exp

def AB(x1, y1, x2, y2, h):
    return y2 + (1.5 * h * fxy(x2, y2) - 0.5 * h * fxy(x1, y1))  # adams bashforth

def euler(x0, y0, h):
    return y0 + h * fxy(x0, y0)   # metodo de euler

def rungeKutta(x, y, h):
    m0 = h * fxy(x, y)
    m1 = h * fxy(x + h, y + m0)
    return y + (m0 + m1) / 2

def PVI(y0, dominio, h):
    y = numpy.zeros(len(dominio))
    y[0] = y0
#     y[1] = euler(dominio[0], y0, h);
    y[1] = rungeKutta(dominio[0], y0, h)
    for i, xi in enumerate(dominio[1:-1], start=1):
        y[i + 1] = AB(dominio[i - 1], y[i - 1], xi, y[i], h) 
    return y

def fxy(x, y):
    return y

def know(x):
    return exp(x)

x = numpy.arange(0, 2.2, 0.2)
y = PVI(1., x, 0.2)
plt.plot(x, y, '-o', label='Passo 0.2')

x = numpy.arange(0, 2.4, 0.4)
y = PVI(1, x, 0.4)
plt.plot(x, y, '-o', label='Passo 0.4')

x = numpy.arange(0, 2.5, 0.5)
y = PVI(1, x, 0.5)
plt.plot(x, y, '-o', label='Passo 0.5')

x = numpy.arange(0, 2.1, 0.1)
plt.plot(x, [know(i) for i in x], 'k--', label='Known')

plt.xlabel('$x$'), plt.ylabel('$y$')
plt.legend(loc=2)

plt.savefig("temp1.png")
