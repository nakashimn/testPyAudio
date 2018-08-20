# -*- coding:utf-8 -*-
import sys
import numpy as np
import pyaudio
import wave
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui
from time import sleep

class EffectAudio:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.REC_SEC = 15

        self.filename = "test.wav"
        self.plotdata = np.empty(0)
        self.spectrum = np.empty(0)

    def toInt16(self, data_str):
        data_int16 = np.frombuffer(data_str, "int16")
        return data_int16

    def toStr(self, data_int16):
        data_str = np.frombuffer(np.array(data_int16), "S1")
        return data_str

    def toMonoralLeft(self, input):
        output = input[::2]
        return output

    def toMonoralRight(self, input):
        output = input[1::2]
        return output

    def toStereo(self, input):
        output = np.concatenate(np.array([input,input]).T)
        return output

    def effect(self, input):
        processed = input
        self.spectrum = np.fft.fft(input)
        output = np.array(processed, dtype="int16")
        return output

    def plot(self, plotdata):
        pass

    def main(self):
        with wave.open(self.filename, "rb") as wf:

            p=pyaudio.PyAudio()

            stream=p.open(format = p.get_format_from_width(wf.getsampwidth()),
            		      channels = wf.getnchannels(),
            		      rate = wf.getframerate(),
            		      output = True)

            for i in range(int(self.RATE/self.CHUNK*self.REC_SEC)):
                input_data = wf.readframes(self.CHUNK)
                raw_data = self.toInt16(input_data)
                raw_data = self.toMonoralRight(raw_data)
                processed_data = self.effect(raw_data)
                self.plotdata = np.append(self.plotdata,processed_data)
                output_data = self.toStereo(processed_data)
                output_data = self.toStr(output_data)
                stream.write(output_data)

            stream.stop_stream()
            stream.close()
            p.terminate()

class PlotWindow:
    def __init__(self):
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle("test")
        self.plt = self.win.addPlot()
        self.plt.setYRange(-1,1)
        self.curve = self.plt.plot()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        self.data = np.zeros(1024)
        #マイクインプット設定
        self.CHUNK=1024             #1度に読み取る音声のデータ幅
        self.RATE=44100             #サンプリング周波数
        self.audio=pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK)

    def update(self):
        self.data = np.append(self.data, self.AudioInput())
        if len(self.data) > 5*1024:
            self.data = self.data[1024:]
        self.curve.setData(self.data)

    def AudioInput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.frombuffer(ret, dtype="int16")/32768.0
        return ret

if __name__ == "__main__":
    plotwin = PlotWindow()
    if (sys.flags.interactive!=1) or not hasattr(QtCore, "PYQT_VERSION"):
        QtGui.QApplication.instance().exec_()
#    cEffectAudio = EffectAudio()
#    cEffectAudio.main()
