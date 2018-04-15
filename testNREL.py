# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 08:36:26 2018

@author: pragathi
"""

import cv2
import glob, os
import cloudOpticalFlow

def getNRELImages(dir_, type_):
    color_imgs = []
    os.chdir(dir_)
    for file in glob.glob(type_):
        img = cv2.imread(file,1)
        color_imgs.append(img)
        
    return color_imgs

def main():
    imgs = getNRELImages("20180408/", "*_11.jpg")
    prev = imgs[0]
    for i in range(1,len(imgs)):
        curr = imgs[i]
        cloudOpticalFlow.opticalFlow(prev, curr, vis=True)
        prev = curr
        
if __name__ == "__main__":
    main()
