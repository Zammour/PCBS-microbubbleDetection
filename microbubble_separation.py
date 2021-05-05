#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 21:31:57 2021

@author: zammour
"""

import numpy as np
from numpy.fft import fftn, fftshift, ifftn, ifftshift

def create_cone_filter(IQ, parameters, speed_range):
    
    f = parameters['frame_rate']
    fx = parameters['lateral_spatial_frequency']
    fz = parameters['depth_spatial_frequency']
    
    [x_length, z_length, t_length] = IQ.shape
    
    f_vector = np.linspace(-f/2, f/2, t_length)
    fx_vector = np.linspace(-fx/2, fx/2, x_length)
    fz_vector = np.linspace(-fz/2, fz/2, z_length)

    k_space = np.zeros((x_length, z_length))

    for i in range(x_length):
        for j in range(z_length):
            k_space[i,j] = np.sqrt(fx_vector[i]**2 + fz_vector[j]**2)
            
    low_pass_cone = np.zeros(IQ.shape)
    high_pass_cone = np.zeros(IQ.shape)

    for frame in range(t_length):
        low_pass_cone[:,:,frame] = k_space > abs(f_vector[frame])/speed_range[-1]
        high_pass_cone[:,:,frame] = k_space < abs(f_vector[frame])/speed_range[0]

    band_pass_cone = low_pass_cone * high_pass_cone

    return band_pass_cone



def cone_filter_separation(IQ, parameters):
    
    v_min = parameters['minimal_speed']
    v_max = parameters['maximal_speed']
    n_subsets = parameters['number_of_subsets']

    IQ_separated = np.zeros((IQ.shape +  tuple([n_subsets])), dtype=complex)
    
    speed_vector = np.linspace(v_min, v_max, n_subsets+2)
    
    fourier_domain = fftshift(fftn(IQ.astype(np.complex)))
    
    for subset in range(n_subsets):
        
        band_pass_cone_filter = create_cone_filter(IQ, parameters, speed_vector[subset:subset+2])
        
        IQ_separated[:,:,:,subset] = np.abs(ifftn(ifftshift(fourier_domain * band_pass_cone_filter)))
        
    return IQ_separated
        

"""
def cone_filter_separation(IQ, minimal_speed=1, maximal_speed=50, frame_rate=50, n_subsets = 7, lateral_FOV = (0,12), depth_FOV = (0,12)):
    
    [x_length, z_length, t_length] = IQ.shape
    
    IQ_separated = np.zeros((x_length, z_length, t_length, n_subsets), dtype=complex)
                                
    dx = (max(lateral_FOV)- min(lateral_FOV)) / x_length
    dz = (max(depth_FOV)- min(depth_FOV)) / z_length
    dt =  1/t_length/frame_rate
    
    x_spatial_frequency = np.linspace(-1/dx/2, 1/dx/2, x_length)
    z_spatial_frequency = np.linspace(-1/dz/2, 1/dz/2, z_length)
    time_frequency = np.linspace(-1/dt/2, 1/dt/2, t_length)
    
    
    k_space = np.zeros((x_length, z_length))
    
    for i in range(x_length):
        for j in range(z_length):
            k_space[i,j] = np.sqrt(x_spatial_frequency[i]**2 + z_spatial_frequency[j]**2)
       
    speed_vector = np.linspace(minimal_speed, maximal_speed, n_subsets+1)
    
    low_pass_cone = np.zeros(IQ.shape)
    high_pass_cone = np.zeros(IQ.shape)
    
    fourier_domain = fftshift(fftn(IQ.astype(np.complex)))
    
    for subset in range(n_subsets):
        for frame in range(t_length):
            low_pass_cone[:,:,frame] = k_space > abs(time_frequency[frame])/speed_vector[subset+1]/1.5
            high_pass_cone[:,:,frame] = k_space < abs(time_frequency[frame])/speed_vector[subset]/0.5
        
        band_pass_cone = low_pass_cone * high_pass_cone
        
        IQ_filtered = np.abs(ifftn(ifftshift(fourier_domain * band_pass_cone)))
        
        IQ_separated[:,:,:,subset] = IQ_filtered

    return IQ_separated

def orientation_separation(IQ, minimal_speed=1, maximal_speed=50, frame_rate=50, lateral_FOV = (0,12), depth_FOV = (0,12)):
    
    [x_length, z_length, t_length] = IQ.shape
    
    IQ_separated = np.zeros((x_length, z_length, t_length, 2), dtype=complex)
    
    fourier_domain = fftshift(fftn(IQ.astype(np.complex)))

    up = np.zeros(IQ.shape)
    up[:, 1:int(z_length/2), 1:int(t_length/2)] = 1
    up[:, int(z_length/2):, int(t_length/2):] = 1
    
    down = np.zeros(IQ.shape)
    down[:, 1:int(z_length/2), int(t_length/2):] = 1
    down[:, int(z_length/2):, 1:int(t_length/2)] = 1
    
    IQ_separated[:,:,:,0] = np.abs(ifftn(ifftshift(fourier_domain * up)))
    IQ_separated[:,:,:,1] = np.abs(ifftn(ifftshift(fourier_domain * down)))

    return IQ_separated
"""