#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
from keras.models import load_model
model_v2 = load_model("Model/traffic_classifier.h5")
#model_v1 = load_model("Model/Model_Comp_v1.h5")
model_v1 = load_model("Model/Model_Comp_v4.h5")
def reqdetection(img):
    img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 200)
    contours,hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    area =0
    if (len(contours)!=0):
        for i in range(len(contours)):
            approx = cv2.approxPolyDP(contours[i], 0.01*cv2.arcLength(contours[i], True), True)
            if(len(approx) <= 6):
                x,y,w,h= cv2.boundingRect(contours[i])
                Area = w*h
                if(Area>area):
                    cropped_img=img[y:y+h, x:x+w]
                    area = Area
                    W=w
                    H=h
    if(area>1):
        return contours,cropped_img,area,W,H
    else:
        return 0,0,0,1000,1
    
def detect(cropped_img,area,ratio):
    if(area>6000)and(area<15000):
        if((ratio>1.25)and(ratio<2)):
            pred_1= model_v2(cv2.resize(cropped_img[10:-10,10:-10,:], (30,30), interpolation = cv2.INTER_AREA).reshape(1,30,30,3))
            c_27 = np.argmax(pred_1[0,:], axis=-1)
            pred= model_v1(cv2.resize(cropped_img[10:-10,10:-10,:], (40,40), interpolation = cv2.INTER_AREA).reshape(1,40,40,3))
            c_id = np.argmax(pred[0,:], axis=-1)
            if(c_27==14)and(c_id==14):
                if(area>7500)and(area<15000):
                    if((ratio>1.45)and(ratio<1.7)):
                        c_27=14
                        c_id=14
                    else:
                        c_id = 0
                        c_27 = 0
                else:
                    c_id = 0
                    c_27 = 0      
                
        else:
            c_id = 0
            c_27 = 0
    else:
        c_id = 0
        c_27 = 0
    return c_id,c_27

