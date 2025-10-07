#!/bin/bash

BINSIZE[10]=6.9e-3
BINSIZE[9]=2.9e-3
BINSIZE[8]=2.9e-3
BINSIZE[7]=4.3e-3
BINSIZE[6]=12.4e-3
BINSIZE[5]=9.6e-3
BINSIZE[4]=5.5e-3
BINSIZE[3]=3.8e-3
BINSIZE[2]=3.4e-3
BINSIZE[1]=4.4e-3

gnuplot -e binsize1=${BINSIZE[1]} -e binsize2=${BINSIZE[2]} -e binsize3=${BINSIZE[3]} -e binsize4=${BINSIZE[4]} -e binsize5=${BINSIZE[5]} -e binsize6=${BINSIZE[6]} -e binsize7=${BINSIZE[7]} -e binsize8=${BINSIZE[8]} -e binsize9=${BINSIZE[9]} -e binsize10=${BINSIZE[10]} -e gf=0 -e alt=0 D15.48_pr_NEW.gp

cd Plots
pdflatex D15.48_pr_NEW.tex
cd ..
