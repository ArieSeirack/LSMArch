# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 2020

@author: ustc Zhiying Lu

"""
import h5py
import pickle


# help to check the items in hdf5 file
def lavcheck(hdfname):
    hf = h5py.File(hdfname+".lav", "r")
    mode = hf.attrs['decode mode']
    if mode == 0:
        print("\nEncoding Parameters")
        print("Data Shape(x,y,z) = " + str(hf.attrs['shape']))
        print("CRF = " + str(hf.attrs['crf']))
        print("Encoding mode = " + str(hf.attrs['encoding mode']))
        print("Bit Depth = " + str(hf.attrs['bit depth']))
        print("Compression ratio = " + str(hf.attrs['compression ratio']))

        #  explanation for the meaning of 'resize'
        if hf.attrs['resize'] == "1":
            print("resize = delete one row")
        elif hf.attrs['resize'] == "2":
            print("resize = delete one column")
        elif hf.attrs['resize'] == "3":
            print("resize = delete one row and one column")
    if mode == 1:
        print("\nEncoding Parameters")
        print("The LAV contains other LAV file")
        print("The layer structure is\n")
        layer = pickle.loads(hf.attrs['layers'])
        print(layer)

