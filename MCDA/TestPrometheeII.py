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
from PrometheeII import PrometheeII

pd.set_option('display.width', 1000)


""" Test for different criteria weighting """
criteria = ['Consumption', 'Energy sold to grid', '|PMV|', '(500 - LUX)', 'CO2', 'Monetary Profit']

scenarios = np.array([[6000, 3000, 0.2, 100, 500, 210],
                      [3000, 5000, 1.1, 200, 800, 500],
                      [9000, 300, 0, 0, 250, -100],
                      [5000, 3500, 0.5, 150, 550, 100]
                      ], ndmin=2)



# Indicate -1 for minimization and +1 for maximization
minMax = np.array([-1, 1, -1, -1, -1, 1], ndmin=2)

# Test 1: care for comfort
weightsComfort = np.array([3, 5, 10, 8, 10, 8], ndmin=2)
rankedScenariosComfort = PrometheeII(scenarios, minMax, weightsComfort, criteria)
print("----------------------------------------------------------------")
print("Test 1: care for comfort:")
print("Criteria = " + str(criteria))
print("Weights = " + str(weightsComfort))
print("                         -----------------------------------------------")
print(rankedScenariosComfort)
print("----------------------------------------------------------------")

# Test 2: care for profit
weightsProfit = np.array([10, 10, 5, 5, 3, 10], ndmin=2)
rankedScenariosProfit = PrometheeII(scenarios, minMax, weightsProfit, criteria)
print("Test 2: care for profit:")
print("Criteria = " + str(criteria))
print("Weights = " + str(weightsProfit))
print("                         -----------------------------------------------")
print(rankedScenariosProfit)
print("----------------------------------------------------------------")

# Test 3: no preference
weightsNoPreference = np.array([5, 5, 5, 5, 5, 5], ndmin=2)
rankedScenariosNoPreference = PrometheeII(scenarios, minMax, weightsNoPreference, criteria)
print("Test 3: no preference:")
print("Criteria = " + str(criteria))
print("Weights = " + str(weightsNoPreference))
print("                         -----------------------------------------------")
print(rankedScenariosNoPreference)
print("----------------------------------------------------------------")

# Test 4: slight preference
weightsSlightPreference = np.array([5, 5, 6, 6, 6, 5], ndmin=2)
rankedScenariosSlightPreference = PrometheeII(scenarios, minMax, weightsSlightPreference, criteria)
print("Test 4: slight preference:")
print("Criteria = " + str(criteria))
print("Weights = " + str(weightsSlightPreference))
print("                         -----------------------------------------------")
print(rankedScenariosSlightPreference)
print("----------------------------------------------------------------")


""" Save all variables to a file """
filename='Results/workspace.out'
# Saving the objects:
with open(filename, 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([scenarios, minMax, weightsComfort, rankedScenariosComfort, weightsProfit, rankedScenariosProfit,
                 weightsNoPreference, rankedScenariosNoPreference, weightsSlightPreference, rankedScenariosSlightPreference], f)

## Getting back the objects:
#filename='Results/workspace.out'
#with open(filename, 'rb') as f:  # Python 3: open(..., 'rb')
#    scenarios, minMax, weightsComfort, rankedScenariosComfort, weightsProfit, rankedScenariosProfit,
#                 weightsNoPreference, rankedScenariosNoPreference, weightsSlightPreference, rankedScenariosSlightPreference = pickle.load(f)