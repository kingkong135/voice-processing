import tkinter as tk
import threading
import pyaudio
import wave
from os import walk
from nltk.tokenize import sent_tokenize


class App:
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100

    frames = []

    def __init__(self, master, topics):
        self.sentences = []
        self.current_index = -1
        self.is_recording = False
        self.button1 = tk.Button(main, text='record', command=self.start, width=10)
        self.button2 = tk.Button(main, text='stop', command=self.stop, width=10)
        self.text = tk.Text(main, height=10, width=200)
        self.lable = tk.Label(main, text='Sentences')

        self.emo = tk.StringVar(main)
        self.emo.set('choose topic')
        self.popupMenu = tk.OptionMenu(main, self.emo, *topics)
        self.emo.trace('w', self.getTopic)

        self.sentence = 'article here'

        self.next_button = tk.Button(main, text='next', command=self.goNext, width=10)

        self.popupMenu.pack()
        self.lable.pack()
        self.text.pack()
        self.next_button.pack()
        self.button1.pack()
        self.button2.pack()

    def getTopic(self, *args):
        topic_name = self.emo.get()
        file_name = topic_name + '.txt'
        with open('Data/' + topic_name + '/' + file_name, 'r') as f:
            lines = f.readlines()
            url = lines[0]
            lines = lines[1:]
            lines = ' '.join(lines)
        content = sent_tokenize(lines)
        with open('Data/' + topic_name + '/' + 'index.txt', 'w') as f:
            f.write(url)
            for i in range(len(content)):
                f.write(str(i) + '.wav\n')
                f.write(content[i] + '\n')
        self.sentences = content
        self.current_index = -1

    def goNext(self):
        self.current_index += 1

        if self.current_index >= len(self.sentences):
            print('End of article')
            print('Pick other topic')

        self.text.delete('1.0', tk.END)
        content = self.sentences[self.current_index]
        self.text.insert(tk.END, content)
        print(self.sentences[self.current_index])

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

        filename = 'Data/' + self.emo.get() + '/' + str(self.current_index) + '.wav'
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.frames.clear()

    def record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)


# Get list of topics
topics = {}
for (dirpath, dirnames, filenames) in walk('Data'):
    for dirname in dirnames:
        topics.update({dirname: dirname})
    break

main = tk.Tk()
main.title('recording')
main.geometry('1000x500')
app = App(main, topics)
main.mainloop()
