from PyQt5 import QtWidgets, uic,QtGui,QtCore, QtTest
import sys
from enum import Enum,auto
import albumentations as A
import cv2
import numpy as np
import glob
import datetime
import threading
IMAGE_SIZE = (608,608)          # image dimension in pixels (x and y equal) default (None, None)
import cgitb
cgitb.enable(format = 'text')

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
        stu_id_regx = QtCore.QRegExp('^imglabel_[0-9]*')

        self.generatedImages = self.findChildren(QtWidgets.QLabel,stu_id_regx)
        self.generatedImages = np.array(self.generatedImages)

        print(len(self.generatedImages))
        [dspox.setSingleStep(0.05) for dspox in self.doublespinbox_list]
        self.allg.released.connect(self.generateIMG)
        self.selectImage.released.connect(self.loadImage)
        self.todo0.released.connect(self.todo1f)
        self.todo1.released.connect(self.todo0f)
        self.imageFolder.released.connect(self.fimageFolder)
        self.labelFolder.released.connect(self.flabelFolder)
        self.comboBox.currentIndexChanged.connect(self.showImage)

        self.gone.released.connect(self.generateOne)
        self.gall.released.connect(self.generateAll)

        self.pushbutton_list = self.findChildren(QtWidgets.QPushButton)
        [dbutton.released.connect(self.justOneFilter) for dbutton in self.pushbutton_list if "b_" in dbutton.objectName()]
        self.image = ""
        self.imagespath = ""
        self.labelspath = ""

        self.setAllValue(0.50)
        self.d_randomsizecrop.setValue(0.00)
        self.d_centercrop.setValue(0.00)


        self.show()

    def showListView(self, imagesList):

        hasta = min (8,len(imagesList))
        for pimg in range(0,hasta):
            pimgpix = QtGui.QPixmap.fromImage(self.img_2_QImage(imagesList[pimg]))
            self.generatedImages[pimg].setPixmap(pimgpix.scaled(self.generatedImages[pimg].width(), self.generatedImages[pimg].height(),
                                                                        QtCore.Qt.KeepAspectRatio))


    def generateAll(self):
        imagesList = []

        self.updateData(PROBABILITIES_GLOB)
        strong = self.compose(PROBABILITIES_GLOB)
        save_path = (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Image Directory"))

        if (self.labelcheckbox.isChecked()):
            save_path_lb = (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Label Directory"))
            for image,label in zip(self.imagespath,self.labelspath):
                img = cv2.imread(image)
                lb = cv2.imread(label)
                for i in range(0, self.spinBox.value()):
                    r = strong(image=img,mask=lb)
                    image_show = r["image"]
                    lb_show = r["mask"]
                    images_time = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f"))
                    cv2.imwrite(
                        save_path + '/' + str(i) + images_time + '.png',
                        image_show)
                    cv2.imwrite(
                        save_path_lb + '/' + str(i) + images_time + '.png',
                        lb_show)
                imagesList.append(image_show)
        else:
            for image in self.imagespath:
                img = cv2.imread(image)
                for i in range(0, self.spinBox.value()):
                    r = strong(image=img)
                    image_show = r["image"]
                    cv2.imwrite(save_path + '/' + str(i) + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f")) + '.png',
                                image_show)
                imagesList.append(image_show)
        self.showListView(imagesList)


    def generateOne(self):
        imagesList = []
        self.updateData(PROBABILITIES_GLOB)
        strong = self.compose(PROBABILITIES_GLOB)
        save_path =  (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Image Directory"))

        self.image = self.comboBox.currentText()
        img = cv2.imread(self.image)
        if (self.labelcheckbox.isChecked()):
            save_path_lb = (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Label Directory"))
            lb = cv2.imread(self.labelspath[self.comboBox.currentIndex()])
            for i in range(0, self.spinBox.value()):
                r = strong(image=img,mask=lb)
                image_show = r["image"]
                lb_show = r["mask"]
                images_time = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f"))

                cv2.imwrite(
                    save_path + '/' + str(i) + images_time + '.png',
                    image_show)
                cv2.imwrite(
                    save_path_lb + '/' + str(i) + images_time + '.png',
                    lb_show)
                imagesList.append(image_show)
        else:
            for i in range(0,self.spinBox.value()):
                r = strong(image=img)
                image_show = r["image"]
                cv2.imwrite(save_path+'/'+str(i)+str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f"))+ '.png', image_show)
                imagesList.append(image_show)

        self.showListView(imagesList)


        print("se ha terminado el Show")

    def showImage(self):
        self.updateData(PROBABILITIES_GLOB)
        strong = self.compose(PROBABILITIES_GLOB)
        self.image = self.comboBox.currentText()
        img = cv2.imread(self.image)
        r = strong(image=img)
        image_show = r["image"]
        cv2.imwrite('ima_gen' + '.png', image_show)
        qimage = self.img_2_QImage(image_show)
        self.label.setPixmap(QtGui.QPixmap.fromImage(qimage).scaled(self.label.width(),self.label.height(),QtCore.Qt.KeepAspectRatio))


    def fimageFolder(self):
        img_path =  (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Image Directory"))
        self.imagespath =  [glob.glob(img_path + "/" + x) for x in ("*.png", "*.jpg", "*.jpeg")]
        self.imagespath = [ img for img in self.imagespath if img != []][0]
        self.comboBox.addItems(self.imagespath)

    def flabelFolder(self):
        lb_path =  (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Image Directory"))
        self.labelspath =  [glob.glob(lb_path + "/" + x) for x in ("*.png", "*.jpg", "*.jpeg")]
        self.labelspath = [ img for img in self.labelspath if img != []][0]
        self.labelcheckbox.setChecked(True)


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
        qimage = self.img_2_QImage(image_show)

        self.label.setPixmap(QtGui.QPixmap.fromImage(qimage).scaled(self.label.width(),self.label.height(),QtCore.Qt.KeepAspectRatio))
    def img_2_QImage(self,image_show):
        h, w, channels = image_show.shape
        bgrx = np.empty((h, w, 4), np.uint8, "C")
        bgrx[..., :3] = image_show
        qimage = QtGui.QImage(bgrx.data, w, h, QtGui.QImage.Format_RGB32)
        qimage.data = bgrx
        return qimage

    def todo0f(self):
        self.setAllValue(0.00)

    def todo1f(self):
        self.setAllValue(1.00)

    def setAllValue(self,val):
        [dspox.setValue(val) for dspox in self.doublespinbox_list]
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
        qimage = self.img_2_QImage(image_show)
        self.label.setPixmap(QtGui.QPixmap.fromImage(qimage).scaled(self.label.width(),self.label.height(),QtCore.Qt.KeepAspectRatio))

    def loadImage(self):
        imagen  = (QtWidgets.QFileDialog.getOpenFileName(self, "Select Image"))[0]
        self.image = imagen
        copy = QtGui.QPixmap(imagen).scaled(self.label.width(),self.label.height(),QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(copy)

# def except_hook(cls, exception, traceback):
#     sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":


    app = QtWidgets.QApplication(sys.argv)

    window = Ui()
    app.exec_()