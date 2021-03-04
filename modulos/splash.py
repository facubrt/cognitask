### Splash - Cognitask ###################################################
##########################################################################
## Autor: Facundo Barreto ################################################
## 
## BCI basada en P300 para rehabilitación cognitiva ######################
## 
## Proyecto Final de Bioingeniería ### 2020 ##############################

### LICENCIA GPL #########################################################
## This file is part of Cognitask. #######################################
##
##  Cognitask is free software: you can redistribute it and/or modify ####
##  it under the terms of the GNU General Public License as published by #
##  the Free Software Foundation, either version 3 of the License, or ####
##  (at your option) any later version. ##################################
##
##  Cognitask is distributed in the hope that it will be useful, #########
##  but WITHOUT ANY WARRANTY; without even the implied warranty of #######
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the ########
##  GNU General Public License for more details. #########################
##
##  You should have received a copy of the GNU General Public License ####
##  along with Cognitask.  If not, see <https://www.gnu.org/licenses/>. ##

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Splash(object):
    def setupSplash(self, Splash):
            Splash.setObjectName("Splash")
            Splash.resize(450, 300)
            self.centralwidget = QtWidgets.QWidget(Splash)
            self.centralwidget.setMinimumSize(QtCore.QSize(450, 300))
            self.centralwidget.setMaximumSize(QtCore.QSize(450, 300))
            self.centralwidget.setStyleSheet("border-radius:6px;")
            self.centralwidget.setObjectName("centralwidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setSpacing(0)
            self.verticalLayout.setObjectName("verticalLayout")
            self.frame = QtWidgets.QFrame(self.centralwidget)
            self.frame.setStyleSheet("background-color:rgb(255,255,255);\n"
            "border-bottom-left-radius:0px;\n"
            "border-bottom-right-radius:0px;")
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.label = QtWidgets.QLabel(self.frame)
            self.label.setMaximumSize(QtCore.QSize(450, 16777215))
            self.label.setStyleSheet("")
            self.label.setLineWidth(0)
            self.label.setText("")
            self.label.setPixmap(QtGui.QPixmap("img/splash.png"))
            self.label.setObjectName("label")
            self.horizontalLayout.addWidget(self.label)
            self.verticalLayout.addWidget(self.frame)
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setMinimumSize(QtCore.QSize(0, 30))
            self.label_2.setMaximumSize(QtCore.QSize(450, 30))
            font = QtGui.QFont()
            font.setFamily("Gilroy-Regular")
            font.setPointSize(10)
            self.label_2.setFont(font)
            self.label_2.setStyleSheet("background-color: rgb(38, 43, 50);\n"
            "color: rgb(255,255,255);\n"
            "border-top-left-radius:0px;\n"
            "border-top-right-radius:0px;")
            self.label_2.setLineWidth(0)
            self.label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.label_2.setObjectName("label_2")
            self.verticalLayout.addWidget(self.label_2)
            Splash.setCentralWidget(self.centralwidget)
            self.label_2.setText("Despertando BCI2000...")

class Splash(Ui_Splash):
   
    def __init__(self):
        super(Splash, self).__init__()
        self.setupSplash(self)
        
        # Eliminacion de la barra de titulo por defecto
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)