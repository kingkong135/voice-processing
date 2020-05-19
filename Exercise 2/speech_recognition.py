import tkinter as tk
import threading
import pyaudio
import wave
import pickle
import librosa
import math
import numpy as np
import operator

class App:
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    frames = []

    with open("output1.pkl", "rb") as file:
        models = pickle.load(file)


    def __init__(self, master):
        self.sentences = []
        self.is_recording = False
        self.button1 = tk.Button(main, text='record', command=self.start, width=10)
        self.button2 = tk.Button(main, text='stop', command=self.stop, width=10)
        self.text = tk.Text(main, height=20, width=50)
        self.lable = tk.Label(main, text='Predict')
        self.button1.pack()
        self.button2.pack()
        self.lable.pack()
        self.text.pack()

        self.predict = ''



    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)
        self.is_recording = True

        print('Recording')
        self.t = threading.Thread(target=self.record)
        self.t.start()

    def stop(self):
        self.is_recording = False
        print('recording complete')

        filename = 'data.wav'
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.frames.clear()

        O = self.get_mfcc(filename)
        score = {cname: model.score(O, [len(O)]) for cname, model in self.models.items()}
        inverse = [(value, key) for key, value in score.items()]
        self.predict = max(inverse)[1]
        self.set_predict_text()

    def record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def set_predict_text(self):
        text = 'Không thể đoán nhận từ vừa đọc'
        if self.predict == 'song':
            text = 'Song'
        elif self.predict == 'toi':
            text = 'Tôi'
        elif self.predict == 'truoc':
            text = 'Trước'
        elif self.predict == 'nhan_vien':
            text = 'Nhân Viên'
        elif self.predict == 'gia_dinh':
            text = 'Gia Đình'
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, text)

    def get_mfcc(self, file_path):
        y, sr = librosa.load(file_path)  # read .wav file
        hop_length = math.floor(sr * 0.010)  # 10ms hop
        win_length = math.floor(sr * 0.025)  # 25ms frame
        # mfcc is 12 x T matrix
        mfcc = librosa.feature.mfcc(
            y, sr, n_mfcc=12, n_fft=1024,
            hop_length=hop_length, win_length=win_length)
        # substract mean from mfcc --> normalize mfcc
        mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1, 1))
        # delta feature 1st order and 2nd order
        delta1 = librosa.feature.delta(mfcc, order=1)
        delta2 = librosa.feature.delta(mfcc, order=2)
        # X is 36 x T
        X = np.concatenate([mfcc, delta1, delta2], axis=0)  # O^r
        # return T x 36 (transpose of X)
        return X.T  # hmmlearn use T x N matrix



main = tk.Tk()
main.title('Speech Recognition')
main.geometry('400x400')
app = App(main)
main.mainloop()
