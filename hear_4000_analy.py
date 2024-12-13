import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def read_audio(filename):
    print(f"Reading audio from {filename}...")
    audio, samplerate = sf.read(filename)
    print("Reading complete.")
    return audio, samplerate


def plot_frequency_spectrum(audio, samplerate):
    print("Computing frequency spectrum...")
    n = len(audio)
    freq = np.fft.rfftfreq(n, d=1/samplerate)
    magnitude = np.abs(np.fft.rfft(audio))

    plt.figure(figsize=(10, 6))
    plt.plot(freq, magnitude)
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    input_filename = "resampled_audio.wav"
    audio, samplerate = read_audio(input_filename)
    print(audio, samplerate)
    plot_frequency_spectrum(audio, samplerate)
