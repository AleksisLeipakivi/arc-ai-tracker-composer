"""Dependency-free offline WAV rendering for generated compositions."""

import math
import random
import struct
import wave
from array import array
from pathlib import Path

from .models import Composition, Note, Track

_SAMPLE_RATE = 22050
_STYLE_WAVES = {
    "synthwave": ("saw", "triangle", "square"),
    "chiptune": ("square", "square", "square"),
    "metal": ("saw", "saw", "square"),
    "ambient": ("triangle", "triangle", "sine"),
    "industrial": ("saw", "square", "square"),
    "punk77": ("saw", "saw", "square"),
    "goa": ("saw", "square", "triangle"),
    "trance90s": ("saw", "sine", "triangle"),
    "house90s": ("square", "triangle", "square"),
    "jazz_lounge": ("sine", "triangle", "sine"),
}


def _envelope(position: int, duration: int, attack: int, release: int, sustain: float) -> float:
    if position < attack:
        return position / max(1, attack)
    if position >= duration - release:
        return max(0.0, (duration - position) / max(1, release) * sustain)
    return sustain


def _render_note(
    mix: array,
    note: Note,
    track: Track,
    composition: Composition,
    start_frame: int,
    rng: random.Random,
) -> None:
    step_seconds = 60.0 / composition.tempo / 4
    note_seconds = max(0.03, note.duration_steps * step_seconds)
    release_seconds = {"ambient": 0.45, "synthwave": 0.18}.get(composition.style, 0.12)
    duration = int((note_seconds + release_seconds) * _SAMPLE_RATE)
    attack = max(1, int(_SAMPLE_RATE * (0.025 if track.channel == 0 else 0.008)))
    release = max(1, int(_SAMPLE_RATE * release_seconds))
    sustain = 0.68 if track.channel == 0 else 0.78
    frequency = 440.0 * 2 ** ((note.pitch - 69) / 12)
    amplitude = min(1.0, note.velocity / 127) * 0.24
    waveform = _STYLE_WAVES[composition.style][track.channel] if track.channel < 3 else "noise"
    phase = 0.0
    previous = 0.0
    cutoff_alpha = {
        0: 0.2 if waveform == "saw" else 0.8,
        1: 0.12,
        2: 0.18 if waveform == "square" else 0.38,
        9: 1.0,
    }.get(track.channel, 0.3)

    for position in range(duration):
        progress = position / max(1, duration)
        if track.channel == 9:
            if note.pitch == 36:
                instantaneous = frequency * (1.8 - min(1.0, progress))
                phase += 2 * math.pi * instantaneous / _SAMPLE_RATE
                raw = math.sin(phase) * math.exp(-progress * 8)
            else:
                noise = rng.uniform(-1.0, 1.0)
                if note.pitch == 38:
                    raw = noise * math.exp(-progress * 12) + 0.15 * math.sin(phase)
                else:
                    raw = noise * math.exp(-progress * 22)
        else:
            vibrato_depth = 0.0035 if track.channel == 0 and composition.style != "ambient" else 0.0
            vibrato = 1.0 + vibrato_depth * math.sin(2 * math.pi * 5.2 * position / _SAMPLE_RATE)
            phase += 2 * math.pi * frequency * vibrato / _SAMPLE_RATE
            cycle = (phase / (2 * math.pi)) % 1.0
            if waveform == "saw":
                raw = 2 * cycle - 1
            elif waveform == "triangle":
                raw = 2 / math.pi * math.asin(math.sin(phase))
            elif waveform == "square":
                raw = 1.0 if cycle < 0.5 else -1.0
            else:
                raw = math.sin(phase)
        filtered = previous + cutoff_alpha * (raw - previous)
        previous = filtered
        envelope = _envelope(position, duration, attack, release, sustain)
        index = start_frame + position
        if index >= len(mix):
            break
        mix[index] += filtered * envelope * amplitude


def render_wav(composition: Composition, output_path: str | Path) -> Path:
    """Render a mono 16-bit PCM WAV without third-party audio dependencies."""
    seconds_per_step = 60.0 / composition.tempo / 4
    song_duration = composition.total_steps * seconds_per_step
    tail_seconds = 0.5
    frames = int((song_duration + tail_seconds) * _SAMPLE_RATE)
    mix = array("f", [0.0]) * frames
    rng = random.Random(composition.seed)

    for track in composition.tracks:
        for note in track.notes:
            note_start = note.start_step * seconds_per_step + note.offset_ticks * seconds_per_step / 6
            start_frame = int(note_start * _SAMPLE_RATE)
            _render_note(mix, note, track, composition, start_frame, rng)

    pcm = bytearray()
    for value in mix:
        clipped = max(-1.0, min(1.0, value * 0.82))
        pcm.extend(struct.pack("<h", round(clipped * 32767)))

    output = Path(output_path)
    with wave.open(str(output), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(_SAMPLE_RATE)
        wav_file.writeframes(pcm)
    return output
