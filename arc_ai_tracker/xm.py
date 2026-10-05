"""FastTracker II Extended Module (XM) serialization."""

import math
import random
import struct
from dataclasses import dataclass, replace

from .models import Composition, Note, Track

_PATTERN_ROWS = 64
_SAMPLE_RATE = 8363


@dataclass(frozen=True)
class _Instrument:
    name: bytes
    sample_name: bytes
    waveform: str
    looped: bool
    envelope: tuple[tuple[int, int], ...]
    sustain_point: int | None = None
    vibrato: tuple[int, int, int, int] = (0, 0, 0, 0)


_INSTRUMENTS = (
    _Instrument(
        b"ARC Saw Lead",
        b"Saw oscillator",
        "saw",
        True,
        ((0, 0), (3, 64), (12, 44), (36, 0)),
        sustain_point=2,
        vibrato=(0, 8, 4, 5),
    ),
    _Instrument(
        b"ARC Triangle Bass",
        b"Triangle wave",
        "triangle",
        True,
        ((0, 0), (2, 64), (8, 48), (28, 0)),
        sustain_point=2,
    ),
    _Instrument(
        b"ARC Square Chords",
        b"Square oscillator",
        "square",
        True,
        ((0, 0), (4, 64), (12, 36), (32, 0)),
        sustain_point=2,
        vibrato=(0, 5, 2, 4),
    ),
    _Instrument(
        b"ARC Kick",
        b"Synth kick",
        "kick",
        False,
        ((0, 64), (24, 0)),
    ),
    _Instrument(
        b"ARC Snare",
        b"Synth snare",
        "snare",
        False,
        ((0, 64), (20, 0)),
    ),
    _Instrument(
        b"ARC Hi-Hat",
        b"Synth hi-hat",
        "hat",
        False,
        ((0, 64), (12, 0)),
    ),
)

_XM_CHANNELS = {0: 0, 1: 1, 2: 2, 9: 3}
_DRUM_INSTRUMENTS = {36: 4, 38: 5, 42: 6, 46: 6}


def _instrument_for_track(track: Track, pitch: int) -> int:
    if track.channel == 0:
        return 1
    if track.channel == 1:
        return 2
    if track.channel == 2:
        return 3
    if track.channel == 9 and pitch in _DRUM_INSTRUMENTS:
        return _DRUM_INSTRUMENTS[pitch]
    raise ValueError(f"no XM instrument for track {track.name!r}, pitch {pitch}")


def _xm_event(event: tuple[int, int | None, int] | None) -> bytes:
    if event is None:
        return b"\x80"
    note, instrument, delay = event
    if instrument is None:
        return bytes((0x81, note))
    if delay:
        return bytes((0x9B, note, instrument, 0x0E, 0xD0 | delay))
    return bytes((0x83, note, instrument))


def _pattern_chunk(
    rows: int,
    events: dict[tuple[int, int], tuple[int, int | None, int]],
) -> bytes:
    packed = bytearray()
    for row in range(rows):
        for channel in range(4):
            packed.extend(_xm_event(events.get((row, channel))))
    return struct.pack("<IBHH", 9, 0, rows, len(packed)) + packed


def _pattern_events(
    track: Track, first_step: int, rows: int
) -> dict[tuple[int, int], tuple[int, int | None, int]]:
    channel = _XM_CHANNELS[track.channel]
    events: dict[tuple[int, int], tuple[int, int | None, int]] = {}
    for note in track.notes:
        start = note.start_step - first_step
        if not 0 <= start < rows:
            continue
        # XM pitches are 1..96; 97 is the note-off marker.
        xm_note = note.pitch - 11
        if not 1 <= xm_note <= 96:
            raise ValueError(f"pitch {note.pitch} cannot be represented in XM")
        delay = max(0, min(5, note.offset_ticks))
        events[(start, channel)] = (xm_note, _instrument_for_track(track, note.pitch), delay)
        end = start + note.duration_steps
        if end < rows:
            events[(end, channel)] = (97, None, 0)
        elif rows > 0:
            events[(rows - 1, channel)] = (97, None, 0)
    return events


_STYLE_WAVES = {
    "synthwave": ("saw", "triangle", "square"),
    "chiptune": ("square", "square", "square"),
    "metal": ("saw", "saw", "square"),
    "ambient": ("triangle", "triangle", "saw"),
    "industrial": ("saw", "square", "square"),
    "punk77": ("saw", "saw", "square"),
    "goa": ("saw", "square", "triangle"),
    "trance90s": ("saw", "sine", "triangle"),
    "house90s": ("square", "triangle", "square"),
    "jazz_lounge": ("sine", "triangle", "sine"),
}

_STYLE_INSTRUMENT_NAMES = {
    "punk77": (b"Punk77 Overdrive", b"Punk77 Pick Bass", b"Punk77 Power Chord"),
    "goa": (b"Goa Pulse Lead", b"Goa Rolling Bass", b"Goa Acid Chord"),
    "trance90s": (b"Trance90 Pluck", b"Trance90 Sub Bass", b"Trance90 Pad"),
    "house90s": (b"House90 Organ", b"House90 Funk Bass", b"House90 Stab"),
    "jazz_lounge": (b"Jazz Lounge Rhodes", b"Jazz Lounge Upright", b"Jazz Lounge Vibes"),
}


def _style_instrument(instrument: _Instrument, index: int, style: str) -> _Instrument:
    if style not in _STYLE_INSTRUMENT_NAMES:
        if index >= 3:
            return instrument
        waveform = _STYLE_WAVES[style][index]
        label = {"saw": "Saw", "square": "Pulse", "triangle": "Soft", "sine": "Pure"}[waveform]
        role = ("Lead", "Bass", "Chords")[index]
        return replace(
            instrument,
            name=f"ARC {label} {role}".encode("ascii"),
            sample_name=f"{label} oscillator".encode("ascii"),
            waveform=waveform,
        )

    prefix = style.replace("_", " ").title().encode("ascii")
    if index >= 3:
        drum_role = (b"Kick", b"Snare", b"Hi-Hat")[index - 3]
        short_prefix = {
            "punk77": b"Punk77",
            "goa": b"Goa",
            "trance90s": b"Trance90",
            "house90s": b"House90",
            "jazz_lounge": b"Jazz",
        }[style]
        category = instrument.waveform
        return replace(
            instrument,
            name=short_prefix + b" " + drum_role,
            sample_name=short_prefix + b" " + drum_role + b" sample",
            waveform=f"{category}:{style}",
        )

    waveform = _STYLE_WAVES[style][index]
    names = _STYLE_INSTRUMENT_NAMES[style]
    customized = replace(
        instrument,
        name=names[index],
        sample_name=names[index] + b" sample",
        waveform=waveform,
    )
    if style == "goa" and index == 0:
        return replace(customized, vibrato=(0, 12, 6, 7), envelope=((0, 0), (2, 64), (10, 42), (40, 0)))
    if style == "trance90s" and index == 0:
        return replace(customized, vibrato=(0, 5, 3, 3), envelope=((0, 0), (1, 64), (8, 34), (30, 0)))
    if style == "house90s" and index == 2:
        return replace(customized, envelope=((0, 0), (1, 64), (4, 48), (18, 0)))
    if style == "jazz_lounge":
        return replace(customized, vibrato=(0, 2, 1, 2), envelope=((0, 0), (8, 64), (24, 48), (48, 0)))
    return customized


def _pcm_wave(instrument: _Instrument) -> tuple[bytes, int]:
    """Synthesize an original looped oscillator or one-shot drum sample."""
    rng = random.Random(instrument.sample_name)
    if instrument.looped:
        length = 256
        samples = []
        for index in range(length):
            phase = index / length
            angle = 2 * math.pi * phase
            if instrument.waveform == "saw":
                value = 2 * phase - 1
            elif instrument.waveform == "square":
                value = 1 if phase < 0.5 else -1
            else:
                value = (
                    math.sin(angle)
                    if instrument.waveform == "sine"
                    else 2 / math.pi * math.asin(math.sin(angle))
                )
            samples.append(round(value * 112))
        loop_type = 1
    else:
        length = 2048
        samples = []
        previous_noise = 0
        for index in range(length):
            progress = index / length
            waveform = instrument.waveform.split(":", 1)[0]
            if waveform == "kick":
                frequency = 95 - 52 * progress
                phase = 2 * math.pi * frequency * index / _SAMPLE_RATE
                value = math.sin(phase) * math.exp(-progress * 8)
            else:
                noise = rng.randint(-112, 112)
                if waveform == "snare":
                    tone = math.sin(2 * math.pi * 185 * index / _SAMPLE_RATE)
                    value = (0.72 * noise + 0.28 * tone * 112) * math.exp(-progress * 7)
                else:
                    high_pass_noise = noise - previous_noise * 0.72
                    value = high_pass_noise * math.exp(-progress * 12)
                previous_noise = noise
            samples.append(max(-120, min(120, round(value))))
        loop_type = 0

    delta = bytearray()
    previous = 0
    for sample in samples:
        delta.append((sample - previous) & 0xFF)
        previous = sample
    return bytes(delta), loop_type


def _instrument_chunk(instrument: _Instrument) -> bytes:
    sample, loop_type = _pcm_wave(instrument)
    header = bytearray(struct.pack("<I22sBH", 263, instrument.name[:22].ljust(22, b"\0"), 0, 1))
    header.extend(struct.pack("<I", 40))
    header.extend(bytes(96))

    volume_points = bytearray()
    for tick, volume in instrument.envelope[:12]:
        volume_points.extend(struct.pack("<HH", tick, volume))
    volume_points.extend(bytes(48 - len(volume_points)))
    header.extend(volume_points)
    header.extend(bytes(48))

    sustain = instrument.sustain_point
    header.extend(
        bytes(
            (
                len(instrument.envelope),
                0,
                sustain if sustain is not None else 0,
                0,
                0,
                0,
                0,
                0,
            )
        )
    )
    volume_type = 1 | (2 if sustain is not None else 0)
    header.extend(bytes((volume_type, 0, *instrument.vibrato)))
    header.extend(struct.pack("<H", 768))
    header.extend(bytes(22))
    if len(header) != 263:
        raise AssertionError(f"XM instrument header must be 263 bytes, got {len(header)}")

    loop_start = 0
    loop_length = len(sample) if loop_type else 0
    sample_header = struct.pack(
        "<III BbBBbB22s",
        len(sample),
        loop_start,
        loop_length,
        64,
        0,
        loop_type,
        128,
        0,
        0,
        instrument.sample_name[:22].ljust(22, b"\0"),
    )
    return bytes(header) + sample_header + sample


def to_xm(composition: Composition) -> bytes:
    """Serialize a four-channel song with synthesized instruments and drums."""
    if len(composition.tracks) != 4:
        raise ValueError("XM export requires melody, bass, chords, and drums tracks")
    if {track.channel for track in composition.tracks} != set(_XM_CHANNELS):
        raise ValueError("XM export requires tracks on MIDI channels 0, 1, 2, and 9")

    pattern_count = (composition.total_steps + _PATTERN_ROWS - 1) // _PATTERN_ROWS
    if pattern_count > 256:
        raise ValueError("XM supports at most 256 patterns in this export")

    name = b"ARC.AI Tracker Composer"[:20].ljust(20, b" ")
    tracker = b"ARC.AI Composer"[:20].ljust(20, b" ")
    header = bytearray(b"Extended Module: " + name + b"\x1a" + tracker)
    header.extend(struct.pack("<H", 0x0104))
    header.extend(struct.pack("<I", 276))
    header.extend(
        struct.pack(
            "<HHHHHHHH",
            pattern_count,
            0,
            4,
            pattern_count,
            len(_INSTRUMENTS),
            0,
            6,
            composition.tempo,
        )
    )
    header.extend(bytes(range(pattern_count)) + bytes(256 - pattern_count))
    if len(header) != 336:
        raise AssertionError(f"XM song header must be 336 bytes, got {len(header)}")

    output = bytearray(header)
    for pattern_index in range(pattern_count):
        first_step = pattern_index * _PATTERN_ROWS
        rows = min(_PATTERN_ROWS, composition.total_steps - first_step)
        events: dict[tuple[int, int], tuple[int, int | None, int]] = {}
        for track in composition.tracks:
            events.update(_pattern_events(track, first_step, rows))
        output.extend(_pattern_chunk(rows, events))

    for index, instrument in enumerate(_INSTRUMENTS):
        output.extend(_instrument_chunk(_style_instrument(instrument, index, composition.style)))
    return bytes(output)
