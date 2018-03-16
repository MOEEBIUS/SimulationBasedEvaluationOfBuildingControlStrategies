#==============================================================================
# This project has received funding from the European Union's Horizon 2020 
# research and innovation programme under grant agreement No 680517 (MOEEBIUS)
# 
# MIT License
# 
# Copyright (c) 2018 Technische Hochschule Nuernberg Georg Simon Ohm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==============================================================================

import numpy as np
import pandas as pd
import pickle
from pylab import *

def PrometheeII(scenarios, minMax=[], weights=[], criteria=[]):
    # Seting up indexes and input values
    scen = scenarios.shape[0]
    crit = scenarios.shape[1]
    indexDf = ['Scen'+str(i) for i in range(1, scen +1)]
    if len(weights) == 0:
        weights = 5.0 * np.ones([1,crit])
    if len(minMax) == 0:
        minMax = np.ones([1,crit])
    if len(criteria) == 0:
        colDf = ['Crit'+str(i) for i in range(1, scen +1)]
    else:
        colDf = list(criteria)
    
    
    # Initializations
    rankedScenarios = scenarios.copy()
    p = np.zeros([2, crit])
    phi = np.zeros([scen, scen])

    # Calculate column-wise variance of scenarios
    sigma2 = np.atleast_2d(np.var(rankedScenarios, axis=0))
    
    # Convert to maximization problem
    rankedScenarios = rankedScenarios*minMax
    
    # Rank the scenarios
    for ii in range(0, scen-1):
        for jj in range(ii+1, scen):
            for kk in range(0, crit):
                # ------------------ pk(xi,xj) -------------------------------------
                if(rankedScenarios[ii, kk] <= rankedScenarios[jj, kk]):
                    p[0, kk] = 0
                else:
                    p[0, kk] = weights[0, kk] * (1-np.exp(-np.power(rankedScenarios[ii, kk]-rankedScenarios[jj, kk],2)/(2*sigma2[0,kk])))
                # ------------------ pk(xj,xi) -------------------------------------
                if(rankedScenarios[jj, kk] <= rankedScenarios[ii, kk]):
                    p[1,kk] = 0
                else:
                    p[1, kk] = weights[0, kk] * (1-np.exp(-np.power(rankedScenarios[jj, kk]-rankedScenarios[ii, kk],2)/(2*sigma2[0,kk])))
            
            # Construct the flows Matrix
            phi[ii,jj] = np.sum([p[0,]])
            phi[jj,ii] = np.sum([p[1,]])    
    
    # Calculate the pure flows for each scenario
    phi_pure = np.zeros([scen, 1])
    for ii in range(0, scen):
        phi_plus = np.sum(phi[ii,])
        phi_minus = np.sum(phi[:,ii])
        phi_pure[ii, 0] = (phi_plus - phi_minus)/(scen-1)    
    
    # Rank the solutions
    IX = np.flipud(phi_pure.argsort(axis=0)) # sort DESCENDING
    for ii in range(0, scen):
        rankedScenarios[ii,:] = scenarios[IX[ii,0],:]
        IX[ii,0]
        scenarios[IX[ii,0],:]
    
    df = pd.DataFrame(rankedScenarios, columns = colDf, index = indexDf)
    
    return df;






























