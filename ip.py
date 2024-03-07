#!/usr/bin/env python
# coding: utf-8

# In[8]:


def ip_finder():
    import cv2
    from tqdm import tqdm
    cv2.CAP_PROP_OPEN_TIMEOUT_MSEC=3
    cv2.CAP_PROP_READ_TIMEOUT_MSEC=3
    for i in tqdm(range(1,7)):
        try:
            URL = "http://192.168.1."+str(i)
            cap = cv2.VideoCapture(URL + ":81/stream")
            if (cap.isOpened()):
                ip = "http://192.168.1."+str(i)
                print("Your ip is: "+ip)
                return ip 
                break
        except:
            pass

