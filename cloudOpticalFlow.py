# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 08:29:37 2018

@author: pragathi
"""

import numpy as np
import cv2
import warnings

warnings.simplefilter("ignore")

def opticalFlow(img1, img2, vis=False):
    prev = processImage(img1)
    curr = processImage(img2)
    flow = cv2.calcOpticalFlowFarneback(prev,curr, None, 0.5, 7, 15, 5, 7, 1.5, 0)
    #(np.sum(np.square(flow[..., 0])+np.square(flow[..., 1])))
        
    if vis:
        horz = cv2.normalize(flow[..., 0], None, 0, 255, cv2.NORM_MINMAX)
        vert = cv2.normalize(flow[..., 1], None, 0, 255, cv2.NORM_MINMAX)
        horz = horz.astype('uint8')
        vert = vert.astype('uint8')                
        cv2.imshow('Horizontal Component', cv2.resize(horz, (0,0), fx=0.4, fy=0.4) )
        cv2.imshow('Vertical Component', cv2.resize(vert, (0,0), fx=0.4, fy=0.4) )
        cv2.imshow('Image', cv2.resize(img2, (0,0), fx=0.3, fy=0.3) )
        cv2.waitKey(10) & 0xff
        
    return flow

def processImage(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        
    candidate_indices1 = gray_img < 30
    ratio = img[:, :, 2]/img[:, :, 0]
    candidate_indices2 = ratio < 0.7
    cloud_indices = np.logical_or(candidate_indices1,candidate_indices2)
    ratio[cloud_indices] = 0        
    ratio = cv2.erode(ratio, None, iterations=2)
    ratio = cv2.dilate(ratio, None, iterations=2)
    processed_img = (ratio*255)
        
    return processed_img