import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import resample

# 오디오 파일 읽기
audio_file = "input_music.wav"  # 분석할 오디오 파일 경로
# audio_file = "output_audio.wav"  # 분석할 오디오 파일 경로
#audio_file = "output_audio.wav"
audio_data, original_sample_rate = sf.read(audio_file)

print(f"원본 샘플링 레이트: {original_sample_rate} Hz")
print(f"데이터 형태: {audio_data.shape}")

# 단일 채널 변환 (필요시)
if audio_data.ndim > 1:
    audio_data = audio_data.mean(axis=1)
    print("오디오 데이터를 단일 채널로 변환했습니다.")

# 샘플링 레이트를 40000 Hz로 지정 (목표 샘플링 레이트)
target_sample_rate = 2000

# 현재 샘플링 레이트가 목표 샘플링 레이트와 다른 경우 리샘플링 수행
if original_sample_rate != target_sample_rate:
    print(f"샘플링 레이트를 {original_sample_rate} Hz에서 {target_sample_rate} Hz로 리샘플링 중...")
    num_samples = int(len(audio_data) * target_sample_rate / original_sample_rate)
    audio_data_resampled = resample(audio_data, num_samples)
    print("리샘플링 완료.")
else:
    audio_data_resampled = audio_data
    print("리샘플링이 필요하지 않습니다.")

# FFT 수행
fft_data = np.fft.fft(audio_data_resampled)
fft_freq = np.fft.fftfreq(len(fft_data), 1 / target_sample_rate)

# 주파수 성분 계산 (양쪽 절반만 보기)
magnitude = np.abs(fft_data)
half_len = len(magnitude) // 2
half_mag = magnitude[:half_len]
half_freq = fft_freq[:half_len]

# 상위 3개 주파수 추출
top3_indices = np.argsort(half_mag)[-3:]
top3_indices = top3_indices[::-1]  # 내림차순 정렬

print("가장 강한 주파수 상위 3개:")
for i in top3_indices:
    print(f"주파수: {half_freq[i]:.2f} Hz, 크기(Magnitude): {half_mag[i]:.5f}")

# 그래프 시각화
plt.figure(figsize=(12, 6))
plt.plot(half_freq, half_mag, label='Magnitude Spectrum')

# 상위 3개 주파수에 마커와 레이블 추가
for i in top3_indices:
    plt.plot(half_freq[i], half_mag[i], 'ro')  # 빨간 점 표시
    plt.text(half_freq[i], half_mag[i],
             f"{half_freq[i]:.2f} Hz",
             fontsize=10, color='red',
             horizontalalignment='right')

plt.title("오디오 파일 주파수 스펙트럼 상위 3개 강력 주파수")
plt.xlabel("주파수 (Hz)")
plt.ylabel("크기 (Magnitude)")
plt.xlim(0, 20000)  # x축을 0부터 20,000 Hz까지 설정
plt.ylim(0, np.max(half_mag) * 1.1)  # y축 범위 약간 확장
plt.grid(True)
plt.legend()
plt.show()
