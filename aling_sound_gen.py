import numpy as np
from scipy.io.wavfile import write

# 파라미터 설정
fs_original = 44100
fs_target = 4000
duration = 0.5  # 각 음을 0.5초씩
f_do = 261.63
f_re = 293.66
f_mi = 329.63

# 다운샘플링 비율
ratio = fs_target / fs_original  # 약 0.0907
inv_ratio = 1.0 / ratio          # 약 11.025

# 다운샘플링 후 도레미를 얻기 위해 원본에서의 주파수
f_do_org = f_do * inv_ratio    # ≈ 2885.9 Hz
f_re_org = f_re * inv_ratio    # ≈ 3238.8 Hz
f_mi_org = f_mi * inv_ratio    # ≈ 3635.1 Hz

def sine_wave(freq, fs, duration, amp=0.5):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return amp * np.sin(2*np.pi*freq*t)

# 원본(44100 Hz)에서 도레미 사인파 생성
do_wave = sine_wave(f_do_org, fs_original, duration)
re_wave = sine_wave(f_re_org, fs_original, duration)
mi_wave = sine_wave(f_mi_org, fs_original, duration)

doremi_wave = np.concatenate([do_wave, re_wave, mi_wave])
scaled_wave = np.int16(doremi_wave * 32767)
write("original_highfreq_sine.wav", fs_original, scaled_wave)
