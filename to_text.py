#!/usr/bin/python3

# this program transforms a pickle output file into a text output file
# Warning: if there is already a file named as the output file, it is simply overwritten without any check!

import math
import numpy as np
import pickle
import sys
import os

sp="    "
sf='{:6.3f}'
lf='{:7.4e}'

N_args=len(sys.argv)

if(N_args!=3):
   print('Syntax: ./to_text.py <input file> <output file>')
   sys.exit(1)

inputfile=sys.argv[1]
outputfile=sys.argv[2]

with open(inputfile,"rb") as infile:
    data = pickle.load(infile)

info_results, hadrons, total_events, pT_min_cut, pT_max_cut, rap_cut, y_arr, pT_arr, dy, dpT, y_spectra, pT_spectra = data[:]

ny = len(y_arr)
npT = len(pT_arr)
nh = len(hadrons)

with open(outputfile,"w") as outf:
    outf.write("# Total sampling events: " + str(total_events) + "\n")    
    outf.write("# Block 1 - average dN/dy within the pT range: " + sf.format(pT_min_cut) + " " + sf.format(pT_max_cut) + " [GeV]\n")
    outf.write("# dy: " + sf.format(dy) + "\n")
    outf.write("# Columns: 01: rapidity,  ")
    for k, v in hadrons.items():
        outf.write('{:02d}'.format(v[0] + 2) + ": " + k + " (" + v[1] + "),  ")
    outf.write("\n")
    for i in range(ny):
        outf.write(sf.format(y_arr[i]))
        for h in range(nh):
            outf.write(sp + lf.format(y_spectra[h,i]/(dy * total_events)))
        outf.write("\n")
    outf.write("\n\n") # separation block for gnuplot
    outf.write("# Block 2 - dN/dpT [1/GeV] within the y rapidity range: " + sp.format(-rap_cut) + " " + sp.format(rap_cut) + "\n")
    outf.write("# dpT: " + sf.format(dpT) + "\n")
    outf.write("# Columns: 01: pT [GeV],  ")
    for k, v in hadrons.items():
        outf.write('{:02d}'.format(v[0] + 2) + ": " + k + " (" + v[1] + ")")
    outf.write("\n")
    for i in range(npT):
        outf.write(sf.format(pT_arr[i]))
        for h in range(nh):
            outf.write(sp + lf.format(pT_spectra[h,i]/(dpT * total_events)))
        outf.write("\n")
    
    outf.close()
