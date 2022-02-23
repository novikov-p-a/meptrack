# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 21:15:12 2022

@author: Pavel Novikov
"""

import pyautogui as pag
import numpy as np

from pylsl import StreamInlet, resolve_stream


print("looking for an EEG stream...")
#streams = resolve_stream('type', 'EEG')
streams = resolve_stream()

print("...qqq...")

for info in streams:
    print(info.type())

print("...end.")

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])


s = 0
s_on = False
smax = 1000
spscr = 800
sample_lim = 2.0e-4
for i in range(30000):
    #print('i =', i)
#while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()
    if np.abs(sample[0]) >= sample_lim and (not s_on):
        s_on = True
        s = 0
        print(timestamp, sample)        

    elif s_on and s < smax :
        if s == spscr:
            pscr = pag.screenshot()
            fname = r'c:\p\pscr\mep_' + str(i)  + r'.png'
            pscr.save(fname)
        s += 1        
    elif s_on and s >= smax and (np.abs(sample[0]) < sample_lim):
        s_on = False
        s = 0
    else:
        pass
        
        
    #print(timestamp, sample)

#print("looking for an EEG stream...")
#streams = resolve_stream('type', 'EEG')

#pscr = pag.screenshot()
#pscr.save(r'c:\p\pscr\pscr_01.png')


# def main():
#     # first resolve an EEG stream on the lab network
#     print("looking for an EEG stream...")
#     streams = resolve_stream('type', 'EEG')

#     # create a new inlet to read from the stream
#     inlet = StreamInlet(streams[0])

#     while True:
#         # get a new sample (you can also omit the timestamp part if you're not
#         # interested in it)
#         sample, timestamp = inlet.pull_sample()
#         print(timestamp, sample)


# if __name__ == '__main__':
#     main()



