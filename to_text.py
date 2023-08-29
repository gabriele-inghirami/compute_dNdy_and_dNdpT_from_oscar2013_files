#!/usr/bin/python3

# this program transforms a pickle output file into separate text output files
# Warning: if there is already a file named as the output file, it is simply overwritten without any check!

import math
import numpy as np
import pickle
import sys
import os

sp="    "
sf='{:6.3f}'
lf='{:7.4e}'

# third indexes of multidimensional arrays with results
dN_idx = 0
v1_idx = 1
v2_idx = 2

N_args=len(sys.argv)

if(N_args!=3):
   print('Syntax: ./to_text.py <input file> <prefix of output files>')
   sys.exit(1)

inputfile=sys.argv[1]
outputfile_prefix=sys.argv[2]

with open(inputfile,"rb") as infile:
    data = pickle.load(infile)

info_results, hadrons, total_events, pT_min_cut, pT_max_cut, rap_cut, y_arr, pT_arr, dy, dpT, y_spectra, pT_spectra = data[:]

ny = len(y_arr)
npT = len(pT_arr)
nh = len(hadrons)

for k, v in hadrons.items():
    outputfile_basename = outputfile_prefix + "_" + v[1]
    
    outputfile = outputfile_basename + "_vs_rapidity.dat"
    with open(outputfile,"w") as outf:
        outf.write("# Hadron: " + v[1] + " , PDG ID: " + k + "\n")
        outf.write("# Total sampling events: " + str(total_events) + "\n")    
        outf.write("# Results for the pT range: " + sf.format(pT_min_cut) + " <-> " + sf.format(pT_max_cut) + " [GeV]\n")
        outf.write("# dy: " + sf.format(dy) + "\n")
        outf.write("# Columns: 1: rapidity, 2: <dN/dy>, 3: <v1>, 4: <v2>\n")
        h_index = v[0]
        for i in range(ny):
            outf.write(sf.format(y_arr[i]))
            N_in_bin = y_spectra[h_index,i,dN_idx]
            outf.write(sp + lf.format(N_hadrons / (dy * total_events)))
            if (N_in_bin > 0):
                v1_in_bin = y_spectra[h_index,i,dN_v1] / N_hadrons
                v2_in_bin = y_spectra[h_index,i,dN_v2] / N_hadrons
            else:
                v1_in_bin = 0
                v2_in_bin = 0
            outf.write(sp + lf.format(v1_in_bin))
            outf.write(sp + lf.format(v2_in_bin))
            outf.write("\n")
            
    outputfile = outputfile_basename + "_vs_pT.dat"
    with open(outputfile,"w") as outf:
        outf.write("# Hadron: " + v[1] + " , PDG ID: " + k + "\n")
        outf.write("# Total sampling events: " + str(total_events) + "\n")    
        outf.write("# Results within the y rapidity range: " + sp.format(-rap_cut) + " " + sp.format(rap_cut) + " [GeV]\n")
        outf.write("# dpT: " + sf.format(dpT) + "\n")
        outf.write("# Columns: 1: pT [GeV], 2: <dN/dpT> [1/GeV], 3: <v1>, 4: <v2>\n")
        h_index = v[0]
        for i in range(npT):
            outf.write(sf.format(pT_arr[i]))
            N_in_bin = pT_spectra[h_index,i,dN_idx]
            outf.write(sp + lf.format(N_hadrons / (dpT * total_events)))
            if (N_in_bin > 0):
                v1_in_bin = pT_spectra[h_index,i,dN_v1] / N_hadrons
                v2_in_bin = pT_spectra[h_index,i,dN_v2] / N_hadrons
            else:
                v1_in_bin = 0
                v2_in_bin = 0
            outf.write(sp + lf.format(v1_in_bin))
            outf.write(sp + lf.format(v2_in_bin))
            outf.write("\n")
