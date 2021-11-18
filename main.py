from PyQt5 import QtWidgets, uic,QtGui,QtCore
import sys
from enum import Enum,auto
import albumentations as A
import cv2
import numpy as np


IMAGE_SIZE = (250,250)          # image dimension in pixels (x and y equal) default (None, None)


# creating enumerations using class
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

    # FOR MORE :
    #https://tugot17.github.io/data-science-blog/albumentations/data-augmentation/tutorial/2020/09/20/Pixel-level-transforms-using-albumentations-package.html
}



class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('inicio.ui', self)
        self.doublespinbox_list = self.findChildren(QtWidgets.QDoubleSpinBox)
        [dspox.setSingleStep(0.05) for dspox in self.doublespinbox_list]
        self.allg.released.connect(self.generateIMG)
        self.selectImage.released.connect(self.loadImage)
        self.todo0.released.connect(self.todo1f)
        self.todo1.released.connect(self.todo0f)
        self.pushbutton_list = self.findChildren(QtWidgets.QPushButton)
        [dbutton.released.connect(self.justOneFilter) for dbutton in self.pushbutton_list if "b_" in dbutton.objectName()]
        self.image = ""
        self.show()

    def justOneFilter(self):
        wid = self.sender()
        dic_aux =  dict(PROBABILITIES_GLOB)
        dic_aux = dict.fromkeys(dic_aux, 0)
        for a in filters:
            if (a.name == self.sender().objectName().replace("b_","")):
                val_bus = a
        dic_aux[val_bus] = 1
        strong = self.compose(dic_aux)
        self.label.clear()
        img = cv2.imread(self.image)
        r = strong(image=img)
        image_show = r["image"]
        cv2.imwrite('ima_gen' + '.png', image_show)
        h, w, channels = image_show.shape
        bgrx = np.empty((h, w, 4), np.uint8, "C")
        bgrx[..., :3] = image_show
        qimage = QtGui.QImage(bgrx.data, w, h, QtGui.QImage.Format_RGB32)
        qimage.data = bgrx

        self.label.setPixmap(QtGui.QPixmap.fromImage(qimage).scaled(self.label.width(),self.label.height(),QtCore.Qt.KeepAspectRatio))


    def todo0f(self):
        [dspox.setValue(0.00) for dspox in self.doublespinbox_list]

    def todo1f(self):
        [dspox.setValue(1.00) for dspox in self.doublespinbox_list]

    def updateData(self,PROBABILITIES):

        PROBABILITIES[filters.resize]= self.d_resize.value()
        PROBABILITIES[filters.horizontalflip]     = self.d_horizontalflip.value()
        PROBABILITIES[filters.randomsizecrop]     = self.d_randomsizecrop.value()
        PROBABILITIES[filters.centercrop]     = self.d_centercrop.value()
        PROBABILITIES[filters.rgbshift]     = self.d_rgbshift.value()
        PROBABILITIES[filters.blur]     = self.d_blur.value()
        PROBABILITIES[filters.randombrightnesscontrast]     = self.d_randombrightnesscontrast.value()
        PROBABILITIES[filters.clahe]     = self.d_clahe.value()
        PROBABILITIES[filters.vertflip]     = self.d_vertflip.value()
        PROBABILITIES[filters.elastictransform]     = self.d_elastictransform.value()
        PROBABILITIES[filters.randomcontrast90]     = self.d_randomcontrast90.value()
        PROBABILITIES[filters.tosepia]     = self.d_tosepia.value()
        PROBABILITIES[filters.multi]     = self.d_multi.value()
        PROBABILITIES[filters.multiplicativenoise]     = self.d_multiplicativenoise.value()
        PROBABILITIES[filters.imagecompression]     = self.d_imagecompression.value()
        PROBABILITIES[filters.channeldropout]     = self.d_channeldropout.value()
        PROBABILITIES[filters.colorjitter]     = self.d_colorjitter.value()
        PROBABILITIES[filters.emboss]     = self.d_emboss.value()
        PROBABILITIES[filters.equalize]     = self.d_equalize.value()
        PROBABILITIES[filters.griddistortion]     = self.d_griddistortion.value()
        PROBABILITIES[filters.togray]     = self.d_togray.value()

    def compose(self,PROBABILITIES):
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
        ], p=1)
        return strong


    def generateIMG(self):
        self.updateData(PROBABILITIES_GLOB)
        strong = self.compose(PROBABILITIES_GLOB)
        self.label.clear()
        img = cv2.imread(self.image)
        r = strong(image=img)
        image_show = r["image"]
        cv2.imwrite('ima_gen' + '.png', image_show)
        h, w, channels = image_show.shape

        bgrx = np.empty((h, w, 4), np.uint8, "C")
        bgrx[..., :3] = image_show
        qimage = QtGui.QImage(bgrx.data, w, h, QtGui.QImage.Format_RGB32)
        qimage.data = bgrx

        self.label.setPixmap(QtGui.QPixmap.fromImage(qimage).scaled(self.label.width(),self.label.height(),QtCore.Qt.KeepAspectRatio))

    def loadImage(self):
        imagen  = (QtWidgets.QFileDialog.getOpenFileName(self, "Select Image"))[0]
        self.image = imagen
        copy = QtGui.QPixmap(imagen).scaled(self.label.width(),self.label.height(),QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(copy)





app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()