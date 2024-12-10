import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
import math

# 설정
SAMPLE_RATE = 4000  # 샘플링 레이트 4000 Hz
FREQUENCY_LOW = 100  # 100 Hz
FREQUENCY_HIGH = 20000  # 20 kHz
DURATION = 2  # 초 (음성 길이)

# 오디오 스트림 설정
p = pyaudio.PyAudio()

# 마이크 입력 설정
input_stream = p.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=SAMPLE_RATE,
                      input=True,
                      frames_per_buffer=1024)

# 스피커 출력 설정
output_stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=SAMPLE_RATE,
                       output=True)

# 고주파 신호 생성 (100Hz ~ 20kHz)
def generate_signal(freq_low, freq_high, duration, sample_rate):
    # 시간 배열 생성
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # 랜덤하게 주파수 선택 (100 Hz ~ 20 kHz)
    freq = np.random.uniform(freq_low, freq_high)
    signal = np.sin(2 * np.pi * freq * t)
    return signal, freq

# 고주파 신호를 샘플링 레이트로 맞추기
def downsample_signal(signal, target_rate, original_rate):
    # 신호의 샘플 수를 목표 샘플링 주파수에 맞게 축소
    factor = original_rate / target_rate
    downsampled_signal = signal[::int(factor)]
    return downsampled_signal

# 고주파 신호 생성
generated_signal, generated_frequency = generate_signal(FREQUENCY_LOW, FREQUENCY_HIGH, DURATION, SAMPLE_RATE * 50)

# 신호를 샘플링 레이트로 맞추기
downsampled_signal = downsample_signal(generated_signal, SAMPLE_RATE, SAMPLE_RATE * 50)

# 신호를 16비트 PCM 형식으로 변환 (pyaudio에서 처리할 수 있도록)
audio_signal = np.int16(downsampled_signal * 32767)

# 출력 스트림으로 신호 재생
output_stream.write(audio_signal.tobytes())

# 입력 스트림에서 음성 캡처 (마이크로부터)
input_data = input_stream.read(1024)
input_signal = np.frombuffer(input_data, dtype=np.int16)

# 주파수 분석 (FFT)
def analyze_frequency(signal, sample_rate):
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1/sample_rate)
    fft_magnitude = np.abs(np.fft.rfft(signal)) / n
    return freqs, fft_magnitude

# 생성된 신호 주파수 분석
gen_freqs, gen_fft_magnitude = analyze_frequency(downsampled_signal, SAMPLE_RATE)

# 캡처된 신호 주파수 분석
captured_freqs, captured_fft_magnitude = analyze_frequency(input_signal, SAMPLE_RATE)

# 주파수 비교 시각화
plt.figure(figsize=(12, 8))

# 생성된 신호 주파수 스펙트럼
plt.subplot(2, 1, 1)
plt.plot(gen_freqs, gen_fft_magnitude)
plt.title(f"Generated Signal (Frequency Domain) - Frequency: {generated_frequency:.2f} Hz")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, SAMPLE_RATE / 2)  # Nyquist 주파수까지만 표시

# 캡처된 신호 주파수 스펙트럼
plt.subplot(2, 1, 2)
plt.plot(captured_freqs, captured_fft_magnitude)
plt.title("Captured Signal (Frequency Domain)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, SAMPLE_RATE / 2)  # Nyquist 주파수까지만 표시

plt.tight_layout()
plt.show()

# 스트림 종료
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()
