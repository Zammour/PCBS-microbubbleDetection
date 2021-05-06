#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The model of microbubble flow in the vessels comes from "Tracking of Microbubbles with a Recurrent Neural Network for Super-Resolution Imaging", (D. Wilmes et al., 2020).
The simple model assumes that the bubbles have a constant and relatively small curvature radius. Therefore, the vessels are almost circles.
To be more realistic, the authors propsoed to vary randomly the curvature radius, in order to have more tortuous vessels. This is the complex model.

NB: x and z refer to the positions of the microbubbles respectively on x-axis and z-axis. phi is the angle of the movement of the bubble.


Created on Wed Apr 14 11:55:15 2021

@author: zammour
"""

import numpy as np
import pandas as pd

def simulate_motion_simple(p):
    
    # Initialization
    
    x = pd.DataFrame(np.zeros((p.number_of_bubbles, p.number_of_frames)))
    z = pd.DataFrame(np.zeros((p.number_of_bubbles, p.number_of_frames)))
    phi = pd.DataFrame(np.zeros((p.number_of_bubbles, p.number_of_frames)))
    
    x.iloc[:, 0] = np.random.uniform(p.lateral_field_of_view[0],
                                     p.lateral_field_of_view[1],
                                     p.number_of_bubbles)
    z.iloc[:, 0] = np.random.uniform(p.depth_field_of_view[0],
                                     p.depth_field_of_view[1],
                                     p.number_of_bubbles)
    phi.iloc[:, 0] = np.random.uniform(0,
                                       2 * np.pi,
                                       p.number_of_bubbles)
    
    turning_rate = np.random.uniform(p.minimal_turning_rate,
                                     p.maximal_turning_rate,
                                     p.number_of_bubbles)
    flow_velocity = np.random.uniform(p.minimal_speed,
                                      p.maximal_speed,
                                      p.number_of_bubbles)
    curvature_radius = flow_velocity / turning_rate


    
    # Simulation
    
    for i in range(1, p.number_of_frames): 
        x.iloc[:,i] = x.iloc[:, i-1] + curvature_radius * (np.sin(phi.iloc[:, i-1]) - np.sin(phi.iloc[:, i-1] + turning_rate / p.frame_rate))
        z.iloc[:,i] = z.iloc[:, i-1] + curvature_radius * ( - np.cos(phi.iloc[:, i-1]) + np.cos(phi.iloc[:, i-1] + turning_rate / p.frame_rate))
        phi.iloc[:,i] = phi.iloc[:, i-1] + turning_rate / p.frame_rate
        
    # Adding noise
    
    x_inaccuracy = np.random.normal(0, 5e-3, (p.number_of_bubbles, p.number_of_frames))
    z_inaccuracy = np.random.normal(0, 5e-3, (p.number_of_bubbles, p.number_of_frames))

    x += x_inaccuracy
    z += z_inaccuracy
        
    return x, z

def simulate_motion_complex(p):
    
    # Initilization
    
    x = pd.DataFrame(np.zeros((p.number_of_bubbles, p.number_of_frames)))
    z = pd.DataFrame(np.zeros((p.number_of_bubbles, p.number_of_frames)))
    phi = pd.DataFrame(np.zeros((p.number_of_bubbles, p.number_of_frames)))
    
    x.iloc[:, 0] = np.random.uniform(p.lateral_field_of_view[0],
                                    p.lateral_field_of_view[1],
                                    p.number_of_bubbles)
    z.iloc[:, 0] = np.random.uniform(p.depth_field_of_view[0],
                                    p.depth_field_of_view[1],
                                    p.number_of_bubbles)
    phi.iloc[:, 0] = np.random.uniform(0,
                                      2 * np.pi,
                                      p.number_of_bubbles)
    
    turning_rate = np.random.uniform(p.minimal_turning_rate,
                                     p.maximal_turning_rate,
                                     (p.number_of_bubbles, p.number_of_frames))
    flow_velocity = np.repeat(np.random.uniform(p.minimal_speed,
                                                p.maximal_speed,
                                                p.number_of_bubbles),
                              p.number_of_frames).reshape((p.number_of_bubbles, p.number_of_frames))
    curvature_radius = flow_velocity / turning_rate


    # Simulation
    
    for i in range(1, p.number_of_frames):
        x.iloc[:, i] = x.iloc[:, i-1] + curvature_radius[:, i] * (np.sin(phi.iloc[:, i-1]) - np.sin(phi.iloc[:, i-1] + turning_rate[:, i] / p.frame_rate))
        z.iloc[:, i] = z.iloc[:, i-1] + curvature_radius[:, i] * ( - np.cos(phi.iloc[:, i-1]) + np.cos(phi.iloc[:, i-1] + turning_rate[:, i] / p.frame_rate))
        phi.iloc[:, i] = phi.iloc[:, i-1] + turning_rate[:, i] / p.frame_rate
        
    # Adding noise
    
    x_inaccuracy = np.random.normal(0, 5e-3, (p.number_of_bubbles, p.number_of_frames))
    z_inaccuracy = np.random.normal(0, 5e-3, (p.number_of_bubbles, p.number_of_frames))
    x += x_inaccuracy
    z += z_inaccuracy
        
    return x, z



def convert_position_to_IQ(x, z, p):
    
    # Initialization
    
    IQ = np.zeros((int((p.lateral_field_of_view[1] - p.lateral_field_of_view[0]) * p.lateral_spatial_frequency), int((p.depth_field_of_view[1] - p.depth_field_of_view[0]) * p.depth_spatial_frequency), p.number_of_frames))
        
    # Conversion
    
    for frame in range(p.number_of_frames):
        for bubble in range(p.number_of_bubbles):
            x_index = int(x.iloc[bubble, frame] * p.lateral_spatial_frequency)
            z_index = int(z.iloc[bubble, frame] * p.depth_spatial_frequency)
            if (x_index <= IQ.shape[0] - 1) and (x_index >= 0) and (z_index <= IQ.shape[1] - 1) and (z_index >= 0):
    
                IQ[x_index:x_index + 2, z_index:z_index + 2, frame] = 1

    # Adding noise

    background_noise = np.random.normal(0, 0.1, IQ.shape)                
    IQ += background_noise    
    
    return IQ
