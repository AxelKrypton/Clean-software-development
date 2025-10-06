import os
import sys
from math import isclose
sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from Kristallite import crystallite

def functional_test():
    datdatei = os.path.join(os.path.dirname(__file__), "DATA/SILIZIUM.DAT")
    lambda_=1.5406 #Wavelength in Angström
    t=30 # thickness of the crystal in mu m
    nseed = 10
    assert isclose(cristallite(datdatei,lambda_,t,nseed),-3.6059854189874456e-34,abs_tol=0.0001)
    
