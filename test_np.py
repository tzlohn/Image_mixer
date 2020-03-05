import numpy as np 
from PIL import Image
from tkinter import filedialog
import tkinter as tk
import os
import export_3D_PIL_object as s3D #import convert_3D_frames_to_image

temp_app = tk.Tk()
temp_app.withdraw()
filepath = filedialog.askdirectory()
os.chdir(filepath)

#imnp = []
#for n in range(20):
    #data = np.random.rand(256,256)
data = np.ones((256,256,20), dtype = 'uint16')
    #imnp.append(data)

im = s3D.convert_3D_frames_to_image(data)

im[0].save("test2.tif", save_all = True, append_images = im)

