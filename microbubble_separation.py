#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'IQ' stands for In-phase-in-Quadrature, that comes from the signals (that are complex numbers) recorded using ultrasound devices.
Herre, we will only take the real part of the signal. Therefore, here, 'IQ' is equivalent to an ultrasound movie.

The present module filters the IQ data according to "Short Acquisition time Super- Resolution Ultrasound Microvessel imaging via Microbubble Separation" (C. Huang et al. 2020).
Without entering in the detailed maths of the method, the authors used 3D spatio-temporalal filtering in the fourier domain. To isolate a specific speed in the IQ movies, they used oriented 3D cone filters.
This allows to separate microbubbles depending on the speed and the orientation.
In clinics this technique would be very useful when we have a lot of microbubbles that overlap so that can't be detected.

Created on Sat Feb 20 21:31:57 2021

@author: zammour
"""

import numpy as np
from numpy.fft import fftn, fftshift, ifftn, ifftshift

def create_cone_filter(IQ, p, speed_range):
        
    [x_length, z_length, t_length] = IQ.shape
    
    f_vector = np.linspace( - p.frame_rate / 2, p.frame_rate / 2, t_length)
    fx_vector = np.linspace( - p.lateral_spatial_frequency / 2, p.lateral_spatial_frequency / 2, x_length)
    fz_vector = np.linspace( - p.depth_spatial_frequency / 2, p.depth_spatial_frequency / 2, z_length)

    k_space = np.zeros((x_length, z_length))
    for i in range(x_length):
        for j in range(z_length): 
            k_space[i, j] = np.sqrt(fx_vector[i] ** 2 + fz_vector[j] ** 2)
            
    low_pass_cone = np.zeros(IQ.shape)
    high_pass_cone = np.zeros(IQ.shape)

    for frame in range(t_length):
        low_pass_cone[:, :, frame] = k_space > abs(f_vector[frame]) / speed_range[-1]
        high_pass_cone[:, :, frame] = k_space < abs(f_vector[frame]) / speed_range[0]

    band_pass_cone = low_pass_cone * high_pass_cone

    return band_pass_cone


def create_orientation_filter(IQ):
        
    [x_length, z_length, t_length] = IQ.shape
    
    up_filter = np.zeros(IQ.shape)
    up_filter[:, 1:int(z_length / 2), 1:int(t_length / 2)] = 1
    up_filter[:, int(z_length / 2):, int(t_length / 2):] = 1
    
    down_filter = np.zeros(IQ.shape)
    down_filter[:, 1:int(z_length / 2), int(t_length / 2):] = 1
    down_filter[:, int(z_length / 2):, 1:int(t_length / 2)] = 1
    
    return up_filter, down_filter 


def cone_filter_separation(IQ, p):
    
    IQ_separated = np.zeros((IQ.shape +  tuple([2 * p.number_of_subsets])), dtype=complex)
    
    speed_vector = np.linspace(p.minimal_speed, p.maximal_speed, p.number_of_subsets+2)
    
    fourier_domain = fftshift(fftn(IQ.astype(np.complex)))
    
    up_filter, down_filter = create_orientation_filter(IQ)
    
    for subset in range(p.number_of_subsets):
                
        band_pass_cone_filter = create_cone_filter(IQ, p, speed_vector[subset:subset + 2])
        
        IQ_separated[:, :, :, subset] = np.abs(ifftn(ifftshift(fourier_domain * band_pass_cone_filter * up_filter)))
        IQ_separated[:, :, :, subset + p.number_of_subsets] = np.abs(ifftn(ifftshift(fourier_domain * band_pass_cone_filter * down_filter)))

        
    return IQ_separated