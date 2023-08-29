### Terminal type and line styles **********

set term pos eps col enh font "Helvetica, 18"
ending=".eps" # please, change it if you change terminal type

common_name="test_AuAu_1000_events_"

set style line 1 dt 1 lc "navy" lw 4

set mxtics 4
set mytics 4

# list of hadrons for file names

had_names = "pion_plus pion_minus pion_0 kaon_plus kaon_minus proton anti-proton neutron anti-neutron"
had_labels = "'{/Symbol p}^+-' '{/Symbol p}^-' '{/Symbol p}^0' 'K^+' 'K^-' 'p' 'anti-p' 'n' 'anti-n'"

### Plot title **********

tbase= "Au+Au, {/Symbol \326}s=200 GeV, b=10 fm, 1K IC events, 100K samplings, "

do for [i=1:words(had_names)] {

  set title tbase.word(had_labels,i)

  ### Plots vs rapidity **********

  set xlabel "y (rapidity)"

  # this is to avoid issues with the stat commands
  set autoscale y
  set autoscale x
  set out "dNdy_vs_rapidity_".word(had_names,i).ending
  set ylabel "dN/dy"
  stat common_name.word(had_names,i)."_vs_rapidity.dat" u 2 nooutput
  set yrange [0:STATS_max*1.05]
  set xrange [-5:5]
  plot common_name.word(had_names,i)."_vs_rapidity.dat" u 1:2 w l ls 1 t ""

  set autoscale y
  set autoscale x
  set out "v1_vs_rapidity_".word(had_names,i).ending
  set ylabel "v_1"
  stat common_name.word(had_names,i)."_vs_rapidity.dat" u 3 nooutput
  set yrange [STATS_min*1.05:STATS_max*1.05]
  set xrange [-2:2]
  plot common_name.word(had_names,i)."_vs_rapidity.dat" u 1:3 w l ls 1 t ""

  set autoscale y
  set autoscale x
  set out "v2_vs_rapidity_".word(had_names,i).ending
  set ylabel "v_2"
  stat common_name.word(had_names,i)."_vs_rapidity.dat" u 4 nooutput
  set yrange [STATS_min*1.05:STATS_max*1.05]
  set xrange [-5:5]
  plot common_name.word(had_names,i)."_vs_rapidity.dat" u 1:4 w l ls 1 t ""

  set xlabel "p_T [GeV]"

  set autoscale y
  set autoscale x
  set out "dNdpT_vs_pT_".word(had_names,i).ending
  set ylabel "dN/dpT [GeV^{-1}]"
  stat common_name.word(had_names,i)."_vs_pT.dat" u 2 nooutput
  set yrange [0:STATS_max*1.05]
  set xrange [0:4]
  plot common_name.word(had_names,i)."_vs_pT.dat" u 1:2 w l ls 1 t ""

  set out "dNdpT_vs_pT_".word(had_names,i)."_logscale".ending
  set logscale y
  set autoscale x
  set yrange [STATS_min:STATS_max*1.2]
  set xrange [0:4]
  set format y "10^{%L}"
  plot common_name.word(had_names,i)."_vs_pT.dat" u 1:2 w l ls 1 t ""
  unset logscale y
  set format y

  # we do not print v1 vs pT because usually it is not very interesting

  set autoscale y
  set autoscale x
  set out "v2_vs_pT_".word(had_names,i).ending
  set ylabel "v_2"
  stat common_name.word(had_names,i)."_vs_pT.dat" u 4 nooutput
  set yrange [STATS_min*1.05:STATS_max*1.05]
  set xrange [0:3]
  plot common_name.word(had_names,i)."_vs_pT.dat" u 1:4 w l ls 1 t ""

}
