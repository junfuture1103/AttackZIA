import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from pydub import AudioSegment
import matplotlib.pyplot as plt

# 1. MP3 파일 읽기
# 분석할 MP3 파일 경로
input_mp3 = "input.mp3"
print("MP3 파일을 읽는 중...")

# MP3 파일을 WAV로 변환하여 로드
audio_segment = AudioSegment.from_file(input_mp3, format="mp3")
wav_file = "temp.wav"
audio_segment.export(wav_file, format="wav")

# WAV 파일 로드
audio, Fs_orig = sf.read(wav_file)
print(f"원본 샘플링 레이트: {Fs_orig} Hz")

# 스테레오 -> 모노 변환
if audio.ndim > 1:
    audio = audio.mean(axis=1)

# 2. 상향 변조 (1.5 kHz 반송파 곱하기)
f_carrier = 1000.0  # 반송파 주파수
t = np.arange(len(audio)) / Fs_orig
audio_mod = (audio * np.cos(2 * np.pi * f_carrier * t)).astype(np.float32)
print("상향 변조 완료: 주파수 이동")

# 3. 다운샘플링 (2 kHz로 에일리어싱 유도)
Fs_low = 2000  # 타겟 샘플링 레이트
audio_low = resample_poly(audio_mod, up=Fs_low, down=Fs_orig).astype(np.float32)
print(f"다운샘플링 완료: 타겟 샘플링 레이트 {Fs_low} Hz")

# 4. 변환된 신호 저장 (MP3로 저장)
output_mp3 = "aliased_output.mp3"

# WAV로 임시 저장 후 MP3로 변환
aliased_wav = "aliased_output.wav"
sf.write(aliased_wav, audio_low, Fs_low)
AudioSegment.from_wav(aliased_wav).export(output_mp3, format="mp3")
print(f"MP3 파일이 생성되었습니다: {output_mp3}")



# 5. 스펙트럼 분석 및 시각화
N = len(audio_low)
freqs = np.fft.fftfreq(N, 1 / Fs_low)
X = np.fft.fft(audio_low)

plt.figure(figsize=(12, 6))

# 시간 영역
plt.subplot(2, 1, 1)
time_axis = np.arange(N) / Fs_low
plt.plot(time_axis, audio_low)
plt.title("Time Domain (Aliased signal, Fs=2kHz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# 주파수 영역
plt.subplot(2, 1, 2)
plt.plot(freqs[:N // 2], np.abs(X[:N // 2]))
plt.title("Frequency Domain (Aliased signal)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")

plt.tight_layout()
plt.show()
print("변환된 신호의 시각화 완료.")
