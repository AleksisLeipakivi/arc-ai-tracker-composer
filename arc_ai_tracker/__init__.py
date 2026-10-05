"""Deterministic music pattern generation and tracker-oriented exports."""

from .generator import generate
from .models import Composition, Note, Track

__all__ = ["Composition", "Note", "Track", "generate"]
