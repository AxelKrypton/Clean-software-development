# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 17:41:08 2025

@author: judith
"""

# energy = 8048
# lambda_ = 6.62606e-34 * 2.9979e8 / (energy * 1e-10 * 1.602e-19)
# hm, km, lm = 4, 4, 0 #reflex
# methode=1

import numpy as np
import math
from someDefs import  read_crystal_parameters_uni

from Henke import Henke


def susi2(datdatei, hm, km, lm, lambda_, methode):
    re = 2.817696e-5
    Rydbg = 1.097373e-3
    lambdaC = 2.4263e-2

    theta = 0
    psi0r = 0
    psi0i = 0
    psi1r_Pi = 0
    psi1r_Sigma = 0
    psi1i_Pi = 0
    psi1i_Sigma = 0
    psi2r_Pi = 0
    psi2r_Sigma = 0
    psi2i_Pi = 0
    psi2i_Sigma = 0
    vez = 0
    my = 0
    h = 0
    fa0=None
    f2 = f0 = f1 = 0
    # Laden der Strukturdaten im Uni format
    name, rho, nue, alpha, beta, gamma, aK, bK, cK, Element, nha, oz, ez, Mrel, lamk, xh, xk, xl, tf_anzahl, tf_gleiche, tfk, a, o = read_crystal_parameters_uni(datdatei)
    
    # Generelle Berechnungen
    z1 = np.radians(alpha) # alpha-winkel in rad
    z2 = np.radians(beta) # beta-winkel in rad
    z3 = np.radians(gamma) # gamma-winkel in rad
        
    vez = aK**2 * bK**2 * cK**2 * (1 - np.cos(z1)**2 - np.cos(z2)**2 - np.cos(z3)**2 + 2 * np.cos(z1) * np.cos(z2) * np.cos(z3))
       
    z4 = bK**2 * cK**2 * np.sin(z1)**2 #s11
    z5 = aK**2 * cK**2 * np.sin(z2)**2 #s22
    z6 = aK**2 * bK**2 * np.sin(z3)**2 #s33
    
    z7 = aK * bK * cK**2 * (np.cos(z1) * np.cos(z2) - np.cos(z3))
    z8 = aK**2 * bK * cK * (np.cos(z3) * np.cos(z2) - np.cos(z1))
    z9 = aK * bK**2 * cK * (np.cos(z3) * np.cos(z1) - np.cos(z2))
    
    z10 = z4 * hm**2 + z5 * km**2 + z6 * lm**2 + 2 * z7 * hm * km + 2 * z8 * km * lm + 2 * z9 * hm * lm
   
    z10 = (lambda_**2 * z10) / (4 * vez)
    
    #print(z1,z2,z3,z4,z5,z6,z7,z8,z9,z10)
    if z10 > 1:
        error = 'Bragg-Bedingung nicht erfüllt'
        stopp = 0
        #print(error, stopp)
        #theta = psi0r = psi0i = psi1r_Pi = psi1r_Sigma = None 
        #psi1i_Pi = psi1i_Sigma = psi2r_Pi = psi2r_Sigma = None 
        #psi2i_Pi = psi2i_Sigma = vez = my = f2 = f0 = f1 = None
    else:
        thetab = np.arctan(np.sqrt(z10) / np.sqrt(1 - z10))
        theta = np.degrees(thetab)
        vez = np.sqrt(vez)
            
        z8 = abs(np.cos(2 * thetab))
        z9 = abs(np.cos(4 * thetab))
        error=None 
        stopp = 1
        #print(theta, vez, z8, z9, stopp)
        
        
    if stopp == 1:
        
        fa0 = np.zeros(nue+1)
        v1 = np.zeros(nue+1)
        v2 = np.zeros(nue+1)
        v3 = np.zeros(nue+1)
        f0r = np.zeros(nue+1)
        far_Pi = np.zeros(nue+1)
        far_Sigma = np.zeros(nue+1)
        f0i = np.zeros(nue+1)
        fai_Pi = np.zeros(nue+1)
        fai_Sigma = np.zeros(nue+1)
        mue=np.zeros((nue+1,17))
        tf=np.zeros((nue+1,max(tf_anzahl)))
        
        #Atomamplitude
        for i in range(nue):
            z1 = (np.sin(thetab) / lambda_)**2
            for j in range(4):
                fa0[i] += a[i, j] * np.exp(-a[i, j + 4] * z1)
            fa0[i] += a[i, 8]
            
            #Dispersionskorrektur
            z5 = oz[i] - o[i, 0]
            v1[i] = (z5)**2 + 1.33e-5 * z5**4 + 3.55e-10 * z5**6 + 11.7e-15 * z5**8
            v2[i] = (v1[i] - 911 / lamk[i, 0]) / v1[i]
            v3[i] = lamk[i, 0] / lambda_
            
            z1 = 4 * np.log(abs(v3[i]**2 - 1)) / ((1 - v2[i])**2 * v3[i]**2)
            z2 = 1 / ((1 - v2[i])**3)
            z3 = 2 / (v3[i]**2)
            z4 = np.log(abs((v3[i] - 1) / (v3[i] + 1))) / (v3[i]**3)
            z5 = 0.2604891 * (z1 - z2 * (z3 + z4))
            f1 = z5
            f0r[i] = ez[i] + z5
            far_Pi[i] = fa0[i] + z5 * z8
            far_Sigma[i] = fa0[i] + z5
            
            #Absorptionskorrektur
            if methode == 1:
                for i in range(len(Element)):  #for loop ist notwendig da sonst iteration over 0d-array
                    el = Element[i]  # Extract single element
                    #print(f"Element[{i}] = {el}, Type: {type(el)}")  # Debugging line
                    f2 = Henke(lambda_, str(el))  # Ensure el is a regular Python string
                    #print(f2)
                    f0i[i] = f2
                    fai_Pi[i] = f2
                    fai_Sigma[i] = f2
                    v1[i] = f0i[i] * nha[i]
                #print(f0i,fai_Pi,fai_Sigma,v1)
                
            else:
                if (ez[i] > 0) and (lambda_ < lamk[i, 0]):  
                    
                    El1s = 2 if ez[i] > 1 else 1
            
                    z1 = 1 / ((oz[i] - o[i, 0]) ** 2 * Rydbg)
                    z2 = math.sqrt(lambda_ / abs(z1 - lambda_))
                    z3 = (lambda_ / z1) ** 3
            
                    if z1 > lambda_:
                        mue[i, 0] = 67.021 * z3 * math.exp(-4 * z2 * math.atan(1 / z2)) / (1 - math.exp(-2 * math.pi * z2))
                    else:
                        mue[i, 0] = 67.021 * z3 * math.exp(-2 * z2 * math.log((1 + (1 / z2)) / (1 - (1 / z2))))
            
                    mue[i, 1] = 0.4 * (lambdaC / lambda_) * (4 - (3 * lambda_ / z1))
                    mue[i, 2] = 0.4 * (lambdaC / lambda_) * (1 - (2 * lambda_ / z1))
            
                else:
                    for j in range(3):
                        mue[i, j] = 0
                        El1s = 0
                if ez[i] > 2 and (lambda_ < lamk[i, 1] or lamk[i, 1] == 0):  

                    El2s = 2 if ez[i] > 3 else 1
                    z1 = 4 / ((oz[i] - o[i, 1]) ** 2 * Rydbg)
                    z2 = (lambda_ / z1) ** 3
                    z3 = 2 * math.sqrt(lambda_ / abs(z1 - lambda_))
            
                    if z1 > lambda_:
                        z4 = 536.165 * z2 * math.exp(-4 * z3 * math.atan(2 / z3)) / (1 - math.exp(-2 * math.pi * z3))
                    else:
                        z4 = 536.165 * z2 * math.exp(-2 * z3 * math.log((1 + (2 / z3)) / (1 - (2 / z3))))
            
                    mue[i, 3] = z4 * (1 + (3 * lambda_ / z1))
                    mue[i, 4] = 1.6 * (lambdaC / lambda_) * ((lambda_ / z1) - 1) ** 2
                    mue[i, 5] = 0.4 * (lambdaC / lambda_) * (1 - (2 * lambda_ / z1))
            
                else:
                    for j in range(3, 6):  
                        mue[i, j] = 0
                        El2s = 0
            
                if ez[i] > 4 and (lambda_ < lamk[i, 3] or lamk[i, 3] == 0):
                    
                    El2p = 6 if ez[i] > 9 else ez[i] - 4 
                    z1 = 4 / ((oz[i] - o[i, 3]) ** 2 * Rydbg)
                    z2 = (lambda_ / z1) ** 3
                    z3 = 2 * math.sqrt(lambda_ / abs(z1 - lambda_))
                    if z1 > lambda_:
                        z4 = 536.165 * z2 * math.exp(-4 * z3 * math.atan(2 / z3)) / (1 - math.exp(-2 * math.pi * z3))
                    else:
                        z4 = 536.165 * z2 * math.exp(-2 * z3 * math.log((1 + (2 / z3)) / (1 - (2 / z3))))
                    mue[i, 7] = z4 * (lambda_ / z1) * (1 + (8 * lambda_) / (3 * z1))
                    mue[i, 8] = 0.8 * (lambdaC / lambda_) * (11 - (6 * lambda_ / z1)) * (1 + (3 * lambda_) / z1) / (3 + (8 * lambda_) / z1)
                    mue[i, 9] = 0.4 * (lambdaC / lambda_) * (1 - (2 * lambda_ / z1))
                else:
                    for j in range(7, 10):  
                        mue[i, j] = 0
                        El2p = 0
                
                if ez[i] > 10:
                    El3s = 2 if ez[i] > 11 else 1
                    z1 = 9 / ((oz[i] - o[i, 4]) ** 2 * Rydbg)
                    z2 = (lambda_ / z1) ** 3
                    z3 = 3 * math.sqrt(lambda_ / abs(z1 - lambda_))
                    if z1 > lambda_:
                        z4 = 201.062 * z2 * math.exp(-4 * z3 * math.atan(3 / z3)) / (1 - math.exp(-2 * math.pi * z3))
                    else:
                        z4 = 201.062 * z2 * math.exp(-2 * z3 * math.log((1 + (3 / z3)) / (1 - (3 / z3))))
                    mue[i, 10] = z4 * (9 + (96 * lambda_ / z1) + 208 * (lambda_ / z1) ** 2 + 128 * z2)
                    mue[i, 11] = 0.4 * (lambdaC / lambda_) * (4 + (5 * lambda_ / z1))
                    mue[i, 11] *= (3 - (4 * lambda_ / z1)) / (3 + (4 * lambda_ / z1))
                    mue[i, 12] = 0.8 * (lambdaC / lambda_) * (1 - (2 * lambda_ / z1))
                    mue[i, 12] *= (3 + (4 * lambda_ / z1)) / (3 - (2 * lambda_ / z1))
                else:
                    for j in range(10, 13): 
                        mue[i, j] = 0
                        El3s = 0
            
                if ez[i] > 12:
                    El3p = 6 if ez[i] > 17 else ez[i] - 12
                    z1 = 9 / ((oz[i] - o[i, 5]) ** 2 * Rydbg)
                    z2 = (lambda_ / z1) ** 4
                    z3 = 3 * math.sqrt(lambda_ / abs(z1 - lambda_))
                    if z1 > lambda_:
                        z4 = 1608.495 * z2 * math.exp(-4 * z3 * math.atan(3 / z3)) / (1 - math.exp(-2 * math.pi * z3))
                    else:
                        z4 = 1608.495 * z2 * math.exp(-2 * z3 * math.log((1 + (3 / z3)) / (1 - (3 / z3))))
                    mue[i, 13] = z4 * (3 + (26 * lambda_ / z1) + 28 * (lambda_ / z1) ** 2)
                else:
                    mue[i, 13] = 0
                    El3p = 0
                    
                if ez[i] > 18:
                    El4s = 2 if ez[i] > 19 else 1
                    z1 = 16 / ((oz[i] - o[i, 6]) ** 2 * Rydbg)
                    z2 = (lambda_ / z1) ** 3
                    z3 = 4 * math.sqrt(lambda_ / abs(z1 - lambda_))
                    if z1 > lambda_:
                        z4 = 1429.774 * z2 * math.exp(-4 * z3 * math.atan(4 / z3)) / (1 - math.exp(-2 * math.pi * z3))
                    else:
                        z4 = 1429.774 * z2 * math.exp(-2 * z3 * math.log((1 + (4 / z3)) / (1 - (4 / z3))))
                    z5 = 3 + (69 * lambda_ / z1) + (424 * (lambda_ / z1) ** 2) + (1024 * z2)
                    z5 += (29944 * ((lambda_ / z1) ** 2) ** 2 / 3) + (320 * (lambda_ / z1) ** 2 * z2)
                    mue[i, 14] = z4 * z5
                else:
                    mue[i, 14] = 0
                    El4s = 0
                if ez[i] > 20:
                    if ez[i] > 29:
                        El3d = 10
                    else:
                        El3d = ez[i] - 20
                    z1 = 9 / ((oz[i] - o[i, 7]) ** 2 * Rydbg)
                    z2 = (lambda_ / z1) ** 5
                    z3 = 3 * math.sqrt(lambda_ / abs(z1 - lambda_))
                    if z1 > lambda_:
                        z4 = 643.398 * z2 * math.exp(-4 * z3 * math.atan(3 / z3)) / (1 - math.exp(-2 * math.pi * z3))
                    else:
                        z4 = 643.398 * z2 * math.exp(-2 * z3 * math.log((1 + (3 / z3)) / (1 - (3 / z3))))
                    mue[i, 15] = z4 * (5 + (46 * lambda_ / z1) + (48 * (lambda_ / z1) ** 2))
                else:
                    mue[i, 15] = 0
                    El3d = 0
                    
                if ez[i] > 30:
                    if ez[i] > 35:
                        El4p = 6
                    else:
                        El4p = ez[i] - 30
                    z1 = 16 / ((oz[i] - o[i, 8]) ** 2 * Rydbg)
                    z2 = (lambda_ / z1) ** 4
                    z3 = 4 * math.sqrt(lambda_ / abs(z1 - lambda_))
                    if z1 > lambda_:
                        z4 = 857.864 * z2 * math.exp(-4 * z3 * math.atan(4 / z3)) / (1 - math.exp(-2 * math.pi * z3))
                    else:
                        z4 = 857.864 * z2 * math.exp(-2 * z3 * math.log((1 + (4 / z3)) / (1 - (4 / z3))))
                    z5 = 75 + (1400 * lambda_ / z1) + (5304 * (lambda_ / z1) ** 2)
                    z5 += (6016 * (lambda_ / z1) ** 3) + (2112 * z2)
                    mue[i, 16] = z4 * z5
                else:
                    mue[i, 16] = 0
                    El4p = 0 
                f0i[i] = (El1s * mue[i, 1] * (1 + mue[i, 3] + mue[i, 2])
                          + El2s * mue[i, 4] * (1 + mue[i, 6] + mue[i, 5])
                          + El2p * mue[i, 7] * (1 + mue[i, 9] + mue[i, 8])
                          + El3s * mue[i, 10] * (1 + mue[i, 12] + mue[i, 11])
                          + El3p * mue[i, 13] + El4s * mue[i, 14] + El3d * mue[i, 15] + El4p * mue[i, 16]
                          )

                v1[i] = f0i[i] * nha[i]

                fai_Pi[i] = (El1s * mue[i, 1] * (((1 + mue[i, 3]) * z8) + mue[i, 2] * z9)
                             + El2s * mue[i, 4] * (((1 + mue[i, 6]) * z8) + mue[i, 5] * z9)
                             + El2p * mue[i, 7] * (((1 + mue[i, 9]) * z8) + mue[i, 8] * z9)
                             + El3s * mue[i, 10] * (((1 + mue[i, 12]) * z8) + mue[i, 11] * z9)
                             + El3p * mue[i, 13] + El4s * mue[i, 14] + El3d * mue[i, 15] + El4p * mue[i, 16]
                             )

                fai_Sigma[i] = (El1s * mue[i, 1] * (1 + mue[i, 3] + mue[i, 2] * z8)
                                + El2s * mue[i, 4] * (1 + mue[i, 6] + mue[i, 5] * z8)
                                + El2p * mue[i, 7] * (1 + mue[i, 9] + mue[i, 8] * z8)
                                + El3s * mue[i, 10] * (1 + mue[i, 12] + mue[i, 11] * z8)
                                + El3p * mue[i, 13] + El4s * mue[i, 14] + El3d * mue[i, 15] + El4p * mue[i, 16]
                                )
        #print(f0i,fai_Pi,fai_Sigma,v1)
        
        #Strukturamplitude
        psi1r_Pi = 0 
        psi1r_Sigma = 0 
        psi1i_Pi = 0 
        psi1i_Sigma = 0
        psi2r_Pi = 0
        psi2r_Sigma = 0
        psi2i_Pi = 0
        psi2i_Sigma = 0
        i = 0
        
        for j in range(nue):
            for f in range(tf_anzahl[j]):
                tf[j, f] = (
                    tfk[j, f, 0] * hm * hm
                    + tfk[j, f, 1] * km * km
                    + tfk[j, f, 2] * lm * lm)
                
                tf[j, f] += (
                    tfk[j, f, 3] * hm * km
                    + tfk[j, f, 4] * hm * lm
                    + tfk[j, f, 5] * km * lm)
                
                tf[j, f] += (
                    tfk[j, f, 6] * hm * km
                    + tfk[j, f, 7] * hm * lm
                    + tfk[j, f, 8] * km * lm)
                
                tf[j, f] = np.exp(-1.0 * tf[j, f])
                # print(tf_gleiche)
                # print(j)
                # print(f)
                h = int(tf_gleiche[j, f])
                
                z1=0
                z2=0

                for k in range(h):
                    g = k + i
                    #print(g)
                    z1 += np.cos(2 * np.pi * (hm * xh[g] + km * xk[g] + lm * xl[g]))
                    z2 += np.sin(2 * np.pi * (hm * xh[g] + km * xk[g] + lm * xl[g]))
                    
                psi1r_Pi += far_Pi[j] * tf[j, f] * z1
                psi1r_Sigma += far_Sigma[j] * tf[j, f] * z1
                psi1i_Pi += far_Pi[j] * tf[j, f] * z2
                psi1i_Sigma += far_Sigma[j] * tf[j, f] * z2
                psi2r_Pi += fai_Pi[j] * tf[j, f] * z1
                psi2r_Sigma += fai_Sigma[j] * tf[j, f] * z1
                psi2i_Pi += fai_Pi[j] * tf[j, f] * z2
                psi2i_Sigma += fai_Sigma[j] * tf[j, f] * z2
                i += h
                
        #print(psi1r_Pi,psi1i_Pi,psi2r_Pi,psi2i_Pi)

        #Dielektrische Suszeptibilitäten
        fhkl_Pi = np.sqrt((psi1r_Pi + psi2i_Pi) ** 2 + (psi2r_Pi + psi1i_Pi) ** 2)
        fhkl_Sigma = np.sqrt((psi1r_Sigma + psi2i_Sigma) ** 2 + (psi2r_Sigma + psi1i_Sigma) ** 2)
        fhkl = [fhkl_Sigma, fhkl_Pi]
        z1 = -1 * re * lambda_ * lambda_ / (vez * np.pi)
        psi0r = 0
        psi0i = 0

        for i in range(nue):
            psi0r += f0r[i] * nha[i] 
            psi0i += f0i[i] * nha[i] 
        
        psi0r *= z1
        psi0i *= z1
        psi1r_Pi *= z1
        psi1r_Sigma *= z1
        psi1i_Pi *= z1
        psi1i_Sigma *= z1
        
        if abs(psi1i_Pi) < 5e-12:
            psi1i_Pi = 0 #{Im(F)=0 bei Zentrosymm.}
        
        if abs(psi1i_Sigma) < 5e-12:
            psi1i_Sigma = 0 #{Im(F)=0 bei Zentrosymm.}
        
        psi2r_Pi *= z1
        psi2r_Sigma *= z1
        psi2i_Pi *= z1
        psi2i_Sigma *= z1

        if abs(psi2i_Pi) < 5.e-12:
            psi2i_Pi = 0 #{Im(F)=0 bei Zentrosymm.}
        
        if abs(psi2i_Sigma) < 5.e-12:
            psi2i_Sigma = 0 #{Im(F)=0 bei Zentrosymm.}
        
        psi0 = np.sqrt(psi0r**2 + psi0i**2)
        chihr_Pi = np.sqrt(psi1r_Pi**2 + psi1i_Pi**2)
        chihr_Sigma = np.sqrt(psi1r_Sigma**2 + psi1i_Sigma**2)
        chihi_Pi = np.sqrt(psi2r_Pi**2 + psi2i_Pi**2)
        chihi_Sigma = np.sqrt(psi2r_Sigma**2 + psi2i_Sigma**2)
        z2=0
        for i in range(nue):
            z2 = z2+v1[i]
        
        my = 100000000 * z2 * 2 * re * lambda_ / vez  

    f0 = fa0
    #print(psi1r_Pi, psi1r_Sigma, psi1i_Pi, psi1i_Sigma, psi2r_Pi, psi2r_Sigma, psi2i_Pi, psi2i_Sigma)
    return lambda_, theta, psi0r, psi0i, psi1r_Pi, psi1r_Sigma, psi1i_Pi, psi1i_Sigma, psi2r_Pi, psi2r_Sigma, psi2i_Pi, psi2i_Sigma, vez, my, error, f2, f0, f1