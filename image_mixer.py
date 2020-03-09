import numpy as np 
import export_3D_PIL_object as e3PO
import os.path
import glob,re,sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, TiffImagePlugin
import tifffile as TFF
#TiffImagePlugin.WRITE_LIBTIFF = True

# assign and open the folder
root = tk.Tk()
root.withdraw()

folderpath = filedialog.askdirectory()
os.chdir(folderpath)

# list all the file end with raw
file_list = glob.glob('*')
print(file_list)

# rename all files, remove the serial number in the end
for aFile in file_list:
    pattern = re.compile(r'(.raw_meta.txt|.raw)')
    exts = pattern.findall(aFile)    
    ext = exts[-1]
    pattern = re.compile(r'(.*)(_\d+)?%s'%ext)
    new_name = pattern.findall(aFile)  
    if new_name:
        new_name = new_name[0][0] + ext
        if not os.path.exists(new_name):
            os.rename(aFile,new_name)

# list all files again, with their new name
file_list = glob.glob('*.raw')    

# work with every file in the loop
for aFile in file_list:
    if not os.path.exists(aFile):
        pass
    else:            
        # get the value for x position_
        x_value = re.findall(r'_X((-)?\d+)',aFile)    
        x_value = x_value[0]
        x_value = int(x_value[0])
        
        # get pixel number, pixel size and dimensions
        dim_names = ['z_planes','y_pixels','x_pixels']
        dim_size = [0, 0, 0]        
        n = 0
        with open(aFile+"_meta.txt") as metaFile:
            image_info = metaFile.read()
            for dim_name in dim_names:
                pattern = re.compile(r"[\[]%s[\]] (\d+)"%dim_name)
                value = pattern.findall(image_info)
                dim_size[n] = int(value[0])
                n=n+1
            pattern = re.compile(r"[\[]%s[\]] (.*)"%'Pixelsize in um')
            value = pattern.findall(image_info) 

        x_pixels = dim_size[2]
        image_size = x_pixels * float(value[0])
        dim_size = tuple(dim_size)     
                
        # get the new file name from the old file name (shutterconfig will be removed)
        pattern = re.compile(r'(.*)(_left|_right|_Left|_Right)(.*)%s'%('.raw'))
        filename_piece = pattern.findall(aFile)
        filename_piece = filename_piece[0]
        new_file_name = filename_piece[0]+filename_piece[2]+".tif"
        print(new_file_name)

        # calculate the range of image for every file
        x_start = x_value - 0.5*image_size 
        x_end = x_value + 0.5*image_size

        # save the range in a dictionary?
        if x_start * x_end >= 0:                     
            with open(aFile) as imfile:
                im_np = np.memmap(imfile, dtype = 'uint16', mode = 'r', shape = dim_size)

        else:   # if a file with a range includes 0, check shutterconfig
        # calculates the percentage of the positive part and the negative part  
            Right_percentage = abs(x_end)/image_size
            Left_percentage = abs(x_start)/image_size 
            
            with open(aFile) as data_1:
                one_image = np.memmap(data_1, dtype = 'uint16', mode = 'r', shape = dim_size)
                #pg.image(positive_image)

            # find out whether p_data is left or right, replace the shutterconfig in the name of n_data
            if filename_piece[1] == 'Left':
                theOtherFile = filename_piece[0] + '_Right' + filename_piece[2] + '.raw'
                Left_image = one_image
                the_other_image = 'Right_image = one_image'
            else:
                theOtherFile = filename_piece[0] + '_Left' + filename_piece[2] + '.raw'
                Right_image = one_image
                the_other_image = 'Left_image = one_image'    

            with open(theOtherFile) as data_2:    
                one_image = np.memmap(data_2, dtype = "uint16", mode = 'r', shape = dim_size)
            
            exec(the_other_image)

            # combine them     
            im_np = np.zeros(dim_size, dtype = 'uint16')
            im_np[:,:,0:round(x_pixels*Right_percentage)] = Right_image[:,:,0:round(x_pixels*Right_percentage)]
            im_np[:,:,round(x_pixels*Right_percentage):-1] = Left_image[:,:,round(x_pixels*Right_percentage):-1]
                    
        # Save it as a tiff file with the same name but no shutterconfig and LZW compressed
        new_image = im_np.transpose(1,2,0)
        #TFF.imwrite(new_file_name, new_image, ijmetadata = {'magnification':'4.0','resolution': '1.6 um'})
        im = e3PO.convert_3D_frames_to_image(new_image)
        im[0].save(new_file_name, save_all = True, append_images = im, compression = 'tiff_lzw')
        
            # delete both files     
            #os.remove(p_data)
            #os.remove(n_data)
     
