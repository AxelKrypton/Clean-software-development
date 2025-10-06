import subprocess
import sys
import os

gnuplot_path = 'c:/Program_Files/gnuplot/bin/gnuplot.exe' #change this according to your gnuplot installation
script_path = os.path.dirname(__file__) + "/The_Script/D15.48_pr_NEW.gp"

proc = subprocess.Popen([gnuplot_path,'-p', script_path],
                        shell=True,
                        stdin=subprocess.PIPE,
                        )















#######################  Basic gnuplot functionality test
#proc = subprocess.Popen([gnuplot_path,'-p'], 
#                        shell=True,
#                        stdin=subprocess.PIPE,
#                        )
#proc.stdin.write(b'set xrange [0:10]; set yrange [-2:2]\n')
#proc.stdin.write(b'plot sin(x)\n')
#proc.stdin.write(b'quit\n') #close the gnuplot window
#proc.stdin.flush()
########################