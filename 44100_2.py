import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import sounddevice as sd

# 파라미터 설정
fs = 44100
duration = 1.0
f_target = 261.63  # 듣고 싶은 도 음높이
f_high = fs - f_target  # 43838.37 Hz

def sine_wave(freq, fs, duration, amp=0.5):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return t, amp * np.sin(2*np.pi*freq*t)

# 고주파 사인파 생성
t, highfreq_do = sine_wave(f_high, fs, duration)
# 실제 도 소리 생성
t, do = sine_wave(f_target, fs, duration)

# WAV 파일로 저장
scaled = np.int16(highfreq_do * 32767)
write("aliased_do_44100.wav", fs, scaled)

scaled_orig = np.int16(do * 32767)
write("aliased_do_44100_orig.wav", fs, scaled_orig)

# WAV 파일 재생
data_float = scaled.astype(np.float32)/32767.0
sd.play(data_float, fs)
sd.wait()

# WAV 파일 다시 읽기
fs_read, data = read("aliased_do_44100.wav")
data_float_from_file = data.astype(np.float32)/32767.0

# 그래프 비교: 처음 생성한 사인파와 파일에서 읽어들인 파형 비교
# 시간축은 두 신호 모두 1초 길이이므로 동일
t_file = np.linspace(0, duration, len(data_float_from_file), endpoint=False)

plt.figure(figsize=(10, 5))

plt.subplot(2,1,1)
plt.title("Original High-Freq Sine Wave")
plt.plot(t[:200], highfreq_do[:200])  # 처음 200샘플만 확대해서 확인
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(2,1,2)
plt.title("Read from aliased_do_44100.wav")
plt.plot(t_file[:200], data_float_from_file[:200], color='orange')
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()
