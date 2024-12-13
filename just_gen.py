import numpy as np
import wave

# Parameters
sample_rate = 44100
frequencies = [4000-260, 4000-300, 4000-330]
duration = 1  # 1 second per tone

# Generate tone
def generate_tone(frequency, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = 0.5 * np.sin(2 * np.pi * frequency * t)
    return signal

# Save to .wav file
def save_wav(filename, signal, sample_rate):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(sample_rate)
        # Convert to 16-bit PCM
        signal_int = np.int16(signal * 32767)
        wf.writeframes(signal_int.tobytes())

# Main process
total_signal = np.concatenate([generate_tone(freq, sample_rate, duration) for freq in frequencies])
save_wav('tones_sequence.wav', total_signal, sample_rate)

print("WAV file 'tones_sequence.wav' generated successfully.")