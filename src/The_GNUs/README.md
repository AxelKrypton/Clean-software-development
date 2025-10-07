-Install gnuplot if you do not have already: on Linux run "sudo apt install gnuplot" in the terminal, on Mac run "brew install gnuplot", on Windows download the installer from http://www.gnuplot.info/ and execute it (try to avoid spaces in absolute path of the installation folder)
-Optionally install TeX Live if you do not have already: on Linux run "sudo apt-get install texlive" (if this is not enough: "sudo apt-get install texlive-latex-extra")
-Move to "The_Script"
-Run "python exampleTest.py" in the terminal and check if the test passed
-Then the files "D15.48_me_NEW" and "D15.48_pr_NEW.pdf" (if pdflatex is installed) should be created
(-On Windows I had to manually execute "pdflatex D15.48_pr_NEW.tex" in the Plots folder after the first test execution)
-Compare the PDF file in the folder "Supposed_Outcome"
