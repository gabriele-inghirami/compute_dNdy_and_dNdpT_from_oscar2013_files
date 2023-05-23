#!/usr/bin/python3

# this program reads a Oscar 2013 file and writes in an output pickle file:
# number of events
# the y array
# the pT array
# dN(y)
# dN(dpT)
# the python dictionary with the considered hadrons
# for the following hadrons (the first number is the PDG id):
# 2212 proton
# -2212 anti-proton
# 2112 neutron
# -2212 anti-neutron
# 211 pion plus
# -211 pion minus
# 111 pion 0
# 321 Kaon plus
# -321 Kaon minus

import argparse
from datetime import date, datetime
import math
import numpy as np
import os
import sys
import pickle

# rapidity cut for dN/dpT
rap_cut = 1000

# minimum transverse momentum cut for dN/dy
pT_min_cut = 0.
# maximum transverse momentum cut for dN/dy
pT_max_cut = 1000

# rapidity resolution (dy)
rap_resolution = 0.2
# max rapidity (absolute value), referred to the border of the bin
# please, notice the the actual used value will be rounded so to have an integer number of cells
max_rapidity = 5

# pT resolution (dpT)
pT_resolution = 0.1
# max pT, referred to the border of the bin
# please, notice the the actual used value will be rounded so to have an integer number of cells
max_pT = 4

#################

hadrons = {"211":(0,"pion_plus"),\
           "-211":(1,"pion_minus"),\
           "111":(2,"pion_0"),\
           "321":(3,"kaon_plus"),\
           "-321":(4,"kaon_minus"),\
           "2212":(5,"proton"),\
           "-2212":(6,"anti-proton"),\
           "2112":(7,"neutron"),\
           "-2112":(8,"anti-neutron"),\
          }

parser = argparse.ArgumentParser(description='A scripts that computes dN/dy and dN/dpT of selected hadrons from Oscar 2013 output files')

parser.add_argument('--output', '-o', help='Path to the output file (pickle format). Default is "./output.pickle".', default="./output.pickle")
parser.add_argument('--text_output', '-t', help='Path to the output file in txt format (disabled by default).')
parser.add_argument('inputs', nargs='+', help='Oscar 2013 input files')

args = parser.parse_args()

outputfile = args.output

if (args.text_output == None):
    enable_text_outputfile = False
else:
    enable_text_outputfile = True
    text_outputfile = args.text_output

nh = len(hadrons)

dy = rap_resolution

dpT = pT_resolution

ny = int(2*max_rapidity/dy)

npT = int(max_pT/pT_resolution)

y_arr = np.linspace(-(ny*dy+dy)/2, (ny*dy+dy)/2, num = ny)

pT_arr = np.linspace(0, npT*dpT, num = npT)

y_spectra = np.zeros((nh,ny),dtype=np.float64)

pT_spectra = np.zeros((nh,npT),dtype=np.float64)

total_events = 0

# format for quantities in output file
cf='{:7.3f}'
ff='{:16.12e}'
sp="    "

# if we want to print debugging messages or not (0=none,1=advancement infos)
verbose = 1


def extract_data_oscar(infile, y_arr, pT_arr):
    unfinished_event = False
    with open(infile,"r") as ifile:

        # we count the hadrons event by event and we add them only if the event is complete
        events_in_file = 0 
        y_spectra_event = np.zeros((nh,ny),dtype=np.float64)
        pT_spectra_event = np.zeros((nh,npT),dtype=np.float64)
        y_spectra_file = np.zeros((nh,ny),dtype=np.float64)
        pT_spectra_file = np.zeros((nh,npT),dtype=np.float64)

        for iline in ifile:
 
            line = iline.split()
            if (line[0][0] == "#"):
                if (line[1] == "event"):
                    if (line[3] == "out"):
                        unfinished_event = True
                    elif (line[3] == "end"):
                        if unfinished_event:
                            unfinished_event = False
                            events_in_file += 1
                            y_spectra_file += y_spectra_event
                            y_spectra_event.fill(0.)
                            pT_spectra_file += pT_spectra_event
                            pT_spectra_event.fill(0)                 
                        else:
                            print("Error, detected end of event without detecting its beginning")
                            sys.exit(1)
                    else:
                        print("Error, unkown event label: " + line[3])
                        sys.exit(1)
                continue
        
            pdg_ID = line[10]
            if (pdg_ID in hadrons):
                hadron_index = hadrons[pdg_ID][0]
            else:
                continue
            t, x, y, z, mass, p0, px, py, pz = np.float64(line[0:9])
        

            if (((p0 - pz)*(p0 + pz)) <= 0):
                continue
            rapidity = 0.5 * math.log((p0+pz)/(p0-pz))
            pT = math.sqrt(px**2+py**2)
            rapidity_index = int(math.floor((rapidity - y_arr[0])/dy))
            
            if ((rapidity_index >= 0) and (rapidity_index < ny) and (pT >= pT_min_cut) and (pT < pT_max_cut)):
                y_spectra_event[hadron_index, rapidity_index] += 1 

            pT_index = int(math.floor((pT - pT_arr[0])/dpT))

            if ((pT_index >= 0) and (pT_index < npT) and abs(rapidity) < rap_cut):
                pT_spectra_event[hadron_index, pT_index] += 1 
              
    return events_in_file, y_spectra_file, pT_spectra_file

""" if (len(sys.argv)<2):
    parser.print_help()
    sys.exit(1) """

if os.path.exists(outputfile):
    current_date = datetime.now()
    date_string = current_date.strftime("%Y-%m-%d-%H-%M-%S")
    new_name_for_old_outputfile = outputfile + "_backup_copy_" + date_string
    os.rename(outputfile, new_name_for_old_outputfile)
    
for infile in args.inputs:
    new_events, new_y_spectra, new_pT_spectra = extract_data_oscar(infile, y_arr, pT_arr)
    if new_events == None:
        print("Warning, error detected when reading " + infile + ", file discarded.")
        continue
    if new_events == 0:
        print("Warning, 0 events found in " + infile + ", file unused.")
        continue
    total_events += new_events
    y_spectra += new_y_spectra
    pT_spectra += new_pT_spectra

if total_events == 0:
    print("Sorry, something went wrong, I collected 0 events...")
    sys.exit(2)
    
# now we print the results

if enable_text_outputfile:
    outf = open(text_outputfile,"w")
    outf.write("# events: " + str(total_events) + "\n")    
    outf.write("# Block 1 - average dN/dy within the pT range: " + '{:5.2f}'.format(pT_min_cut) + " " + '{:5.2f}'.format(pT_max_cut) + " [GeV]\n")
    outf.write("# Columns: (01) rapidity, ")
    for k, v in hadrons.items():
        outf.write('{:02.d}'.format(v[0] + 1) + sp + k + " (" + v[1] + ")")
    outf.write("\n")
    for i in range(ny):
        outf.write(cf.format(y_arr[i]))
        for h in range(nh):
            outf.write(sp + ff.format(y_spectra[h,i]/(dy * total_events)))
        outf.write("\n")
    outf.write("# Block 2 - dN/dpT [1/GeV] within the y rapidity range: " + '{:5.2f}'.format(-rap_cut) + " " + '{:5.2f}'.format(rap_cut) + "\n")
    outf.write("# Columns: (01) pT [GeV], ")
    for k, v in hadrons.items():
        outf.write('{:02.d}'.format(v[0] + 1) + sp + k + " (" + v[1] + ")")
    outf.write("\n")
    for i in range(npT):
        outf.write(cf.format(pT_arr[i]))
        for h in range(nh):
            outf.write(sp + ff.format(pT_spectra[h,i]/(dpT * total_events)))
        outf.write("\n")
    
    outf.close()

with open(outputfile,"wb") as outf:
    info_results = "The pickled file contains a tuple with:\n"
    info_results += "0 this information string\n"
    info_results += "1 the dictionary of the considered hadrons"
    info_results += "2 the total number of events\n"
    info_results += "3 the minimum transverse momentum pT allowed in dN/dy plots\n"
    info_results += "4 the maximum transverse momentum pT allowed in dN/dy plots\n"
    info_results += "5 the absolute value of the rapidity in dN/dpT plots\n"
    info_results += "6 the y rapidity bin array (central points)\n"
    info_results += "7 the pT transverse momentum bin array (central points)\n"
    info_results += "8 the average dN/dy spectra\n"
    info_results += "9 the average dN/dpT spectra\n"

    pickle.dump((info_results, hadrons, total_events, pT_min_cut, pT_max_cut, rap_cut, y_arr, pT_arr, y_spectra, pT_spectra),outf)
