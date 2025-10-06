import numpy as np
from subprocess import run, PIPE

def shell(*args):
    """ 
    Carry out the passed arguments args in the shell. Can be passed as a single
    string or as a list. Captures and returns output of shell command. E.g.
        shell('ls -lah')
    """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,check=True,stderr=PIPE,stdout=PIPE,universal_newlines=True)
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

print('================')
print(output)

