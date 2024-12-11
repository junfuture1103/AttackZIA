import numpy as np
from gtts import gTTS
import soundfile as sf
from scipy.signal import resample
import librosa

# 1. 텍스트-투-스피치(TTS)로 "hello" 음성 생성
tts = gTTS(text="hello", lang='en', slow=False)
tts.save("input_music.wav")
print("원본 'hello' 음성 파일 생성 완료: input_music.wav")
