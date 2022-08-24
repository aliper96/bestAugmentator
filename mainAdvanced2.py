# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt,QThreadPool)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QSizePolicy,
    QStatusBar, QWidget, QHBoxLayout, QVBoxLayout,QPushButton,QStackedLayout,QDoubleSpinBox,QLabel,QScrollArea,QFileDialog,QListWidget,QListWidgetItem)

import albumentations as A
import  cv2 as cv
from enum import Enum, auto
import sys
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed


IMAGE_SIZE = (424,424)



class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class filters(Enum):
    resize    = auto()
    horizontalflip = auto()
    randomsizecrop    = auto()
    centercrop    = auto()
    rgbshift    = auto()
    blur    = auto()
    randombrightnesscontrast    = auto()
    clahe    = auto()
    vertflip    = auto()
    elastictransform    = auto()
    randomcontrast90    = auto()
    tosepia    = auto()
    multi    = auto()
    multiplicativenoise    = auto()
    imagecompression  = auto()
    channeldropout    = auto()
    colorjitter    = auto()
    emboss    = auto()
    equalize    = auto()
    griddistortion    = auto()
    togray    = auto()
    channelshuffle = auto()
    fancypca = auto()


PROBABILITIES_GLOB = {

    filters.resize:1,
    filters.horizontalflip:1,
    filters.randomsizecrop:0,
    filters.centercrop:0,
    filters.rgbshift:1,
    filters.blur:1,
    filters.randombrightnesscontrast:1,
    filters.clahe:1,
    filters.vertflip:1,
    filters.elastictransform:1,
    filters.randomcontrast90:1,
    filters.tosepia:1,
    filters.multi:1,
    filters.multiplicativenoise:1,
    filters.imagecompression:1,
    filters.channeldropout:1,
    filters.colorjitter:1,
    filters.emboss:1,
    filters.equalize:1,
    filters.griddistortion:1,
    filters.togray:0,
    filters.channelshuffle:0,
    filters.fancypca:0.5,


    # FOR MORE :
    #https://tugot17.github.io/data-science-blog/albumentations/data-augmentation/tutorial/2020/09/20/Pixel-level-transforms-using-albumentations-package.html
}






class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.resize(800,700)

    # setupUi
        self.image = None

    # sel
        self.threadpool = QThreadPool()

        # Obtenemos el nombre de todos los filtros
        pagelayout = QVBoxLayout()
        all_filters_names = [filter.name for filter in filters]
        all_filters_names = sorted(all_filters_names, key=len)

#Creamos el boton y el spinbox por cada filtro
        for filter in all_filters_names:
            filterLine = QHBoxLayout()
            btnr =  QPushButton(filter,self)
            btnr.setObjectName(filter)
            btnr.setMaximumWidth(75)
            if(len(filter)>=10):
                btnr.setToolTip(filter)
            spinValue = QDoubleSpinBox(parent=self)
            spinValue.setObjectName(filter)
            spinValue.setMaximum(1.0)
            spinValue.setMinimum(0.0)
            spinValue.setSingleStep(0.05)
            btnr.released.connect(lambda  text=filter : self.justOneFilter(text))
            spinValue.valueChanged.connect(self.updateValues)

            filterLine.addWidget(btnr)
            filterLine.addWidget(spinValue)
            pagelayout.addLayout(filterLine)


        self.doublespin = self.findChildren(QDoubleSpinBox)

#Botones de la parte de arriba
        buttonsLayout = QHBoxLayout()
        btn_img = QPushButton("Select Image")
        btn_img.released.connect(self.loadImage)
        btn_g = QPushButton("Generate Images")
        btn_gt = QPushButton("Generate withGT")
        btn_preview = QPushButton("Preview")
        btn_preview.released.connect(self.setPreviewImages)
        btn_setAllValue = QPushButton("Set all")
        btn_setAllValue.released.connect(self.setAllValue)
        self.spin_setAllValue = QDoubleSpinBox()
        self.spin_setAllValue.setMaximum(1.0)
        self.spin_setAllValue.setMinimum(0.0)
        self.spin_setAllValue.setSingleStep(0.05)

        buttonsLayout.addWidget(btn_img)
        buttonsLayout.addWidget(btn_g)
        buttonsLayout.addWidget(btn_gt)
        buttonsLayout.addWidget(btn_preview)
        buttonsLayout.addWidget(btn_setAllValue)
        buttonsLayout.addWidget(self.spin_setAllValue)


# Widget List
        self.widgetList = QListWidget()
        self.widgetList.setFlow(QListWidget.Flow.LeftToRight)
        self.widgetList.setIconSize(QSize(150,200))
        # firstItem =            QListWidgetItem()
        # self.widgetList.addItem(firstItem)



# Widget con todos los botones
        widget = QWidget()
        widget.setLayout(pagelayout)
        scroll = QScrollArea()
        scroll.setWidget(widget)

# Zona de la imagen ( donde se carga la imagen)

        self.imageLabel =  QLabel()
        self.imageLabel.setStyleSheet("border: 1px solid black;")
        self.imageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


# Main layouts
        mainLabel_H = QHBoxLayout()
        mainLabel_H.addWidget(scroll,stretch=1.5)
        mainLabel_H.addWidget(self.imageLabel,stretch=3)

        mainLabel_V = QVBoxLayout()
        mainLabel_V.addLayout(buttonsLayout,stretch=0.2)
        mainLabel_V.addLayout(mainLabel_H,stretch=1.5)
        mainLabel_V.addWidget(self.widgetList,stretch=0.5)


        mainWidget = QWidget()
        mainWidget.setLayout(mainLabel_V)
        self.setCentralWidget(mainWidget)

    def setAllValue(self):
        [spin.setValue(self.spin_setAllValue.value()) for spin in self.doublespin]
        self.updateValues()
        
    def updateValues(self):

        for filter in filters:
            PROBABILITIES_GLOB[filter] = [spin for spin in self.doublespin if filter.name == spin.objectName()][0].value()



    def justOneFilter(self,filter):
        self.widgetList.clear()
        dic_aux =  dict(PROBABILITIES_GLOB)
        dic_aux = dict.fromkeys(dic_aux, 0)
        # dic_aux[filters[filter]] = [spin for spin in self.doublespin if filter == spin.objectName()][0].value()
        dic_aux[filters[filter]] = 1

        img = cv.imread(self.image)
        strong = self.compose(dic_aux)
        r = strong(image=img)
        icon_pixmap = QPixmap.fromImage(self.img_2_QImage(r["image"]))
        icon = QIcon()
        icon.addPixmap(icon_pixmap)
        itm = QListWidgetItem(icon, "")
        self.widgetList.addItem(itm)

    def loadImage(self):
        imagen  = (QFileDialog.getOpenFileName(self, "Select Image"))[0]
        self.image = imagen
        copy = QPixmap(imagen).scaled(self.imageLabel.width(),self.imageLabel.height(),Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(copy)
    # retranslateUi

    def setPreviewImages(self):
        self.widgetList.clear()
        self.updateValues()

        Parallel(backend='threading',n_jobs=8)(delayed(self.exec_setPreviewImages)() for _ in range(10))

    def exec_setPreviewImages(self):
        img = cv.imread(self.image)
        strong = self.compose(PROBABILITIES_GLOB)

        # for _ in tqdm(range(1, 20)):
        r = strong(image=img)
        icon_pixmap = QPixmap.fromImage(self.img_2_QImage(r["image"]))
        icon = QIcon()
        icon.addPixmap(icon_pixmap)
        itm = QListWidgetItem(icon, "")
        self.widgetList.addItem(itm)




    def compose(self, PROBABILITIES):
        strong = A.Compose([
            # A.resize(IMAGE_SIZE[1],IMAGE_SIZE[0],p=PROBABILITIES[filters.resize]),
            A.HorizontalFlip(p=PROBABILITIES[filters.horizontalflip]),
            A.RandomSizedCrop((250, 250), 250, 250, p=PROBABILITIES[filters.randomsizecrop]),
            A.CenterCrop(IMAGE_SIZE[0], IMAGE_SIZE[1], p=PROBABILITIES[filters.centercrop]),
            A.RGBShift(p=PROBABILITIES[filters.rgbshift]),
            A.Blur(blur_limit=11, p=PROBABILITIES[filters.blur]),
            A.CLAHE(p=PROBABILITIES[filters.clahe]),
            A.VerticalFlip(p=PROBABILITIES[filters.vertflip]),
            A.ElasticTransform(p=PROBABILITIES[filters.elastictransform]),
            A.RandomRotate90(p=PROBABILITIES[filters.randomcontrast90]),
            A.RandomBrightnessContrast(p=PROBABILITIES[filters.randombrightnesscontrast]),
            A.ToSepia(p=PROBABILITIES[filters.tosepia]),
            A.MultiplicativeNoise(p=PROBABILITIES[filters.multi]),
            A.ImageCompression(p=PROBABILITIES[filters.imagecompression]),
            A.ChannelDropout(p=PROBABILITIES[filters.channeldropout]),
            A.ColorJitter(p=PROBABILITIES[filters.colorjitter]),
            A.Emboss(p=PROBABILITIES[filters.emboss]),
            A.Equalize(p=PROBABILITIES[filters.equalize]),
            A.GridDistortion(p=PROBABILITIES[filters.griddistortion]),
            A.ToGray(p=PROBABILITIES[filters.togray]),
            A.augmentations.transforms.ChannelShuffle(p=PROBABILITIES[filters.togray]),
            A.augmentations.transforms.FancyPCA(alpha=0.1, always_apply=False, p=PROBABILITIES[filters.fancypca]),
        ], p=1)
        return strong

    def img_2_QImage(self,image_show):
        h, w, channels = image_show.shape
        bgrx = np.empty((h, w, 4), np.uint8, "C")
        bgrx[..., :3] = image_show
        qimage = QImage(bgrx.data, w, h, QImage.Format_RGB32)
        qimage.data = bgrx
        return qimage





if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Ui_MainWindow()
    window.show()

    sys.exit(app.exec())