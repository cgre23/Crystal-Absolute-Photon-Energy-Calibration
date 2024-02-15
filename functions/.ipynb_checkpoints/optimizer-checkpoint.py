#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 13:46:02 2021

@author: christiangrech
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
from HXRSS_Bragg_fun_lstsq import HXRSSopt
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
from matplotlib import cm
import re


output = pd.read_pickle("detected.pkl")
centroid_pa=list(output['line_centroid_pa'])
centroid_phen=np.array(list(output['line_centroid_phen']))
Bragg_centroid_pa = output['Bragg_centroid_pa']
Bragg_centroid_phen = output['Bragg_centroid_phen']

gid = output['gid']
roll = list(output['roll_angle'])
# Define new figure
fig_2, axes2 = plt.subplots(1, 1, figsize=(15, 7))
ax2 = axes2

h_list, k_list, l_list = [], [], []
# some artificially noisy data to fit
for gid_item in zip(gid):
    num = [int(s) for s in re.findall(r'-?\d+', str(gid_item))]
    h_list.append(num[0])
    k_list.append(num[1])
    l_list.append(num[2])

ax2.plot(centroid_pa, centroid_phen, 'bx') # Line centroid
ax2.plot(Bragg_centroid_pa, Bragg_centroid_phen, 'g.') # Bragg centroid

    # initial guesses for DTHP, DTHR, DTHY, G, Intercept


#p0 = -0.388, 1.07, 0, 0.98695, 0.
tplInitial1 =(-0.388, 1.07, 1.7,  0.98695)
xdata = (h_list, k_list, l_list, roll, centroid_pa)
ErrorFunc=lambda tpl, x, y: HXRSSopt(x,tpl)-y
#phen = HXRSSopt((h_list, k_list, l_list, roll, centroid_pa), -0.388, 1.07, 0, 0.98695, 0)
#best_vals, covar = curve_fit(HXRSSopt, xdata, centroid_phen)
best_vals, covar = leastsq(ErrorFunc, tplInitial1[:], args=(xdata, centroid_phen), ftol=1.49012e-09, xtol=1.49012e-09, gtol=0.0)
print(best_vals)

phen = HXRSSopt((h_list, k_list, l_list, roll, centroid_pa), (best_vals[0], best_vals[1], best_vals[2], best_vals[3]))
ax2.plot(centroid_pa, phen, 'r.')

#plt.ylabel('Angle')
#plt.xlabel('Spectrometer Energy (eV)')

