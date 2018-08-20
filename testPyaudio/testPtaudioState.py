# -*- coding:utf-8 -*-
import pyaudio

p=pyaudio.PyAudio()

hostAPICount = p.get_host_api_count()
print("Host API Count = " + str(hostAPICount))

# ホストAPIの情報を列挙
for cnt in range(0, hostAPICount):
    print(p.get_host_api_info_by_index(cnt))

# ASIOデバイスの情報を列挙
asioInfo = p.get_host_api_info_by_type(pyaudio.paASIO)
print("ASIO Device Count = " + str(asioInfo.get("deviceCount")))
for cnt in range(0, asioInfo.get("deviceCount")):
    print(p.get_device_info_by_host_api_device_index(asioInfo.get("index"), cnt))
