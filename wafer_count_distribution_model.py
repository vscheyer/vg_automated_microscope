# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:23:10 2016

@author: Administrator
"""

# This program is intended to model random sampling of a population (resevoir) of homogenous particles to give some indication on what are expected standard deviations should be for 
# multiple wafer manual counting. 

# Not totally sure where to start so this will need to be a evolution 
# the random seed we use might be what we're actually testing 

import random as r
import numpy as np
import matplotlib.pyplot as plt

def main() : 
    expected_val = int(input("Mean particle count: "))
    N = int(input("Number of iterations: "))

    sample_count = expected_val * 2 
    d = create_distribution(N, sample_count)
    print("Standard Deviation: " + str(np.std(d)))
    plt.hist(d)
    plt.show()
    
    std_ls = [0]*200
    for i, x in enumerate(std_ls) :  
        s = np.std(create_distribution(200, i+1))
        std_ls[i] = s
        
    plt.plot(std_ls, 'ro')    
    
    t = range(0,200) 
    ts = list(map(lambda x: np.sqrt(x/2), t))
    ts2 = list(map(lambda x: np.sqrt(x/3), t))
    ts3 = list(map(lambda x: np.sqrt(x/4), t))
    ts4 = list(map(lambda x: np.sqrt(x/6), t))
    
    plt.plot(ts4,'b-')
    plt.plot(ts3,'b-')
    plt.plot(ts2,'b-')
    plt.plot(ts,'b-')    
    plt.show()
    
def take_sample() : 
    x = r.random() 
    if (x < .5) : 
        return True 
    else : 
        return False 
        
def count_particles(num_draws) : 
    count = 0
    for i in range(0, num_draws) : 
        if (take_sample()) : 
            count = count + 1 
    return count
    
def create_distribution(N, num_draws) : 
    dist = [0] * N 
    for i,val in enumerate(dist) : 
        val = count_particles(num_draws)
        dist[i] = val
    return dist

# execute 
main()
