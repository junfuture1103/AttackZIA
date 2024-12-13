import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import sounddevice as sd
from scipy.io.wavfile import write

# 생성 파라미터
fs_original = 44100  # 원래 샘플링 레이트
fs_new = 4000  # 새 샘플링 레이트

duration = 1.0  # 1초 지속

# 도레미 주파수 목록 (미디 음계 기준)
k = 2
do = 262 * k
re = 262 * k
mi = 262 * k

note_frequencies = [262, 294, 330]  # 도, 레, 미

# 소리 생성 (44100Hz 기준)
signal = np.concatenate([
    np.sin(2 * np.pi * f * np.linspace(0, duration/3, int(fs_original * duration/3), endpoint=False))
    for f in note_frequencies
])

# 원본 소리 저장
write("original_doremi_k2.wav", fs_original, (signal * 32767).astype(np.int16))

# 새 샘플링 레이트로 리샘플링
samples_new = np.arange(0, len(signal), fs_original / fs_new, dtype=int)
resampled_signal = signal[samples_new]

# 리샘플링된 소리 저장
write("resampled_doremi.wav", fs_original, (resampled_signal * 32767).astype(np.int16))

# 소리 재생
print("리샘플링된 소리 재생 중...")
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
