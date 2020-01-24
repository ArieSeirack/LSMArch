# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 2020

@author: ustc Zhiying Lu

"""
import numpy as np
import os
import cv2
import getopt
import sys
from PIL import Image


def initpara(argv):
    indir = ""
    outdir = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["help"])
    except getopt.GetoptError:
        print('Error: try\npython divide.py -h\nto see instruction')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("\nDividing\npython divide.py -i <input_dir> -o <output_dir>")
            sys.exit()

        if opt == "-i":
            indir = arg

        if opt == '-o':
            outdir = arg

    print("input_dir = %s\noutput_dir = %s" % (indir, outdir))
    return indir, outdir


def picdevide(indir, outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    dir_high = os.path.join(outdir, 'high6')
    dir_low = os.path.join(outdir, 'low10')

    if not os.path.exists(dir_high):
        os.mkdir(dir_high)
    if not os.path.exists(dir_low):
        os.mkdir(dir_low)

    N = 0

    #  get the number of images
    for root, dirs, files in os.walk(indir):
        for each in files:
            N += 1

    # get image shape
    for pic in os.listdir(indir):
        img = Image.open(os.path.join(indir, pic))
        shape = list(img.size)
        break

    width = shape[0]
    height = shape[1]

    # zero means the original height and width enable compression, 1 means one row needs to be deleted
    # 2 means one column needs to be deleted, 3 means one column and one row need to be deleted
    resize = 0
    if height % 2 == 1:  # height is odd, delete one row
        resize = 1
    if width % 2 == 1:  # width is odd, delete one column
        resize = 2
    if height % 2 == 1 and width % 2 == 1:
        resize = 3

    i = 0
    for file in os.listdir(indir):
        img = cv2.imread(os.path.join(indir, file), -1)
        if resize == 1:
            im = img.astype(np.uint16)
            new = np.delete(im, -1, axis=0)  # delete one row
        elif resize == 2:
            im = img.astype(np.uint16)
            new = np.delete(im, -1, axis=1)  # delete one column
        elif resize == 3:
            im = img.astype(np.uint16)
            new = np.delete(im, -1, axis=0)  # delete one row
            new = np.delete(new, -1, axis=1)  # delete one column

        print(file)
        #  divide the image into lower 10 bits and higher 6 bits
        cv2.imwrite(dir_high + os.sep + "{:0>5d}.tif".format(i), (new >> 10).astype(np.uint8))
        left = (new << 6).astype(np.uint16)
        cv2.imwrite(dir_low + os.sep + "{:0>5d}.tif".format(i), left)
        i = i + 1
        if i == N:
            break
    return resize


if __name__ == "__main__":
    para = initpara(sys.argv[1:])
    sizechange = picdevide(para[0], para[1])
    f = open(os.path.join(os.getcwd(), "resize.txt"), 'w')
    f.write(str(sizechange))
    f.close()
