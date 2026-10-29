# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pistasAdmin.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(729, 629)
        Form.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_10 = QFrame(Form)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMaximumSize(QSize(16777215, 60))
        self.frame_10.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frame_12 = QFrame(self.frame_10)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMaximumSize(QSize(600, 800))
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_12)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_12)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(22)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_5)


        self.horizontalLayout_5.addWidget(self.frame_12)

        self.horizontalSpacer = QSpacerItem(168, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.frame_11 = QFrame(self.frame_10)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.fecha = QLabel(self.frame_11)
        self.fecha.setObjectName(u"fecha")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.fecha.setFont(font1)
        self.fecha.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.fecha)

        self.hora = QLabel(self.frame_11)
        self.hora.setObjectName(u"hora")
        self.hora.setFont(font1)
        self.hora.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.hora)


        self.horizontalLayout_5.addWidget(self.frame_11)


        self.verticalLayout.addWidget(self.frame_10)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setLayoutDirection(Qt.LeftToRight)
        self.frame_4.setStyleSheet(u"")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_6 = QFrame(self.frame_4)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_3 = QLabel(self.frame_6)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setFamilies([u"Arial Rounded MT Bold"])
        font2.setPointSize(18)
        self.label_3.setFont(font2)

        self.verticalLayout_5.addWidget(self.label_3)

        self.label_7 = QLabel(self.frame_6)
        self.label_7.setObjectName(u"label_7")
        font3 = QFont()
        font3.setPointSize(18)
        font3.setBold(True)
        font3.setItalic(True)
        self.label_7.setFont(font3)
        self.label_7.setLayoutDirection(Qt.LeftToRight)
        self.label_7.setStyleSheet(u"color: rgb(0, 176, 0);")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_7)

        self.btn_pista1 = QPushButton(self.frame_6)
        self.btn_pista1.setObjectName(u"btn_pista1")
        self.btn_pista1.setMaximumSize(QSize(200, 40))
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        self.btn_pista1.setFont(font4)
        self.btn_pista1.setStyleSheet(u"#btn_pista1 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#btn_pista1 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#btn_pista1 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_5.addWidget(self.btn_pista1)


        self.horizontalLayout_2.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.frame_4)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_4 = QLabel(self.frame_7)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u"C:/Users/Javy/.designer/iconos/PIsta1.jpg"))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_4)


        self.horizontalLayout_2.addWidget(self.frame_7)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame_8 = QFrame(self.frame_5)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_8)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_2 = QLabel(self.frame_8)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.verticalLayout_7.addWidget(self.label_2)

        self.label_6 = QLabel(self.frame_8)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font3)
        self.label_6.setLayoutDirection(Qt.LeftToRight)
        self.label_6.setStyleSheet(u"color: rgb(0, 176, 0);")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_6)

        self.btn_pista2 = QPushButton(self.frame_8)
        self.btn_pista2.setObjectName(u"btn_pista2")
        self.btn_pista2.setMaximumSize(QSize(200, 40))
        self.btn_pista2.setFont(font4)
        self.btn_pista2.setStyleSheet(u"#btn_pista2 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#btn_pista2 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#btn_pista2 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_7.addWidget(self.btn_pista2)


        self.horizontalLayout_3.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.frame_5)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_9)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label = QLabel(self.frame_9)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u"C:/Users/Javy/.designer/iconos/PIsta1.jpg"))
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label)


        self.horizontalLayout_3.addWidget(self.frame_9)


        self.verticalLayout_2.addWidget(self.frame_5)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(150, 16777215))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_3 = QPushButton(self.frame_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(16777215, 25))
        self.pushButton_3.setFont(font4)
        self.pushButton_3.setStyleSheet(u"#pushButton_3 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#pushButton_3 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#pushButton_3 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_8 = QPushButton(self.frame_3)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setMaximumSize(QSize(16777215, 25))
        self.pushButton_8.setFont(font4)
        self.pushButton_8.setStyleSheet(u"#pushButton_8 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#pushButton_8 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#pushButton_8 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_3.addWidget(self.pushButton_8)

        self.pushButton_7 = QPushButton(self.frame_3)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMaximumSize(QSize(16777215, 25))
        self.pushButton_7.setFont(font4)
        self.pushButton_7.setStyleSheet(u"#pushButton_7 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#pushButton_7 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#pushButton_7 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_3.addWidget(self.pushButton_7)

        self.pushButton_4 = QPushButton(self.frame_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setFont(font4)
        self.pushButton_4.setStyleSheet(u"#pushButton_4 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#pushButton_4 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#pushButton_4 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_6 = QPushButton(self.frame_3)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setFont(font4)
        self.pushButton_6.setStyleSheet(u"#pushButton_6 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#pushButton_6 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#pushButton_6 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_3.addWidget(self.pushButton_6)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_3.addItem(self.spacer)

        self.groupBox = QGroupBox(self.frame_3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(200, 150))
        self.groupBox.setFont(font4)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_tv1 = QPushButton(self.groupBox)
        self.btn_tv1.setObjectName(u"btn_tv1")
        self.btn_tv1.setMaximumSize(QSize(16777215, 30))
        self.btn_tv1.setFont(font4)
        self.btn_tv1.setStyleSheet(u"#btn_tv1 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#btn_tv1 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#btn_tv1 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_4.addWidget(self.btn_tv1)

        self.btn_tv2 = QPushButton(self.groupBox)
        self.btn_tv2.setObjectName(u"btn_tv2")
        self.btn_tv2.setMaximumSize(QSize(16777215, 30))
        self.btn_tv2.setFont(font4)
        self.btn_tv2.setStyleSheet(u"#btn_tv2 {\n"
"    background-color: rgba(215, 0, 0, 210); /* Fondo rojo s\u00f3lido */\n"
"    color: rgba(255, 255, 255, 210); /* Texto en blanco */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#btn_tv2 :hover {\n"
"    background-color: rgba(200, 0, 0, 255); /* Rojo m\u00e1s oscuro para el hover */\n"
"    color: rgba(255, 255, 255, 210); /* Mantenemos el texto en blanco */\n"
"}\n"
"\n"
"#btn_tv2 :pressed {\n"
"    background-color: rgba(150, 0, 0, 255); /* Rojo a\u00fan m\u00e1s oscuro para el estado presionado */\n"
"    padding-left: 5px; /* Efecto de presi\u00f3n */\n"
"    padding-top: 5px; /* Efecto de presi\u00f3n */\n"
"}")

        self.verticalLayout_4.addWidget(self.btn_tv2)


        self.verticalLayout_3.addWidget(self.groupBox)


        self.horizontalLayout.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Gesti\u00f3n de Pistas", None))
        self.fecha.setText(QCoreApplication.translate("Form", u"21-11-2024", None))
        self.hora.setText(QCoreApplication.translate("Form", u"20:21:03", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Pista 1", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Libre", None))
        self.btn_pista1.setText(QCoreApplication.translate("Form", u"Jugar", None))
        self.label_4.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Pista 2", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Libre", None))
        self.btn_pista2.setText(QCoreApplication.translate("Form", u"Jugar", None))
        self.label.setText("")
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Comunicaci\u00f3n", None))
        self.pushButton_8.setText(QCoreApplication.translate("Form", u"Configuraci\u00f3n", None))
        self.pushButton_7.setText(QCoreApplication.translate("Form", u"Base de datos", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"TV 1", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"TV2", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Ventanas", None))
        self.btn_tv1.setText(QCoreApplication.translate("Form", u" Abrir TV 1", None))
        self.btn_tv2.setText(QCoreApplication.translate("Form", u"Abrir TV 2", None))
    # retranslateUi

