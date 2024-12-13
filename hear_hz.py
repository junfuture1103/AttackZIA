import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# 설정값
duration = 2.0    # 캡처 지속 시간 (초)
sample_rate = 40000  # 표준 샘플링 속도

# 마이크 입력 캡처
print("마이크 입력을 캡처 중...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()  # 캡처 완료 대기

# FFT 수행
print("주파수 분석 중...")
fft_data = np.fft.fft(recording.flatten())
fft_freq = np.fft.fftfreq(len(fft_data), 1 / sample_rate)

# 주파수 성분 계산 (양쪽 절반만 보기)
magnitude = np.abs(fft_data)
peak_freq = fft_freq[np.argmax(magnitude[:len(magnitude)//2])]

# 결과 출력
print(f"가장 강한 주파수: {peak_freq:.2f} Hz")

# 시각화: 모든 주파수 스펙트럼
plt.figure(figsize=(12, 6))
#plt.plot(fft_freq[:len(magnitude)//2], magnitude[:len(magnitude)//2])///
plt.plot(fft_freq[:len(magnitude)//2], magnitude[:len(magnitude)//2])
plt.xlim(0, 5000)  # x축 범위 설정
plt.title(f"마이크 입력 주파수 스펙트럼 (가장 강한 주파수: {peak_freq:.2f} Hz)")
plt.xlabel("주파수 (Hz)")
plt.ylabel("크기 (Magnitude)")
plt.grid(True)
plt.show()
