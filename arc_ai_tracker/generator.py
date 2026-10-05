"""Seeded, rule-based melody, harmony, bass, and drum generation."""

import random

from .models import Composition, Note, Track
from .styles import STYLES, style_scale

KEYS = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}

MOODS = {
    "bright": {"mode": (0, 2, 4, 5, 7, 9, 11), "density": 0.72, "velocity": 94},
    "dark": {"mode": (0, 2, 3, 5, 7, 8, 10), "density": 0.58, "velocity": 78},
    "calm": {"mode": (0, 2, 4, 5, 7, 9, 11), "density": 0.42, "velocity": 68},
    "energetic": {"mode": (0, 2, 4, 5, 7, 9, 11), "density": 0.9, "velocity": 112},
}

_PROGRESSIONS = {
    "bright": (0, 4, 5, 3),
    "dark": (0, 5, 2, 6),
    "calm": (0, 3, 4, 0),
    "energetic": (0, 5, 3, 4),
}


def _note(
    rng: random.Random,
    *,
    start_step: int,
    duration_steps: int,
    pitch: int,
    velocity: int,
    swing: float,
    humanize: float,
) -> Note:
    swing_ticks = round(swing * 6) if start_step % 4 == 2 else 0
    timing_jitter = rng.randint(-2, 2) if humanize else 0
    offset_ticks = max(0, min(5, swing_ticks + round(timing_jitter * humanize)))
    velocity_jitter = round(rng.randint(-6, 6) * humanize)
    return Note(
        start_step=start_step,
        duration_steps=duration_steps,
        pitch=pitch,
        velocity=max(1, min(127, velocity + velocity_jitter)),
        offset_ticks=offset_ticks,
    )


def generate(
    *,
    tempo: int | None = None,
    key: str = "C",
    mood: str = "bright",
    bars: int = 4,
    seed: int = 0,
    style: str = "synthwave",
    swing: float | None = None,
    humanize: float = 0.0,
) -> Composition:
    """Generate deterministic melody, bass, chord arpeggios, and drums in 4/4.

    Pitches use MIDI numbering (middle C is 60); timing is measured in
    sixteenth-note steps. All choices derive from the supplied seed.
    """
    normalized_key = key.strip()
    if normalized_key not in KEYS:
        raise ValueError(f"unsupported key {key!r}; choose from {', '.join(KEYS)}")
    if mood not in MOODS:
        raise ValueError(f"unsupported mood {mood!r}; choose from {', '.join(MOODS)}")
    if style not in STYLES:
        raise ValueError(f"unsupported style {style!r}; choose from {', '.join(STYLES)}")
    if tempo is None:
        tempo = STYLES[style].default_tempo
    if not 30 <= tempo <= 300:
        raise ValueError("tempo must be between 30 and 300 BPM")
    if not 1 <= bars <= 64:
        raise ValueError("bars must be between 1 and 64")
    if not -(2**31) <= seed < 2**31:
        raise ValueError("seed must fit a signed 32-bit integer")
    if not 0.0 <= humanize <= 1.0:
        raise ValueError("humanize must be between 0 and 1")
    selected_style = STYLES[style]
    if swing is None:
        swing = selected_style.swing
    if not 0.0 <= swing <= 0.5:
        raise ValueError("swing must be between 0 and 0.5")

    rng = random.Random(seed)
    mood_settings = MOODS[mood]
    scale = style_scale(style, mood_settings["mode"])
    density = min(1.0, mood_settings["density"] * selected_style.density)
    tonic = KEYS[normalized_key]
    melody: list[Note] = []
    bass: list[Note] = []
    chords: list[Note] = []
    drums: list[Note] = []
    previous_degree = 4
    progression = (
        selected_style.progression
        if style != "synthwave"
        else _PROGRESSIONS[mood]
    )

    for bar in range(bars):
        bar_start = bar * 16
        degree = progression[bar % len(progression)]
        chord_root = scale[degree]
        chord_fifth = scale[(degree + 4) % len(scale)]

        for bass_index, beat_step in enumerate(selected_style.bass_pattern):
            next_step = (
                selected_style.bass_pattern[bass_index + 1]
                if bass_index + 1 < len(selected_style.bass_pattern)
                else 16
            )
            bass_degree = (degree + (0 if bass_index % 2 == 0 else 4)) % 7
            bass_pitch = 36 + tonic + scale[bass_degree]
            bass.append(
                _note(
                    rng,
                    start_step=bar_start + beat_step,
                    duration_steps=max(1, min(4, next_step - beat_step)),
                    pitch=bass_pitch,
                    velocity=max(45, mood_settings["velocity"] - 12),
                    swing=swing,
                    humanize=humanize,
                )
            )

        chord_tones = (
            (degree, (degree + 2) % 7, (degree + 4) % 7, (degree + 6) % 7)
            if style == "jazz_lounge"
            else (degree, (degree + 2) % 7, (degree + 4) % 7)
        )
        for chord_index, chord_step in enumerate(selected_style.chord_pattern):
            chord_degree = chord_tones[chord_index % len(chord_tones)]
            chords.append(
                _note(
                    rng,
                    start_step=bar_start + chord_step,
                    duration_steps=3,
                    pitch=48 + tonic + scale[chord_degree],
                    velocity=max(40, mood_settings["velocity"] - 24),
                    swing=swing,
                    humanize=humanize,
                )
            )

        for drum_step, drum_pitch, velocity in selected_style.drum_pattern:
            drums.append(
                _note(
                    rng,
                    start_step=bar_start + drum_step,
                    duration_steps=1,
                    pitch=drum_pitch,
                    velocity=velocity,
                    swing=swing,
                    humanize=humanize,
                )
            )

        step = 0
        while step < 16:
            if rng.random() > density:
                step += 4
                continue
            move = rng.choice((-2, -1, 0, 1, 2))
            previous_degree = max(0, min(6, previous_degree + move))
            octave = 1 if rng.random() < 0.78 else 2
            pitch = 60 + tonic + scale[previous_degree] + (octave - 1) * 12
            duration = rng.choice((2, 4, 4, 8))
            duration = min(duration, 16 - step)
            melody.append(
                _note(
                    rng,
                    start_step=bar_start + step,
                    duration_steps=duration,
                    pitch=pitch,
                    velocity=mood_settings["velocity"] + rng.randint(-8, 7),
                    swing=swing,
                    humanize=humanize,
                )
            )
            step += duration

    return Composition(
        tempo=tempo,
        key=normalized_key,
        mood=mood,
        bars=bars,
        seed=seed,
        style=style,
        swing=swing,
        humanize=humanize,
        tracks=(
            Track("Melody", 0, tuple(melody)),
            Track("Bass", 1, tuple(bass)),
            Track("Chords", 2, tuple(chords)),
            Track("Drums", 9, tuple(drums)),
        ),
    )
