import numpy as np
from scipy.io.wavfile import write
import pydub

# 출력용 파라미터
Fs_out = 40000    # 출력 샘플링 레이트
frequencies = [4000-300, 4000-350, 4000-400]  # 출력할 사인파 주파수들

#frequencies = [1500, 1000, 500]  # 출력할 사인파 주파수들
duration = 1.0    # 각 주파수당 재생 시간(초)

# 여러 톤을 이어붙인 신호 생성
combined_signal = np.array([], dtype=np.float32)

for f_tone in frequencies:
    t_out = np.linspace(0, duration, int(Fs_out * duration), endpoint=False)
    x_out = np.sin(2 * np.pi * f_tone * t_out).astype(np.float32)
    combined_signal = np.concatenate((combined_signal, x_out))

# WAV 파일 저장
write("result_test.wav", Fs_out, (combined_signal * 32767).astype(np.int16))

# MP3 파일로 변환
audio = pydub.AudioSegment.from_wav("result.wav")
#audio.export("result.wav", format="wav")

print("result.mp3 파일이 저장되었습니다.")
