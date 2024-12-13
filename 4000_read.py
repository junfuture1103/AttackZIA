import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import threading

# Constants
RATE = 4000  # Sampling rate in Hz
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1

# Audio stream initialization
def audio_stream():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    return stream, p

def update_plot(stream):
    plt.ion()
    fig, ax = plt.subplots()
    x = np.linspace(0, RATE / 2, CHUNK // 2)
    line, = ax.plot(x, np.random.rand(CHUNK // 2))
    ax.set_title("Real-time Frequency Spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    ax.set_ylim(0, 100)

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            fft_data = np.abs(np.fft.rfft(audio_data) / CHUNK)
            line.set_ydata(fft_data)
            fig.canvas.draw()
            fig.canvas.flush_events()
    except KeyboardInterrupt:
        print("Visualization stopped.")

if __name__ == "__main__":
    stream, p = audio_stream()
    visualizer_thread = threading.Thread(target=update_plot, args=(stream,))
    visualizer_thread.start()
    visualizer_thread.join()
    stream.stop_stream()
    stream.close()
    p.terminate()
