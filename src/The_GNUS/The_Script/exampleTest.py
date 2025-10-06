import numpy as np
import sys
import os
from subprocess import run, PIPE
from pathlib import Path
import shutil

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


output = shell(f'gnuplot -e binsize1={BINSIZE[1]} -e binsize2={BINSIZE[2]} -e binsize3={BINSIZE[3]} -e binsize4={BINSIZE[4]} -e binsize5={BINSIZE[5]} -e binsize6={BINSIZE[6]} -e binsize7={BINSIZE[7]} -e binsize8={BINSIZE[8]} -e binsize9={BINSIZE[9]} -e binsize10={BINSIZE[10]} -e gf=0 -e alt=0 D15.48_pr_NEW.gp')



if shutil.which('pdflatex'): shell('pdflatex Plots/D15.48_pr_NEW.tex')

this_fit = os.path.join(os.path.dirname(__file__), "D15.48_me_NEW")
with open(this_fit) as f:
   this_fit_parameters = f.read()
supposed_fit = os.path.join(os.path.dirname(__file__), "Supposed_Outcome/D15.48_me_NEW")
with open(supposed_fit) as f:
   supposed_fit_parameters = f.read()



tol = 1e-8
for i, line in enumerate(this_fit_parameters.splitlines()):
    if i>0:  #skip first line with comments
        for k, entry in enumerate(line.split()):
            entry = float(entry)
            comp_entry = float(supposed_fit_parameters.splitlines()[i].split()[k])
            if not np.isclose(entry, comp_entry, rtol=tol):
                print('================')
                print(output)
                print('================')
                print(f"The test has failed. These fit parameters differ from the supposed outcome by the tolerance of {tol}.")
                print(f"Entry {k} in line {i} ({entry}) differs from supposed outcome ({comp_entry}).")
                sys.exit(1)

print("The test has passed. The fit parameters are identical to the supposed outcome.")
