# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:15:00 2025

@author: judith
"""

import numpy as np
import chardet
from fractions import Fraction
from math import gcd

#Laden der Strukturdaten im Uni format
 #RETURN name: KRISTALLNAME, rho: Dichte, nue: Anzahl , alpha/beta/gamma: Winkel Einheitszelle, aK/bK/cK: lattice parameters, 
 #Element: Liste Elemente des Kristalls, nha: Atome pro Einheitszelle für jedes Element, oz: list of atomic numbers, ez: , Mrel: , lamk: Absorptionskanten
 #xh/xk/xl: Atomkoordinaten, tf_anzahl: Zahl der 9er Gruppen, tf_gleiche: , 
def read_crystal_parameters_uni(datdatei):
    element=[]
    atoms_per_unitcell_per_element = []
    atomic_numbers = []
    unitcell = []
    relative_mass = []

    with open(datdatei, "rb") as file:  # Open in binary mode/ in whatever detetected mode
        raw_data = file.read()
        detected = chardet.detect(raw_data)

    with open(datdatei, "r", encoding=detected["encoding"]) as fid:
        molecular_name = fid.readline().strip()
        rho = float(fid.readline().strip())  # [g/cm^3] 
        number_unique_elements = int(fid.readline().strip())  # TODO check this one
        fid.readline()  # Skip one line
        alpha = float(fid.readline().strip())   # [deg]
        beta = float(fid.readline().strip())   # [deg]
        gamma = float(fid.readline().strip())   # [deg]
        aK = float(fid.readline().strip())   # [Angström]
        bK = float(fid.readline().strip())   # [Angström]
        cK = float(fid.readline().strip())   # [Angström]
        
        lambda_k = np.zeros((number_unique_elements, 9)) #Absorption edges TODO: unit?
        xh, xk, xl = [], [], [] #atomic coordinates
        tf_anzahl = [] #Zahl der 9er Gruppen
        max_size=100 #da tf_anzahl noch nicht bekannt (wenn größer als 100 anpassen :) )
        tf_gleiche=np.zeros((number_unique_elements,max_size))
        tfk = np.zeros((number_unique_elements, 3, 9))
        a = np.zeros((number_unique_elements, 9))
        o = np.zeros((number_unique_elements, 8))
        h=1
        
        for i_mol in range(number_unique_elements):
            Elemen = fid.readline().strip()     #TODO: squash 3 lines
            element.append(Elemen)
            element[i_mol]=Elemen
            nrofatoms = int(fid.readline().strip())  # Atoms per unit cell [stück]
            atoms_per_unitcell_per_element.append(nrofatoms)
            Z = int(fid.readline().strip())  # Atomic number [stück]
            atomic_numbers.append(Z)
            unitcell.append(int(fid.readline().strip()))
            relative_mass.append(float(fid.readline().strip()))
            fid.readline()  # Skip one line
            for j in range(9):
                lambda_k[i_mol, j] = float(fid.readline().strip())
                
            fid.readline()  # Skip one line 
            for j in range(atoms_per_unitcell_per_element[i_mol]): #Atomkoordinaten
                #xh_wert=float(fid.readline().strip())
                #xk_wert=float(fid.readline().strip())
                #xl_wert=float(fid.readline().strip())
                #xh_list.append(xh)
                #xh[j][i]=xh_wert
                #xk[j][i]=xh_wert
                #xl[j][i]=xh_wert
                xh.append(float(fid.readline().strip()))
                xk.append(float(fid.readline().strip()))
                xl.append(float(fid.readline().strip()))
                h += 1
           
                
            fid.readline()  # Skip one line DWF
            tf_anzahl.append(int(fid.readline().strip()))  # Number of 9-groups 
            count=0 #wird zur Größenbestimmung von tf_gleiche notwendig
            for j in range(tf_anzahl[i_mol]):
                 #tf_gleiche_i.append(int(fid.readline().strip()))
                 tf_gleiche_i=int(fid.readline().strip())
                # tf_gleiche.append(tf_gleiche_i)
                 tf_gleiche[i_mol,j]=tf_gleiche_i
                 count+=1
            tf_gleiche = tf_gleiche[i_mol, :count].reshape(number_unique_elements, count) # schneidet nur einträge raus (max-size wird damit unwichtig)
            fid.readline()  # Skip one line DWF-Koeffizienten
            for j in range(tf_anzahl[i_mol]):
                for g in range(9):
                    tfk[i_mol, j, g] = float(fid.readline().strip())
        
            fid.readline()  # Skip one line Atomstreufaktor
            for j in range(9):
                a[i_mol, j] = float(fid.readline().strip())
        
            fid.readline()  # Skip one line Abschirmkonstanten
            for j in range(8):
                o[i_mol, j] = float(fid.readline().strip())
    #print(Element)
    
             
    return molecular_name, rho, number_unique_elements, alpha, beta, gamma, aK, bK, cK, element, atoms_per_unitcell_per_element, atomic_numbers, unitcell, relative_mass, lambda_k, xh, xk, xl, tf_anzahl, tf_gleiche, tfk, a, o
               
def base_vector_tricline(aK,bK,cK,alpha,beta,gamma):
    #base vectors triclinic crystal
    a1=np.array([aK,0,0])
    a2=np.array([bK*np.cos(np.radians(gamma)),bK*np.sin(np.radians(gamma)),0])
    a3_x=cK*np.cos(np.radians(beta))
    a3_y=cK*(np.cos(np.radians(alpha))-np.cos(np.radians(beta))*np.cos(np.radians(gamma)))/np.sin(np.radians(gamma))
    a3_z=np.sqrt(cK**2-a3_x**2-a3_y**2)
    a3=np.array([a3_x,a3_y,a3_z])

    #matrix base vectors
    A=np.column_stack([a1,a2,a3]) 
    return a1,a2,a3,A 

def reciprocal_vector(a1_R,a2_R,a3_R):
    #reciprocal lattice vectors
    Vc=np.dot(a1_R,(np.cross(a2_R,a3_R)))

    b1=2*np.pi/Vc*(np.cross(a2_R,a3_R)) 
    b2=2*np.pi/Vc*(np.cross(a3_R,a1_R))
    b3=2*np.pi/Vc*(np.cross(a1_R,a2_R))

    B=np.column_stack([b1,b2,b3]) #reciprocal base of the oriented crystal
    return b1,b2,b3,B 

def G_surface(hkl_raw,b1,b2,b3):
    # check orientation of G_surface
    G_surface = hkl_raw[0]*b1 + hkl_raw[1]*b2 + hkl_raw[2]*b3
    G_surface_unit= G_surface/np.linalg.norm(G_surface)
    return G_surface, G_surface_unit
          

#Berechnen des Einheitszellenvolumens und Netebenenabstandes
def calculate_volume_and_dhkl(alpha, beta, gamma, a, b, c, h, k, l):
    # Physical constants
    re = 2.817696e-5  # Electron radius in Angstrom
    
    # Calculate Volume and dhkl
    s11 = b**2 * c**2 * (np.sin(np.radians(alpha)))**2
    s22 = a**2 * c**2 * (np.sin(np.radians(beta)))**2
    s33 = a**2 * b**2 * (np.sin(np.radians(gamma)))**2
    s12 = a * b * c**2 * (np.cos(np.radians(alpha)) * np.cos(np.radians(beta)) - np.cos(np.radians(gamma)))
    s23 = a**2 * b * c * (np.cos(np.radians(beta)) * np.cos(np.radians(gamma)) - np.cos(np.radians(alpha)))
    s13 = a * b**2 * c * (np.cos(np.radians(gamma)) * np.cos(np.radians(alpha)) - np.cos(np.radians(beta)))
    s=min(min(s11,s22),s33)
    
    Vsq = (a**2 * b**2 * c**2 * (1 - np.cos(np.radians(alpha))**2 - np.cos(np.radians(beta))**2 - np.cos(np.radians(gamma))**2 
                                  + 2 * np.cos(np.radians(alpha)) * np.cos(np.radians(beta)) * np.cos(np.radians(gamma))))
    Volume = np.sqrt(Vsq)
    dhkl = np.sqrt(Vsq / (s11 * h**2 + s22 * k**2 + s33 * l**2 + 2 * s12 * h * k + 2 * s23 * k * l + 2 * s13 * h * l))
    
    return s11,s22,s33,s12,s23,s13,s,Vsq,Volume, dhkl

def calculate_volume(alpha, beta, gamma, a, b, c):
    # Physical constants
    re = 2.817696e-5  # Electron radius in Angstrom
    
    # Calculate Volume 
    s11 = b**2 * c**2 * (np.sin(np.radians(alpha)))**2
    s22 = a**2 * c**2 * (np.sin(np.radians(beta)))**2
    s33 = a**2 * b**2 * (np.sin(np.radians(gamma)))**2
    s12 = a * b * c**2 * (np.cos(np.radians(alpha)) * np.cos(np.radians(beta)) - np.cos(np.radians(gamma)))
    s23 = a**2 * b * c * (np.cos(np.radians(beta)) * np.cos(np.radians(gamma)) - np.cos(np.radians(alpha)))
    s13 = a * b**2 * c * (np.cos(np.radians(gamma)) * np.cos(np.radians(alpha)) - np.cos(np.radians(beta)))
    s=min(min(s11,s22),s33)
    
    Vsq = (a**2 * b**2 * c**2 * (1 - np.cos(np.radians(alpha))**2 - np.cos(np.radians(beta))**2 - np.cos(np.radians(gamma))**2 
                                  + 2 * np.cos(np.radians(alpha)) * np.cos(np.radians(beta)) * np.cos(np.radians(gamma))))
    Volume = np.sqrt(Vsq)
    
    return s,s11,s22,s33,s12,s23,s13,s,Vsq,Volume

#
def azimuth_90degree_to_startdirection(datdatei,startdirection, surfnormal):
    """
    Find 90 degree azimuth
    Example:
    surfnormal=[1,0,0] :hkl surface
    startdirection=[0,1,0]
    -> result: [0,0,1]
    """
    name, rho, nue, alpha, beta, gamma, aK, bK, cK, \
        Element, nha, oz, ez, Mrel, lamk, xh, xk, xl, tf_anzahl, tf_gleiche, tfk, a, o =  read_crystal_parameters_uni(datdatei)
    av,bv,cv,am,bm=perpendicular_vector(aK,bK,cK,alpha,beta,gamma)

    # Compute vek = cross product of transformed vectors
    vek = np.cross(np.dot(bm, surfnormal), np.dot(bm, startdirection))

    # Convert vek to rational approximation with a tolerance of 1e-9
    rat_vek = np.array([Fraction(v).limit_denominator(int(1e9)) for v in vek])

    # Extract numerators and denominators
    n = np.array([rat.numerator for rat in rat_vek])
    d = np.array([rat.denominator for rat in rat_vek])

    # Compute least common multiple (LCM) of denominators
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    dummy = lcm(lcm(d[0], d[1]), d[2])  # Compute LCM of all denominators
    dummy2 = (dummy / d) * n  # Scale numerators

    # Compute greatest common divisor (GCD) of the scaled numerators
    dummy3 = gcd(gcd(int(dummy2[0]), int(dummy2[1])), int(dummy2[2]))
    
    # Normalize by dividing by GCD
    dummy2 = dummy2 / dummy3

    # Extract final values
    pdh, pdk, pdl = int(dummy2[0]), int(dummy2[1]), int(dummy2[2])

    return pdh, pdk, pdl


def unwrap_like_matlab(phi):
    unwrapped = np.zeros_like(phi)
    unwrapped[0] = phi[0]
    for i in range(1, len(phi)):
        delta = phi[i] - phi[i - 1]
        delta_mod = (delta + np.pi) % (2 * np.pi) - np.pi
        if delta_mod == -np.pi and delta > 0:
            delta_mod = np.pi
        unwrapped[i] = unwrapped[i - 1] + delta_mod
    return unwrapped

def unwrap_like_matlab(phi):
    out = np.zeros_like(phi)
    out[0] = phi[0]
    for i in range(1, len(phi)):
        delta = phi[i] - phi[i - 1]
        delta = (delta + np.pi) % (2 * np.pi) - np.pi
        out[i] = out[i - 1] + delta
    return out

# Function to unwrap with MATLAB-style continuity
def unwrap_with_global_trend(phi):
    out = np.zeros_like(phi)
    out[0] = phi[0]
    for i in range(1, len(phi)):
        delta = phi[i] - phi[i - 1]
        delta_mod = (delta + np.pi) % (2 * np.pi) - np.pi
        if delta_mod == -np.pi and delta > 0:
            delta_mod = np.pi
        out[i] = out[i - 1] + delta_mod
    return out

#perpendicular vctor
def perpendicular_vector(aK,bK,cK,alpha,beta,gamma):
    # Assume angles are in degrees
    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)
    gamma_rad = np.radians(gamma)
    # Direct lattice vectors
    av = aK * np.array([1, 0, 0])
    bv = bK * np.array([np.cos(gamma_rad), np.sin(gamma_rad), 0])
    cv = cK * np.array([np.cos(beta_rad),(np.cos(alpha_rad) - np.cos(gamma_rad) * np.cos(beta_rad)) / np.sin(gamma_rad), \
                        np.sqrt(np.sin(beta_rad)**2 -((np.cos(alpha_rad) - np.cos(gamma_rad) * np.cos(beta_rad))**2) / (np.sin(gamma_rad)**2))])
    # Combine into matrix
    am = np.column_stack((av, bv, cv))
    bm = np.linalg.inv(am)
    return av,bv,cv,am,bm

def maximum_hkl(datdatei,lambda_):
    
    name, rho, nue, alpha, beta, gamma, aK, bK, cK, \
        Element, nha, oz, ez, Mrel, lamk, xh, xk, xl, tf_anzahl, tf_gleiche, tfk, a, o =  read_crystal_parameters_uni(datdatei)
    s,s11,s22,s33,s12,s23,s13,s,Vsq,Volume=calculate_volume(alpha, beta, gamma, aK, bK, cK)
    
    i=0
    for h in range(1, 21):
        dhkl=np.sqrt(Vsq / (s * h**2))
        if lambda_ / (2 * dhkl) <= 1:
            ii = h
    return ii

def Auswahlregel_Beryllium(h,k,l):
    # (00l): nur gerade l erlaubt
    if h == 0 and k == 0:
        return l % 2 == 0
    # (h0l): h + l muss gerade sein
    elif k == 0 and l != 0:
        return (h + l) % 2 == 0
    # (0kl): k + l muss gerade sein
    elif h == 0 and l != 0:
        return (k + l) % 2 == 0
    # (hk0): h + 2k durch 3 teilbar
    elif l == 0:
        return (h + 2 * k) % 3 == 0
    else:
        # optional: immer erlauben wenn keine spezielle Regel greift
        return True
    
def Auswahlregel_Silizium(h, k, l):
    hkl_sum_even = (h + k + l) % 2 == 0
    same_parity = (h % 2 == k % 2) & (k % 2 == l % 2)
    divisible_by_4 = (h + k + l) % 4 == 0
    return hkl_sum_even & same_parity & divisible_by_4