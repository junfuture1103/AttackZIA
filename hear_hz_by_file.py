import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import resample

# 오디오 파일 읽기
audio_file = "result2.wav"  # 분석할 오디오 파일 경로
print("오디오 파일을 읽는 중...")
audio_data, original_sample_rate = sf.read(audio_file)

# 단일 채널로 변환 (스테레오일 경우)
# if audio_data.ndim > 1:
#    audio_data = audio_data.mean(axis=1)

# 샘플링 레이트를 4000 Hz로 변경
target_sample_rate = 4000
#print(f"원본 샘플링 레이트: {original_sample_rate} Hz -> 목표 샘플링 레이트: {target_sample_rate} Hz")
#num_samples = int(len(audio_data) * target_sample_rate / original_sample_rate)
#audio_data_resampled = resample(audio_data, num_samples)
audio_data_resampled = audio_data

# FFT 수행
print("주파수 분석 중...")
fft_data = np.fft.fft(audio_data_resampled.flatten())
fft_freq = np.fft.fftfreq(len(fft_data), 1 / target_sample_rate)

# 주파수 성분 계산 (양쪽 절반만 보기)
magnitude = np.abs(fft_data)
peak_freq = fft_freq[np.argmax(magnitude[:len(magnitude)//2])]

# 결과 출력
print(f"가장 강한 주파수: {peak_freq:.2f} Hz")

# 시각화: 모든 주파수 스펙트럼
plt.figure(figsize=(12, 6))
plt.plot(fft_freq[:len(magnitude)//2], magnitude[:len(magnitude)//2])
plt.title(f"오디오 파일 주파수 스펙트럼 (가장 강한 주파수: {peak_freq:.2f} Hz)")
plt.xlabel("주파수 (Hz)")
plt.ylabel("크기 (Magnitude)")
plt.grid(True)
plt.show()
