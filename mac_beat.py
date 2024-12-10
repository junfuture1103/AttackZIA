import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 설정값
duration = 5.0     # 시각화 시간 (초)
sample_rate = 44100  # 표준 샘플링 속도

# 주파수 설정 (맥놀이 생성)
left_freq = 440  # 왼쪽 귀 주파수 (Hz)
right_freq = 445  # 오른쪽 귀 주파수 (Hz)

# 시간 축 생성
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# 사운드 신호 생성
left_signal = 0.5 * np.sin(2 * np.pi * left_freq * t)
right_signal = 0.5 * np.sin(2 * np.pi * right_freq * t)

# 맥놀이 신호 결합 (양쪽 합성파)
binaural_signal = left_signal + right_signal

# 그래프 설정
fig, ax = plt.subplots(figsize=(12, 6))
line_left, = ax.plot([], [], lw=2, label="Left Channel (440Hz)")
line_right, = ax.plot([], [], lw=2, label="Right Channel (445Hz)")
line_binaural, = ax.plot([], [], lw=2, label="Binaural Beat (Sum)")

ax.set_xlim(0, 0.02)  # 시간축 제한 (20ms만 표시)
ax.set_ylim(-1, 1)
ax.set_title("Binaural Beat Visualization")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.legend()

# 업데이트 함수
def update(frame):
    time_window = t[frame:frame + 1000]  # 1000 샘플 시각화
    left_window = left_signal[frame:frame + 1000]
    right_window = right_signal[frame:frame + 1000]
    binaural_window = binaural_signal[frame:frame + 1000]

    line_left.set_data(time_window, left_window)
    line_right.set_data(time_window, right_window)
    line_binaural.set_data(time_window, binaural_window)

    return line_left, line_right, line_binaural

# 애니메이션 생성
ani = animation.FuncAnimation(fig, update, frames=range(0, len(t)-1000, 1000), interval=50, blit=True)

plt.show()
