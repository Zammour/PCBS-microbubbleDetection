#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 21:31:57 2021

@author: zammour
"""

import matplotlib.pyplot as plt

def plot_bubble_trajectories(x,z, parameters):

    lateral_FOV = parameters['lateral_field_of_view']
    depth_FOV = parameters['depth_field_of_view']

    plt.figure()
    
    for i in range(len(x)):
        plt.xlim(lateral_FOV[0], lateral_FOV[1])
        plt.ylim(depth_FOV[0], depth_FOV[1])
        plt.plot(x.iloc[i,:],z.iloc[i,:], marker='x')
        
def show_IQ_movie(IQ, parameters):
    plt.figure()
    for ii in range(IQ.shape[2]):
        plt.imshow(IQ[:,:,ii].real, cmap = 'gray')
        plt.title('Frame {}'.format(ii))
        plt.pause(1/parameters['frame_rate'])
