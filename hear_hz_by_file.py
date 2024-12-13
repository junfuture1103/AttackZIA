import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import resample

# 오디오 파일 읽기
#audio_file = "aliased_doremi.wav"
audio_file = "original_doremi.wav"
#audio_file = "aliased_4000_doremi.wav"
audio_data, original_sample_rate = sf.read(audio_file)

print(f"원본 샘플링 레이트: {original_sample_rate} Hz")
print(f"데이터 형태: {audio_data.shape}")

# 단일 채널 변환 (필요시)
if audio_data.ndim > 1:
    audio_data = audio_data.mean(axis=1)
    print("오디오 데이터를 단일 채널로 변환했습니다.")

# 목표 샘플링 레이트 지정
target_sample_rate = 4000

# 리샘플링 수행
if original_sample_rate != target_sample_rate:
    print(f"샘플링 레이트를 {original_sample_rate} Hz에서 {target_sample_rate} Hz로 리샘플링 중...")
    num_samples = int(len(audio_data) * target_sample_rate / original_sample_rate)
    audio_data_resampled = resample(audio_data, num_samples)
    print("리샘플링 완료.")
else:
    audio_data_resampled = audio_data
    print("리샘플링이 필요하지 않습니다.")

# 리샘플링된 오디오를 파일로 저장
output_file = "resampled_output.wav"
sf.write(output_file, audio_data_resampled, target_sample_rate)
print(f"리샘플링된 오디오 파일이 '{output_file}'에 저장되었습니다.")


# FFT 함수 정의
def compute_fft(data, fs):
    fft_data = np.fft.fft(data)
    fft_freq = np.fft.fftfreq(len(fft_data), 1/fs)
    magnitude = np.abs(fft_data)
    half_len = len(magnitude) // 2
    return fft_freq[:half_len], magnitude[:half_len]

# 원본 오디오 FFT 계산
original_freq, original_mag = compute_fft(audio_data, original_sample_rate)
# 리샘플링 오디오 FFT 계산
resampled_freq, resampled_mag = compute_fft(audio_data_resampled, target_sample_rate)

# 원본 오디오 상위 3개 주파수
top3_indices_original = np.argsort(original_mag)[-3:][::-1]
print("원본 오디오에서 가장 강한 주파수 상위 3개:")
for i in top3_indices_original:
    print(f"주파수: {original_freq[i]:.2f} Hz, 크기(Magnitude): {original_mag[i]:.5f}")

# 리샘플링 오디오 상위 3개 주파수
top3_indices_resampled = np.argsort(resampled_mag)[-3:][::-1]
print("리샘플링된 오디오에서 가장 강한 주파수 상위 3개:")
for i in top3_indices_resampled:
    print(f"주파수: {resampled_freq[i]:.2f} Hz, 크기(Magnitude): {resampled_mag[i]:.5f}")

# 그래프 시각화
plt.figure(figsize=(14, 6))

# 원본 스펙트럼
plt.subplot(1, 2, 1)
plt.plot(original_freq, original_mag, label='Original Magnitude Spectrum', color='blue')
for i in top3_indices_original:
    plt.plot(original_freq[i], original_mag[i], 'ro')
    plt.text(original_freq[i], original_mag[i], f"{original_freq[i]:.2f} Hz", fontsize=10, color='red', horizontalalignment='right')
plt.title("원본 오디오 주파수 스펙트럼")
plt.xlabel("주파수 (Hz)")
plt.ylabel("크기 (Magnitude)")
plt.grid(True)
plt.legend()

# 리샘플링 스펙트럼
plt.subplot(1, 2, 2)
plt.plot(resampled_freq, resampled_mag, label='Resampled Magnitude Spectrum', color='green')
for i in top3_indices_resampled:
    plt.plot(resampled_freq[i], resampled_mag[i], 'ro')
    plt.text(resampled_freq[i], resampled_mag[i], f"{resampled_freq[i]:.2f} Hz", fontsize=10, color='red', horizontalalignment='right')
plt.title("리샘플링된 오디오 주파수 스펙트럼")
plt.xlabel("주파수 (Hz)")
plt.ylabel("크기 (Magnitude)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
