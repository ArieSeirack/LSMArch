# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 2020

@author: ustc Zhiying Lu

"""
import numpy as np
import subprocess as sp
import h5py
import os
import cv2
import shutil
import pickle


def extract_from_hdf(hdfname, dsetname, outfilename):
    '''hdfname: the name of the hdf5 file you want to visit
       dsetname: the name of the dataset where your file save
       outfilename: the name of file that generates after extraction'''
    hf = h5py.File(hdfname, "r")  # open the hdf5 file with read-only mode
    tardset = hf[dsetname]
    outdata = tardset[...]

    outfile = open(outfilename, "wb")
    outfile.write(outdata)
    outfile.close()


#  decode lav file
def lavdecode(outdir, filename):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
        os.mkdir(os.path.join(outdir, 'low10'))
        os.mkdir(os.path.join(outdir, 'high6'))

    #  get ffmpeg path
    f = open("path.txt", "r")
    ffmpegpath = f.read()
    ffmpegpath = ffmpegpath.strip('\n')
    f.close()

    filename = filename+".lav"
    f = h5py.File(filename, 'r')
    mode = f.attrs['decode mode']
    if mode == 0:  # for lav that contains tif
        extract_from_hdf(filename, 'high6', 'high.mkv')
        extract_from_hdf(filename, 'low10', 'low.mkv')
        lowdecomp(outdir, ffmpegpath)
        highdecomp(outdir, ffmpegpath)
        piccp(outdir, filename)
        print("Decoding Complete")
    elif mode == 1:  # for lav that contains other lavs
        content = f.attrs['layers']
        dtype = type(content).__name__
        if dtype == 'ndarray':  # the bottom layer lav
            layers = list(content)
            for lav in layers:
                if not os.path.exists(os.path.join(outdir, lav)):
                    os.mkdir(os.path.join(outdir, lav))
                extract_from_hdf(filename, lav, os.path.join(outdir, lav, lav+'.lav'))
        elif dtype == 'bytes':  # the layer above the bottom
            layers = list(pickle.loads(f.attrs['layers']))
            for lav in layers:
                if not os.path.exists(os.path.join(outdir, lav)):
                    os.mkdir(os.path.join(outdir, lav))
                extract_from_hdf(filename, lav, os.path.join(outdir, lav, lav+'.lav'))


#  decompression for lower 10 bits
def lowdecomp(outdir, ffmpegpath):
    if not os.path.exists(os.path.join(outdir, 'low10')):
        os.mkdir(os.path.join(outdir, 'low10'))
    lmkv = os.path.join(os.getcwd(), 'low.mkv')
    lotif = os.path.join(outdir, 'low10', '%05d.tif')
    excmd = [ffmpegpath,
             '-i', lmkv,
             '-pix_fmt', 'gray16le',
             lotif]

    pipe = sp.Popen(excmd, stdin=sp.PIPE, stderr=sp.PIPE, bufsize=10 ^ 12)
    pipe.communicate()


#  decompression for higher 6 bits
def highdecomp(outdir, ffmpegpath):
    if not os.path.exists(os.path.join(outdir, 'high6')):
        os.mkdir(os.path.join(outdir, 'high6'))
    hmkv = os.path.join(os.getcwd(), 'high.mkv')
    hotif = os.path.join(outdir, 'high6', '%05d.tif')
    excmd = [ffmpegpath,
             '-i', hmkv,
             hotif]

    pipe = sp.Popen(excmd, stdin=sp.PIPE, stderr=sp.PIPE, bufsize=10 ^ 12)
    pipe.communicate()


def piccp(outdir, hdfname):
    i = 0
    hf = h5py.File(hdfname, "r")
    rsize = hf.attrs['resize']
    shape = hf.attrs['shape']
    width = shape[0]
    height = shape[1]
    if rsize == '1':
        row = np.zeros((1, int(width)), dtype=np.uint16)
    elif rsize == '2':
        col = np.zeros((int(height), 1), dtype=np.uint16)
    elif rsize == '3':
        row = np.zeros((1, int(width)+1), dtype=np.uint16)
        col = np.zeros((int(height), 1), dtype=np.uint16)

    picnames = os.listdir(os.path.join(outdir, 'low10'))
    picnames.sort(key=lambda x:int(x[:-4]))
    for pic in picnames:
        limg = cv2.imread(os.path.join(outdir, 'low10', pic), -1)
        himg = cv2.imread(os.path.join(outdir, 'high6', pic), -1)
        lowarr = np.asarray(limg, dtype=np.uint16)
        higharr = np.asarray(himg, dtype=np.uint16)
        higharr = np.left_shift(higharr, 10)
        lowarr = np.right_shift(lowarr, 6)
        wholearr = np.bitwise_or(higharr, lowarr)

        # if the images were resize, then add one row or one column or both to original shape
        if rsize == '1':
            wholearr = np.row_stack((wholearr, row))
        elif rsize == '2':
            wholearr = np.column_stack((wholearr, col))
        elif rsize == '3':
            wholearr = np.row_stack((wholearr, col))
            wholearr = np.column_stack((wholearr, row))

        cv2.imwrite(outdir + os.sep + "{:0>5d}".format(i) + ".tif", wholearr)
        i += 1

    os.remove("low.mkv")
    os.remove("high.mkv")
    shutil.rmtree(os.path.join(outdir, 'low10'), True)
    shutil.rmtree(os.path.join(outdir, 'high6'), True)

