# -*- coding:utf-8 -*-
import sys
import numpy as np
import pyaudio
import wave
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui
from time import sleep

class ModelVoiceEffect:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024

        self.plotdata = np.empty(0)
        self.spectrum = np.empty(0)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.FORMAT,
            		              channels = self.CHANNELS,
            		              rate = self.RATE,
                                  input = True,
            		              output = True)

    def __del__(self):
        self.delete()

    def delete(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    """ 取得データの変換(文字列→INT16) """
    def toInt16(self, data_str):
        data_int16 = np.frombuffer(data_str, "int16")
        return data_int16

    """ 取得データの変換(文字列→FLOAT(-1.0～1.0)) """
    def toNormalizedFloat(self, data_str):
        data_float = np.frombuffer(data_str, "float")/32768.0
        return data_float

    """ 処理済データの変換(INT16→文字列) """
    def toStr(self, data_int16):
        data_str = np.frombuffer(np.array(data_int16), "S1")
        return data_str

    """ 処理済データの変換(float(-1.0～1.0)→文字列) """
    def toDenormalizedStr(self, data_float):
        data_str = np.frombuffer(np.array(data_float)*32768.0, "S1")
        return data_str

    """ ステレオ(左側)→モノラル """
    def toMonoralLeft(self, input):
        output = input[::2]
        return output

    """ ステレオ(右側)→モノラル """
    def toMonoralRight(self, input):
        output = input[1::2]
        return output

    """ モノラル→ステレオ(中心) """
    def toStereo(self, input):
        output = np.concatenate(np.array([input,input]).T)
        return output

    """ 音響処理 """
    def effect(self, input):
        processed = []
        for i in range(len(input)):
            if input[i] > 2000:
                processed.append(2000)
            elif input[i] < -2000:
                processed.append(-2000)
            else:
                processed.append(input[i])

        self.spectrum = np.fft.fft(input)
        output = np.array(processed, dtype="int16")
        return output

    def readSound(self, stream):
        """ input Data """
        input_data = stream.read(self.CHUNK)
        """ Pre-Process """
        raw_data = self.toInt16(input_data)
        raw_data = self.toMonoralRight(raw_data)
        """ Main Process """
        processed_data = self.effect(raw_data)
        self.plotdata = processed_data
        """ Post-Process """
        processed_data = self.toStereo(processed_data)
        output_data = self.toStr(processed_data)
        """ output Data """
        stream.write(output_data)

    def main(self):
        self.readSound(self.stream)

class ViewVoiceEffect:
    def __init__(self, model):
        """ Model """
        self.model = model
        """ Data """
        self.plotdata = np.zeros(1024)
        self.update_msec = 10
        """ Widget """
        self.graph = pg.GraphicsWindow()
        self.graph.setWindowTitle("test")
        self.plt = self.graph.addPlot()
        self.plt.setYRange(-1,1)
        self.curve = self.plt.plot()
        """ timer """
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_msec)

    def update(self):
        self.model.main()
        self.plotdata = np.append(self.plotdata, self.model.plotdata/32768.0)
        if len(self.plotdata) > 5*1024:
            self.plotdata = self.plotdata[1024:]
        self.curve.setData(self.plotdata)

class ControllerVoiceEffect:
    def __init__(self, model, view):
        pass

if __name__ == "__main__":
    model = ModelVoiceEffect()
    view = ViewVoiceEffect(model)
    controller = ControllerVoiceEffect(view, model)
    try:
        QtGui.QApplication.instance().exec_()
    except:
        model.delete()
