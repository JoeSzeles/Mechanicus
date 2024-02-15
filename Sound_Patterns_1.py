import numpy as np
import pyaudio
import tkinter as tk
from tkinter import Scale, Button

class FrequencyGenerator:
    def __init__(self):
        self.sample_rate = 44100
        self.amplitude = 1.0
        self.channels = 1
        self.duration = 1.0
        self.frequency = 440.0
        self.sound_on = False  # Initially, sound is off

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=self.sample_rate,
            output=True,
        )

    def play_frequency(self):
        if self.sound_on:
            num_samples = int(self.sample_rate * self.duration)
            t = np.linspace(0, self.duration, num_samples, False)
            audio_data = self.amplitude * np.sin(2 * np.pi * self.frequency * t)
            self.stream.write(audio_data.tobytes())

    def update_frequency(self, frequency):
        self.frequency = float(frequency)
        self.play_frequency()

    def update_amplitude(self, amplitude):
        self.amplitude = float(amplitude)
        self.play_frequency()

    def toggle_sound(self):
        self.sound_on = not self.sound_on

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

def update_frequency_callback(value):
    generator.update_frequency(value)

def update_amplitude_callback(value):
    generator.update_amplitude(value)

def toggle_sound_callback():
    generator.toggle_sound()
    sound_button.config(text="Sound On" if generator.sound_on else "Sound Off")

if __name__ == "__main__":
    generator = FrequencyGenerator()

    root = tk.Tk()
    root.title("Real-time Frequency Control")

    frequency_scale = Scale(root, label="Frequency (Hz)", from_=20, to=2000, orient="horizontal", command=update_frequency_callback)
    frequency_scale.pack()

    amplitude_scale = Scale(root, label="Amplitude", from_=0, to=1, resolution=0.01, orient="horizontal", command=update_amplitude_callback)
    amplitude_scale.pack()

    sound_button = Button(root, text="Sound Off", command=toggle_sound_callback)
    sound_button.pack()

    root.mainloop()

    generator.close()
