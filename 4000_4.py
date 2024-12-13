import sounddevice as sd
from scipy.io.wavfile import read

# 파일 읽기
fs, resampled_signal = read("resampled_doremi.wav")
print(fs, resampled_signal)

print("리샘플링된 소리 4000 재생 중...")
sd.play(resampled_signal, samplerate=4000)
sd.wait()