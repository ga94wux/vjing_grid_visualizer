import sounddevice as sd
import numpy as np
import threading

class AudioAnalyzer:
    def __init__(self):
        self.bass_energy = 0.0
        self.mid_energy = 0.0
        self.global_level = 0.0
        self.smoothed_bass = 0.0
        self.smoothed_mid = 0.0
        self.smoothed_level = 0.0
        self.running = False
        self.stream = None

    def audio_callback(self, indata, frames, time, status):
        mono = np.mean(indata, axis=1)
        fft_vals = np.abs(np.fft.rfft(mono))
        freqs = np.fft.rfftfreq(len(mono), d=1/44100)

        bass = np.mean(fft_vals[(freqs >= 20) & (freqs < 250)])
        mid = np.mean(fft_vals[(freqs >= 400) & (freqs < 3000)])
        level = np.linalg.norm(mono) / len(mono)

        # Glättung
        self.smoothed_bass = 0.9 * self.smoothed_bass + 0.1 * bass
        self.smoothed_mid = 0.9 * self.smoothed_mid + 0.1 * mid
        self.smoothed_level = 0.9 * self.smoothed_level + 0.1 * level

        self.bass_energy = self.smoothed_bass
        self.mid_energy = self.smoothed_mid
        self.global_level = self.smoothed_level

    def start(self):
        self.running = True
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=44100)
        self.stream.start()

    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
