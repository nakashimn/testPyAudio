# -*- coding:utf-8 -*-
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

CHUNK=1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE=44100
REC_SEC = 15
output_file_name = "test01.wav"

p=pyaudio.PyAudio()

stream=p.open(format = FORMAT,
		      channels = CHANNELS,
		      rate = RATE,
		      frames_per_buffer = CHUNK,
		      input = True)

frames = []
print("Recording...")

for i in range(0, int(RATE/CHUNK*REC_SEC)):
	data = stream.read(CHUNK)
	frames.append(data)
#	    output = stream.write(input)

stream.stop_stream()
stream.close()
p.terminate()
print("Stop Streaming")

with wave.open(output_file_name,"wb") as wf:
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b"".join(frames))
