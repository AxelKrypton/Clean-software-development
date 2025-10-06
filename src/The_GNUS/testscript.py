import subprocess
import sys

gnuplot_path = 'c:/Program_Files/gnuplot/bin/gnuplot.exe' #change this according to your gnuplot installation

proc = subprocess.Popen([gnuplot_path,'-p'], 
                        shell=True,
                        stdin=subprocess.PIPE,
                        )
proc.stdin.write(b'set xrange [0:10]; set yrange [-2:2]\n')
proc.stdin.write(b'plot sin(x)\n')
proc.stdin.write(b'quit\n') #close the gnuplot window
proc.stdin.flush()
