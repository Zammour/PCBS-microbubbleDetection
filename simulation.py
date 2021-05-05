#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 21:31:57 2021

@author: zammour
"""

import numpy as np
import vizualisation
import simulate_microbubble_positions
import microbubble_separation


parameters = {}

# Motion simulation settings

parameters['number_of_bubbles'] = 25
parameters['number_of_frames'] = 10
parameters['frame_rate'] = 1000 # in Hz
parameters['lateral_field_of_view'] = (-6,6) # in mm
parameters['depth_field_of_view'] = (0,12) # in mm
parameters['minimal_turning_rate'] = -100*np.pi # in rad/s
parameters['maximal_turning_rate'] = 100*np.pi # in rad/s

# Vizualisation settings

parameters['lateral_spatial_frequency'] = 11 # in mm^-1
parameters['depth_spatial_frequency'] = 10 # in mm^-1

# Cone filter settings

parameters['minimal_speed'] = 1 # in mm/s
parameters['maximal_speed'] = 300 # in mm/s
parameters['number_of_subsets'] = 3


### Start simulation ###

x, z = simulate_microbubble_positions.simulate_motion_complex(parameters)

IQ = simulate_microbubble_positions.convert_position_to_IQ(x, z, parameters)

vizualisation.plot_bubble_trajectories(x,z, parameters)

vizualisation.show_IQ_movie(IQ, parameters)

IQ_sep = microbubble_separation.cone_filter_separation(IQ, parameters)

vizualisation.show_IQ_movie(IQ_sep[:,:,:,0], parameters)
vizualisation.show_IQ_movie(IQ_sep[:,:,:,-1], parameters)


