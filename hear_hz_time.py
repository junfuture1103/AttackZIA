import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 설정값
sample_rate = 44100  # 표준 샘플링 속도
window_size = 1024   # FFT 창 크기 (버퍼)
update_interval = 10  # 업데이트 주기 (ms)

# 그래프 설정
fig, ax = plt.subplots(figsize=(12, 6))
line, = ax.plot([], [], lw=2)
ax.set_title("실시간 주파수 스펙트럼")
ax.set_xlabel("주파수 (Hz)")
ax.set_ylabel("크기 (Magnitude)")
ax.grid(True)
ax.set_xlim(0, 5000)  # 주파수 범위 제한 (최대 5000Hz)
ax.set_ylim(0, 100)   # 초기 크기 범위 설정

# 업데이트 함수
def update_spectrum(frame):
    # 마이크 입력 캡처
    recording = sd.rec(window_size, samplerate=sample_rate, channels=1, blocking=True).flatten()
    
    # FFT 수행
    fft_data = np.fft.fft(recording)
    fft_freq = np.fft.fftfreq(len(fft_data), 1 / sample_rate)
    magnitude = np.abs(fft_data[:window_size//2])

    # 그래프 업데이트
    line.set_data(fft_freq[:window_size//2], magnitude)
    ax.set_ylim(0, np.max(magnitude) + 10)  # Y축 동적 조정
    return line,

# 실시간 애니메이션 생성
ani = animation.FuncAnimation(fig, update_spectrum, interval=update_interval, blit=True)

# 시각화 시작
plt.show()
