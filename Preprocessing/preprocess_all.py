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
        
        lead_data = {}
        tree = parse(path+file_name)
        root = tree.getroot()
        waveform = root.findall("Waveform")
        
        for idx, WF in enumerate(waveform):
            WF_data = {}
            leaddata = WF.findall('LeadData')
            
            for LD in leaddata:
                lead_id = LD.findtext('LeadID')
                WFD = LD.findtext('WaveFormData')
                sample_size = LD.findtext('LeadSampleCountTotal')

                bdata = base64.b64decode(WFD)
                ff = 'h' * int(len(bdata) / 2) #int(sample_size)
                signal = struct.unpack(ff,bdata)
                
                if len(signal) == 4999:
                    signal = signal + (signal[-1],)
                    
                WF_data[lead_id] = signal
                
            if idx == 1 or len(waveform) == 1:
                lead_data['Rhythm'] = WF_data
            else:
                lead_data['Median'] = WF_data
        
        data['Lead'].append(lead_data)

        
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
df.to_csv('train.csv', index=False)


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
