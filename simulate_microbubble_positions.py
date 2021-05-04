#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:55:15 2021

@author: zammour
"""

import numpy as np
import pandas as pd

def simulate_motion_simple(parameters):
    
    n_bubbles = parameters['number_of_bubbles']
    n_frame = parameters['number_of_frames']
    f = parameters['frame_rate']
    omega_min = parameters['minimal_turning_rate']
    omega_max = parameters['maximal_turning_rate']
    v_min = parameters['minimal_speed']
    v_max = parameters['maximal_speed']
    lateral_FOV = parameters['lateral_field_of_view']
    depth_FOV = parameters['depth_field_of_view']
    
    x = pd.DataFrame(np.zeros((n_bubbles,n_frame)))
    z = pd.DataFrame(np.zeros((n_bubbles,n_frame)))
    phi = pd.DataFrame(np.zeros((n_bubbles,n_frame)))
    
    turning_rate = np.random.uniform(omega_min, omega_max, n_bubbles)
    flow_velocity = np.random.uniform(v_min, v_max, n_bubbles)
    curvature_radius = flow_velocity / turning_rate

    x.iloc[:,0] = np.random.uniform(lateral_FOV[0],lateral_FOV[1],n_bubbles)
    z.iloc[:,0] = np.random.uniform(depth_FOV[0],depth_FOV[1],n_bubbles)
    phi.iloc[:,0] = np.random.uniform(0, 2*np.pi, n_bubbles)
    
    for i in range(1,n_frame):
        x.iloc[:,i] = x.iloc[:,i-1] + curvature_radius*(np.sin(phi.iloc[:,i-1]) - np.sin(phi.iloc[:,i-1] + turning_rate/f))
        z.iloc[:,i] = z.iloc[:,i-1] + curvature_radius*(-np.cos(phi.iloc[:,i-1]) + np.cos(phi.iloc[:,i-1] + turning_rate/f))
        phi.iloc[:,i] = phi.iloc[:,i-1] + turning_rate/f
        
    x_inaccuracy = np.random.normal(0, 5e-3, (n_bubbles, n_frame))
    z_inaccuracy = np.random.normal(0, 5e-3, (n_bubbles, n_frame))

    x += x_inaccuracy
    z += z_inaccuracy
        
    return x, z


def simulate_motion_complex(parameters):
    
    n_bubbles = parameters['number_of_bubbles']
    n_frame = parameters['number_of_frames']
    f = parameters['frame_rate']
    omega_min = parameters['minimal_turning_rate']
    omega_max = parameters['maximal_turning_rate']
    v_min = parameters['minimal_speed']
    v_max = parameters['maximal_speed']
    lateral_FOV = parameters['lateral_field_of_view']
    depth_FOV = parameters['depth_field_of_view']
    
    x = pd.DataFrame(np.zeros((n_bubbles,n_frame)))
    z = pd.DataFrame(np.zeros((n_bubbles,n_frame)))
    phi = pd.DataFrame(np.zeros((n_bubbles,n_frame)))
    
    turning_rate = np.random.uniform(omega_min, omega_max, (n_bubbles, n_frame))
    flow_velocity = np.repeat(np.random.uniform(v_min,v_max, n_bubbles), n_frame).reshape((n_bubbles,n_frame))
    curvature_radius = flow_velocity / turning_rate

    x.iloc[:,0] = np.random.uniform(lateral_FOV[0],lateral_FOV[1],n_bubbles)
    z.iloc[:,0] = np.random.uniform(depth_FOV[0],depth_FOV[1],n_bubbles)
    phi.iloc[:,0] = np.random.uniform(0, 2*np.pi, n_bubbles)
    
    for i in range(1,n_frame):
        x.iloc[:,i] = x.iloc[:,i-1] + curvature_radius[:,i]*(np.sin(phi.iloc[:,i-1]) - np.sin(phi.iloc[:,i-1] + turning_rate[:,i]/f))
        z.iloc[:,i] = z.iloc[:,i-1] + curvature_radius[:,i]*(-np.cos(phi.iloc[:,i-1]) + np.cos(phi.iloc[:,i-1] + turning_rate[:,i]/f))
        phi.iloc[:,i] = phi.iloc[:,i-1] + turning_rate[:,i]/f
        
    x_inaccuracy = np.random.normal(0, 5e-3, (n_bubbles, n_frame))
    z_inaccuracy = np.random.normal(0, 5e-3, (n_bubbles, n_frame))

    x += x_inaccuracy
    z += z_inaccuracy

    return x, z

def convert_position_to_IQ(x, z, parameters):
    
    n_bubbles = parameters['number_of_bubbles']
    n_frames = parameters['number_of_frames']
    fx = parameters['lateral_spatial_frequency']
    fz = parameters['depth_spatial_frequency']
    lateral_FOV = parameters['lateral_field_of_view']
    depth_FOV = parameters['depth_field_of_view']
    
    model = np.zeros((int(max(lateral_FOV) - min(lateral_FOV))*fx , int(max(depth_FOV)-min(depth_FOV))*fz, n_frames))
    
    background_noise = np.random.normal(0, 0.1, model.shape)
    
    for frame in range(n_frames):
        for bubble in range(n_bubbles):
            x_index = int(x.iloc[bubble,frame]*fx)
            z_index = int(z.iloc[bubble,frame]*fz)
            if (x_index <= model.shape[0]-1) and (x_index >= 0) and (z_index <= model.shape[1]-1) and (z_index >= 0):
        
                model[x_index:x_index+2, z_index:z_index+2,frame] = 1
        
    return model + background_noise