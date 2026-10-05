# ARC.AI Tracker Composer

A small, deterministic Python tool for composing melody, bass, chords, and drum
patterns from explicit musical parameters. It has no network or LLM dependency.
Notes are generated on a 4/4 sixteenth-note grid; the same settings and seed
always produce the same patterns.

## Install

Requires Python 3.10 or newer. From a checkout:

```sh
python -m pip install .
```

If PowerShell cannot find the installed `arc-ai-tracker` script because the
Python `Scripts` directory is not on `PATH`, run the same CLI through Python:
`python -m arc_ai_tracker.cli generate --help`.

## Use

Print structured note data:

```sh
arc-ai-tracker generate --style synthwave --key D --mood bright --bars 8 --seed 7
```

Export a standard MIDI file or a playable XM module:

```sh
arc-ai-tracker generate --style synthwave --key D --bars 8 --seed 7 --format midi --output song.mid
arc-ai-tracker generate --style synthwave --key D --bars 8 --seed 7 --format xm --output song.xm
arc-ai-tracker generate --style industrial --swing 0.18 --humanize 0.5 --bars 8 --seed 7 --format wav --output preview.wav
```

To create an XM tune that already has synthesized instruments and can be
played as soon as you open it in MilkyTracker, run this from the project folder:

```powershell
python compose.py
```

This creates `KUNNES_AURINKO_RÄJÄHTÄÄ.xm` in the current folder. Open that file
in MilkyTracker; the tune has melody, bass, chord arpeggios, and a kick/snare/
hi-hat beat across four tracker channels. It includes six synthesized
instruments: saw lead, triangle bass, square-wave chords, and three procedural
drum sounds. Oscillator instruments have volume envelopes and the lead has
tracker vibrato. You can change the settings or destination, for example:

```powershell
python compose.py --style chiptune --key C --mood energetic --bars 8 --seed 42 --output oma-biisi.xm
```

Styles are `synthwave`, `chiptune`, `metal`, `ambient`, `industrial`, `punk77`,
`goa`, `trance90s`, `house90s`, and `jazz_lounge`. Each
sets a default tempo, scale/progression, density, groove, and drum pattern;
`--tempo` overrides its tempo. The five new styles have dedicated named XM
instruments and unique bass, chord, and drum patterns. Moods are `bright`,
`dark`, `calm`, and `energetic`. Supported keys include common sharp/flat
spellings. Tempo is limited to 30–300 BPM, length to 1–64 bars, swing to 0–0.5,
and humanization to 0–1. Both swing and humanization are deterministic for a
given seed and apply as MIDI timing offsets and XM note-delay effects, as well
as velocity variation.

The JSON output contains four tracks as MIDI pitches, with note start and
duration in sixteenth-note steps. MIDI export is a real Standard MIDI File
format 1 with tempo metadata, separate instrument tracks, and drums on the
standard percussion channel.

Both XM entry points produce valid XM 1.04 modules with patterns and
algorithmically synthesized instruments/samples, ready to play without sample
assignment. The new presets use standard XM packed patterns, note-delay effects
and XM 1.04 instrument/sample headers supported by MilkyTracker. WAV export
renders a mono 22.05 kHz, 16-bit PCM preview using the same generated notes,
simple oscillator/envelope synthesis, and per-voice filtering. No external or
copyrighted samples are bundled.

## Test

```sh
python -m unittest discover -s tests -v
```
