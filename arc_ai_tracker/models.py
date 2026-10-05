"""Core immutable data structures used by generators and exporters."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    """A MIDI pitch and duration, positioned in sixteenth-note steps."""

    start_step: int
    duration_steps: int
    pitch: int
    velocity: int
    offset_ticks: int = 0


@dataclass(frozen=True)
class Track:
    """A tracker channel containing timed notes."""

    name: str
    channel: int
    notes: tuple[Note, ...]


@dataclass(frozen=True)
class Composition:
    """A generated song arrangement and its explicit generation settings."""

    tempo: int
    key: str
    mood: str
    bars: int
    seed: int
    tracks: tuple[Track, ...]
    style: str = "synthwave"
    swing: float = 0.0
    humanize: float = 0.0

    @property
    def total_steps(self) -> int:
        """Return the song length in sixteenth-note steps (4/4 time)."""
        return self.bars * 16
