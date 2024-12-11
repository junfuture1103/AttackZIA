import numpy as np
import soundfile as sf
from scipy.signal import resample

def double_audio_frequency(input_file, output_file):
    # 오디오 파일 읽기
    audio_data, sample_rate = sf.read(input_file)

    scale = 2
    # 주파수 2배로 높이기 (시간을 50%로 줄임)
    new_length = len(audio_data) // scale
    if len(audio_data.shape) > 1:  # 스테레오 처리
        new_audio_data = np.array([resample(channel, new_length) for channel in audio_data.T]).T
    else:  # 모노 처리
        new_audio_data = resample(audio_data, new_length)
    
    # 새로운 샘플레이트를 기존의 2배로 설정
    new_sample_rate = 4000*scale#sample_rate * 2

    # 결과 파일 저장
    sf.write(output_file, new_audio_data, new_sample_rate)
    print(f"Frequency-doubled audio saved to: {output_file}")

# 사용 예시
input_path = "input_music.wav"  # 입력 오디오 파일
output_path = "output_audio.wav"  # 출력 오디오 파일
double_audio_frequency(input_path, output_path)
