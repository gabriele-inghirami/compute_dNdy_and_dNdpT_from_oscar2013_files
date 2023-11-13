### Terminal type and line styles **********

set term pos eps col enh font "Helvetica, 18"
ending=".eps" # please, change it if you change terminal type

# full paths and common initial names of the input files
fA="../results_ideal_"
fB="../results_visc_"

# labels of the plotted curves (for fA and fB, respectively)
tA="Ideal"
tB="Shear"

# common path and initial name of the output files
outfile_comm="./comparisons/"

set style line 1 dt 1 lc "navy" lw 4
set style line 2 dt 2 lc "dark-pink" lw 4

set mxtics 4
set mytics 4

# list of hadrons for file names

had_names = "pion_plus pion_minus pion_0 kaon_plus kaon_minus proton anti-proton neutron anti-neutron"
had_labels = "'{/Symbol p}^+-' '{/Symbol p}^-' '{/Symbol p}^0' 'K^+' 'K^-' 'p' 'anti-p' 'n' 'anti-n'"

# user defined helper functions
max( a, b ) = ( a > b ) ? a : b
min( a, b ) = ( a < b ) ? a : b

# minimum value in logarithmic plots
minlogval=1.e-5

### Plot title **********

tbase= "Au+Au, {/Symbol \326}s=200 GeV, b=10 fm, 1K IC events, "

do for [i=1:words(had_names)] {

  set title tbase.word(had_labels,i)

  ### Plots vs rapidity **********

  set xlabel "y (rapidity)"

  # this is to avoid issues with the stat commands
  set autoscale y
  set autoscale x
  set out outfile_comm."dNdy_vs_rapidity_".word(had_names,i).ending
  set ylabel "dN/dy"
  stat fA.word(had_names,i)."_vs_rapidity.dat" u 2 nooutput
  maxA=STATS_max
  stat fB.word(had_names,i)."_vs_rapidity.dat" u 2 nooutput
  maxB=STATS_max
  maxval=max(maxA, maxB)
  set yrange [0:maxval*1.05]
  set xrange [-5:5]
  plot fA.word(had_names,i)."_vs_rapidity.dat" u 1:2 w l ls 1 t tA, fB.word(had_names,i)."_vs_rapidity.dat" u 1:2 w l ls 2 t tB

  set autoscale y
  set autoscale x
  set out outfile_comm."v1_vs_rapidity_".word(had_names,i).ending
  set ylabel "v_1"
  stat fA.word(had_names,i)."_vs_rapidity.dat" u 3 nooutput
  maxA=STATS_max
  minA=STATS_min
  stat fB.word(had_names,i)."_vs_rapidity.dat" u 3 nooutput
  maxB=STATS_max
  minB=STATS_min
  maxval=max(maxA, maxB)
  minval=min(minA, minB)
  set yrange [minval*1.05:maxval*1.05]
  set xrange [-2:2]
  plot fA.word(had_names,i)."_vs_rapidity.dat" u 1:3 w l ls 1 t tA, fB.word(had_names,i)."_vs_rapidity.dat" u 1:3 w l ls 2 t tB

  set autoscale y
  set autoscale x
  set out outfile_comm."v2_vs_rapidity_".word(had_names,i).ending
  set ylabel "v_2"
  stat fA.word(had_names,i)."_vs_rapidity.dat" u 4 nooutput
  maxA=STATS_max
  minA=STATS_min
  stat fB.word(had_names,i)."_vs_rapidity.dat" u 4 nooutput
  maxB=STATS_max
  minB=STATS_min
  maxval=max(maxA, maxB)
  minval=min(minA, minB)
  set yrange [minval*1.05:maxval*1.05]
  set xrange [-5:5]
  plot fA.word(had_names,i)."_vs_rapidity.dat" u 1:4 w l ls 1 t tA, fB.word(had_names,i)."_vs_rapidity.dat" u 1:4 w l ls 2 t tB

}

do for [i=1:words(had_names)] {

  set title tbase.word(had_labels,i)

  ### Plots vs pT **********

  set xlabel "p_T [GeV]"

  set autoscale y
  set autoscale x
  set out outfile_comm."dNdpT_vs_pT_".word(had_names,i).ending
  set ylabel "dN/dpT [GeV^{-1}]"
  stat fB.word(had_names,i)."_vs_pT.dat" u 2 nooutput
  maxB=STATS_max
  minB=STATS_min
  stat fA.word(had_names,i)."_vs_pT.dat" u 2 nooutput
  maxB=STATS_max
  minB=STATS_min
  maxval=max(maxA, maxB)
  minval=min(minA, minB)
  minval=max(minval, minlogval)
  set yrange [0:maxval*1.05]
  set xrange [0:4]
  plot fA.word(had_names,i)."_vs_pT.dat" u 1:2 w l ls 1 t tA, fB.word(had_names,i)."_vs_pT.dat" u 1:2 w l ls 2 t tB

  set out outfile_comm."dNdpT_vs_pT_".word(had_names,i)."_logscale".ending
  set logscale y
  set autoscale x
  set yrange [minval:maxval*1.2]
  set xrange [0:4]
  set format y "10^{%L}"
  plot fA.word(had_names,i)."_vs_pT.dat" u 1:2 w l ls 1 t tA, fB.word(had_names,i)."_vs_pT.dat" u 1:2 w l ls 2 t tB
  unset logscale y
  set format y

  set out outfile_comm."dNdpT_over_pT_vs_pT_".word(had_names,i)."_logscale".ending
  set logscale y
  set autoscale x
  set autoscale y
  stat fA.word(had_names,i)."_vs_pT.dat" u (($2)/($1)) nooutput
  maxA=STATS_max
  minA=STATS_min
  stat fB.word(had_names,i)."_vs_pT.dat" u (($2)/($1)) nooutput
  maxB=STATS_max
  minB=STATS_min
  maxval=max(maxA, maxB)
  minval=min(minA, minB)
  minval=max(minval, minlogval)
  set xrange [0:4]
  set yrange [minval:maxval*1.2]
  set ylabel "1/p_T dN/dpT [GeV^{-1}]"
  set format y "10^{%L}"
  plot fA.word(had_names,i)."_vs_pT.dat" u 1:(($2)/($1)) w l ls 1 t tA, fB.word(had_names,i)."_vs_pT.dat" u 1:(($2)/($1)) w l ls 2 t tB
  unset logscale y
  set format y

  # we do not print v1 vs pT because usually it is not very interesting

  set autoscale y
  set autoscale x
  set out outfile_comm."v2_vs_pT_".word(had_names,i).ending
  set ylabel "v_2"
  stat fA.word(had_names,i)."_vs_pT.dat" u 4 nooutput
  maxA=STATS_max
  minA=STATS_min
  stat fB.word(had_names,i)."_vs_pT.dat" u 4 nooutput
  maxB=STATS_max
  minB=STATS_min
  maxval=max(maxA, maxB)
  minval=min(minA, minB)
  set yrange [minval*1.05:maxval*1.05]
  set xrange [0:3]
  plot fA.word(had_names,i)."_vs_pT.dat" u 1:4 w l ls 1 t tA, fB.word(had_names,i)."_vs_pT.dat" u 1:4 w l ls 2 t tB

}
