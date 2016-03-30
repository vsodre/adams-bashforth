# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os
import random
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import numpy as numpy

def AB(x1, y1, x2, y2, h):
    return y2 + (h * (3 * fxy(x2, y2) - 1 * fxy(x1, y1)) / 2)  # adams bashforth

def euler(x0, y0, h):
    return y0 + h * fxy(x0, y0)  # metodo de euler

def rungeKutta(x, y, h):
    m0 = h * fxy(x, y)
    m1 = h * fxy(x + h, y + m0)
    return y + (m0 + m1) / 2

def rungeKutta4o(x, y, h):
    m0 = h * fxy(x, y)
    m1 = h * fxy(x + h / 2, y + m0 / 2)
    m2 = h * fxy(x + h / 2, y + m1 / 2)
    m3 = h * fxy(x + h, y + m2)
    return y + ((m0 + 2 * m1 + 2 * m2 + m3) / 6)

def PVI(y0, dominio, h):
    y = numpy.zeros(len(dominio))
    y[0] = y0
    y[1] = rungeKutta4o(dominio[0], y0, h)
    for i, xi in enumerate(dominio[1:-1], start=1):
        y[i + 1] = AB(dominio[i - 1], y[i - 1], xi, y[i], h) 
    return y

def fxy(x, y):
    return (1 / (1 + x * x)) - (2 * y * y)

def PVIRK(y0, dominio, h):
    y = numpy.zeros(len(dominio))
    for i, xi in enumerate(dominio[0:-1], start=0):
        y[i + 1] = rungeKutta4o(xi, y[i], h)
    return y;

class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        self.axes = self.fig.add_subplot(111)
        self.axes.ylabel = '$y$'
        self.axes.xlabel = '$x$'
        # We don't want the axes cleared every time plot() is called
        self.axes.hold(True)
        self.lines = []
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.draw()

    def addPlot(self, y0, step, domain, function, label):
        self.lines.append(label)
        if function == "Adams-Bashforth":
            y = PVI(y0, domain, step)
        else:
            y = PVIRK(y0, domain, step)
        self.plot(domain, y)
    
    def plot(self, domain, y):
        self.axes.plot(domain, y, '-o')
        self.fig.legend(self.axes.get_lines(), self.lines, 'upper right')
        self.draw()
    
    def clear(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.draw()
        

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")        
        self.main_widget = QtGui.QWidget(self)
        self.sc = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.tfY0 = QtGui.QLineEdit()
        self.tfDomainStart = QtGui.QLineEdit()
        self.tfDomainEnd = QtGui.QLineEdit()
        self.tfStep = QtGui.QLineEdit()
        self.tfLabel = QtGui.QLineEdit()
        self.cbFunctions = QtGui.QComboBox()
        
        self.cbFunctions.addItems(["Adams-Bashforth", "Runge-Kutta 4o"])
        self.tfDomainStart.setText("0")
        self.tfDomainEnd.setText("5")
        self.tfStep.setText("0.2")
        
#         mainPanel = QtGui.QGridLayout(self.main_widget)
        mainPanel = QtGui.QHBoxLayout(self.main_widget)
        menuPanel = QtGui.QVBoxLayout()
        PVIPanel = QtGui.QHBoxLayout()
        domainPanel = QtGui.QHBoxLayout()
        bpanel = QtGui.QHBoxLayout()
        
        PVIPanel.addWidget(QtGui.QLabel("y0:"))
        PVIPanel.addWidget(self.tfY0)
        PVIPanel.addWidget(QtGui.QLabel("passo:"))
        PVIPanel.addWidget(self.tfStep)
        domainPanel.addWidget(QtGui.QLabel("inicio:"))
        domainPanel.addWidget(self.tfDomainStart)
        domainPanel.addWidget(QtGui.QLabel("fim:"))
        domainPanel.addWidget(self.tfDomainEnd)
        
        plotar = QtGui.QPushButton("Plotar")
        apagar = QtGui.QPushButton("Apagar")
        bpanel.addWidget(apagar)
        bpanel.addWidget(plotar)
        
        menuPanel.addWidget(QtGui.QLabel("Dominio"))
        menuPanel.addLayout(domainPanel)
        menuPanel.addSpacing(10)
        menuPanel.addWidget(QtGui.QLabel("Solução e passo"))
        menuPanel.addLayout(PVIPanel)
        menuPanel.addSpacing(10)
        menuPanel.addWidget(QtGui.QLabel("Função"))
        menuPanel.addWidget(self.cbFunctions)
        menuPanel.addSpacing(10)
        menuPanel.addWidget(QtGui.QLabel("Legenda"))
        menuPanel.addWidget(self.tfLabel)
        menuPanel.addSpacing(20)
        menuPanel.addLayout(bpanel)
        menuPanel.addStretch()
        mainPanel.addLayout(menuPanel, 1)
        mainPanel.addWidget(self.sc, 3)
#         mainPanel.setColumnMinimumWidth(400, 100)
        
        plotar.clicked.connect(self.plot)
        apagar.clicked.connect(self.apagar)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
    
    def apagar(self):
        self.sc.clear()

    
    def plot(self):
        if len(self.tfDomainEnd.text()) > 0 and len(self.tfDomainStart.text()) > 0 and len(self.tfStep.text()) > 0 and len(self.tfY0.text()) > 0 and len(self.tfLabel.text()) > 0:
            start = float(self.tfDomainStart.text())
            end = float(self.tfDomainEnd.text())
            y0 = float(self.tfY0.text())
            step = float(self.tfStep.text())
            label = self.tfLabel.text();
            domain = numpy.arange(start, end, step)
            self.sc.addPlot(y0, step, domain, self.cbFunctions.currentText(), label)


qApp = QtGui.QApplication(sys.argv)
aw = ApplicationWindow()
aw.show()
sys.exit(qApp.exec_())