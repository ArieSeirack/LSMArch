# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 2020

@author: ustc Zhiying Lu

"""

import numpy as np
import subprocess as sp
import h5py
import os
from PIL import Image


def lavencode(indir, fname, crf, gpu):
    highdir = os.path.join(indir, "high6", "%05d.tif")
    lowdir = os.path.join(indir, "low10", "%05d.tif")

    #  get ffmpeg path
    f = open("path.txt", "r")
    ffmpegpath = f.read()
    ffmpegpath = ffmpegpath.strip('\n')
    f.close()

    #  calculate the number of images
    count = 0
    for root, dirs, files in os.walk(os.path.join(indir, 'low10')):
        for each in files:
            count += 1

    #  get image shape
    for pic in os.listdir(os.path.join(indir, 'low10')):
        img = Image.open(os.path.join(indir, 'low10', pic))
        shape = list(img.size)
        shape.append(count)
        break

    #  compress two parts
    highsize = highcomp(highdir, crf, ffmpegpath, gpu)
    lowsize = lowcomp(lowdir, crf, ffmpegpath, gpu)
    print("crf = "+crf+" encoding complete")

    #  calculate compression ratio
    orisize = shape[0]*shape[1]*shape[2]*2
    wholemkvsize = highsize+lowsize
    cprratio = orisize/wholemkvsize
    print("The compress ratio is "+str('%.4f' % cprratio))
    f = open("resize.txt", "r")
    rsize = f.read()
    f.close()

    # create lav file
    metadata = [shape, crf, cprratio, rsize]
    savelav(fname, metadata)
    print("Encoding Complete")


# compression for higher 6 bits
def highcomp(hidir, crf, ffmpegpath, gpu):
    hmkv = os.path.join(os.getcwd(), "high.mkv")
    if gpu == 1:
        hcprcmd = [ffmpegpath,
                   '-y',
                   '-i', hidir,
                   '-codec', 'hevc_nvenc',
                   '-preset', 'lossless',
                   '-pix_fmt', 'yuv420p',
                   hmkv]
    else:
        hcprcmd = [ffmpegpath,
                   '-y',
                   '-i', hidir,
                   '-codec', 'libx265',
                   '-x265-params', 'lossless=1',
                   hmkv]
    print("crf = " + crf + " high6 encoding start")
    pipe = sp.Popen(hcprcmd, stdin=sp.PIPE, stderr=sp.PIPE, bufsize=10 ^ 12)
    pipe.communicate()
    print("crf = " + crf + " high6 encoding complete")
    highsize = os.path.getsize(hcprcmd[-1])
    return highsize


#  compression for lower 10 bits
def lowcomp(lowdir, crf, ffmpegpath, gpu):
    lmkv = os.path.join(os.getcwd(), "low.mkv")
    if gpu == 1:
        lcprcmd = [ffmpegpath,
                   '-y',
                   '-i', lowdir,
                   '-codec', 'hevc_nvenc',
                   '-preset', 'medium',
                   '-pix_fmt', 'p010le',
                   '-qp', crf,
                   lmkv]
    else:
        lcprcmd = [ffmpegpath,
                   '-y',
                   '-i', lowdir,
                   '-codec', 'libx265',
                   '-preset', 'medium',
                   '-pix_fmt', 'yuv420p10le',
                   '-x265-params', "crf="+crf,
                   lmkv]

    print("crf = " + crf + " low10 encoding start")

    pipe = sp.Popen(lcprcmd, stdin=sp.PIPE, stderr=sp.PIPE, bufsize=10 ^ 12)
    pipe.communicate()
    print("crf = " + crf + " low10 encoding complete")
    lowsize = os.path.getsize(lcprcmd[-1])
    return lowsize


#  create lav file
def savelav(filename, meta):
    lavfile = h5py.File(filename+".lav", "w")
    lf = open("low.mkv", "rb")
    lowdata = lf.read()
    lf.close()
    hf = open('high.mkv', 'rb')
    highdata = hf.read()
    hf.close()

    hbdata = np.void(highdata)
    lbdata = np.void(lowdata)
    lavfile.create_dataset("high6", dtype=hbdata.dtype, data=hbdata)
    lavfile.create_dataset("low10", dtype=lbdata.dtype, data=lbdata)
    lavfile.attrs['shape'] = meta[0]
    lavfile.attrs['crf'] = meta[1]
    lavfile.attrs['decode mode'] = 0
    #  only support H6L10 and 16-bit image compression currently
    lavfile.attrs['encoding mode'] = 'H6L10'
    lavfile.attrs['bit depth'] = '16-bit'
    lavfile.attrs['compression ratio'] = meta[2]
    lavfile.attrs['resize'] = meta[3]

    os.remove("low.mkv")
    os.remove("high.mkv")








