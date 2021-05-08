# PCBS-microbubbleDetection

*The diffraction-limit has long represented an unreachable summit to conquer in ultrasound imaging. Within a few years after the introduction of optical localization microscopy, we proposed its acoustic alter-ego that exploits the micrometric localization of microbubble contrast agents to reconstruct the finest vessels in the body in-depth. [...] It has since been used in-vivo in the brain, the kidney and in tumors. In the clinic, ULM is bound to improve drastically our vision of the microvasculature, which could revolutionize the diagnosis of cancer, arteriosclerosis, stroke and diabetes, among others.*<br>
[*(O. Couture, M. Tanter et al., 2018)*](<https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8396283>)

<br><br><br>
<p align="center">
  <b>Rat brain</b>
  <br>
  <img width="460" height="300" src="https://github.com/Zammour/PCBS-microbubbleDetection/blob/main/Mice%20brain.gif">
  <br>
  <em> From (O. Couture, M. Tanter et al., 2018)</em>
</p>
<br><br><br>
  
Echography is widely used in the clinic to detect vessels by means of the well known Doppler-effect. We can increase considerably the images by injecting parenterally contrast agent that are microbubbles of gas. We can further increase the acquisition time in order to detect microvessels up to tens of µm.

In this project, we aim to model *in silico* vessels by simulating microbubble loclization as in [*D . Wilmes et al.*](<https://ieeexplore.ieee.org/document/9251643>). Then, we will try to separate the microbubbles depending on their speed to improve detection, as in [*C. Huang et al., 2020*](<https://www.nature.com/articles/s41598-020-62898-9>).


## How to use the program ?
  
### Parameters
 
All the parameters can be set up in the main_simulation.py file. Then, the instrucitons should be written in this file also. Finally, just run the file.

### Workflow
  1. Simulate microbubble positions using a simple or a complex model (see simulate_microbubble_position.py) and store x and y positions.
  2. Plot the trajectories (function : 'plot_microbubble_positions')
  3. Convert x & z positions to a movie (function : 'convert_positions_to_IQ')
  4. Show the movie ( function : 'show_IQ_movie')
  5. Entertain by varying parameters, or by filtering with the function 'cone_filter_separation' (see microbubble_separation.py)


## Results

### Simulation

<p align="center">
<b>Trajectories of 100 microbubbles</b>
  <br>
  <img width="361" height="279" src="https://github.com/Zammour/PCBS-microbubbleDetection/blob/main/Results/Trajectories.png" title="Trajectories of 100 microbubbles">
</p>

<br><br><br>

<p align="center">
<b>Movie of the trajectories</b>
  <br>
<video style="width:70%" controls>
  <source src="https://github.com/Zammour/PCBS-microbubbleDetection/blob/main/Results/High%20speed%20down.mp4">
</video>
</p>

https://github.com/Zammour/PCBS-microbubbleDetection/blob/main/Results/High%20speed%20down.mp4


https://user-images.githubusercontent.com/61946463/117534054-1be5f800-aff0-11eb-95d8-51eb3eb3ab1d.mp4
