# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 2020

@author: ustc Zhiying Lu

"""

import numpy as np
import h5py
import os
import pickle


def lavstack(indirs, mode, outname):
    outlav = h5py.File(outname + ".lav", mode)
    dirs = indirs.split(',')
    lavlist = []
    lavdict = {}
    # include all the directories
    for dir in dirs:
        lavdir = os.path.join(os.getcwd(), dir)  # get exact dir location
        lavnames = os.listdir(lavdir)  # get all the lav names in the dir
        for lav in lavnames:  # for each lav, append it in the output lav file
            lavf = open(os.path.join(lavdir, lav), "rb")
            lavdata = lavf.read()
            lavf.close()
            lavbdata = np.void(lavdata)
            outlav.create_dataset(lav.strip('.lav'), dtype=lavbdata.dtype, data=lavbdata)
            lavf = h5py.File(os.path.join(lavdir, lav), "r")
            mode = lavf.attrs['decode mode']
            if mode == 0:  # for lav that contains tif
                lavlist.append(lav.strip('.lav'))
            else:  # for lav that contains other lavs
                content = lavf.attrs['layers']
                dtype = type(content).__name__
                if dtype == 'ndarray':  # the second layer lav
                    layer = list(content)
                elif dtype == 'bytes':  # the third and above lav
                    layer = pickle.loads(lavf.attrs['layers'])
                lavdict[lav.strip('.lav')] = layer
    print("\nstack complete\n")
    if len(lavdict) == 0:
        outlav.attrs['layers'] = lavlist
        print(outlav.attrs['layers'])
    else:
        picobj = pickle.dumps(lavdict, protocol=0)
        outlav.attrs['layers'] = picobj
        print("The layers are")
        print(pickle.loads(outlav.attrs['layers']))
    outlav.attrs['decode mode'] = 1  # 1 means this lav is a stack of lav files









