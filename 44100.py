import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd

# 파라미터 설정
fs = 44100
duration = 1.0
f_target = 261.63  # 듣고 싶은 도 음높이
f_high = fs - f_target  # 43838.37 Hz

def sine_wave(freq, fs, duration, amp=0.5):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return amp * np.sin(2*np.pi*freq*t)

# 고주파 사인파 생성 (나이퀴스트 초과)
highfreq_do = sine_wave(f_high, fs, duration)

# 16비트 정수 변환
scaled = np.int16(highfreq_do * 32767)
write("aliased_do_44100.wav", fs, scaled)

# 사운드 재생 (이 신호는 실제로 261.63 Hz 대역으로 들린다)
data_float = scaled.astype(np.float32)/32767.0
sd.play(data_float, fs)
sd.wait()
