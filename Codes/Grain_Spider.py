# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:09:17 2023

@author: mario
"""

import cv2 
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io, color, measure

image = cv2.imread('../LFP_PÓ_TIFF/10k_2.tiff', 0)
pixels_to = 0.5
plt.hist(image.flat, bins= 100, range=(0,255))
ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
kernel = np.ones((3,3), np.uint8)
eroded = cv2.erode(thresh, kernel, iterations = 1)
dilated = cv2.dilate(eroded, kernel, iterations = 1)
cv2.imshow("Dilated Image", dilated)
