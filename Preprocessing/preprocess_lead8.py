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

id_list = ('III','aVR','aVL','aVF')

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
        
        lead_8 = []
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
            
            lead_8.append(signal)
        data['Lead'].append(lead_8)
        
# Train
print('\nTrain\n')

data = {
        'Subject' : [],
        'Lead' : [],
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
df.to_csv('train_8.csv', index=False)



# Validation
print('\nValidation\n')

data = {
        'Subject' : [],
        'Lead' : [],
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
df.to_csv('validation_8.csv', index=False)
