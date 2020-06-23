# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 2020

@author: ustc Zhiying Lu

"""

import numpy as np
import h5py
import os
import pickle
from lav_check import lavcheck


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


def stackdel(filename, dsname):
    hf = h5py.File(filename+".lav", "r+")
    newf = h5py.File("new.lav", "w")
    # delete one dataset from the top layer of the lav tree
    # note: the size of lav file will not change even if one dataset was deleted
    # the delete function only makes the memory not accessible
    if dsname in hf.keys():  # delete one dataset from the lav tree
        hf.__delitem__(dsname)

    for dset in hf.keys():
        dataset = hf[dset]
        newf.create_dataset(dset, dtype=dataset.dtype, data=dataset)

    # the following steps will delete the name in the layer list/dict
    mode = hf.attrs['decode mode']
    if mode == 1:
        layer = pickle.loads(hf.attrs['layers'])
        layer.pop(dsname)
        piclayers = pickle.dumps(layer, protocol=0)
        newf.attrs['layers'] = piclayers
        newf.attrs['decode mode'] = mode
    hf.close()
    newf.close()
    os.remove(filename+".lav")
    os.rename("new.lav", filename+".lav")
