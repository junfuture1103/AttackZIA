import numpy as np
import soundfile as sf
import librosa
import sounddevice as sd

def read_audio(filename):
    print(f"Reading audio from {filename}...")
    audio, samplerate = sf.read(filename)
    print("Reading complete.")
    return audio, samplerate


def resample_audio(audio, original_rate, target_rate):
    if original_rate == target_rate:
        print("Original and target sample rates are the same. No resampling needed.")
        return audio
    print(f"Resampling from {original_rate} Hz to {target_rate} Hz using Librosa...")
    resampled_audio = librosa.resample(audio.T, orig_sr=original_rate, target_sr=target_rate).T
    print("Resampling complete.")
    return resampled_audio


def save_audio(filename, audio, samplerate):
    sf.write(filename, audio, samplerate)
    print(f"Audio saved to {filename}")


def play_audio(audio, samplerate):
    print(f"Playing audio at {samplerate} Hz...")
    sd.play(audio, samplerate)
    sd.wait()

if __name__ == "__main__":
    input_filename = "1500hz_tone.wav"  # Specify the input audio file
    target_samplerate = 4410

    audio, original_samplerate = read_audio(input_filename)
    resampled_audio = resample_audio(audio, original_samplerate, target_samplerate)
    save_audio("resampled_audio.wav", resampled_audio, target_samplerate)

    # Play the resampled audio at 44100 Hz
    play_audio(resample_audio(resampled_audio, target_samplerate, 44100), 44100)
