import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
import matplotlib.pyplot as plt

# 1. sample.wav 로드
# 오디오 파일 읽기
audio_file = "input.mp3"  # 분석할 오디오 파일 경로
print("오디오 파일을 읽는 중...")
audio, Fs_orig = sf.read(audio_file)
print("완료 : ", audio, Fs_orig)

# 단일 채널로 변환 (스테레오일 경우)
if audio.ndim > 1:
    audio = audio.mean(axis=1)

# 2. 상향 변조: 1.5kHz 반송파 곱하기
f_carrier = 1500.0
t = np.arange(len(audio)) / Fs_orig
audio_mod = (audio * np.cos(2 * np.pi * f_carrier * t)).astype(np.float32)

# 3. 2kHz로 다운샘플링해 에일리어싱 유도
Fs_low = 2000
audio_low = resample_poly(audio_mod, up=Fs_low, down=Fs_orig).astype(np.float32)

# 4. 결과 저장
sf.write("aliased_speech.wav", audio_low, Fs_low)
print("aliased_speech.wav (2kHz) 파일이 생성되었습니다.")

# 5. 스펙트럼 분석 및 시각화
N = len(audio_low)
freqs = np.fft.fftfreq(N, 1/Fs_low)
X = np.fft.fft(audio_low)

plt.figure(figsize=(12,6))

# 시간 영역
plt.subplot(2,1,1)
time_axis = np.arange(N) / Fs_low
plt.plot(time_axis, audio_low)
plt.title("Time Domain (Aliased speech, Fs=2kHz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# 주파수 영역
plt.subplot(2,1,2)
plt.plot(freqs[:N//2], np.abs(X[:N//2]))
plt.title("Frequency Domain (Aliased speech)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")

plt.tight_layout()
plt.show()
print("에일리어싱 변조 결과 확인 완료.")
