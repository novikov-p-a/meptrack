# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 21:15:12 2022

@author: Pavel Novikov
"""

from pylsl import StreamInlet, resolve_stream
import numpy as np
import pyautogui as pag
import keyboard as kb


# Settings
TRIG_CH_NUM = 0 # number of trigger channel 
EMG_CH_NUM = 1 # number of trigger channel 
TRIG_CH_THRESHOLD = 200 # in mcV (microvolt)
SCR_CAPTURE_DELAY = 800 # in ms (millisecond)
MIN_TIME_BETWEEN_STIMULI = 1000 # in ms (millisecond)
TRIAL_START_BEF_TRIG = 400 # in ms, start of trial recording before trigger
TRIAL_END_AFT_TRIG = 600 # in ms, end of trial recording after trigger

# Path to store screenshots and data
PATH = r'c:\p\pscr'

# Subject name/code
SUBJNAME = 'Pavel'

# Advanced settings
MAX_NONACTIVE_TIME = 600 # in seconds


# START
print('Looking for an EMG stream ...')
streams = resolve_stream()
print('   ... okay.')

print('Block starts for subject', SUBJNAME, '...')

for info in streams:
    print(info.type())

print("...end.")

# create an inlet to read from the stream
inlet_trig = StreamInlet(streams[TRIG_CH_NUM])
#inlet_emg = StreamInlet(streams[TRIG_CH_NUM])


s = 0
s_on = False
smax = MIN_TIME_BETWEEN_STIMULI
spscr = SCR_CAPTURE_DELAY
sample_lim = 1.0e-6*TRIG_CH_THRESHOLD
i = 0
mep_data = np.zeros((smax), dtype = np.float32)
emg_rec = np.zeros((MAX_NONACTIVE_TIME*1000), dtype=np.float32)

irec = 0
irec_trig = -1
while True:
    
    sample, timestamp = inlet_trig.pull_sample()
    
    emg_rec[irec] = sample[0]
    
    if np.abs(sample[0]) >= sample_lim and (not s_on):
        s_on = True
        s = 0
        irec_trig = irec
        print(timestamp, sample)

    elif s_on and s < smax :
        if s == spscr:
            pscr = pag.screenshot()
            fname = PATH + r'\mep_' + str(i)  + r'.png'
            pscr.save(fname)
            
            mep_data[:] = emg_rec[irec]
        
            
        s += 1       
        
    elif s_on and s >= smax and (np.abs(sample[0]) < sample_lim):
        s_on = False
        s = 0
        
    else:
        pass
    
    if kb.is_pressed('q'):
        print('... terminated by user.')
        break
    
    i += 1
    irec +=1
        



