import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import sounddevice as sd

# 생성 파라미터
fs_original = 44100  # 원래 샘플링 레이트
fs_new = 4000  # 새 샘플링 레이트
f_tone = 3000  # 생성할 톤 주파수

duration = 1.0  # 1초 지속

# 소리 생성 (44100Hz 기준)
t = np.linspace(0, duration, int(fs_original * duration), endpoint=False)
signal = np.sin(2 * np.pi * f_tone * t)

print("재생 중...")
sd.play(signal, samplerate=fs_original)
sd.wait()

# 새 샘플링 레이트로 리샘플링
samples_new = np.arange(0, len(signal), fs_original / fs_new, dtype=int)
resampled_signal = signal[samples_new]

# 소리 재생
print("재생 중...")
sd.play(resampled_signal, samplerate=fs_new)
sd.wait()

# 주파수 성분 분석
N = len(resampled_signal)
frequencies = np.fft.fftfreq(N, d=1/fs_new)
magnitude = np.abs(fft(resampled_signal))

# 플롯
plt.figure(figsize=(10, 6))
plt.plot(frequencies[:N//2], magnitude[:N//2])
plt.title(f'Frequency Spectrum at {fs_new} Hz Sampling Rate')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.show()
