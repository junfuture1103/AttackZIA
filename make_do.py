import numpy as np
from scipy.io.wavfile import write

# 파라미터 설정
fs_original = 44100
fs_target = 4000
duration = 1.0  # 1초 재생
f_do = 261.63

# 다운샘플링 비율 계산
ratio = fs_target / fs_original  # 약 0.0907
inv_ratio = 1.0 / ratio          # 약 11.025

# 원본에서 필요한 주파수 계산
f_do_org = f_do * inv_ratio  # 약 2885.9 Hz

def sine_wave(freq, fs, duration, amp=0.5):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return amp * np.sin(2*np.pi*freq*t)

# 원본(44100 Hz)에서 도 음높이를 위한 높은 주파수 톤 생성
do_wave = sine_wave(f_do_org, fs_original, duration)
scaled_wave = np.int16(do_wave * 32767)
write("original_highfreq_do.wav", fs_original, scaled_wave)

###################################
# 사용 가이드:
# 1. "original_highfreq_do.wav"를 44100 Hz로 재생하면 매우 높은 톤.
# 2. sox로 리샘플링:
#    sox original_highfreq_do.wav -r 4000 aliased_do.wav
# 3. "aliased_do.wav"를 4000 Hz로 재생하면 원래의 도(261.63 Hz)로 들리는 앨리어싱 효과.
###################################
