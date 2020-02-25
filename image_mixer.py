import numpy as np 
import os,glob,re

Chip_size = 2160*6.5
# open folder
# list all the file end with raw
file_list = glob.glob('*.raw')
print(file_list)
# for loop
for aFile in file_list:
    x_value = re.findall(r'%s(\d+)'%'x_',aFile)
    zoom_value = re.findall(r'%s(\d+)'%'zoom_',aFile)
    print(x_value)
    print(zoom_value)

    # calculate the range of image for every file
    x_start = x_value - chip_size/2 
    x_end = x_value + chip_size/2
    
    # Check whether they have x_, y_, zoom_
    
        # save the range in a dictionary?
    if x_start * x_end >= 0:          # if a file with a range doesn't include 0, rename the file without shutterconfig
        # save it as a tiff file with LZW-compressed
    else   # if a file with a range includes 0, check shutterconfig
       # calculates the percentage of the positive part and the negative part  
        positive_percentage = abs(x_end)/Chip_size
        negative_percentage = abs(x_start)/Chip_size 
            
       # open both files, extract the corresponding part from them 
        positive_image = np.fromfile()
        negative_image = np.fromfile()
       # combine them     

       # Save it as a tiff file with the same name but no shutterconfig and LZW compressed     
       # delete both files     
            
