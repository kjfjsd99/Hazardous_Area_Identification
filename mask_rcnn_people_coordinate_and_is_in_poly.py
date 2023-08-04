#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import the necessary packages
from mrcnn.config import Config
from mrcnn import model as modellib


# In[2]:


import imutils
import cv2
import os
import argparse
import colorsys
import random
import numpy as np


# In[3]:


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default=None,
	help="path to input video file")
ap.add_argument('-f', "--folder", type=str, default=None, help="path to input video folder")
ap.add_argument("-o", "--output", type=str, default="./output", help="path to output images folder")
ap.add_argument("-s", "--source", type=str, default="./source", help="path to save sorce video to image folder")
ap.add_argument("-c", "--csvfolder", type=str, default="./csvfiles", help="path to output csv files folder")
ap.add_argument("-e", "--extendsion", type=str, default="mp4", help="video extendsion file")
ap.add_argument("--fps", type=int, default=30, help="count video to image per frame")
ap.add_argument("-r", "--result", type=int, default=1, help='whether storage source and result image')
args = vars(ap.parse_args())


# In[4]:


#Project: current directory
pathProject = os.getcwd()
pathLib     = os.path.sep.join([pathProject,"lib"])
#testing dataset
videoPath = args["input"]
videoFolder = args["folder"]
inputPath   = args["input"]
csvfolder = args["csvfolder"]
fps = args['fps']
outputPath  = args["output"]
if args['result'] == 1:
    save = True
else:
    save = False
sorucePath = args['source']
labelsPath  = os.path.sep.join([pathLib, "coco_labels.txt"])
weightsPath = os.path.sep.join([pathLib, "mask_rcnn_coco.h5"])

color={"red":(0,0,255),"green":(0,255,0),"blue":(255,0,0),
       "yellow":(0,255,255),"cyan":(255,255,0)} #BGR


# In[5]:


# load the class label names from disk, one label per line
CLASS_NAMES = open(labelsPath).read().strip().split("\n")

# generate random (but visually distinct) colors for each class label
# (thanks to Matterport Mask R-CNN for the method!)
hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]
COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
random.seed(42)
random.shuffle(COLORS)

class SimpleConfig(Config):
    # give the configuration a recognizable name
    NAME = "coco_inference"
    # set the number of GPUs to use along with the number of images per GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    # number of classes (we would normally add +1 for the background
    # but the background class is *already* included in the class names)
    NUM_CLASSES = len(CLASS_NAMES)

# initialize the inference configuration
config = SimpleConfig()

# initialize the Mask R-CNN model for inference and then load the weights
print("[INFO] loading Mask R-CNN model...")
model = modellib.MaskRCNN(mode="inference", config=config,	model_dir=os.getcwd())
model.load_weights(weightsPath, by_name=True)


# In[6]:


def mask_rcnn(image, convertSize, showName=False, showNumberOfPerson=False):
    img = image.copy()
    # perform a forward pass of the network to obtain the results
    print("[INFO] making predictions with Mask R-CNN...")
    color = (0,255,0) #BGR
    width_img   = img.shape[1] #x
    ratio = convertSize/width_img
    img = imutils.resize(img, width=convertSize)
    
    #detect results   
    r = model.detect([img], verbose=1)[0]
    
    #convert the image back to BGR so we can use OpenCV's drawing functions
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    count  = 0 #count people
    bboxes = [] #boxes in image
    #loop over the predicted scores and class labels
    for i in range(0, len(r["scores"])):
    #extract the bounding box information, class ID, label, predicted probability, and visualization color
        classID = r["class_ids"][i]
        label   = CLASS_NAMES[classID]
        if label != "person": #check person class
            continue
        
        count  = count + 1
        (startY, startX, endY, endX) = r["rois"][i] #get bbox
        #covert to original codinate
        startY = int(startY/ratio)
        startX = int(startX/ratio)
        endY   = int(endY/ratio)
        endX   = int(endX/ratio)
        bbox = [startY, startX, endY, endX]
        bboxes.append(bbox)
        img = imutils.resize(img, width=width_img) #covert image to orginal size
        
        #draw the bounding box
        cv2.rectangle(img, (startX, startY), (endX, endY), color, 2)
        #show class label, and score of the object
        if showName:
            #score = r["scores"][i]
            #text = "{}: {:.3f}".format(label, score)
            text ="#"+str(count)
            y    = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(img, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
      #Total of boxs
    if showNumberOfPerson:
        cv2.putText(img, str(len(bboxes)),(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)
            
    return img, bboxes


# In[7]:


img = cv2.imread("./my_images/image87.jpg")
img = cv2.resize(img, (1800, 1000), interpolation=cv2.INTER_AREA)
overlay = img.copy()


# In[8]:


bb=[]
widthMask= 512 #image size for Mask RCNN

crop_img,bb = mask_rcnn(img, widthMask)

cv2.imwrite('crop_img.jpg', crop_img)
print(bb)


# In[9]:


#print((bb[0][1] + bb[0][3])/2, (bb[0][0] + bb[0][2])/2) 
#print((bb[1][1] + bb[1][3])/2, (bb[1][0] + bb[1][2])/2)
#print((bb[2][1] + bb[2][3])/2, (bb[2][0] + bb[2][2])/2)
#print((bb[3][1] + bb[3][3])/2, (bb[3][0] + bb[3][2])/2)


# In[10]:


list_f = []
for i in range(len(bb)):
    x = (bb[i][1] + bb[i][3])/2
    y = (bb[i][0] + bb[i][2])/2
    
    list_f.append([x, y])
print(list_f)
    


# In[11]:


def is_in_poly(p, poly):
    """

    :param p: [x, y]
    :param poly: [[], [], [], [], ...]
    :return:
    """
    px, py = p
    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner
        x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:  # if point is on edge
                is_in = True
                break
            elif x > px:  # if point is on left-side of line
                is_in = not is_in
    return is_in


# In[12]:


person = list_f

poly = [[50, 50], [1750, 30], [1500, 350], [30, 800]]

points2 = np.array([[50, 50], [1750, 30], [1500, 350], [30, 800]])

light_red = (0, 0, 255)
light_green = (144, 238, 144)

for per_person in person: 
    if is_in_poly(per_person, poly) == True:
       #points2 = np.array([[50, 50], [1400, 30], [1500, 380], [30, 800]])
       #light_red = (0, 0, 255)
       cv2.fillPoly(img, [points2], light_red)
    
       alpha = 0.4  # Transparency factor.

       # Following line overlays transparent rectangle over the image
       img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
       cv2.imwrite('colored_region.jpg', img_new)

    else:
       cv2.fillPoly(img, [points2], light_green)
    
       alpha = 0.4  # Transparency factor.

       # Following line overlays transparent rectangle over the image
       img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
       cv2.imwrite('colored_region.jpg', img_new)


# In[ ]:




