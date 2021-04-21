#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:55:15 2021

@author: zammour
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def simulate_motion_simple(number_bubbles=25, number_frame=10, frame_rate = 50, lateral_field_of_view = (-6,6), depth_field_of_view = (0,12)):
    
    x = pd.DataFrame(np.zeros((number_bubbles,number_frame)))
    z = pd.DataFrame(np.zeros((number_bubbles,number_frame)))
    phi = pd.DataFrame(np.zeros((number_bubbles,number_frame)))
    
    turning_rate = np.random.uniform(-10, 10, number_bubbles)
    curvature_radius = np.random.uniform(1,5,number_bubbles)
    flow_velocity = turning_rate * curvature_radius

    x.iloc[:,0] = np.random.uniform(lateral_field_of_view[0],lateral_field_of_view[1],number_bubbles)
    z.iloc[:,0] = np.random.uniform(depth_field_of_view[0],depth_field_of_view[1],number_bubbles)
    
    for i in range(1,number_frame):
        x.iloc[:,i] = x.iloc[:,i-1] + curvature_radius*(np.sin(phi.iloc[:,i-1]) - np.sin(phi.iloc[:,i-1] + turning_rate/frame_rate))
        z.iloc[:,i] = z.iloc[:,i-1] + curvature_radius*(-np.cos(phi.iloc[:,i-1]) + np.cos(phi.iloc[:,i-1] + turning_rate/frame_rate))
        phi.iloc[:,i] = phi.iloc[:,i-1] + turning_rate/frame_rate
        
    return x, z


def simulate_motion_complex(number_bubbles=50, number_frame=8, frame_rate = 50, lateral_field_of_view = (0,12), depth_field_of_view = (0,12)):
    
    np.random.seed(0)
    
    x = pd.DataFrame(np.zeros((number_bubbles,number_frame)))
    z = pd.DataFrame(np.zeros((number_bubbles,number_frame)))
    phi = pd.DataFrame(np.zeros((number_bubbles,number_frame)))
    
    turning_rate = pd.DataFrame(np.random.uniform(-50, 50, size=(number_bubbles,number_frame)))
    flow_velocity = np.repeat(np.random.uniform(1,50,number_bubbles), number_frame).reshape((number_bubbles,number_frame))
    curvature_radius = flow_velocity/turning_rate

    x.iloc[:,0] = np.random.uniform(lateral_field_of_view[0],lateral_field_of_view[1],number_bubbles)
    z.iloc[:,0] = np.random.uniform(depth_field_of_view[0],depth_field_of_view[1],number_bubbles)
    
    for i in range(1,number_frame):
        x.iloc[:,i] = x.iloc[:,i-1] + curvature_radius.iloc[:,i]*(np.sin(phi.iloc[:,i-1]) - np.sin(phi.iloc[:,i-1] + turning_rate.iloc[:,i]/frame_rate))
        z.iloc[:,i] = z.iloc[:,i-1] + curvature_radius.iloc[:,i]*(-np.cos(phi.iloc[:,i-1]) + np.cos(phi.iloc[:,i-1] + turning_rate.iloc[:,i]/frame_rate))
        phi.iloc[:,i] = phi.iloc[:,i-1] + turning_rate.iloc[:,i]/frame_rate
        
    return x, z