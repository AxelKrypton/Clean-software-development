def set_terminal_parameters():
    return (r'set terminal epslatex size 15.11787cm,20cm standalone header "\\usepackage{amsmath,amstext,amssymb} \n \\usepackage[utf8]{inputenc} \n \\usepackage[outdir=./]{epstopdf} \n \
    \\renewcommand{\\bar}[1]{\\mkern 1.5mu\\overline{\\mkern-1.5mu#1\\mkern-1.5mu}\\mkern 1.5mu} \n \\graphicspath{{../}}  \n \\newcommand{\\upright}[1]{\\mathsf{#1}} \n \
    \\renewcommand{\\familydefault}{\\sfdefault} \n \\usepackage{sfmath}" font ",11" linewidth 4' + "\n\n")

def set_initial_fit_parameters(num_fit_functions):
    a_initial_value = 100.0
    b_initial_value = -1000.0
    c_initial_value = 10000.0
    d_initial_value = -1000.0

    string = ""
    for i in range(1, num_fit_functions+1):
        string += f"a{i}="
    string += f"{a_initial_value}\n"

    for i in range(1, num_fit_functions+1):
        string += f"b{i}="
    string += f"{b_initial_value}\n"

    for i in range(1, num_fit_functions+1):
        string += f"c{i}="
    string += f"{c_initial_value}\n"

    for i in range(1, num_fit_functions+1):
        string += f"d{i}="
    string += f"{d_initial_value}\n"

    return string + "\n"

def define_fit_model_functions(num_fit_functions):
    string = ""
    for i in range(1, num_fit_functions+1):
        string += f"f{i}(x)=y{i}+a{i}*(x-x{i})+b{i}*(x-x{i})**3+c{i}*(x-x{i})**4\n"
    return string + "\n"

#TODO
def perform_fits(bool: gf, bool: alt):
    #TODO: generate the code to perform fits here
    raise NotImplementedError()
    
#TODO
def configure_multiplot():
    raise NotImplementedError()

#TODO
def create_multiplot_with_data_and_fit_curve():
    raise NotImplementedError()
    



def main():
    GNUPLOT_SCRIPT_STRING = ""
    NUM_FIT_FUNCTIONS = 10

    GNUPLOT_SCRIPT_STRING += set_terminal_parameters()
    GNUPLOT_SCRIPT_STRING += set_initial_fit_parameters(NUM_FIT_FUNCTIONS)
    GNUPLOT_SCRIPT_STRING += define_fit_model_functions(NUM_FIT_FUNCTIONS)
    
    # Not Implemented yet
    #GNUPLOT_SCRIPT_STRING += perform_fits()
    #GNUPLOT_SCRIPT_STRING += configure_multiplot()
    #GNUPLOT_SCRIPT_STRING += create_multiplot_with_data_and_fit_curve()

    #TODO: generate the rest of the gnuplot code and add it to GNUPLOT_SCRIPT_STRING
    # Then pass the GNUPLOT_SCRIPT_STRING to the python wrapper to run gnuplot

    #Debug print statement
    print(GNUPLOT_SCRIPT_STRING)

    return

if __name__=="__main__":
    main()


