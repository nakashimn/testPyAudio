# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE=44100
CHUNK=1024
REC_SEC = 15

p=pyaudio.PyAudio()

stream=p.open(	format = FORMAT,
		channels = CHANNELS,
		rate = RATE,
		frames_per_buffer = CHUNK,
		input = True,
		output = True) # inputとoutputを同時にTrueにする

def effect(input):
	data.append(np.frombuffer(input,"int16"))
	return input*1

data = []
for i in range(int(RATE/CHUNK*REC_SEC)):
    input = stream.read(CHUNK)
    input = effect(input)
    output = stream.write(input)

stream.stop_stream()
stream.close()
p.terminate()

plt.plot(data)
plt.show()

print("Stop Streaming")
