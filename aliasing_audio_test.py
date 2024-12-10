import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time

# 출력용 파라미터
Fs_out = 44100    # 출력 샘플링 레이트
f_tone = 1900      # 출력 사인파 주파수
duration = 2.0    # 재생 시간(초)

# 입력용 파라미터
Fs_in = 2000       # 입력(녹음) 샘플링 레이트
record_duration = 2.0  # 녹음 시간(초)
frames_to_record = int(Fs_in * record_duration)

# 사인파 생성 (출력 신호)
t_out = np.linspace(0, duration, int(Fs_out * duration), endpoint=False)
x_out = np.sin(2 * np.pi * f_tone * t_out).astype(np.float32)

# PyAudio 초기화
p = pyaudio.PyAudio()

# 출력 스트림 열기
stream_out = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=Fs_out,
                    output=True)

# 입력 스트림 열기
stream_in = p.open(format=pyaudio.paInt16,
                   channels=1,
                   rate=Fs_in,
                   input=True,
                   frames_per_buffer=1024)

# 톤 재생 시작
stream_out.write(x_out.tobytes())

# 녹음 진행
# 여기서는 톤 재생과 녹음을 동시에 하기위해 톤 재생 직후 녹음 시작
# 톤이 출력되는 동안 마이크로 녹음
time.sleep(0.5)  # 톤이 완전히 시작될 때까지 살짝 대기 (옵션)
audio_frames = []
for i in range(0, int(frames_to_record/1024)+1):
    data = stream_in.read(1024)
    audio_frames.append(data)

# 스트림 종료
stream_out.stop_stream()
stream_out.close()

stream_in.stop_stream()
stream_in.close()
p.terminate()

# 녹음 데이터 처리
audio_data = b''.join(audio_frames)
audio_samples = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
# audio_samples는 정수형이므로 float32로 변환 (규모정규화 필요시 추가 처리)
# 길이 조정을 통한 정확한 프레임 확보
audio_samples = audio_samples[:frames_to_record]

# FFT 계산
X = np.fft.fft(audio_samples)
N = len(X)
freqs = np.fft.fftfreq(N, 1/Fs_in)
X_half = X[:N//2]
freqs_half = freqs[:N//2]

# 스펙트럼 성분 분석
magnitude = np.abs(X_half)

# 시간 파형 및 스펙트럼 시각화
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
t_in = np.linspace(0, record_duration, frames_to_record, endpoint=False)
plt.plot(t_in, audio_samples)
plt.title(f"Recorded Time Domain Signal (Fs_in={Fs_in} Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

plt.subplot(2,1,2)
plt.stem(freqs_half, magnitude, use_line_collection=True)
plt.title("Frequency Spectrum of Recorded Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.tight_layout()
plt.show()

# 이 결과에서 원래 900 Hz였던 신호가 Nyquist(=500 Hz)를 초과하므로
# folding되어 100 Hz 근처 성분으로 나타나는지 확인 가능.
