"""
This function finds out whether an image is from left or right illuminatoins by its file name. 
When an image is identified, it will be moved to the corresponding folder.
"""
import numpy as np
import tifffile as TFF
import tkinter as tk
from tkinter import filedialog
from shutil import copyfile
import os,re,glob,shutil,time

root = tk.Tk()
root.withdraw()

working_folder = filedialog.askdirectory()
os.chdir(working_folder)

all_raw_files = glob.glob("*.tif")

t_start = time.time()
for a_raw_file in all_raw_files:
    its_meta_file = a_raw_file + "_meta.txt"
    # get pixel number, pixel size and dimensions for memmap to load the image
    dim_names = ['z_planes','y_pixels','x_pixels']
    dim_size = [0, 0, 0]        
    n = 0
    with open(its_meta_file) as metaFile:
        image_info = metaFile.read()
        for dim_name in dim_names:
            pattern = re.compile(r"[\[]%s[\]] (\d+)"%dim_name)
            value = pattern.findall(image_info)
            dim_size[n] = int(value[0])
            n=n+1
    
        pattern = re.compile(r"[\[]is\sscanned[\]] (\w+)")
        is_scanned = pattern.findall(image_info)  
    
    dim_size = tuple(dim_size)

    # save to tiff
    if is_scanned[0] == "False":
        print(a_raw_file)
        im = np.ones(shape = dim_size, dtype = "uint16")
        im = im*120
        TFF.imwrite(a_raw_file, data = im, bigtiff = True, append = False) 