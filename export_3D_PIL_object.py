'''
This module output a 3D data (3D numpy matrix or a list of 2D frames) to a list of PIL.Image objects
'''
import numpy as np
from PIL import Image

def convert_3D_frames_to_image(Data_3d):
    # Data_3d can be either a numpy instance or a list with series 2D data inside
    im = []

    # Check data type
    if type(Data_3d).__module__ == np.__name__: 
        dim3 = Data_3d.shape[2]-1
    elif isinstance(Data_3d,list):
        dim3 = len(Data_3d)-1

    for n in range(dim3):
        if type(Data_3d).__module__ == np.__name__: 
            im.append(Image.fromarray(Data_3d[:,:,n]))
        elif isinstance(Data_3d,list):
            im.append(Image.fromarray(Data_3d[n]))
    return im # im is a PIL.Image object now



