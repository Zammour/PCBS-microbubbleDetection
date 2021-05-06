#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main module where to use the program.
We can set up the parameters.
Then we can start the simulation.

If you don't want to rack your brain with the parameters, I already choosed some good ones. You can just run the script.


Created on Sat Feb 20 21:31:57 2021

@author: zammour
"""

import numpy as np
import pandas as pd
import vizualisation as viz
import simulate_microbubble_positions as smp
import microbubble_separation as ms

parameters = pd.Series({
    
    # Motion simulation settings
    
    'number_of_bubbles' : 100,
    'number_of_frames' : 10,
    'frame_rate' : 1000, # in Hz
    'lateral_field_of_view' : (0, 12), # in mm
    'depth_field_of_view' : (0, 12), # in mm
    'minimal_turning_rate' : -100 * np.pi, # in rad/s
    'maximal_turning_rate' : 100 * np.pi, # in rad/s
    
    # Vizualisation settings
    
    'lateral_spatial_frequency' : 11, # in mm^-1
    'depth_spatial_frequency' : 10, # in mm^-1
    
    # Cone filter settings
    
    'minimal_speed' : 1, # in mm/s
    'maximal_speed' : 250, # in mm/s
    'number_of_subsets' : 3
    
    })


### Start simulation ###

x, z = smp.simulate_motion_complex(parameters)

IQ = smp.convert_position_to_IQ(x, z, parameters)

viz.plot_bubble_trajectories(x, z, parameters)

IQ_sep = ms.cone_filter_separation(IQ, parameters)

viz.show_IQ_movie(IQ, parameters, 'Reference')
viz.show_IQ_movie(IQ_sep[:, :, :, 0], parameters, 'Low speed to up')
viz.show_IQ_movie(IQ_sep[:, :, :, 2], parameters, 'High speed to up')
viz.show_IQ_movie(IQ_sep[:, :, :, 3], parameters, 'Low speed to down')
viz.show_IQ_movie(IQ_sep[:, :, :, 5], parameters, 'High speed to down')
