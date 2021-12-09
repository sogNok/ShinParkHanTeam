# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 09:06:48 2021

@author: 이충섭
"""

import numpy as np
from CSP import CSP


a_data = np.load('train_0.npy')
n_data = np.load('train_1.npy')

#%%
data = (a_data, n_data)

csp_filter = CSP(a_data, n_data)

#%%
import matplotlib.pyplot as plt
print(csp_filter[0])

#%%
na_data = csp_filter[0].dot(a_data)
nn_data = csp_filter[0].dot(n_data)

#%%

np.save('csp_filter.npy', csp_filter)

#%%
cf = np.load('csp_filter.npy')

print(cf.shape)