import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io.wavfile import read, write

# 파일 읽기
fs_original, original_signal = read("original_doremi_k2.wav")
fs_original, resampled_signal = read("resampled_doremi.wav")

# 주파수 성분 분석 함수
def plot_frequency_spectrum(signal, fs, title):
    N = len(signal)
    frequencies = np.fft.fftfreq(N, d=1/fs)
    magnitude = np.abs(fft(signal))
    
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies[:N//2], magnitude[:N//2])
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.show()

# 주파수 성분 플로팅
plot_frequency_spectrum(original_signal, fs_original, 'Original Doremi at 44100 Hz')
plot_frequency_spectrum(resampled_signal, fs_original, 'Resampled Doremi at 44100 Hz')
