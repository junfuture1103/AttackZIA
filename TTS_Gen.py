from gtts import gTTS
from pydub import AudioSegment
import os

# 사용할 폴더 경로(Windows 절대경로 예시, 실제 경로로 변경 필요)
temp_mp3 = os.path.join(base_dir, "temp_hello.mp3")
sample_wav = os.path.join(base_dir, "sample.wav")

text = "Hello"
tts = gTTS(text=text, lang='en')

# 임시 mp3 생성
tts.save(temp_mp3)

# MP3 -> WAV 변환 (리샘플링 없이 그대로)
sound = AudioSegment.from_mp3(temp_mp3)
sound.export(sample_wav, format="wav")

# 임시 mp3 삭제
os.remove(temp_mp3)

print(f"{sample_wav} 파일이 생성되었습니다. (기존 TTS MP3 샘플링 레이트 유지)")
