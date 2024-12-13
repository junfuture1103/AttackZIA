import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read

# aliased_doremi.wav 재생
fs, data = read("aliased_doremi.wav")
data_float = data.astype(np.float32) / 32767.0
sd.play(data_float, fs)
sd.wait()  # 재생 끝날 때까지 대기
