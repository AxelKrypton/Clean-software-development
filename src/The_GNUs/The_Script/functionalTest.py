import numpy as np
import sys
import os
from subprocess import run, PIPE
from pathlib import Path
import shutil

from run import run_gnuplot
from gnucode import get_gnuplot_code
import numpy as np
BINSIZE = np.zeros(11)

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
BINSIZE[0]=-1


extra_options=["-e", "gf=0", "-e", "alt=0"]

# build options as ["-e", "BINSIZE1=6.9e-3", "-e", "BINSIZE2=2.9e-3", ...]


OPTIONS = []
for i, val in enumerate(BINSIZE[1:], start=1):
    OPTIONS += ["-e", f"binsize{i}={val}"]
OPTIONS+=extra_options
# run gnuplot with your inline code
# out, err = run_gnuplot(get_gnuplot_code(), OPTIONS)
# print("STDERR:", err)

output,err = run_gnuplot(get_gnuplot_code(),OPTIONS)
def shell(*args):
    """ 
    Carry out the passed arguments args in the shell. Can be passed as a single
    string or as a list. Captures and returns output of shell command. E.g.
        shell('ls -lah')
    """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,stderr=PIPE,stdout=PIPE,universal_newlines=True)
    return process.stderr
#!/bin/bash

# TODO: uncomment
# if shutil.which('pdflatex'): shell('pdflatex Plots/D15.48_pr_NEW.tex')

this_fit = os.path.join(os.path.dirname(__file__), "D15.48_me_NEW")
with open(this_fit) as f:
   this_fit_parameters = f.read()
supposed_fit = os.path.join(os.path.dirname(__file__), "Supposed_Outcome/D15.48_me_NEW")
with open(supposed_fit) as f:
   supposed_fit_parameters = f.read()



rtol = 1e-8
for i, line in enumerate(this_fit_parameters.splitlines()):
    if i>0:  #skip first line with comments
        for k, entry in enumerate(line.split()):
            entry = float(entry)
            comp_entry = float(supposed_fit_parameters.splitlines()[i].split()[k])
            if not np.isclose(entry, comp_entry, rtol=rtol, atol=0):
                print('================')
                print(output)
                print('================')
                print(f"The test has failed. These fit parameters differ from the supposed outcome by the tolerance of {rtol}.")
                print(f"Entry {k} in line {i} ({entry}) differs from supposed outcome ({comp_entry}).")
                sys.exit(1)

print("The test has passed. The fit parameters are identical to the supposed outcome.")

# performe_fits() == r'''
#         a10=100.0
#         b10=-1000.0
#         c10=10000.0
#         d10=-1000.0
#         x10=0.05
#         y10=0.1
#         xl10=0.0					
#         xr10=0.0735
#         fit [xl10:xr10] f10(x) "../Data/D15.48/relvol.Nt24_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x10,y10,a10,b10,c10
#         redchisqr10=FIT_STDFIT**2
# '''