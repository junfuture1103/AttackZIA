import numpy as np
import sounddevice as sd

# 설정값
duration = 5.0    # 사운드 지속 시간 (초)
frequency = 1100   # 가청 주파수 (Hz)
sample_rate = 44100  # 표준 샘플링 속도

# 사인파 생성
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_signal = 0.5 * np.sin(2 * np.pi * frequency * t)

# 사운드 재생
sd.play(audio_signal, samplerate=sample_rate)
sd.wait()  # 재생이 끝날 때까지 대기
