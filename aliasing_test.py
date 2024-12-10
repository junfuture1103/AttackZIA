import numpy as np
import matplotlib.pyplot as plt

# 파라미터 설정
Fs = 2000  # 샘플링 주파수 (1 kHz)
f_signal = 1900  # 실제 입력 신호 주파수
duration = 0.01  # 신호 지속 시간 (초)

# 시간 벡터 생성
t = np.linspace(0, duration, int(Fs*duration), endpoint=False)

# 사인파 신호 생성
x = np.sin(2 * np.pi * f_signal * t)

# FFT 계산
X = np.fft.fft(x)
N = len(X)
freqs = np.fft.fftfreq(N, 1/Fs)

# 스펙트럼 반으로 잘라 대칭성 제거 및 양의 주파수만 보기
X_half = X[:N//2]
freqs_half = freqs[:N//2]

# 주파수 스케일 맞추기
magnitude = np.abs(X_half)

# 시간영역 파형 표시
plt.figure(figsize=(12, 6))
plt.subplot(2,1,1)
plt.plot(t, x)
plt.title(f"Time Domain Signal (f={f_signal} Hz, Fs={Fs} Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# 주파수 영역 스펙트럼 표시
plt.subplot(2,1,2)
plt.stem(freqs_half, magnitude, use_line_collection=True)
plt.title("Frequency Domain Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.tight_layout()
plt.show()
