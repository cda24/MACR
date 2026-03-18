# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'macr_main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys
from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        self.frame.setGeometry(QRect(370, 20, 411, 311))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setGeometry(QRect(40, 20, 113, 22))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(40, 50, 113, 22))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(10, 22, 21, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(10, 52, 21, 16))
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(180, 20, 113, 22))
        self.lineEdit_4 = QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(180, 50, 113, 22))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(160, 22, 21, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setGeometry(QRect(160, 52, 21, 16))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QRect(210, 80, 83, 22))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setGeometry(QRect(140, 340, 83, 22))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(QRect(370, 0, 57, 14))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setGeometry(QRect(390, 340, 83, 22))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setGeometry(QRect(510, 340, 83, 22))
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setGeometry(QRect(10, 120, 341, 211))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setGeometry(QRect(260, 340, 83, 22))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 19))
        self.menuMACR = QMenu(self.menubar)
        self.menuMACR.setObjectName("menuMACR")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMACR.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.label.setText(QCoreApplication.translate("MainWindow", "dx", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", "dy", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", "x", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", "y", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "add", None))
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", "remove last", None)
        )
        self.label_5.setText(QCoreApplication.translate("MainWindow", "Image", None))
        self.pushButton_3.setText(
            QCoreApplication.translate("MainWindow", "load image", None)
        )
        self.pushButton_4.setText(
            QCoreApplication.translate("MainWindow", "reset image", None)
        )
        self.pushButton_5.setText(
            QCoreApplication.translate("MainWindow", "export roi", None)
        )
        self.menuMACR.setTitle(QCoreApplication.translate("MainWindow", "MACR", None))

    # retranslateUi


def main():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
