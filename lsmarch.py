# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 2020

@author: ustc Zhiying Lu

"""
import getopt
import sys
from lav_encode import lavencode
from lav_decode import lavdecode
from lav_check import lavcheck


#  get parameters from command line
def initpara(argv):
    filename = ""
    comp = 0
    indir = ""
    outdir = ""
    crf = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["help", "encode", "decode", "check", "crf="])
    except getopt.GetoptError:
        print('Error: lsmarch.py -i <input_dir> -o <output_dir> -crf <crf_value>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("\nEncoding\npython lsmarch.py --encode -i <input_dir> -o <output_file_name> --crf=<crf_value>")
            print("\nDecoding\npython lsmarch.py --decode -i <input_lav_file_name> -o <output_dir>")
            print("\nCheck the details of LAV file")
            print("\nDecoding\npython lsmarch.py --check -i <lav_file_name>")
            sys.exit()

        if opt == "--encode":
            comp = 1
        elif opt == "--decode":
            comp = 0
        elif opt == "--check":
            comp = 2

        if opt == "-i":
            if comp == 1:
                indir = arg
            elif comp == 0:
                filename = arg
            elif comp == 2:
                filename = arg

        if opt == '-o':
            if comp == 1:
                filename = arg
            elif comp == 0:
                outdir = arg

        if opt == '--crf':
            crf = arg

    if comp == 1:
        print("output_file_name = %s.lav\nindir = %s\ncrf = %s" % (filename, indir, crf))
        return comp, indir, filename, crf
    elif comp == 0:
        print("outdir_name = %s\ninput_file_name = %s.lav" % (outdir, filename))
        return comp, outdir, filename
    elif comp == 2:
        print("input_file_name = %s.lav" % filename)
        return comp, filename


if __name__ == "__main__":
    para = initpara(sys.argv[1:])
    if para[0] == 1:
        indir = para[1]
        filename = para[2]
        crf = para[3]
        lavencode(indir, filename, crf)
    elif para[0] == 0:
        outdir = para[1]
        filename = para[2]
        lavdecode(outdir, filename)
    elif para[0] == 2:
        filename = para[1]
        lavcheck(filename)








