# -*- coding: utf-8 -*-
"""
Created on Fri May 27 16:24:29 2016

@author: Administrator
"""

import sys
sys.path.append('\\\\192.168.8.2\\projects\\Nate\\Python')

from scipy import misc
import matplotlib.pyplot as plt
import time
import os.path
import numpy as np
from skimage import filters
from skimage import measure 
from skimage import color
from scipy import stats
import Wafer
import csv

def main(): 
#    #usr_in = input("use full image? (y/n) ")
#    usr_in = 'n'
#    if (usr_in == 'y' or usr_in == 'Y'): 
#        start_time = time.clock()
#        img = misc.imread('\\\\192.168.8.2\\projects\\Nate\\wafer_stiched_images\\283 1.bmp')
#        img_load_time = time.clock()
#    else: 
#        start_time = time.clock()
#        if ( not os.path.isfile('\\\\192.168.8.2\\projects\\Nate\\wafer_stiched_images\\chunks\\img_0.bmp')): 
#            print("Loading full size image")
#            img = misc.imread('\\\\192.168.8.2\\projects\\Nate\\wafer_stiched_images\\283 1.bmp')
#            img_load_time = time.clock() - start_time
#            
#            img2 = img[10000:15000,10000:15000] # take a sample image from the center to test the alg on first -- 5000 x 5000 pixels
#            misc.imsave('\\\\192.168.8.2\\projects\\Nate\\wafer_stiched_images\\test_image_1.bmp', img2)
#            del(img)
#            img = img2
#        else: 
#            print("Loading cropped image")
#            img = misc.imread('\\\\192.168.8.2\\projects\\Nate\\wafer_stiched_images\\test_image_1.bmp')
#            img_load_time = time.clock() - start_time
    wafer_list = []
    
    convex_area_t = []
    euler_number_t = []
    extent_t = []
    filled_area_t = []
    perimeter_t= []
    solidity_t = []
    focus_score_t = []
    convex_area_f = []
    euler_number_f = []
    extent_f = []
    filled_area_f =[]
    perimeter_f = []
    solidity_f = []
    focus_score_f = []
    mean_r_t = []
    mean_g_t = []
    mean_b_t = []
    mean_r_f = []
    mean_g_f = []
    mean_b_f = []
    
    for i in range(0,9): 

        img = misc.imread('\\\\192.168.8.2\\projects\\Nate\\wafer_stiched_images\\chunks_3\\img_' + str(i) + '.bmp')
     
        val = filters.threshold_otsu(img)
        mask = img < val 

    
        blob_labels = measure.label(color.rgb2grey(mask), background = 0, return_num = False)
        #print(blob_labels.ndim)
    
        #plt.imshow(blob_labels)
        #plt.show()
        
        properties = measure.regionprops(blob_labels)
    
        print("Total number of objects before area filter: " + str(len(properties)))

        #--------------------------------- basic obj rejection based on object areas --------------
#        wafer_area_max = 600 
#        wafer_area_min = 225  
        padding = 5
        
        
        for i,obj_prop in enumerate(properties): 
            if (obj_prop.area > 225 and obj_prop.area < 600 
                and obj_prop. solidity >  0.8
                and obj_prop. perimeter > 50 and obj_prop. perimeter < 125 
                and obj_prop. filled_area < 450
                and obj_prop. extent > 0.6 
                and obj_prop. convex_area < 500): 
                bbox = obj_prop.bbox
                waf = img[bbox[0] : bbox[2], bbox[1] : bbox[3]]
                w = Wafer.Wafer(waf, obj_prop, i, False)
                r,g,b = w.get_color()
                if ((r - g) > 10
                    and (b - r) < -20 
                    and (g - b) > 5):
                    waf_show = img[bbox[0] - padding : bbox[2] + padding, bbox[1] - padding : bbox[3] + padding]
                    plt.imshow(waf_show)
                    plt.show()
                    #in1 = input("is this a wafer? (y/n) ")
                    in1 = 'y'
                    if (in1 == 'y'): 
                        w.isWafer = True
    
                    wafer_list.append(w)
                    #w.focus_score()
                    #w.get_color()
                
                    #w.get_corner_distances()
                    
                    #w.get_hist_modes()
                    
                

    
        for w in wafer_list: 
            if(w.isWafer): 
                convex_area_t.append(w.props['convex_area'])
                euler_number_t.append( w.props['euler_number'])
                extent_t.append(w.props['extent'])
                filled_area_t.append(w.props['filled_area'])
                #mean_intensity_t = w.props['mean_intensity']
                perimeter_t.append(w.props['perimeter'])
                solidity_t.append(w.props['solidity'])
                focus_score_t.append(w.focus_score())
                r,g,b = w.get_color()
                mean_r_t.append(r)
                mean_g_t.append(g)
                mean_b_t.append(b)
                
            else: 
                convex_area_f.append(w.props['convex_area'])
                euler_number_f.append(w.props['euler_number'])
                extent_f.append(w.props['extent'])
                filled_area_f.append(w.props['filled_area'])
                #mean_intensity_f = w.props['mean_intensity']
                perimeter_f.append(w.props['perimeter'])
                solidity_f.append(w.props['solidity'])
                focus_score_f.append(w.focus_score())
                r,g,b = w.get_color()
                mean_r_f.append(r)
                mean_g_f.append(g)
                mean_b_f.append(b)      

             

        
#        print("Time to load image: " + str(img_load_time))
#        print("Total time elapsed: " + str(end_time))
    
    print("Total wafer count: " + str(len(wafer_list)))
    print('convex area')
    plt.plot(convex_area_t, 'r.')
    plt.plot(convex_area_f, 'b.')
    plt.show()
    print('euler_number')
    plt.plot(euler_number_t, 'r.')
    plt.plot(euler_number_f, 'b.')
    plt.show()
    print('extent')
    plt.plot(extent_t, 'r.')
    plt.plot(extent_f, 'b.')
    plt.show()
    print('filled_area')
    plt.plot(filled_area_t, 'r.')
    plt.plot(filled_area_f, 'b.')
    plt.show()
    
#    plt.plot(mean_intensity_t, 'r')
#    plt.plot(mean_intensity_f, 'b')
#    plt.show()
    print('perimeter')
    plt.plot(perimeter_t, 'r.')
    plt.plot(perimeter_f, 'b.')
    plt.show()
    print('solidity')
    plt.plot(solidity_t, 'r.')
    plt.plot(solidity_f, 'b.')
    plt.show()
    print('focus score')
    plt.plot(focus_score_t,'r.')
    plt.plot(focus_score_f,'b.')
    plt.show()
    
    print('experimental combination')
    names = ['convex area', 'euler number', 'extent', 'filled area', 'perimeter', 'solidity', 'focus score']
    ls_t = [convex_area_t, euler_number_t, extent_t, filled_area_t, perimeter_t, solidity_t, focus_score_t]
    ls_f = [convex_area_f, euler_number_f, extent_f, filled_area_f, perimeter_f, solidity_f, focus_score_f]    
    
    for t,f,n in zip(ls_t,ls_f,names): 
        for t2,f2,n2 in zip(ls_t, ls_f,names):
            print(n + " vs " + n2)
            plt.plot(t, t2, 'r.')
            plt.plot(f, f2, 'b.')
            plt.show()
        
            
    names = ['red' , 'blue' , 'green']
    ls_t = [mean_r_t, mean_b_t, mean_g_t]
    ls_f = [mean_r_f, mean_b_f, mean_g_f]
    
    for t,f,n in zip(ls_t,ls_f,names): 
        print(n)
        plt.plot(t, 'r.')
        plt.plot(f, 'b.')
        plt.show()
        for t2,f2,n2 in zip(ls_t, ls_f,names):
            print(n + " vs " + n2)
            plt.plot(t, t2, 'r.')
            plt.plot(f, f2, 'b.')
            plt.show()
            print(n + ' minus ' + n2)
            plt.plot(np.subtract(t,t2),'r.')
            plt.plot(np.subtract(f,f2),'b.')
            plt.show()
    print("Total wafer count: " + str(len(list(filter(lambda x : x.isWafer, wafer_list)))))

start = time.clock()
main()
print("Time elapsed: " + str(time.clock() - start))
        