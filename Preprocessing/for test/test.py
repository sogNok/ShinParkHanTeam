# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 19:29:55 2021

@author: 이충섭
"""
import base64
from xml.etree.ElementTree import parse
import pandas as pd
import os
import os.path
import matplotlib.pyplot as plt
import struct
import numpy as np
from CSP import CSP

id_list = ('III','aVR','aVL','aVF')

def decode_signal(path, data, is_normal):
    file_list = os.listdir(path)
    
    count = 0
    for file_name in file_list:
        print(file_name)
        if file_name[0] == '6':
            continue
        
        tree = parse(path+file_name)
        root = tree.getroot()
        waveform = root.findall("Waveform")
        if len(waveform) == 1:
            leaddata = waveform[0].findall("LeadData")
        else:
            leaddata = waveform[1].findall("LeadData")
        
        lead_8 = np.zeros((8,5000))
        count_2 = 0
        for LD in leaddata:
            lead_id = LD.findtext('LeadID')
            
            if lead_id in id_list:
                continue
            WFD = LD.findtext('WaveFormData')
            sample_size = LD.findtext('LeadSampleCountTotal')
        
            bdata = base64.b64decode(WFD)
            ff = 'h' * int(len(bdata) / 2) #int(sample_size)
            signal = struct.unpack(ff,bdata)

            if len(signal) == 4999:
                signal = signal + (signal[-1],)
            np_signal = np.asarray(signal)
            lead_8[count_2] = np_signal
            count_2 +=1

        data[count] = lead_8
        count += 1

#%%
# Train
print('\nTrain\n')



# train - Arrhythmia
print('Arrhythmia\n')

a_data = np.zeros((10115,8,5000))

path = './data/train/arrhythmia/'
is_normal = False
decode_signal(path, a_data, is_normal)

# train - Normal
print('Normal\n')

n_data = np.zeros((21037,8,5000))

path = './data/train/normal/'
is_normal = True
decode_signal(path, n_data, is_normal)




#%%
np.save('train_0.npy', a_data)
np.save('train_1.npy', n_data)

#%%
# Validation
print('\nValidation\n')


# validation - Arrhythmia
print('Arrhythmia\n')

va_data = np.zeros((2229,8,5000))

path = './data/validation/arrhythmia/'
is_normal = False
decode_signal(path, va_data, is_normal)
    
# validation - Normal
print('Normal\n')

vn_data = np.zeros((2630,8,5000))

path = './data/validation/normal/'
is_normal = True
decode_signal(path, vn_data, is_normal)

np.save('test_0.npy', va_data)
np.save('test_1.npy', vn_data)
