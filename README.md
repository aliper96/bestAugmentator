##Pendiente hacer prueba

# bestAugmentator
## Working everything

I'm going to work on the best data Augmentator, and use this application in CV

Things that I will use here:
* OPENCV
* Qt PySide6
* albumentations
* Export for yolov5 and yolov7
* multithreading
* suport bounding box augmentation

The main idea is to create a appliacation that will help us to select the parameters for our augmentation. 
We will be able to visualize what is happening to our image before doing to for loop. We are going to have a lot of filters and transformation and there is going 
to be a checkbox for each.

### Select Image: Pic just One Image
### Image Folder: Select a folder that contains the images for the augmentation. It will find [ *.jpg, *.png, *.jpeg]
### Label Folder: Select a folder that contains the labels for the augmentation. It will find [ *.jpg, *.png, *.jpeg] 



![](res/resFinal1.jpg)


## The script for the data augmentation is almost done:


Script: augwithlabel.py

Dataset: [DRIVE: Digital Retinal Images for Vessel Extraction](https://drive.grand-challenge.org/)

IMAGES   GENERATED         |  LABEL GENERATED
:-------------------------:|:-------------------------:
![](res/img.JPG)           |  ![](res/lbel.JPG)



