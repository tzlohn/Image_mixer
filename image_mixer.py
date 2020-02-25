import numpy as np 
import os

# open folder
# list all the file end with raw
# for loop
    # Check whether they have x_, y_, zoom_
    # calculate the range of image for every file
        # save the range in a dictionary?
    # if
        # if a file with a range doesn't include 0, rename the file without shutterconfig
            # save it as a tiff file with LZW-compressed
        # if a file with a range includes 0, check shutterconfig
            # get their range
            # calculates the percentage of the positive part and the negative part
            # open both files, extract the corresponding part from them
            # combine them
            # Save it as a tiff file with the same name but no shutterconfig and LZW compressed
