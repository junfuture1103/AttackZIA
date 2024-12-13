import numpy as np
from scipy.io.wavfile import write, read
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq

# 파라미터 설정
fs = 4000
duration = 1.0
f_do = 261.63     # 목표: 도 음높이
offset = 5.0      # 오프셋 Hz (목표 주파수보다 5 Hz 낮은 음으로 Aliasing)
# 앨리어싱용 주파수: f_h = fs - (f_do + offset)
f_alias = fs - (f_do + offset)

t = np.linspace(0, duration, int(fs*duration), endpoint=False)

# 사인파 생성 함수
def sine_wave(freq, amp=0.5, fs=4000, duration=1.0):
    tt = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return amp * np.sin(2 * np.pi * freq * tt)

# 1. 앨리어싱 전 신호(실제 도 음높이)
before_wave = sine_wave(f_do, amp=0.5, fs=fs, duration=duration)
scaled_before = np.int16(before_wave * 32767)
write("before_aliased_doremi.wav", fs, scaled_before)

# 2. 앨리어싱 후 신호(고주파수 사인파)
# 실제 재생시 약 f_do + offset = 261.63+5 = 266.63 Hz보다 낮게 들려야 할 것을 기대했지만
# Aliasing 식에 따라: f_alias_effective = |f_alias - fs| = |(4000-(f_do+offset))-4000| = f_do+offset
# 하지만 부호 반전과 2π배수로 인해 실제 음높이는 약간 다른 피치로 들릴 수 있음
# 정확히 f_alias = 4000 - (261.63+5) = 4000-266.63=3733.37 Hz
# 샘플링 시 Aliasing: |3733.37 - 4000|=266.63 Hz이지만 위상 반전으로 256.63 Hz로 인식되는 상황 구현
# 아래 과정: f_alias에서 살짝 조정할 수도 있음.
aliased_wave = sine_wave(f_alias, amp=0.5, fs=fs, duration=duration)
scaled_alias = np.int16(aliased_wave * 32767)
write("aliased_doremi.wav", fs, scaled_alias)

# 3. FFT 분석 함수
def analyze_fft(signal, fs):
    N = len(signal)
    W = fft(signal)
    freqs = fftfreq(N, 1/fs)
    # 양수 주파수 영역만 추출
    half = N//2
    freqs_half = freqs[:half]
    mag_half = np.abs(W[:half])
    # 피크 주파수 추출
    peak_idx = np.argmax(mag_half)
    peak_freq = freqs_half[peak_idx]
    return freqs_half, mag_half, peak_freq

# FFT 분석
freqs_before, mag_before, peak_before = analyze_fft(before_wave, fs)
freqs_alias, mag_alias, peak_alias = analyze_fft(aliased_wave, fs)

print("Before Aliased Peak Frequency:", peak_before)
print("Aliased Peak Frequency:", peak_alias)
print("Difference in Peak Frequency:", peak_before - peak_alias)

# FFT 결과 시각화
plt.figure(figsize=(10,4))
plt.title("Spectrum Comparison")
plt.plot(freqs_before, mag_before, label='Before Aliased', alpha=0.7)
plt.plot(freqs_alias, mag_alias, label='Aliased', alpha=0.7)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.legend()
plt.xlim(0, 500)  # 저주파 범위 확인
plt.show()

# 4. 맥놀이(Beat) 관찰: before와 aliased 신호 혼합
mixed_wave = before_wave + aliased_wave
mixed_wave /= np.max(np.abs(mixed_wave))
scaled_mixed = np.int16(mixed_wave * 32767)
write("before_aliased_doremi_mixed.wav", fs, scaled_mixed)

# 맥놀이 관찰용 파형 일부 구간 시각화
plt.figure(figsize=(10,4))
plt.title("Mixed Waveform (Beat Observation)")
plt.plot(t[:500], mixed_wave[:500]) # 첫 500샘플 구간
plt.xlabel("Time (s) [zoomed in samples]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

# (옵션) 사운드 재생: 주석 해제 시 사용 가능
import sounddevice as sd
sd.play(before_wave, fs)
sd.wait()
sd.play(aliased_wave, fs)
sd.wait()
sd.play(mixed_wave, fs)
sd.wait()
