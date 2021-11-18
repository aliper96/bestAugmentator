import os
import glob
import cv2
import albumentations as A
from enum import Enum,auto
from tqdm import tqdm



PATH = 'C:/Users/ahamza/PycharmProjects/venasLabeling/prueba/train/'
INFOLDER =  PATH + 'images/'   # folder containing original images relative to working directory
LABELFOLDER =  PATH + 'labels/'   # Just the label Folder Name
OUTFOLDER = 'C:/Users/ahamza/PycharmProjects/venasLabeling/prueba/resul/'          # directory to write variations to
EXTENSION_IMG = '.png'        # image name extension
EXTENSION_LB = '.png'        # image name extension
SAVEIMG = "saveimg/"
SAVELB = "savelb/"
IMAGE_SIZE = (250,250)          # image dimension in pixels (x and y equal) default (None, None)
LABELING = True
ORDER_NAME = "order"    # Se buscan los labels por nombre o por orden
N_MUESTRAS = 10


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








PROBABILITIES = {

    filters.resize:1,
    filters.horizontalflip:1,
    filters.randomsizecrop:1,
    filters.centercrop:1,
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
    filters.togray:1,

    # FOR MORE :
    #https://tugot17.github.io/data-science-blog/albumentations/data-augmentation/tutorial/2020/09/20/Pixel-level-transforms-using-albumentations-package.html
}

# newDict = {key: 0 for key in PROBABILITIES}

print("Vamos a comenzar: ")

strong = A.Compose([
    # A.resize(IMAGE_SIZE[1],IMAGE_SIZE[0],p=PROBABILITIES[filters.resize]),
    A.HorizontalFlip(p=PROBABILITIES[filters.horizontalflip]),
    A.RandomSizedCrop((250, 250), 250, 250,p = PROBABILITIES[filters.randomsizecrop]),
    A.CenterCrop(IMAGE_SIZE[0],IMAGE_SIZE[1],p = PROBABILITIES[filters.centercrop]),
    A.RGBShift(p = PROBABILITIES[filters.rgbshift]),
    A.Blur(blur_limit=11,p = PROBABILITIES[filters.blur]),
    A.CLAHE(p = PROBABILITIES[filters.clahe]),
    A.VerticalFlip(p = PROBABILITIES[filters.vertflip]),
    A.ElasticTransform(p = PROBABILITIES[filters.elastictransform]),
    A.RandomRotate90(p = PROBABILITIES[filters.randomcontrast90]),
    A.RandomBrightnessContrast(p = PROBABILITIES[filters.randombrightnesscontrast]),
    A.ToSepia(p = PROBABILITIES[filters.tosepia]),
    A.MultiplicativeNoise(p = PROBABILITIES[filters.multi]),
    A.ImageCompression(p = PROBABILITIES[filters.imagecompression]),
    A.ChannelDropout(p = PROBABILITIES[filters.channeldropout]),
    A.ColorJitter(p = PROBABILITIES[filters.colorjitter]),
    A.Emboss(p = PROBABILITIES[filters.emboss]),
    A.Equalize(p = PROBABILITIES[filters.equalize]),
    A.GridDistortion(p = PROBABILITIES[filters.griddistortion]),
    A.ToGray(p = PROBABILITIES[filters.togray]),
], p=1)


raw_image_lst = glob.glob(INFOLDER + '*' + EXTENSION_IMG)
lb_image_lst = glob.glob(LABELFOLDER + '*' + EXTENSION_LB)

if ORDER_NAME == "name":

    for epoch in tqdm(range(N_MUESTRAS)):
        for i,r_img in enumerate(raw_image_lst):
            img  =  cv2.imread(r_img)

            if LABELING:
                lb_path = LABELFOLDER + os.path.split(r_img)[-1]
                lb_path = lb_path.replace(lb_path.split(".")[-1],EXTENSION_LB)
                lb = cv2.imread(lb_path)
                r = strong(image =img, mask = lb)
                cv2.imwrite(SAVEIMG+'ima_gen'+str(i)+'.png',r['image'])
                cv2.imwrite(SAVELB+'lb_gen'+str(i)+'.png',r["mask"])
            else:
                r = strong(image =img)
                cv2.imwrite(SAVEIMG+'ima_gen'+str(i)+'.png',r['image'])



elif ORDER_NAME == "order":
    raw_image_lst = sorted(raw_image_lst)
    img_list = [cv2.imread(img) for img in raw_image_lst]
    if LABELING:
        lb_image_lst = sorted(lb_image_lst)
        lb_list = [cv2.imread(lb) for lb in lb_image_lst]


    for epoch in tqdm(range(N_MUESTRAS)):
        for i in range(len(img_list)):
                if LABELING:
                    r = strong(image =img_list[i], mask = lb_list[i])
                    cv2.imwrite(SAVEIMG+'ima_gen'+str(i)+'.png',r['image'])
                    cv2.imwrite(SAVELB+'lb_gen'+str(i)+'.png',r["mask"])
                else:
                    r = strong(image =img_list[i])
                    cv2.imwrite(SAVEIMG+'ima_gen'+str(i)+'.png',r['image'])



