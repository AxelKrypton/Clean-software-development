import subprocess
import sys
import os

#Let it work on Windows or Unix
if "-win" in sys.argv: gnuplot_path = 'c:/Program_Files/gnuplot/bin/gnuplot.exe'
else: gnuplot_path = "gnuplot"

script_path = os.path.join(os.path.dirname(__file__),"The_Script","D15.48_pr_NEW.gp")

BINSIZE = [6.9e-3,2.9e-3,2.9e-3,4.3e-3,12.4e-3,9.6e-3,5.5e-3,3.8e-3,3.4e-3,4.4e-3]

proc = subprocess.Popen([gnuplot_path,'-e', f"binsize1={BINSIZE[0]}", 
						 			  '-e', f"binsize2={BINSIZE[1]}", 
						 			  '-e', f"binsize3={BINSIZE[2]}", 
						 			  '-e', f"binsize4={BINSIZE[3]}", 
						 			  '-e', f"binsize5={BINSIZE[4]}", 
						 			  '-e', f"binsize6={BINSIZE[5]}", 
						 			  '-e', f"binsize7={BINSIZE[6]}", 
						 			  '-e', f"binsize8={BINSIZE[7]}", 
						 			  '-e', f"binsize9={BINSIZE[8]}", 
						 			  '-e', f"binsize10={BINSIZE[9]}",
									  '-e', 'gf=0',
									  '-e', "alt=0", script_path],
                        shell=True,
                        stdin=subprocess.PIPE
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