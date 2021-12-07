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

def decode_signal(path, data, is_normal):
    file_list = os.listdir(path)
    
    for file_name in file_list:
        print(file_name)
        data['Subject'].append(file_name)
        if is_normal:
            data['Label'].append(0)
        else:
            data['Label'].append(1)
        
        tree = parse(path+file_name)
        root = tree.getroot()
        waveform = root.findall("Waveform")
        if len(waveform) == 1:
            leaddata = waveform[0].findall("LeadData")
        else:
            leaddata = waveform[1].findall("LeadData")
        WFD = leaddata[1].findtext('WaveFormData')
        sample_size = leaddata[1].findtext('LeadSampleCountTotal')
        
        bdata = base64.b64decode(WFD)
        ff = 'h' * int(len(bdata) / 2) #int(sample_size)
        signal = struct.unpack(ff,bdata)
        
        if len(signal) == 4999:
            signal = signal + (signal[-1],)
        
        data['Lead2'].append(signal)

        
# Train
print('\nTrain\n')

data = {
        'Subject' : [],
        'Lead2' : [],
        'Label' : [],
        }

# train - Arrhythmia
print('Arrhythmia\n')

path = './data/train/arrhythmia/'
is_normal = False
decode_signal(path, data, is_normal)

    
# train - Normal
print('Normal\n')

path = './data/train/normal/'
is_normal = True
decode_signal(path, data, is_normal)

df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv('train.csv', index=False)


# Validation
print('\nValidation\n')

data = {
        'Subject' : [],
        'Lead2' : [],
        'Label' : [],
        }

# validation - Arrhythmia
print('Arrhythmia\n')

path = './data/validation/arrhythmia/'
is_normal = False
decode_signal(path, data, is_normal)
    
# validation - Normal
print('Normal\n')

path = './data/validation/normal/'
is_normal = True
decode_signal(path, data, is_normal)

df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv('validation.csv', index=False)
