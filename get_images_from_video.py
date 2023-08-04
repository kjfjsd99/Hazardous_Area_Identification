#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import os


# In[2]:


#output_dir = './output/'
output_dir = './my_images/'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


# In[3]:


vidcap = cv2.VideoCapture('video_20210909131846341.mp4')
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(output_dir, "image"+str(count)+".jpg"), image)     # save frame as JPG file
    return hasFrames


# In[4]:


sec = 0
frameRate = 1 #//it will capture image in each 1 second
count=1
success = getFrame(sec)
print(success)


# In[5]:


while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)


# In[ ]:




