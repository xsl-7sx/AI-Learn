import math
import os
import struct
import wave

path = os.path.join(os.path.dirname(__file__), "..", "uniapp", "src", "static", "audio", "correct.wav")
os.makedirs(os.path.dirname(path), exist_ok=True)
rate = 44100
duration = 0.15
frequency = 880
frames = [
    int(12000 * math.sin(2 * math.pi * frequency * t / rate))
    for t in range(int(rate * duration))
]
data = b"".join(struct.pack("<h", sample) for sample in frames)
with wave.open(path, "w") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(rate)
    wav_file.writeframes(data)

print(path)
