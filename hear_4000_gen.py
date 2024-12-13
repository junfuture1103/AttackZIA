import numpy as np
import soundfile as sf

def generate_tone(frequency=1500, duration=5, samplerate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    tone = amplitude * np.sin(2 * np.pi * frequency * t)
    return tone


def save_audio(filename, audio, samplerate):
    sf.write(filename, audio, samplerate)
    print(f"Audio saved to {filename}")


if __name__ == "__main__":
    tone = generate_tone(frequency=4100, duration=5, samplerate=44100)
    save_audio("1500hz_tone.wav", tone, 44100)