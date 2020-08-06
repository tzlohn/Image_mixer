import tkinter as tk
from tkinter import filedialog
import numpy as np
import tifffile as TFF
import os,time,shutil,re
import multiprocessing

def get_value(expression,text):
    output = expression.findall(text)
    value = ""
    for num in output[0]:
        value = value + num 
    value = float(value)
    return value

def finding_index_for_zero(im_file, page_num, side, offset_threshold):
    
    last_layers = TFF.imread(im_file, key = range(page_num-10,page_num,1))
    column_num = last_layers.shape[2]
    row_num = last_layers.shape[1]
    
    if side is "left":
        delta = 1
        n = -1
    elif side is "right":
        delta = -1
        n = column_num

    size_of_0 = 1
    ini_set = n

    while size_of_0 != 0:
        n = n + delta
        column = last_layers[0,offset_threshold:row_num-offset_threshold,n]
        if n == ini_set + delta:
            columns = column
        else:
            columns = columns + column
        index_of_0 = np.where(columns == 0)[0]
        size_of_0 = index_of_0.shape[0]
    return n

def get_dim_match_image(im, x_diff,y_diff,side):
    dim_shape = im.shape
    if side is "Left":
        if x_diff > 0:
            filling_zero_matrix  = np.zeros(shape = (dim_shape[0],x_diff), dtype = "uint16")
            im = np.concatenate([im ,filling_zero_matrix], axis = 1)
        if y_diff > 0:
            filling_zero_matrix  = np.zeros(shape = (y_diff,im.shape[1]), dtype = "uint16")
            im = np.concatenate([im ,filling_zero_matrix], axis = 0)            
    elif side is "Right":
        if x_diff < 0:
            filling_zero_matrix  = np.zeros(shape = (dim_shape[0],abs(x_diff)), dtype = "uint16")
            im = np.concatenate([filling_zero_matrix,im], axis = 1)
        if y_diff < 0:
            filling_zero_matrix  = np.zeros(shape = (abs(y_diff),im.shape[1]), dtype = "uint16")
            im = np.concatenate([im,filling_zero_matrix], axis = 0)
    return im.transpose(1,0)

def remove_comma_from_string(string):
    return string[0:len(string)-1]

def save2_2D(n,imfile,overlap_offset,cutting_pixel,x_diff,y_diff,side,dest_folder):    
    img = TFF.TiffFile(imfile)
    im = TFF.imread(imfile, key = n)
    im = im[:,overlap_offset:cutting_pixel]
    an_image = get_dim_match_image(im,x_diff,y_diff,side)

    page_num_str = str(len(img.pages))
    n_str = str(n)
    digit_diff = len(page_num_str) - len(n_str)  
    n_str = "0"*digit_diff + n_str
    name = "image_" + n_str + ".tif"

    TFF.imwrite(name, an_image, bigtiff = True)
    shutil.move(name,dest_folder)
# part 1: modify images according to meta files
# 1) rotates both images 90 degree
# 2) remove overlapped pixels to make both dimensions identical

def main():
    root =  tk.Tk()
    root.withdraw()

    working_folder = filedialog.askdirectory(title = "selecting the working folder for storing stitched data")
    os.chdir(working_folder)

    left_file = filedialog.askopenfilename(title = "select the left image")
    right_file = filedialog.askopenfilename(title = "select the right image")

    t_start = time.time()

    # get required parameters from meta file
    with open("meta_for_LR_fusion.txt",'r') as meta_file:
        im_info = meta_file.read()
        
        pattern = re.compile(r"[\[]pixel size of x \(µm\)[\]] \: (\d+)(\.)?(\d+)?")
        pixel_size_x = get_value(pattern,im_info)

        pattern = re.compile(r"[\[]pixel size of y \(µm\)[\]] \: (\d+)(\.)?(\d+)?")
        pixel_size_y = get_value(pattern,im_info)
        
        pattern = re.compile(r"[\[]pixel counts in x[\]] \: (\d+)")
        x_pixels = get_value(pattern,im_info)

        pattern = re.compile(r"[\[]z step size \(µm\)[\]] \: (\d+)(\.)?(\d+)?")
        z_stepsize = get_value(pattern,im_info)

        pattern = re.compile(r"[\[]x positions_Left[\]] \: [\[](.*)[\]]")
        all_left_positions = pattern.findall(im_info)
        all_left_positions = all_left_positions[0].split()
        for ind,string in enumerate(all_left_positions):
            all_left_positions[ind] = remove_comma_from_string(string)

        pattern = re.compile(r"[\[]x positions_Right[\]] \: [\[](.*)[\]]")
        all_right_positions = pattern.findall(im_info)
        all_right_positions = all_right_positions[0].split()
        for ind,string in enumerate(all_right_positions):
            all_right_positions[ind] = remove_comma_from_string(string)

    with TFF.TiffFile(right_file) as right_tif:
        size_right = right_tif.pages[0].shape
        page_num_right = len(right_tif.pages)

    with TFF.TiffFile(left_file) as left_tif:
        size_left = left_tif.pages[0].shape
        page_num_left = len(left_tif.pages)

    dest_folder = ["right_rot","left_rot"]
    os.mkdir(dest_folder[0])
    os.mkdir(dest_folder[1])

    ## magic number zone
    offset_threshold = 100
    ##

    ## removing 90% of overlap
    pos = max(all_left_positions)
    pos = float(pos)
    image_size = pixel_size_x * x_pixels
    ratio_L_to_edge = (pos + 0.5*image_size)/image_size
    ratio_R_to_edge = abs(pos - 0.5*image_size)/image_size
    if ratio_L_to_edge >0.95:
        overlap_offset_L = 0
    else:
        overlap_offset_L = round((1-(ratio_L_to_edge+0.05))*image_size)

    if ratio_R_to_edge >0.95:
        overlap_offset_R = 0
    else:
        overlap_offset_R = round((1-(ratio_R_to_edge+0.05))*image_size)


    # finding upper and lower 0 lines
    left_cutting_pixel = finding_index_for_zero(left_file, page_num_left, "left", offset_threshold) # should be a number closer to 0
    right_cutting_pixel = finding_index_for_zero(right_file, page_num_right, "right", offset_threshold) # should be a number closer to size_right
    y_diff = size_right[0]-size_left[0]
    x_diff = (right_cutting_pixel+1-overlap_offset_R)-(size_left[1]- overlap_offset_L - left_cutting_pixel)

    core_no = multiprocessing.cpu_count()-1
    Pool_input_right = [(n,right_file,overlap_offset_R,right_cutting_pixel,x_diff,y_diff,"right",dest_folder[0]) for n in range(0,page_num_right)]
    Pool_input_left = [(n,left_file,overlap_offset_L,left_cutting_pixel,x_diff,y_diff,"left",dest_folder[1]) for n in range(0,page_num_left)]
    Pool = multiprocessing.Pool(processes= core_no)
    result = Pool.starmap(save2_2D,Pool_input_right)
    result = Pool.starmap(save2_2D,Pool_input_left)
    Pool.close()
 
    t_end = time.time()
    print("%.2f"%(t_end-t_start))
        
    # part 2: generate the xml file
    # magic number zone #
    '''
    reference refering is like transpose. ref1 indicates the V in terastitcher
    ref2 indicates H, ref3 indicates D. 1,2,3 is the 3 dimension indicators in your images.
    The follwing assigment tells the code to map the coordinates of your system to terastitcher
    the minus sign indicates that the tile will be aligned/stitched in the reverse order of the index
    ''' 
    ref1 = 1
    ref2 = 2
    ref3 = 3

    ori_V = 0 # unit: mm
    ori_H = 0
    ori_D = 0

    bit = 16
    ###########
    dim_V = pixel_size_y
    dim_H = pixel_size_x
    dim_D = z_stepsize

    xml_name = "terastitcher.xml"

    slice_no = [len(right_tif.pages),len(left_tif.pages)]
    offset_H = 0
    if len(all_right_positions) > 1:
        offset_V = abs(float(all_right_positions[1]) - float(all_right_positions[0]))
    elif len(all_left_positions) >1:
        offset_V = abs(float(all_left_positions[1]) - float(all_left_positions[0]))
    else:
        offset_V = 0 

    stack_rows = 2
    stack_column = 1

    image_files = ["Right_rot.tif","Left_rot.tif"]
    shift_no = [1, an_image.shape[0]-x_pixels]

    with open(xml_name,'w') as xml_file:
        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        xml_file.write("<!DOCTYPE TeraStitcher SYSTEM \"TeraStitcher.DTD\">\n")
        xml_file.write("<TeraStitcher volume_format=\"TiledXY|2Dseries\" input_plugin=\"tiff2D\">\n")
        xml_file.write("    <stacks_dir value=\"%s\" />\n"%(working_folder))
        xml_file.write("    <ref_sys ref1=\"%d\" ref2=\"%d\" ref3=\"%d\" />\n"%(ref1,ref2,ref3))
        xml_file.write("    <voxel_dims V=\"%.2f\" H=\"%.2f\" D=\"%.2f\" />\n"%(dim_V,dim_H,dim_D))
        xml_file.write("    <origin V=\"%.3f\" H=\"%.3f\" D=\"%.3f\" />\n"%(ori_V,ori_H,ori_D))
        xml_file.write("    <mechanical_displacements V=\"%.2f\" H=\"%.2f\" />\n"%(offset_V,offset_H))
        xml_file.write("    <dimensions stack_rows=\"%d\" stack_columns=\"%d\" stack_slices=\"%d\" />\n"%(2,1,max(slice_no)))
        xml_file.write("    <STACKS>\n")
        
        for n in range(len(image_files)):
            xml_file.write("        <Stack N_CHANS=\"1\"")
            xml_file.write(" N_BYTESxCHAN=\"%d\""%(bit/8))
                
            xml_file.write(" ROW=\"%d\""%(n))
            xml_file.write(" COL=\"%d\""%(0))   
            xml_file.write(" ABS_H=\"%.1f\""%(shift_no[n]))
            xml_file.write(" ABS_V=\"%.1f\""%(1))
                
            xml_file.write(" ABS_D=\"0\"")
            xml_file.write(" STITCHABLE=\"yes\"")
            xml_file.write(" DIR_NAME=\"%s\""%(dest_folder[n]))
            xml_file.write(" Z_RANGES=\"[0,%d)\""%(slice_no[n]))
            xml_file.write(" IMG_REGEX=\"%s\">\n"%("image_\d+.tif"))
                
            xml_file.write("            <NORTH_displacements/>\n")
            xml_file.write("            <EAST_displacements/>\n")
            xml_file.write("            <SOUTH_displacements/>\n")
            xml_file.write("            <WEST_displacements/>\n")
            xml_file.write("        </Stack>\n")
        xml_file.write("    </STACKS>\n")
        xml_file.write("</TeraStitcher>\n")

if __name__ == "__main__":
    main()
