# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1243, 984)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(960, 10, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.raw = QtWidgets.QGraphicsView(Form)
        self.raw.setGeometry(QtCore.QRect(20, 40, 1200, 600))
        self.raw.setObjectName("raw")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(200, 10, 151, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 770, 81, 16))
        self.label.setObjectName("label")
        self.aligned = QtWidgets.QLabel(Form)
        self.aligned.setGeometry(QtCore.QRect(400, 650, 481, 301))
        self.aligned.setText("")
        self.aligned.setObjectName("aligned")

        self.retranslateUi(Form)
        self.checkBox.clicked.connect(Form.show_raw)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "0/0"))
        self.checkBox.setText(_translate("Form", "显示原图"))
        self.label.setText(_translate("Form", "配准结果图："))
