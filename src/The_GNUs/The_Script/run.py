import subprocess, tempfile, os
import sys, platform, shutil


def get_gnuplot_path():
    system = platform.system()
    if system == "Windows":
        # try default installation path, fallback to PATH
        path = r"c:/Program Files/gnuplot/bin/gnuplot.exe"
        return path if os.path.exists(path) else shutil.which("gnuplot")
    else:
        # Linux, macOS, etc.
        return shutil.which("gnuplot") or "gnuplot"

def run_gnuplot(gnuplot_code, options=None):
    if options is None:
        options = []

    # create a temporary file
    with tempfile.NamedTemporaryFile("w", suffix=".gp", delete=False) as f:
        f.write(gnuplot_code)
        f.flush()
        script_path = f.name

    args = [get_gnuplot_path()] + options + [script_path]

    try:
        proc = subprocess.run(args,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
        return proc.stdout, proc.stderr
    finally:
        os.remove(script_path)  # cleanup
