"""Command-line interface for generating and exporting patterns."""

import argparse
import json
from pathlib import Path
from typing import Sequence

from .generator import KEYS, MOODS, generate
from .midi import to_midi
from .models import Composition
from .styles import STYLES
from .wav import render_wav
from .xm import to_xm


def _as_json(composition: Composition) -> str:
    return json.dumps(
        {
            "tempo": composition.tempo,
            "key": composition.key,
            "mood": composition.mood,
            "bars": composition.bars,
            "seed": composition.seed,
            "style": composition.style,
            "swing": composition.swing,
            "humanize": composition.humanize,
            "steps_per_bar": 16,
            "tracks": [
                {
                    "name": track.name,
                    "channel": track.channel,
                    "notes": [
                        {
                            "start_step": note.start_step,
                            "duration_steps": note.duration_steps,
                            "pitch": note.pitch,
                            "velocity": note.velocity,
                            "offset_ticks": note.offset_ticks,
                        }
                        for note in track.notes
                    ],
                }
                for track in composition.tracks
            ],
        },
        indent=2,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arc-ai-tracker",
        description="Generate deterministic four-part music for MIDI, XM, or WAV.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate_parser = subparsers.add_parser("generate", help="generate a composition")
    generate_parser.add_argument("--tempo", type=int, help="tempo in BPM (30-300; style default if omitted)")
    generate_parser.add_argument("--key", default="C", choices=sorted(KEYS), help="tonic note")
    generate_parser.add_argument("--mood", default="bright", choices=sorted(MOODS))
    generate_parser.add_argument("--style", default="synthwave", choices=sorted(STYLES))
    generate_parser.add_argument("--bars", type=int, default=4, help="length in 4/4 bars (1-64)")
    generate_parser.add_argument("--seed", type=int, default=0, help="signed 32-bit random seed")
    generate_parser.add_argument("--swing", type=float, help="swing amount from 0 to 0.5")
    generate_parser.add_argument("--humanize", type=float, default=0.0, help="timing/velocity variation from 0 to 1")
    generate_parser.add_argument("--format", choices=("json", "midi", "xm", "wav"), default="json")
    generate_parser.add_argument("--output", type=Path, help="output file; binary formats require this")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        composition = generate(
            tempo=args.tempo,
            key=args.key,
            mood=args.mood,
            bars=args.bars,
            seed=args.seed,
            style=args.style,
            swing=args.swing,
            humanize=args.humanize,
        )
        if args.format == "json":
            content = _as_json(composition)
            if args.output is None:
                print(content)
            else:
                args.output.write_text(content + "\n", encoding="utf-8")
        else:
            if args.output is None:
                parser.error("--output is required for MIDI, XM, and WAV exports")
            if args.format == "wav":
                render_wav(composition, args.output)
            else:
                content = to_midi(composition) if args.format == "midi" else to_xm(composition)
                args.output.write_bytes(content)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
