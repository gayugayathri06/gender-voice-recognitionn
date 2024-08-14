import tkinter as tk
from tkinter import filedialog, messagebox
import pyaudio
import wave
import threading
import librosa
import numpy as np
import os

# Constants
RECORD_SECONDS = 30
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class VoiceGenderApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Voice Gender detectio")
        
        self.record_button = tk.Button(root, text="Record Voice", command=self.record_voice)
        self.record_button.pack(pady=10)
        
        self.upload_button = tk.Button(root, text="Upload Voice Note", command=self.upload_voice_note)
        self.upload_button.pack(pady=10)
        
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)
        
        self.audio_data = None
    
    def record_voice(self):
        self.status_label.config(text="Recording... Please speak.")
        self.root.update_idletasks()
        
        def record():
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            frames = []
            
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            wf = wave.open("output.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            self.status_label.config(text="Recording finished.")
            self.audio_data = "output.wav"
            self.process_audio()
        
        threading.Thread(target=record).start()
    
    def upload_voice_note(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
        if file_path:
            self.audio_data = file_path
            self.process_audio()
    
    def process_audio(self):
        if self.audio_data is None:
            self.status_label.config(text="Please provide an audio file.")
            return
        
        # Check the duration of the audio
        duration = librosa.get_duration(filename=self.audio_data)
        if duration < 30:
            messagebox.showerror("Error", "The voice note must be more than 30 seconds.")
            self.audio_data = None
            return
                # Load the audio and check for the word "HI"
        y, sr = librosa.load(self.audio_data, sr=RATE)
        transcript = self.transcribe_audio(y, sr)
        
        if "hi" in transcript.lower():
            messagebox.showerror("Error", 'The voice note contains the word "HI". Please provide another voice note.')
            self.audio_data = None
            return
        
        # Proceed with gender prediction
        self.predict_gender(y, sr)
    
    def transcribe_audio(self, y, sr):
        # Dummy transcription for the sake of example. In a real application, you would use a proper speech recognition library.
        return "this is a dummy transcription without the word hi"
    
    def predict_gender(self, y, sr):
        # Dummy gender prediction for the sake of example. Replace with your actual model inference code.
        gender = "male" if np.mean(y) > 0 else "female"
        messagebox.showinfo("Prediction", f"The predicted gender is: {gender}")

if _name_ == "_main_":
    root = tk.Tk()
    app = VoiceGenderApp(root)
    root.mainloop()