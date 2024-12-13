import numpy as np
from scipy.io.wavfile import write

# 파라미터 설정
fs = 44100
duration = 1.0
f_target = 261.63  # 듣고 싶은 도 음높이
f_low = f_target / 2  # 더 낮은 주파수

def sine_wave(freq, fs, duration, amp=0.5):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return t, amp * np.sin(2*np.pi*freq*t)

# 저주파 사인파 생성
t, lowfreq_do = sine_wave(f_low, fs, duration)
# 실제 도 소리 생성
t, do = sine_wave(f_target, fs, duration)

# WAV 파일로 저장
scaled_low = np.int16(lowfreq_do * 32767)
write("lowfreq_do_44100.wav", fs, scaled_low)

scaled_orig = np.int16(do * 32767)
write("do_44100_orig.wav", fs, scaled_orig)
