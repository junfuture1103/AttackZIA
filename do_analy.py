import numpy as np
from scipy.io.wavfile import read, write
from scipy.signal import resample
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq

##############################
# 파라미터 설정
##############################
fs_target = 4000
f_do = 261.63
duration = 1.0

##############################
# 함수 정의
##############################
def get_fft(signal, fs):
    N = len(signal)
    W = fft(signal)
    freqs = fftfreq(N, 1/fs)
    half = N//2
    return freqs[:half], np.abs(W[:half])/N

def sine_wave(freq, fs, duration, amp=0.5):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return amp * np.sin(2*np.pi*freq*t)

##############################
# 1. original_highfreq_do.wav 읽기
##############################
fs_original, data = read("original_highfreq_do.wav")
data_float = data.astype(np.float32)/32767.0

##############################
# 2. 4000 Hz로 다운샘플링(리샘플링)
##############################
print(fs_target, fs_original)
ratio = fs_target / fs_original
N_original = len(data_float)
N_target = int(N_original * ratio)
resampled_data = resample(data_float, N_target)

# aliased_do.wav 저장
resampled_int16 = np.int16(resampled_data * 32767)
write("aliased_do.wav", fs_target, resampled_int16)

##############################
# 3. 비교 대상: 진짜 4000 Hz에서의 도(261.63Hz) 사인파
##############################
ideal_do = sine_wave(f_do, fs_target, duration, amp=0.5)

##############################
# 4. FFT 분석
##############################
freqs_aliased, mag_aliased = get_fft(resampled_data, fs_target)
freqs_ideal, mag_ideal = get_fft(ideal_do, fs_target)

##############################
# 5. 스펙트럼 비교 시각화
##############################
plt.figure(figsize=(10,4))
plt.title("Frequency Spectrum Comparison at 4000 Hz")
plt.plot(freqs_ideal, mag_ideal, label='Ideal 261.63 Hz DO')
plt.plot(freqs_aliased, mag_aliased, label='Aliased DO (from highfreq)', alpha=0.7)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.xlim(0, 1000)  # 저역 범위만 확인 (도: 약 261Hz 부근)
plt.legend()
plt.show()

##############################
# 설명
##############################
# original_highfreq_do.wav: 원래 44100 Hz에서 약 2885.9 Hz 사인파 신호.
# aliased_do.wav: 위 신호를 4000 Hz로 리샘플링한 결과. 약 261.63 Hz 대역으로 폴딩되어 도 음높이처럼 들림.
# ideal_do: 4000 Hz에서 직접 생성한 순수 261.63 Hz 사인파.
#
# 그래프 비교:
# ideal_do 스펙트럼은 명확하게 261.63 Hz 근처에 뾰족한 피크가 나타난다.
# aliased_do 스펙트럼도 유사한 위치에 피크가 나타나지만, 위상 반전이나 약간의 스펙트럼 왜곡이 있을 수 있다.
# 이를 통해 앨리어싱으로 인한 주파수 폴딩이 실제로 도 음높이 피크를 형성함을 확인할 수 있다.
