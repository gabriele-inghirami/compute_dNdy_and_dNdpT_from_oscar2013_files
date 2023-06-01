## Introduction
This repository contains python3 scripts to produce spectra vs rapidity and pT from Oscar 2013 files.

- compute_dNdy_and_dNdpT_from_oscar_file.py is the main script that computes dN/dy and dN/dpT for a list of selected hadrons
- combine_results.py sums up the results of different executions of compute_dNdy_and_dNdpT_from_oscar_file.py
- to_text.py converts the pickle output into human readable text format

### compute_dNdy_and_dNdpT_from_oscar_file.py

This program reads one or many Oscar 2013 files and writes in an output pickle file:

- a string with a short description of the other contents of the pickle archive
- the python dictionary of the selected hadrons
- the total number of events (numpy.int64)
- the minimum transverse momentum pT allowed in dN/dy plots (hardcoded parameter pT_min_cut)
- the maximum transverse momentum pT allowed in dN/dy plots (hardcoded parameter pT_max_cut)
- the maximum absolute value of the rapidity in dN/dpT plots (hardcoded parameter rap_cut)
- the y rapidity bin array (central points) (determined by the hardcoded parameters max_rapidity and rap_resolution)
- the pT transverse momentum bin array (central points) (determined by the harcoded parameters max_pT and pT_resolution)
- the y rapidity bin width dy
- the pT transverse momentum bin width dpT
- the average dN/dy spectra (numpy.int64) dimensions: number of hadrons and of y bins
- the average dN/dpT spectra (numpy.int64) dimensions: number of hadrons and of pT bins

Usage: `python3 compute_dNdy_and_dNdpT_from_oscar_file.py [-h] [--output OUTPUT] [--verbose] inputs [inputs ...]`

positional arguments:
  inputs                Oscar 2013 input files (it can be just one filename path or many, separated by spaces)

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Path to the output file (pickle format). Default is "./output.pickle".
  --verbose, -v         increase output verbosity

### combine_results.py

This program combines the results of several output pickle files produced by compute_dNdy_and_dNdpT_from_oscar_file.py

Usage: `python3 combine_results.py <outputfile> <inputfile 1> <inputfile 2> ... [inputfile n]`

(The minimum number of input files is 2)

### to_text.py

This program converts the pickle output into human readable text format.

Usage: `python3 to_text.py <input file in pickle format> <output file in text format>`

Warning: if there is already a file named as the output file, it is simply overwritten without any check!
