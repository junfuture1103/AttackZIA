import numpy as np
import sounddevice as sd

# 설정값
duration = 5.0     # 사운드 지속 시간 (초)
sample_rate = 44100  # 표준 샘플링 속도

# 주파수 설정 (맥놀이 생성)
left_freq = 4400  # 왼쪽 귀 주파수 (Hz)
right_freq = 4401  # 오른쪽 귀 주파수 (Hz)

# 시간 축 생성
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# 사운드 신호 생성
left_signal = 0.5 * np.sin(2 * np.pi * left_freq * t)
right_signal = 0.5 * np.sin(2 * np.pi * right_freq * t)

# 스테레오 사운드 결합
stereo_signal = np.stack((left_signal, right_signal), axis=-1)

# 사운드 재생
print(f"맥놀이 발생: {abs(left_freq - right_freq)}Hz")
sd.play(stereo_signal, samplerate=sample_rate)
sd.wait()
