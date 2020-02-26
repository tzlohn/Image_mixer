import numpy as np 
import os,glob,re
import tkinter as tk
from tkinter import filedialog
import pyqtgraph as pg

chip_size = 2080*6.5 # µm
# open folder
# list all the file end with raw

root = tk.Tk()
root.withdraw()

folderpath = filedialog.askdirectory()
os.chdir(folderpath)
file_list = glob.glob('*.raw')
print(file_list)
# for loop
for aFile in file_list:
    x_value = re.findall(r'%s(\d+)'%'x_',aFile)
    zoom_value = re.findall(r'%s(\d+)'%'zoom_',aFile)
    
    print(x_value)
    print(zoom_value)

    # calculate the range of image for every file
    x_start = int(x_value) - chip_size/2 
    x_end = int(x_value) + chip_size/2
    
    # Check whether they have x_, y_, zoom_
    
        # save the range in a dictionary?
    if x_start * x_end >= 0:          # if a file with a range doesn't include 0, rename the file without shutterconfig
        pass    
        # save it as a tiff file with LZW-compressed
    elif    # this condition used to check whether the file is deleted (because it was processed)
        pass
    else:   # if a file with a range includes 0, check shutterconfig
       # calculates the percentage of the positive part and the negative part  
        positive_percentage = abs(x_end)/chip_size
        negative_percentage = abs(x_start)/chip_size 
        dim_names = ['z_planes','y_pixels','x_pixels']
        dim_size = [0, 0, 0]
        n = 0     
       # open both files, extract the corresponding part from them 
        with open(aFile+"_meta.txt") as metaFile:
            image_info = metaFile.read()
            for dim_name in dim_names:
                pattern = re.compile(r"[\[]%s[\]] (\d+)"%dim_name)
                value = pattern.findall(image_info)
                dim_size[n] = int(value(0))
                n=n+1
        
        with open(aFile) as p_data:
            positive_image = np.memmap(p_data, dtype = 'uint16', mode = 'r', shape = int(dim_size))
            pg.image(positive_image)
        # find out whether p_data is left or right, replace the shutterconfig in the name of n_data
        
        with open(aFile) as n_data    
            negative_image = np.memmap(n_data, dtype = "uint16", mode = 'r', shape = ())
       # combine them     

       # Save it as a tiff file with the same name but no shutterconfig and LZW compressed     
       # delete both files     
            
