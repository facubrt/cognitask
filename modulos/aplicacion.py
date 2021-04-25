### Módulo de Aplicación #################################################
##########################################################################
## Autor: Facundo Barreto ### facubrt@gmail.com ##########################
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


from PyQt5 import QtCore, QtGui, QtWidgets #########
from PyQt5.QtCore import QPropertyAnimation ########
GLOBAL_STATE = 0


class Ui_BCIAplicacion(object):
    def setupUi(self, BCIAplicacion):
        BCIAplicacion.setObjectName("BCIAplicacion")
        BCIAplicacion.resize(1106, 786) ## 745
        BCIAplicacion.setMinimumSize(QtCore.QSize(1106, 786)) ## 745
        BCIAplicacion.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.centralwidget = QtWidgets.QWidget(BCIAplicacion)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_frame = QtWidgets.QFrame(self.centralwidget)
        self.top_frame.setMinimumSize(QtCore.QSize(700, 606))
        self.top_frame.setStyleSheet("border-top-left-radius: 6px;")
        self.top_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.top_frame.setLineWidth(0)
        self.top_frame.setObjectName("top_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.top_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.contenedor_frame = QtWidgets.QFrame(self.top_frame)
        self.contenedor_frame.setMinimumSize(QtCore.QSize(700, 600))
        self.contenedor_frame.setMaximumSize(QtCore.QSize(700, 600))
        self.contenedor_frame.setStyleSheet("border-radius:0px;")
        self.contenedor_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.contenedor_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.contenedor_frame.setLineWidth(0)
        self.contenedor_frame.setObjectName("contenedor_frame")
        self.p3_frame = QtWidgets.QFrame(self.contenedor_frame)
        self.p3_frame.setGeometry(QtCore.QRect(50, 0, 600, 600))
        self.p3_frame.setMinimumSize(QtCore.QSize(600, 600))
        self.p3_frame.setMaximumSize(QtCore.QSize(600, 600))
        self.p3_frame.setStyleSheet("")
        self.p3_frame.setObjectName("p3_frame")
        self.feedback_label = QtWidgets.QLabel(self.contenedor_frame)
        self.feedback_label.setGeometry(QtCore.QRect(10, 225, 680, 150))
        self.feedback_label.setMinimumSize(QtCore.QSize(680, 100))
        self.feedback_label.setMaximumSize(QtCore.QSize(680, 150))
        font = QtGui.QFont()
        font.setFamily("Gilroy-Bold")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.feedback_label.setFont(font)
        self.feedback_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.feedback_label.setStyleSheet("color: rgb(242, 242, 242);\n"
        "border-color: rgb(0, 0, 0);\n"
        "background-color: rgb(35, 181, 156);\n"
        "border-radius: 6px;\n"
        "")
        self.feedback_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.feedback_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.feedback_label.setLineWidth(1)
        self.feedback_label.setMidLineWidth(0)
        self.feedback_label.setAlignment(QtCore.Qt.AlignCenter)
        self.feedback_label.setObjectName("feedback_label")
        self.horizontalLayout_3.addWidget(self.contenedor_frame)
        self.verticalLayout.addWidget(self.top_frame)
        self.bottom_frame = QtWidgets.QFrame(self.centralwidget)
        self.bottom_frame.setMinimumSize(QtCore.QSize(0, 0)) ## 0, 125
        self.bottom_frame.setMaximumSize(QtCore.QSize(16777215, 150)) ## 16777215, 125
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.bottom_frame.setLineWidth(0)
        self.bottom_frame.setObjectName("bottom_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.bottom_frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineal_progreso_frame = QtWidgets.QFrame(self.bottom_frame)
        self.lineal_progreso_frame.setMinimumSize(QtCore.QSize(770, 150)) ##700, 125
        self.lineal_progreso_frame.setMaximumSize(QtCore.QSize(770, 150)) ##700, 125
        self.lineal_progreso_frame.setStyleSheet("border-radius:0px;")
        self.lineal_progreso_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lineal_progreso_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lineal_progreso_frame.setLineWidth(0)
        self.lineal_progreso_frame.setObjectName("lineal_progreso_frame")
        self.layoutWidget_3 = QtWidgets.QWidget(self.lineal_progreso_frame)
        self.layoutWidget_3.setGeometry(QtCore.QRect(0, 40, 770, 111)) ##10, 40, 680, 75
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.lineal_progreso = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.lineal_progreso.setContentsMargins(0, 0, 0, 0) ## 0, 0, 0, 0
        self.lineal_progreso.setSpacing(0)
        self.lineal_progreso.setObjectName("lineal_progreso")
        self.img1_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        self.img1_lineal.setMinimumSize(QtCore.QSize(80, 80)) ## 70, 70
        self.img1_lineal.setMaximumSize(QtCore.QSize(80, 80)) ## 70, 70
        self.img1_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img1_lineal.setText("")
        self.img1_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img1_lineal.setScaledContents(True)
        self.img1_lineal.setObjectName("img1_lineal")
        self.lineal_progreso.addWidget(self.img1_lineal)
        self.img2_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        self.img2_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img2_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img2_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img2_lineal.setText("")
        self.img2_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img2_lineal.setScaledContents(True)
        self.img2_lineal.setObjectName("img2_lineal")
        self.lineal_progreso.addWidget(self.img2_lineal)
        self.img3_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        self.img3_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img3_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img3_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img3_lineal.setText("")
        self.img3_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img3_lineal.setScaledContents(True)
        self.img3_lineal.setObjectName("img3_lineal")
        self.lineal_progreso.addWidget(self.img3_lineal)
        self.img4_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img4_lineal.sizePolicy().hasHeightForWidth())
        self.img4_lineal.setSizePolicy(sizePolicy)
        self.img4_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img4_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img4_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img4_lineal.setText("")
        self.img4_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img4_lineal.setScaledContents(True)
        self.img4_lineal.setObjectName("img4_lineal")
        self.lineal_progreso.addWidget(self.img4_lineal)
        self.img5_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img5_lineal.sizePolicy().hasHeightForWidth())
        self.img5_lineal.setSizePolicy(sizePolicy)
        self.img5_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img5_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img5_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img5_lineal.setText("")
        self.img5_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img5_lineal.setScaledContents(True)
        self.img5_lineal.setObjectName("img5_lineal")
        self.lineal_progreso.addWidget(self.img5_lineal)
        self.img6_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img6_lineal.sizePolicy().hasHeightForWidth())
        self.img6_lineal.setSizePolicy(sizePolicy)
        self.img6_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img6_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img6_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img6_lineal.setText("")
        self.img6_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img6_lineal.setScaledContents(True)
        self.img6_lineal.setObjectName("img6_lineal")
        self.lineal_progreso.addWidget(self.img6_lineal)
        self.img7_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        self.img7_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img7_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img7_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img7_lineal.setText("")
        self.img7_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img7_lineal.setScaledContents(True)
        self.img7_lineal.setObjectName("img7_lineal")
        self.lineal_progreso.addWidget(self.img7_lineal)
        self.img8_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        self.img8_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img8_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img8_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img8_lineal.setText("")
        self.img8_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img8_lineal.setScaledContents(True)
        self.img8_lineal.setObjectName("img8_lineal")
        self.lineal_progreso.addWidget(self.img8_lineal)
        self.img9_lineal = QtWidgets.QLabel(self.layoutWidget_3)
        self.img9_lineal.setMinimumSize(QtCore.QSize(80, 80))
        self.img9_lineal.setMaximumSize(QtCore.QSize(80, 80))
        self.img9_lineal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img9_lineal.setText("")
        self.img9_lineal.setPixmap(QtGui.QPixmap("img/none_light.png"))
        self.img9_lineal.setScaledContents(True)
        self.img9_lineal.setObjectName("img9_lineal")
        self.lineal_progreso.addWidget(self.img9_lineal)
        self.tu_progreso_texto = QtWidgets.QLabel(self.lineal_progreso_frame)
        self.tu_progreso_texto.setGeometry(QtCore.QRect(85, 10, 600, 30)) ## 50, 0, 601, 31
        font = QtGui.QFont()
        font.setFamily("Gilroy-Regular")
        font.setPointSize(14)
        self.tu_progreso_texto.setFont(font)
        self.tu_progreso_texto.setStyleSheet("color: rgb(242, 242, 242);border-color: rgb(0, 0, 0);"
        "background-color: rgb(35, 181, 156); border-radius: 6px;")
        self.tu_progreso_texto.setLineWidth(1)
        self.tu_progreso_texto.setAlignment(QtCore.Qt.AlignCenter)
        self.tu_progreso_texto.setObjectName("tu_progreso_texto")
        self.horizontalLayout_2.addWidget(self.lineal_progreso_frame)
        self.verticalLayout.addWidget(self.bottom_frame)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.right_frame = QtWidgets.QFrame(self.centralwidget)
        self.right_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.right_frame.setMaximumSize(QtCore.QSize(0, 16777215))
        self.right_frame.setStyleSheet("background-color: rgb(46, 51, 58);")
        self.right_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.right_frame.setLineWidth(0)
        self.right_frame.setObjectName("right_frame")
        self.layoutWidget_2 = QtWidgets.QWidget(self.right_frame)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 330, 280, 271))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.grid_progreso = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.grid_progreso.setContentsMargins(10, 0, 10, 0)
        self.grid_progreso.setSpacing(0)
        self.grid_progreso.setObjectName("grid_progreso")
        self.img2_grid = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img2_grid.sizePolicy().hasHeightForWidth())
        self.img2_grid.setSizePolicy(sizePolicy)
        self.img2_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img2_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img2_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img2_grid.setText("")
        self.img2_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img2_grid.setObjectName("img2_grid")
        self.img2_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img2_grid, 0, 1, 1, 1)
        self.img7_grid = QtWidgets.QLabel(self.layoutWidget_2)
        self.img7_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img7_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img7_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img7_grid.setText("")
        self.img7_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img7_grid.setObjectName("img7_grid")
        self.img7_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img7_grid, 2, 0, 1, 1)
        self.img5_grid = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img5_grid.sizePolicy().hasHeightForWidth())
        self.img5_grid.setSizePolicy(sizePolicy)
        self.img5_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img5_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img5_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img5_grid.setText("")
        self.img5_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img5_grid.setObjectName("img5_grid")
        self.img5_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img5_grid, 1, 1, 1, 1)
        self.img9_grid = QtWidgets.QLabel(self.layoutWidget_2)
        self.img9_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img9_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img9_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img9_grid.setText("")
        self.img9_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img9_grid.setObjectName("img9_grid")
        self.img9_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img9_grid, 2, 2, 1, 1)
        self.img3_grid = QtWidgets.QLabel(self.layoutWidget_2)
        self.img3_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img3_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img3_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img3_grid.setText("")
        self.img3_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img3_grid.setObjectName("img3_grid")
        self.img3_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img3_grid, 0, 2, 1, 1)
        self.img1_grid = QtWidgets.QLabel(self.layoutWidget_2)
        self.img1_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img1_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img1_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img1_grid.setText("")
        self.img1_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img1_grid.setObjectName("img1_grid")
        self.img1_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img1_grid, 0, 0, 1, 1)
        self.img8_grid = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img8_grid.sizePolicy().hasHeightForWidth())
        self.img8_grid.setSizePolicy(sizePolicy)
        self.img8_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img8_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img8_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img8_grid.setText("")
        self.img8_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img8_grid.setObjectName("img8_grid")
        self.img8_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img8_grid, 2, 1, 1, 1)
        self.img6_grid = QtWidgets.QLabel(self.layoutWidget_2)
        self.img6_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img6_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img6_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img6_grid.setText("")
        self.img6_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img6_grid.setObjectName("img6_grid")
        self.img6_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img6_grid, 1, 2, 1, 1)
        self.img4_grid = QtWidgets.QLabel(self.layoutWidget_2)
        self.img4_grid.setMinimumSize(QtCore.QSize(80, 80))
        self.img4_grid.setMaximumSize(QtCore.QSize(80, 80))
        self.img4_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.img4_grid.setText("")
        self.img4_grid.setPixmap(QtGui.QPixmap("img/none.png"))
        self.img4_grid.setObjectName("img4_grid")
        self.img4_grid.setScaledContents(True)
        self.grid_progreso.addWidget(self.img4_grid, 1, 0, 1, 1)
        self.firma_texto = QtWidgets.QLabel(self.right_frame)
        self.firma_texto.setGeometry(QtCore.QRect(90, 100, 160, 160))
        font = QtGui.QFont()
        font.setFamily("Gilroy-Regular")
        font.setPointSize(10)
        self.firma_texto.setFont(font)
        self.firma_texto.setStyleSheet("color: rgb(255, 255, 255);")
        self.firma_texto.setLineWidth(0)
        self.firma_texto.setText("")
        self.firma_texto.setPixmap(QtGui.QPixmap("img/isotipo_oscuro.png"))
        self.firma_texto.setScaledContents(True)
        self.firma_texto.setAlignment(QtCore.Qt.AlignCenter)
        self.firma_texto.setObjectName("firma_texto")
        self.tu_progreso_texto_grid = QtWidgets.QLabel(self.right_frame)
        self.tu_progreso_texto_grid.setGeometry(QtCore.QRect(30, 270, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Gilroy-Regular")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.tu_progreso_texto_grid.setFont(font)
        self.tu_progreso_texto_grid.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tu_progreso_texto_grid.setStyleSheet("color: rgb(242, 242, 242);border-color: rgb(0, 0, 0);\n"
        "background-color: rgb(35, 181, 156);border-radius: 6px;")
        self.tu_progreso_texto_grid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tu_progreso_texto_grid.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tu_progreso_texto_grid.setLineWidth(1)
        self.tu_progreso_texto_grid.setMidLineWidth(0)
        self.tu_progreso_texto_grid.setAlignment(QtCore.Qt.AlignCenter)
        self.tu_progreso_texto_grid.setObjectName("tu_progreso_texto_grid")
        self.horizontalLayout.addWidget(self.right_frame)
        self.titlebar_frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titlebar_frame.sizePolicy().hasHeightForWidth())
        self.titlebar_frame.setSizePolicy(sizePolicy)
        self.titlebar_frame.setMinimumSize(QtCore.QSize(40, 0))
        self.titlebar_frame.setMaximumSize(QtCore.QSize(40, 16777215))
        self.titlebar_frame.setStyleSheet("background-color: rgb(46, 51, 58);\n"
"border-top-right-radius:6px;\n"
"border-bottom-right-radius:6px;")
        self.titlebar_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.titlebar_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.titlebar_frame.setLineWidth(0)
        self.titlebar_frame.setObjectName("titlebar_frame")
        self.cerrar_boton = QtWidgets.QPushButton(self.titlebar_frame)
        self.cerrar_boton.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.cerrar_boton.setStyleSheet("QPushButton{\n"
"border-radius:0px;\n"
"border-top-right-radius:6px;\n"
"}\n"
"QPushButton::hover{ background-color: rgb(234, 86, 61);}")
        self.cerrar_boton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cerrar_boton.setIcon(icon)
        self.cerrar_boton.setFlat(True)
        self.cerrar_boton.setObjectName("cerrar_boton")
        self.maximizar_boton = QtWidgets.QPushButton(self.titlebar_frame)
        self.maximizar_boton.setGeometry(QtCore.QRect(0, 40, 41, 41))
        self.maximizar_boton.setStyleSheet("QPushButton{border-radius:0px;}\n"
"QPushButton::hover{ background-color: rgb(54, 60, 66);}")
        self.maximizar_boton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/maximizar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.maximizar_boton.setIcon(icon1)
        self.maximizar_boton.setFlat(True)
        self.maximizar_boton.setObjectName("maximizar_boton")
        self.minimizar_boton = QtWidgets.QPushButton(self.titlebar_frame)
        self.minimizar_boton.setGeometry(QtCore.QRect(0, 80, 41, 41))
        self.minimizar_boton.setStyleSheet("QPushButton{border-radius:0px;}\n"
"QPushButton::hover{ background-color: rgb(54, 60, 66);}")
        self.minimizar_boton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/minimizar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimizar_boton.setIcon(icon2)
        self.minimizar_boton.setFlat(True)
        self.minimizar_boton.setObjectName("minimizar_boton")
        self.expandir_boton = QtWidgets.QPushButton(self.titlebar_frame)
        self.expandir_boton.setGeometry(QtCore.QRect(0, 120, 41, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expandir_boton.sizePolicy().hasHeightForWidth())
        self.expandir_boton.setSizePolicy(sizePolicy)
        self.expandir_boton.setStyleSheet("QPushButton{border-radius:0px;}\n"
        "QPushButton::hover{ background-color: rgb(35, 181, 156);}")
        self.expandir_boton.setText("")
        self.icon3 = QtGui.QIcon()
        self.icon3.addPixmap(QtGui.QPixmap("img/expandirh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon4 = QtGui.QIcon()
        self.icon4.addPixmap(QtGui.QPixmap("img/contraerh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.expandir_boton.setIcon(self.icon3)
        self.expandir_boton.setFlat(True)
        self.expandir_boton.setObjectName("expandir_boton")
        self.horizontalLayout.addWidget(self.titlebar_frame)
        BCIAplicacion.setCentralWidget(self.centralwidget)
        self.Open = 0

        self.progreso_lineal = (self.img1_lineal, self.img2_lineal, self.img3_lineal, self.img4_lineal, self.img5_lineal, self.img6_lineal, self.img7_lineal, self.img8_lineal, self.img9_lineal)
        self.progreso_grid = (self.img1_grid, self.img2_grid, self.img3_grid, self.img4_grid, self.img5_grid, self.img6_grid, self.img7_grid, self.img8_grid, self.img9_grid)
        self.retranslateUi(BCIAplicacion)
        QtCore.QMetaObject.connectSlotsByName(BCIAplicacion)

    def retranslateUi(self, BCIAplicacion):
        _translate = QtCore.QCoreApplication.translate
        BCIAplicacion.setWindowTitle(_translate("BCIAplicacion", "MainWindow"))
        self.feedback_label.setText(_translate("BCIAplicacion", "Comencemos!"))
        self.feedback_label.hide()
        self.tu_progreso_texto.setText(_translate("BCIAplicacion", "Tu progreso"))
        self.tu_progreso_texto_grid.setText(_translate("BCIAplicacion", "Tu progreso"))

class BCIAplicacion(QtWidgets.QMainWindow, Ui_BCIAplicacion):
   
    def __init__(self):
        super(BCIAplicacion, self).__init__()
        self.setupUi(self)

        self.maximizar_boton.clicked.connect(lambda: BCIAplicacion.maximize_restore(self))
        self.minimizar_boton.clicked.connect(lambda: self.showMinimized())
        self.cerrar_boton.clicked.connect(lambda: BCIAplicacion.cerrarAplicacion(self))
        self.expandir_boton.clicked.connect(lambda: self.toggleMenu(310, True))

        def moveWindow(event):
                if event.buttons() == QtCore.Qt.LeftButton and GLOBAL_STATE == 0:
                        self.move(self.pos() + event.globalPos() - self.dragPos)
                        self.dragPos = event.globalPos()
                        event.accept()
        
        self.titlebar_frame.mouseMoveEvent = moveWindow

    def maximize_restore(self):
            global GLOBAL_STATE
            status = GLOBAL_STATE

            # si no está maximizada
            if status == 0:
                    self.showFullScreen()
                    GLOBAL_STATE = 1

            else:
                    GLOBAL_STATE = 0
                    self.showNormal()
    
    def cerrarAplicacion(self):
            self.Open = 0
            self.close()
  
    def mousePressEvent(self, event):
            self.dragPos = event.globalPos()

    def toggleMenu(self, maxWidth, enable):
            if enable:
                width = self.right_frame.width()
                heigth = self.bottom_frame.height()
                maxHeigth = 150 # bottom frame
                minHeight = 0 # bottom frame
                standard = 0

                if width == 0:
                        widthExtended = maxWidth
                        nueva_heigth = minHeight
                        self.expandir_boton.setIcon(self.icon4)

                else:
                        widthExtended = standard
                        nueva_heigth = maxHeigth
                        self.expandir_boton.setIcon(self.icon3)
                
                self.animation = QPropertyAnimation(self.right_frame, b"minimumWidth")
                self.animation_2 = QPropertyAnimation(self.bottom_frame,b"maximumHeight")
                self.animation.setDuration(400)
                self.animation_2.setDuration(400)
                self.animation.setStartValue(width)
                self.animation_2.setStartValue(heigth)
                self.animation.setEndValue(widthExtended)
                self.animation_2.setEndValue(nueva_heigth)
                self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animation_2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animation.start()
                self.animation_2.start()

