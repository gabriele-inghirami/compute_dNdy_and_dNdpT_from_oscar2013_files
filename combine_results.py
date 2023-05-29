#!/usr/bin/python3

import numpy as np
import pickle
import sys
import os

sp="    "

N_args=len(sys.argv)
N_input_files=N_args-2

if(N_input_files<2):
   print('Syntax: ./combine_results.py <outputfile> <inputfile 1> <inputfile 2> ... [inputfile n]')
   print("(The minimum number of input files is 2)")
   sys.exit(1)

outputfile=sys.argv[1]

if os.path.exists(outputfile):
    print("Sorry, but, as a safety measure, I don't overwrite an already existing file.")
    print("Please, check that you used the correct syntax (the output file is the first argument) and,")
    print("if this is the case, rename or cancel the existing file. I stop here.\n")

with open(sys.argv[2],"rb") as infile:
    data = pickle.load(infile)

info_results, hadrons, total_events, pT_min_cut, pT_max_cut, rap_cut, y_arr, pT_arr, dy, dpT, y_spectra, pT_spectra = data[:]

data=None

for fi in range(3,N_args):
    try:
        with open(sys.argv[fi],"rb") as infile:
            data = pickle.load(infile)
    except:
        print("Error in reading "+sys.argv[fi])
        continue
    info_results_new, hadrons_new, total_events_new, pT_min_cut_new, pT_max_cut_new, rap_cut_new, y_arr_new, pT_arr_new, dy_new, dpT_new,\
        y_spectra_new, pT_spectra_new = data[:]
    data = None
    if ((hadrons_new != hadrons) or (pT_min_cut_new != pT_min_cut) or (pT_max_cut_new != pT_max_cut) or (rap_cut_new != rap_cut) or\
        (dy_new != dy) or (dpT_new != dpT) or (y_arr_new.all() != y_arr_new.all()) or (pT_arr_new.all() != pT_arr.all())):
        print("Warning, I skip input file "+sys.argv[fi])
        print("because it does not match the fundamental characteristics of the first file")
        continue
    total_events += total_events_new
    y_spectra += y_spectra_new
    pT_spectra += pT_spectra_new


with open(outputfile,"wb") as outf:
    pickle.dump((info_results, hadrons, total_events, pT_min_cut, pT_max_cut, rap_cut, y_arr, pT_arr, dy, dpT, y_spectra, pT_spectra),outf)


