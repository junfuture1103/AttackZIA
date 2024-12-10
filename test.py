import os
from pydub import AudioSegment

# 현재 작업 디렉토리와 파일 리스트 확인
print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

input_mp3 = "input.mp3"

# 파일 존재 여부 확인
if not os.path.isfile(input_mp3):
    raise FileNotFoundError(f"{input_mp3} 파일이 현재 디렉토리에 존재하지 않습니다.")

# MP3 파일 로드
sound = AudioSegment.from_mp3(input_mp3)
print("input.mp3 파일을 성공적으로 열었습니다.")
