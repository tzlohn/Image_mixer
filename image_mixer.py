import numpy as np 
import os.path
import glob,re,shutil,sys
import tkinter as tk
from tkinter import filedialog
import pyqtgraph as pg
from PyQt5 import QtWidgets 
import tifffile

chip_size = 2080*6.5 # µm
# open folder
# list all the file end with raw

root = tk.Tk()
root.withdraw()

folderpath = filedialog.askdirectory()
os.chdir(folderpath)
file_list = glob.glob('*.raw')
print(file_list)

pg_app = QtWidgets.QApplication(sys.argv)
sys.exit(pg_app.exec_())

for aFile in file_list:
    print(aFile)
    if not os.path.exists(aFile):
        pass
    else:    
        # Check whether they have x_, y_, zoom_
        x_value = re.findall(r'_X((-)?\d+)',aFile)
        zoom_value = re.findall(r'(\d+)x_',aFile)
        
        x_value = x_value[0]
        x_value = int(x_value[0])
        zoom_value = int(zoom_value[0])
        image_size = chip_size/zoom_value

        print(x_value)
        print(zoom_value)

        # find out the new file name
        pattern = re.compile(r'(.*)(_left|_right|_Left|_Right)(.*)%s'%('.raw'))
        filename_piece = pattern.findall(aFile)
        filename_piece = filename_piece[0]
        new_file_name = filename_piece[0]+filename_piece[2]
        print(new_file_name)

        # calculate the range of image for every file
        x_start = x_value - image_size/2 
        x_end = x_value + image_size/2

        # save the range in a dictionary?
        if x_start * x_end >= 0:          # if a file with a range doesn't include 0, rename the file without shutterconfig              
            pass
        else:   # if a file with a range includes 0, check shutterconfig
        # calculates the percentage of the positive part and the negative part  
            positive_percentage = abs(x_end)/image_size
            negative_percentage = abs(x_start)/image_size 
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
                pg.image(positive_image)
            # find out whether p_data is left or right, replace the shutterconfig in the name of n_data
        
            with open(aFile) as n_data:    
                negative_image = np.memmap(n_data, dtype = "uint16", mode = 'r', shape = dim_size)
            # combine them     

            # Save it as a tiff file with the same name but no shutterconfig and LZW compressed
            #imwrite(new_file_name+'.tif', data, compress=6, metadata={'axes': 'TZCYX'})  
            # delete both files     
            #os.remove(p_data)
            #os.remove(n_data)      
