import os
import time
import wave

import pyaudio
from pydiogment.augf import change_tone
from pydiogment.augt import slow_down, speed
from pydub import AudioSegment

from pydub.playback import play


class Process():
    # 修改类
    def __init__(self):
        self.RATE = 44100  # 采样频率
        self.CHUNK = 1024  # 每个缓冲区的帧数
        self.CHANNELS = 1  # 单声道
        self.FORMAT = pyaudio.paInt16  # 采样位数
        self.TIME = 5  # 录音时间
        self.LEVEL = 0  # 变声等级

    def timeChange(self, time):
        self.TIME = int(time)

    def record_audio(self):
        """ 录音功能 """

        p = pyaudio.PyAudio()  # 实例化对象
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)  # 打开流，传入响应参数
        wf = wave.open("record.wav", 'wb')  # 打开 wav 文件。
        wf.setframerate(self.RATE)  # 采样频率设置
        wf.setnchannels(self.CHANNELS)  # 声道设置
        wf.setsampwidth(p.get_sample_size(self.FORMAT))  # 采样位数设置

        for _ in range(0, int(self.RATE * self.TIME / self.CHUNK)):
            data = stream.read(self.CHUNK)
            wf.writeframes(data)  # 写入数据
        stream.stop_stream()  # 关闭流
        stream.close()
        p.terminate()
        wf.close()

    def levelChange(self, level):
        self.LEVEL = level

    def changeVoice(self):
        if os.path.isfile("record1.wav"):
            os.remove("record1.wav")
        if os.path.isfile("record1_augmented_slowed.wav"):
            os.remove("record1_augmented_slowed.wav")
        if os.path.isfile("record1_augmented_speeded.wav"):
            os.remove("record1_augmented_speeded.wav")
        if os.path.isfile("record2.wav"):
            os.remove("record2.wav")
        level = 1 + (self.LEVEL * 0.25)
        change_tone("record.wav", level)
        file = "record_augmented_" + str(level) + "_toned.wav"
        while not os.path.isfile(file):
            time.sleep(0.1)
        os.rename(file, "record1.wav")
        if self.LEVEL > 0:
            slow_down("record1.wav", 1/level)
            while not os.path.isfile("record1_augmented_slowed.wav"):
                time.sleep(0.1)
            os.rename("record1_augmented_slowed.wav", "record2.wav")
        elif self.LEVEL < 0:
            speed("record1.wav", 1/level)
            while not os.path.isfile("record1_augmented_speeded.wav"):
                time.sleep(0.1)
            os.rename("record1_augmented_speeded.wav", "record2.wav")
        else:
            os.system('copy record1.wav record2.wav')

    def play_audio(self):
        while not os.path.isfile("record2.wav"):
            time.sleep(0.1)
        song = AudioSegment.from_wav("record2.wav")
        play(song)
