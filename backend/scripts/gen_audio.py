import math
import os
import struct
import wave

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
CORRECT_OUTPUT = os.path.join(ROOT, "uniapp", "src", "static", "audio", "correct.wav")
WRONG_OUTPUT = os.path.join(ROOT, "uniapp", "src", "static", "audio", "wrong.wav")

RATE = 44100


def soft_envelope(t: float, duration: float) -> float:
  attack = 0.04
  release = max(0.18, duration * 0.55)
  if t < attack:
    return (t / attack) ** 1.6
  if t > duration - release:
    fade = (duration - t) / release
    return fade * fade
  return 1.0


def soft_tone(freq: float, start: float, duration: float, volume: float) -> list[tuple[int, int]]:
  frames: list[tuple[int, int]] = []
  start_idx = int(start * RATE)
  total = int(duration * RATE)
  for i in range(total):
    t = i / RATE
    fundamental = math.sin(2 * math.pi * freq * t)
    harmonic = 0.08 * math.sin(2 * math.pi * freq * 2 * t)
    sample = (fundamental + harmonic) * soft_envelope(t, duration) * volume
    frames.append((start_idx + i, int(12000 * sample)))
  return frames


def mix_tones(segments: list[list[tuple[int, int]]], length: int) -> list[int]:
  buffer = [0] * length
  for segment in segments:
    for index, value in segment:
      if 0 <= index < length:
        buffer[index] += value
  peak = max((abs(v) for v in buffer), default=1)
  if peak > 22000:
    scale = 22000 / peak
    buffer = [int(v * scale) for v in buffer]
  return buffer


def build_correct_pcm() -> bytes:
  duration = 0.55
  length = int(RATE * duration)
  segments = [
    soft_tone(523.25, 0.0, 0.28, 0.32),
    soft_tone(659.25, 0.1, 0.35, 0.26),
  ]
  frames = mix_tones(segments, length)
  return b"".join(struct.pack("<h", max(-32767, min(32767, sample))) for sample in frames)


def build_wrong_pcm() -> bytes:
  duration = 0.42
  length = int(RATE * duration)
  segments = [
    soft_tone(392.0, 0.0, 0.2, 0.22),
    soft_tone(311.13, 0.09, 0.3, 0.18),
  ]
  frames = mix_tones(segments, length)
  return b"".join(struct.pack("<h", max(-32767, min(32767, sample))) for sample in frames)


def write_wav(path: str, pcm: bytes) -> None:
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with wave.open(path, "w") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(RATE)
    wav_file.writeframes(pcm)


def main() -> None:
  write_wav(CORRECT_OUTPUT, build_correct_pcm())
  write_wav(WRONG_OUTPUT, build_wrong_pcm())
  print(CORRECT_OUTPUT)
  print(WRONG_OUTPUT)


if __name__ == "__main__":
  main()
