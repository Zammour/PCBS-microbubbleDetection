#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 21:31:57 2021

@author: zammour
"""

import matplotlib.pyplot as plt

def plot_bubble_trajectories(x, z, p):

    plt.figure()
    
    # Plot the trajectories until last 2 frames
    
    for i in range(p.number_of_bubbles - 2):
        plt.xlim(p.lateral_field_of_view[0], p.lateral_field_of_view[1])
        plt.ylim(p.depth_field_of_view[0], p.depth_field_of_view[1])
        plt.plot(x.iloc[i, :-1],z.iloc[i, :-1], marker='')
        plt.gca().invert_yaxis()

    # Plot an arrow corresponding to the last two frames to see the orientation of the movement

    for j in range(p.number_of_bubbles):
        plt.arrow(x.iloc[j, p.number_of_frames - 2],
                  z.iloc[j, p.number_of_frames - 2],
                  x.iloc[j, p.number_of_frames - 1] - x.iloc[j, p.number_of_frames - 2],
                  z.iloc[j, p.number_of_frames - 1]-z.iloc[j, p.number_of_frames - 2],
                  head_width = 0.1)
        
def show_IQ_movie(IQ, p, title = None):
    
    plt.figure()
    
    for ii in range(IQ.shape[2]):
    
        plt.imshow(IQ[:, :, ii].T.real, cmap = 'gray')
        plot_title = '\nFrame {}'.format(ii)
        if type(title) == str: plot_title = title + plot_title
        plt.title(plot_title)
        plt.pause(1 / p.frame_rate)
