# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:07:05 2025

@author: judith
"""

import scipy.io
import numpy as np

#%% 
def Henke(lambda_, el):
    #convert henke_search.mat to henke_search.npz
    mat_data = scipy.io.loadmat('henke_search.mat')
    
    # Save as NumPy compressed format
    np.savez('henke_search.npz', 
             element=mat_data['element'].flatten(), 
             bytepos=mat_data['bytepos'].flatten(), 
             ln=mat_data['ln'].flatten())
    
    # Load precomputed element metadata from henke_search.npz
    data = np.load('henke_search.npz', allow_pickle=True)
    elements = data['element']
    bytepos = data['bytepos']
    ln = data['ln']

    # if isinstance(el, np.ndarray): #does it work for muliple elements?? No it doesnt
    #     el= el[0][0]
    #     print(el)
    # # Find element position (case-insensitive)
    if isinstance(el, str):
        el_lower = el.lower()
    else:
        #el_lower = np.char.lower(el)
        el_lower = np.vectorize(str.lower)(el)

    elementpos = np.where(np.char.lower(elements) == el_lower)[0]
    #elementpos = np.where(np.char.lower(elements) == el.lower())[0]
    if len(elementpos) == 0:
        raise ValueError(f"Element '{el}' not found in Henke.dat.")
    
    elementpos = elementpos[0]  # Extract first matching index
    
    #print(elementpos)
    # Convert wavelength to energy
    energy = 12398.41876 / lambda_  # Convert wavelength (Å) to energy (eV)
    
    # Open the file and seek to the element position
    with open('Henke.dat', 'r') as fid:
        fid.seek(bytepos[elementpos])  # Move to element's byte position
        fid.readline()  # Skip element name
        # Read only numeric data (ignoring non-numeric lines)
        num_lines = ln[elementpos + 1] - ln[elementpos]
        raw_data = []
        for _ in range(num_lines):
            line = fid.readline().strip()
            try:
                values = [float(x) for x in line.split()]
                if len(values) == 3:  # Ensure correct format (3 columns)
                    raw_data.append(values)
            except ValueError:
                continue  # Ignore non-numeric lines
    
    # Convert to NumPy array
    data = np.array(raw_data)
    if data.ndim == 1:
        data = data.reshape(-1, 3)  
    
    # Find the index of the first energy value greater than or equal to the given energy
    p = np.where(data[:, 0] >= energy)[0][0]  # Equivalent to MATLAB `find(...,1)`

    #p = np.searchsorted(data[:, 0], energy)
    #print(p)
    # Ensure we have enough points for interpolation
    if p >= 3 and (p + 2) < len(data):
        x_points = data[p-3:p+3, 0]  # Energy values
        y_points = data[p-3:p+3, 2]  # f2 values
    else:
        x_points = data[max(0, p-3):p+1, 0]
        y_points = data[max(0, p-3):p+1, 2]
    # Perform PCHIP interpolation
    interpolator = scipy.interpolate.PchipInterpolator(x_points, y_points)
    f2 = interpolator(energy)
    return f2

