# -*- coding: utf-8 -*-
"""
Created on Tue May 31 07:19:09 2016

@author: Administrator

# This class is responsible for making a wafer object. Wafer objects should have feature methods, save method, and all return methods

img          a color (RGB) image of the object as a numpy array with dim (Width x Height x 3) 
props        a property object for the given image (in grayscale - no color info)
ID           a unique ID relative to the given image (not necessarily unique to database) 
waferscore   a representation of how likely the given image is displaying a wafer, 1.0 -> high chance wafer, 0.0 -> low chance
"""
from skimage.morphology import erosion
from skimage.morphology import square
import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage import exposure
from skimage.feature import peak_local_max
from skimage.feature import corner_shi_tomasi
from skimage import filters

class Wafer: 
    
    def __init__(self, bbox, properties, unique_ID, isWafer_training = None): 
        self.img = bbox
        self.props = properties 
        self.ID = unique_ID
        self.waferscore = float(1.0)
        self.isWafer = isWafer_training
        self.img_path = '\\\\192.168.8.2\\projects\\Nate\\wafer_stiched_images\\training_images\\' + str(unique_ID) + '.bmp'
        
    def toList(self):
        return [str(self.ID), str(self.isWafer), str(self.waferscore), self.img_path] + list(self.props)
        
    # normalized focus score - inaccuarate if image contains natural gradients
    def focus_score(self): 
        f_score = (color.rgb2grey(self.img) - erosion(color.rgb2grey(self.img), square(4)))
        non_zero_pixel_area = self.get_nonzero_pixel_area(f_score)
        #print("focus score: " + str(np.sum(f_score) / non_zero_pixel_area))
        #plt.imshow(f_score)
        #plt.show()
        return np.sum(f_score) / non_zero_pixel_area 
        
    # image passed must be a greyscale
        #ideally used for focus score normalization
    def get_nonzero_pixel_area(self, img): 
        count = 0   
        dim = img.shape
        for i in range(dim[0]):
            for n in range(dim[1]): 
                if (img[i][n] > 0): 
                    count = count + 1 
        return count

    # return the histogram mode of each color in the given image [R_mode, G_mode, B_mode]
    def get_hist_modes(self): 
        
        print('histogram')
        plt.hist(self.img[:][:][0] - self.img[:][:][1], bins = 256, range = [-255,255])
        plt.show()
        plt.hist(self.img[:][:][2] - self.img[:][:][0], bins = 256, range = [-255,255])
        plt.show()
        plt.hist(self.img[:][:][2] - self.img[:][:][1], bins = 256, range = [-255,255])
        plt.show()

    def get_corner_distances(self): 
        a = corner_shi_tomasi(color.rgb2grey(self.img))
#        val = filters.threshold_otsu(self.img)
#        mask = self.img < val 
#        a = peak_local_max(mask)
        print(a.shape)
        print(a)
        d1 = self.get_coord_dist(a[0], a[1])
        d2 = self.get_coord_dist(a[1], a[2])
        d3 = self.get_coord_dist(a[2], a[3])
        d4 = self.get_coord_dist(a[3], a[0])
        print('corner distances')
        print(d1)
        print(d2)
        print(d3)
        print(d4)
        print('std dev: ' + str(np.std([d1,d2,d3,4])))
        
        
    def get_coord_dist(self, coord_1, coord_2):
        x1 = coord_1[0]
        y1 = coord_1[1]
        
        x2 = coord_2[0]
        y2 = coord_2[1]
        
        dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        
        return dist
        
    def get_color(self): 
        r = np.average(self.img[:][:][0])
        g = np.average(self.img[:][:][1])
        b = np.average(self.img[:][:][2])
#        print('color means')
#        print(r)
#        print(g)
#        print(b)
        return r,g,b