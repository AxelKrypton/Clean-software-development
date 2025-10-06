# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 09:54:09 2025

@author: judith
"""

import os

import numpy as np

#from someDefs import Auswahlregel_Beryllium
#from someDefs import Auswahlregel_Silizium
from scipy.spatial.transform import Rotation
from someDefs import read_crystal_parameters_uni,base_vector_tricline,reciprocal_vector,G_surface
from susi2 import susi2
#from math import gcd
#from functools import reduce

#possible input:
    #datdatei = os.path.join(os.path.dirname(__file__), "DATA/SILIZIUM.DAT")
    #lambda_=1.5406 #Wavelength in Angström
    #t=30 # thickness of the crystal in mu m
#%%
def crystallite(datdatei,lambda_,t,nseed=None):

    #incident beam along z-axis (normiert)
    Einfall=np.array([0, 0, 1])
    Einfall = Einfall / np.linalg.norm(Einfall)
    #%%
    #read crystal data
    name, rho, nue, alpha, beta, gamma, aK, bK, cK, Element, nha, oz, ez, Mrel, lamk, xh, xk, xl, tf_anzahl, tf_gleiche, tfk, a, o =read_crystal_parameters_uni(datdatei)
    
    a1,a2,a3,A=base_vector_tricline(aK,bK,cK,alpha,beta,gamma)
    
    # random orientation base vectors
    random_rot = Rotation.random(rng=nseed)
    Rotationsmatrix=random_rot.as_matrix()
    A_rotiert=Rotationsmatrix @ A
    
    #rotadet base vectors
    a1_R=A_rotiert[0,:]
    a2_R=A_rotiert[1,:]
    a3_R=A_rotiert[2,:]
    
    
    b1,b2,b3,B=reciprocal_vector(a1_R,a2_R,a3_R)
    #%% latticeplane of the surface (antiparallel to incident beam) 
    X = np.column_stack([B, Einfall])
    _, _, Vt = np.linalg.svd(X)
    
    # last vector of V^T
    solution = Vt[-1, :]  # [h, k, l, const]
    
    hkl_raw = solution[:3] / solution[3]  #  geteilt duch const

    G_surface_vec,G_surface_unit=G_surface(hkl_raw,b1,b2,b3)
    
    cos_theta_surface = np.dot(G_surface_unit, Einfall)
    theta_surface = np.degrees(np.arccos(np.clip(cos_theta_surface, -1, 1)))
    
    #%% 
    #Array with all hkl combinations
    max_=20 #20
    h_values = np.arange(-max_, max_ + 1)
    k_values = np.arange(-max_, max_+ 1)
    l_values = np.arange(-max_, max_ + 1)
    h, k, l = np.meshgrid(h_values, k_values, l_values, indexing='ij') 
    hkl = np.stack([h.flatten(), k.flatten(), l.flatten()], axis=-1) 
    hkl = hkl[~np.all(hkl == 0, axis=1)] 
    
    #G for all combinations
    h_allg=hkl[:,0][:, np.newaxis]
    k_allg=hkl[:,1][:, np.newaxis]
    l_allg=hkl[:,2][:, np.newaxis]
    G_allg=h_allg*b1+k_allg*b2+l_allg*b3 #alle G vectors
    G_allg_norm = np.linalg.norm(G_allg, axis=1) 
    G_allg_unit=G_allg/G_allg_norm[:, np.newaxis] #Normalisierte G-Vektoren
    
    #%% limit hkls: satisfy bragg conditoin
    d_hkl = 2 * np.pi / G_allg_norm #Netzebenenabstand für alle G die Auswahlregeln genügen
    valid= lambda_ / (2 * d_hkl) <= 1 #Bragg-Bed.
    G_valid=G_allg[valid]
    G_valid_unit=G_allg_unit[valid]
    hkl_valid=hkl[valid]
    
    #dhkl for all valid hkl
    d_hkl_valid=d_hkl[valid]
    #Bragg-angle for all valid hkl
    theta_bragg_rad = np.arcsin(lambda_ / (2 * d_hkl_valid))
    theta_bragg_deg = np.degrees(theta_bragg_rad)
    
    #Angle between incident beam and G
    theta_E_rad=np.arccos(np.dot(G_valid_unit,Einfall)) # theta_E=arccos(k*G/|G|) ,because|k|=1
    theta_E_deg=np.degrees(theta_E_rad)
    #Angle only 0- 90 deg, side of the crystal does not matter
    theta_E_0bis90 = np.minimum(theta_E_deg, 180 - theta_E_deg) 
    
    #angle in relation to lattice
    theta=90.0-theta_E_0bis90
    
    #difference angle to angle bragg 
    delta_theta=np.abs(theta-theta_bragg_deg)
    
    #angle lattice to surface
    phi_=np.degrees(np.arccos(np.dot(G_valid_unit,G_surface_unit)))
    #lmit angle to 0 to 90 deg. (side does not matter)
    phi_0bis90=np.minimum(phi_, 180 - phi_)
    #phi=90.0-phi_0bis90
    phi_plus_theta_b=phi_0bis90+theta_bragg_deg
    phi_minus_theta_b=phi_0bis90-theta_bragg_deg
    
    #Gammafactor
    gammafak=np.cos(np.radians(phi_minus_theta_b))/ np.cos(np.radians(phi_plus_theta_b))
    #%%
    #result arrayof all valid combinations (h,k,l,d_hkl (Netebenenabstand),Braggwinkel,Einfallswinkel auf Netzebene,Abstand Einfallswinkel zu Braggwinkel, Gammafaktor,Phi)
    result=np.column_stack((hkl_valid,d_hkl_valid,theta_bragg_deg,theta,delta_theta,gammafak,phi_0bis90,G_valid_unit))
    
    #%%
    #Minimum in delta_theta 
    min_delta_theta=np.min(result[:,6])
    #values for minimum
    rows_with_min = result[result[:, 6] == min_delta_theta]
    #G-vektor of the minimum
    h_min=rows_with_min[0][0]
    k_min=rows_with_min[0][1]
    l_min=rows_with_min[0][2]
    dhkl_min=rows_with_min[0][3]
    theta_b_min=rows_with_min[0][4]
    theta_min=rows_with_min[0][5]
    delta_theta_min=rows_with_min[0][6]
    gammafak_min=rows_with_min[0][7]
    phi_min=rows_with_min[0][8]
    G_unit_min=np.array([rows_with_min[0][9],rows_with_min[0][10],rows_with_min[0][11]])

    #%%
    #Angle scattered beam and surface
    Ausfall=Einfall+G_unit_min
    Ausfall_unit=Ausfall/np.linalg.norm(Ausfall)
    theta_exit_rad = np.arccos(np.dot(-G_surface_unit,Ausfall_unit))  # Winkel zw. Austritt und Oberfläche
    
    T=t/np.cos(theta_exit_rad)
    #print(T)
    #%% 
    tf=np.zeros((nue,max(tf_anzahl)))
    # Debye-Waller-Factor
    for j in range(nue):
        for f in range(tf_anzahl[j]):
            tf[j, f] = (                        #Quadratische Terme
                tfk[j, f, 0] * h_min * h_min
                + tfk[j, f, 1] * k_min * k_min
                + tfk[j, f, 2] * l_min * l_min)
            
            tf[j, f] += (                       #Kreuzterme
                tfk[j, f, 3] * h_min * k_min
                + tfk[j, f, 4] * h_min * l_min
                + tfk[j, f, 5] * k_min * l_min)
            
            tf[j, f] += (                       #zweiterKreuzterm
                tfk[j, f, 6] * h_min * k_min
                + tfk[j, f, 7] * h_min * l_min
                + tfk[j, f, 8] * k_min * l_min)
            
            tf[j, f] = np.exp(-1.0 * tf[j, f]) #Debye-Waller-Faktor
    
    #print(tf)
    valid_tf = tf[j, :tf_anzahl[j]]
    
    n=4  
    
    s = np.sin(np.radians(theta_min)) / lambda_
    
    # calculate structure factor F_h 
    F_h = 0
    a_list=a.tolist()
    positionen=np.array([xh,xk,xl]).T
    #print(positionen)
    positionen_einzelneAtomsorte=[]
    start = 0
    for i in range(nue):
        ende = start + nha[i]
        positionen_einzelneAtomsorte.append(positionen[start:ende])
        start = ende
    
    for atom_idx in range(nue):
        D = a_list[atom_idx][0:n]
        F = a_list[atom_idx][n]
        E = a_list[atom_idx][n+1:]
    
        D = np.array(D)
        E = np.array(E)
        
        f_atom = np.sum(D * np.exp(-E * s**2)) + F
        
        # Thermischer Abschwächungsfaktor (DWF)
        dwf_factor = np.exp(-valid_tf[atom_idx] * s**2)
        f_atom *= dwf_factor
        
        # sum over all positions of atom
        for (x, y, z) in positionen_einzelneAtomsorte[atom_idx]:
            phase = 2 * np.pi * (h_min * x + k_min * y + l_min * z)
            F_h += f_atom * np.exp(1j * phase)
    
    # calculate F_-h
    F_neg_hkl = np.conj(F_h)
    #print(F_neg_hkl)
    re = 2.817696e-5  # Electron radius in Angstrom
    lambda_, theta_b, chi_0r, chi_0i, \
        chi_hr1_pi, chi_hr1_sigma, chi_hr2_pi, chi_hr2_sigma, \
            chi_hi1_pi, chi_hi1_sigma, chi_hi2_pi, chi_hi2_sigma, \
                vez, mu, error, f2, f0, f1 = susi2(datdatei, h_min, k_min, l_min, lambda_, 2)
    Vorsilbe=(lambda_**2*re)/(-np.pi*vez)
    
    chi_h=Vorsilbe*F_h 
    chi_neg_hkl=Vorsilbe*F_neg_hkl
    #assumption: 10
    if abs(delta_theta_min)> 10*abs(chi_h)/(np.sin(2*np.radians(theta_min))): #phasenänderung weit weg vom Bragg Winkel
        delta=-np.pi/2*(np.real(chi_h*chi_neg_hkl)*np.sin(2*np.radians(theta_min))*T*10**-6/(lambda_*10**-10*delta_theta_min))
        #print('Phasechange',delta)
    else:
        ext_depth = np.zeros(2, dtype=complex)
        psi_0_array = np.zeros((1, 2), dtype=complex)
        psi_h_array = np.zeros((1, 2), dtype=complex)
        intensity_0_array = np.zeros((1, 2))
        intensity_h_array = np.zeros((1, 2))
        ima = complex(0, 1)
        wavek = 1 / lambda_
    
        chi_hr = complex(chi_hr1_sigma, chi_hr2_sigma)
        chi_hi = complex(chi_hi1_sigma, chi_hi2_sigma)
        chi_0 = complex(chi_0r, chi_0i)
        chimalchi = np.abs(chi_hr)**2 - np.abs(chi_hi)**2 + ima * chi_hr * np.conj(chi_hi) + ima * chi_hi * np.conj(chi_hr)
    
        for n in range(1, 3):
            if n == 1:
                C = np.cos(np.radians(2 * theta_b)) #pi-polarised
            elif n == 2:
                C = 1 #sigma-polarised
            
            delta_os = C * np.sqrt(np.abs(gammafak_min) * chimalchi) / np.sin(np.radians(2 * theta_b))
            #Lambda_0 = lambda_ * np.sqrt(np.cos(np.radians(90 - phi_min + theta_b)) * np.abs(np.cos(np.radians(90 - phi_min - theta_b)))) / (np.abs(C) * np.sqrt(chimalchi)) 
            Lambda_0 = lambda_ * np.sqrt(np.cos(np.radians(phi_min + theta_b)) * np.abs(np.cos(np.radians(phi_min - theta_b)))) / (C * np.sqrt(chimalchi)) 
            #90-phi_min, da phi_min winkel auf normale bezogen, wollen winkel auf ebene bezogen
                
            delta_theta_os = -chi_0 * (1 - gammafak_min) / (2 * np.sin(np.radians(theta_b * 2))) 
            
            #print('FWHM',np.real(2*delta_os))
            nu = (delta_theta_min / 3600 * np.pi / 180 - delta_theta_os) / delta_os  #deviation parameter
            
            psi_h1 = np.sqrt(chimalchi) / (2 * np.sqrt(np.abs(gammafak_min)) * (np.conj(chi_hr) + ima * np.conj(chi_hi)) * np.sqrt(1 + nu**2))
            psi_h2 = -1 * np.sqrt(chimalchi) / (2 * np.sqrt(np.abs(gammafak_min)) * (np.conj(chi_hr) + ima * np.conj(chi_hi)) * np.sqrt(1 + nu**2))
            
            #MP1 = wavek * chi_0 / (2 * (np.cos(np.radians(90 - phi_min - theta_b - theta_min / 3600)))) + nu / (2 * Lambda_0) + np.sqrt(nu**2 + 1) / (2 * Lambda_0)
            MP1 = wavek * chi_0 / (2 * (np.cos(np.radians(phi_min - theta_b - theta_min / 3600)))) + nu / (2 * Lambda_0) + np.sqrt(nu**2 + 1) / (2 * Lambda_0)
            #MP2 = wavek * chi_0 / (2 * (np.cos(np.radians(90 - phi_min - theta_b - theta_min / 3600)))) + nu / (2 * Lambda_0) - np.sqrt(nu**2 + 1) / (2 * Lambda_0)
            MP2 = wavek * chi_0 / (2 * (np.cos(np.radians(phi_min - theta_b - theta_min / 3600)))) + nu / (2 * Lambda_0) - np.sqrt(nu**2 + 1) / (2 * Lambda_0)
            
            psi_01 = -1 * (nu - np.sqrt(1 + nu**2)) / (2 * np.sqrt(1 + nu**2))
            psi_02 = (nu + np.sqrt(1 + nu**2)) / (2 * np.sqrt(1 + nu**2))
            
            psi_0 = psi_01 * np.exp(-2 * np.pi * ima * MP1 * t * 10**4) + psi_02 * np.exp(-2 * np.pi * ima * MP2 * t * 10**4)
            intensity_0 = np.abs(psi_0)**2
            
            psi_h = psi_h1 * np.exp(-2 * np.pi * ima * MP1 * t * 10**4) + psi_h2 * np.exp(-2 * np.pi * ima * MP2 * t * 10**4)
            intensity_h = gammafak_min* np.abs(psi_h)**2
            
            psi_0_array[:,n - 1] = psi_0
            psi_h_array[:,n - 1] = psi_h
            intensity_0_array[:,n - 1]=intensity_0
            intensity_h_array[:,n - 1]=intensity_h
            #print(intensity_0)
            #print(Lambda_0)
            ext_depth[n-1]=Lambda_0
            
        # Extinctionlength
        ext_depth=np.abs(ext_depth) / 2 / np.pi / 10000

        
        # Fullfield
        psi_total_pi = psi_0_array[:, 0] + psi_h_array[:, 0]
        psi_total_sigma = psi_0_array[:, 1] + psi_h_array[:, 1]
    
        # Phasedifference π – σ
        delta = np.angle(psi_total_pi) - np.angle(psi_total_sigma)
       
    return delta
    
if __name__=="__main__":
    datdatei = os.path.join(os.path.dirname(__file__), "DATA/SILIZIUM.DAT")
    lambda_=1.5406 #Wavelength in Angström
    t=30 # thickness of the crystal in mu m
    print(crystallite(datdatei,lambda_,t,nseed))
