# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CBT_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QSlider,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, toggleTools):
        if not toggleTools.objectName():
            toggleTools.setObjectName(u"toggleTools")
        toggleTools.setMinimumSize(QSize(70, 100))
        toggleTools.setMaximumSize(QSize(450, 850))
        self.toolGrid = QGridLayout(toggleTools)
        self.toolGrid.setObjectName(u"toolGrid")
        self.BrushFadeSlider = QSlider(toggleTools)
        self.BrushFadeSlider.setObjectName(u"BrushFadeSlider")
        self.BrushFadeSlider.setOrientation(Qt.Horizontal)
        self.BrushFadeSlider.setMaximum(100)
        self.BrushFadeSlider.setTickInterval(1)

        self.toolGrid.addWidget(self.BrushFadeSlider, 0, 0, 1, 5)

        self.toggleGrid = QGridLayout()
        self.toggleGrid.setObjectName(u"toggleGrid")

        self.toolGrid.addLayout(self.toggleGrid, 1, 0, 1, 6)


        self.retranslateUi(toggleTools)

        QMetaObject.connectSlotsByName(toggleTools)
    # setupUi

    def retranslateUi(self, toggleTools):
        pass
    # retranslateUi

