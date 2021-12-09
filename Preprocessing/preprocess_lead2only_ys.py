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

def decode_signal(path, data):
    file_list = os.listdir(path)
    
    for file_name in file_list:
        print(file_name)
        
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
        
        data.append(signal)

        
# Train
print('\nTrain\n')


# train - Arrhythmia
print('Arrhythmia\n')

data = []
path = './data/train/arrhythmia/'

decode_signal(path, data)

df = pd.DataFrame(data)
df.to_csv('train_arrhythmia.csv', index=False)

# train - Normal
print('Normal\n')

data = []
path = './data/train/normal/'

decode_signal(path, data)

df = pd.DataFrame(data)
df.to_csv('train_normal.csv', index=False)


# Validation
print('\nValidation\n')


# validation - Arrhythmia
print('Arrhythmia\n')

data = []
path = './data/validation/arrhythmia/'

decode_signal(path, data)

df = pd.DataFrame(data)
df.to_csv('validation_arrhythmia.csv', index=False)
    
# validation - Normal
print('Normal\n')

data = []
path = './data/validation/normal/'

decode_signal(path, data)

df = pd.DataFrame(data)
df.to_csv('validation_normal.csv', index=False)