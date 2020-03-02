import numpy as np 
import os,glob,re
import tkinter as tk
from tkinter import filedialog
import pyqtgraph as pg

chip_size = 2048*6.5 # µm
# open folder
# list all the file end with raw

root = tk.Tk()
root.withdraw()

folderpath = filedialog.askdirectory()
os.chdir(folderpath)
file_list = glob.glob('*.raw')
print(file_list)

for aFile in file_list:

    dim_names = ['z_planes','y_pixels','x_pixels']
    dim_size = [0, 0, 0]
    n = 0     
    # open both files, extract the corresponding part from them 
    with open(aFile+"_meta.txt") as metaFile:
        image_info = metaFile.read()
        for dim_name in dim_names:
            pattern = re.compile(r"[\[]%s[\]] (\d+)"%dim_name)
            value = pattern.findall(image_info)
            dim_size[n] = int(value[0])
            n=n+1
        
    dim_size = tuple(dim_size)

    with open(aFile) as p_data:
        positive_image = np.memmap(p_data, dtype = 'uint16', mode = 'r', shape = dim_size)
        
        # find out whether p_data is left or right, replace the shutterconfig in the name of n_data
    pg.image(positive_image[0,:,:])    
    #with open(aFile) as n_data:           
    #    negative_image = np.memmap(n_data, dtype = "uint16", mode = 'r', shape = ())
       # combine them     

       # Save it as a tiff file with the same name but no shutterconfig and LZW compressed     
       # delete both files     
            
