"""Standard MIDI File (SMF) format 1 serialization."""

from .models import Composition, Note

_TICKS_PER_QUARTER = 480


def _variable_length(value: int) -> bytes:
    if value < 0:
        raise ValueError("MIDI delta time cannot be negative")
    buffer = value & 0x7F
    encoded = bytearray()
    while value >> 7:
        value >>= 7
        buffer <<= 8
        buffer |= ((value & 0x7F) | 0x80)
    while True:
        encoded.append(buffer & 0xFF)
        if buffer & 0x80:
            buffer >>= 8
        else:
            return bytes(encoded)


def _text_meta(kind: int, text: str) -> bytes:
    content = text.encode("ascii", errors="replace")
    return bytes((0xFF, kind)) + _variable_length(len(content)) + content


def _track_chunk(events: list[tuple[int, int, bytes]]) -> bytes:
    events.sort(key=lambda event: (event[0], event[1]))
    data = bytearray()
    previous_tick = 0
    for tick, _, payload in events:
        data.extend(_variable_length(tick - previous_tick))
        data.extend(payload)
        previous_tick = tick
    data.extend(b"\x00\xff\x2f\x00")
    return b"MTrk" + len(data).to_bytes(4, "big") + data


def _note_events(notes: tuple[Note, ...], channel: int) -> list[tuple[int, int, bytes]]:
    events = []
    for note in notes:
        start = note.start_step * (_TICKS_PER_QUARTER // 4) + note.offset_ticks * 20
        end = start + note.duration_steps * (_TICKS_PER_QUARTER // 4)
        events.append((start, 1, bytes((0x90 | channel, note.pitch, note.velocity))))
        events.append((end, 0, bytes((0x80 | channel, note.pitch, 0))))
    return events


def to_midi(composition: Composition) -> bytes:
    """Serialize melody and bass as separate tracks in a format-1 MIDI file."""
    header = b"MThd" + (6).to_bytes(4, "big") + bytes((0, 1, 0, len(composition.tracks) + 1))
    header += _TICKS_PER_QUARTER.to_bytes(2, "big")
    micros_per_quarter = round(60_000_000 / composition.tempo)
    tempo_event = bytes((0xFF, 0x51, 0x03)) + micros_per_quarter.to_bytes(3, "big")
    tempo_track = _track_chunk([(0, 0, tempo_event), (0, 1, _text_meta(0x03, "ARC.AI Tempo"))])
    track_chunks = [tempo_track]

    for track in composition.tracks:
        events = [(0, 0, _text_meta(0x03, track.name))]
        events.extend(_note_events(track.notes, track.channel))
        track_chunks.append(_track_chunk(events))
    return header + b"".join(track_chunks)
