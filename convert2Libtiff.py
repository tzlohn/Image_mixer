from libtiff import TIFF
import tkinter as tk
from tkinter import filedialog
import os,glob,re

root = tk.Tk()
root.withdraw()

workpath = filedialog.askdirectory()
os.chdir(workpath)
file_list = glob.glob('*.tif')

for a_file in file_list:
    image = TIFF.open(a_file,"r")
    np_image = image.read_image()
    new_file_name = "libtiff_"+a_file
    print(new_file_name)
    new_file = TIFF.open(new_file_name,"w")
    new_file.write_image(np_image)
