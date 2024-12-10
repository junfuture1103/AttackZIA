import numpy as np
import matplotlib.pyplot as plt

# 파라미터 설정
sampling_rate = 4000  # 샘플링 레이트 (Hz)
duration = 0.01  # 신호 길이 (초)
time = np.arange(0, duration, 1/sampling_rate)

# 테스트할 원 신호 주파수 목록
signal_frequencies = [1500, 2500, 3000, 4500, 5200, 6000, 7500]

# 시뮬레이션 함수
def simulate_aliasing(freq):
    # 원 신호 생성 (사인파)
    original_signal = np.sin(2 * np.pi * freq * time)
    
    # 주파수 스펙트럼 계산
    freq_spectrum = np.fft.fftfreq(len(time), d=1/sampling_rate)
    signal_spectrum = np.fft.fft(original_signal)

    # 시각화
    plt.figure(figsize=(12, 6))

    # 원 신호 시간 도메인
    plt.subplot(2, 1, 1)
    plt.title(f"Original Signal: {freq} Hz (Sampling Rate: {sampling_rate} Hz)")
    plt.plot(time, original_signal, label=f"Original {freq} Hz")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()

    # 주파수 도메인 스펙트럼
    plt.subplot(2, 1, 2)
    plt.title("Frequency Spectrum (Magnitude)")
    plt.stem(freq_spectrum[:len(freq_spectrum)//2], np.abs(signal_spectrum[:len(signal_spectrum)//2]), use_line_collection=True)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# 모든 테스트 주파수에 대해 시뮬레이션 수행
for freq in signal_frequencies:
    simulate_aliasing(freq)
