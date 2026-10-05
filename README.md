# TrackerForge Composer

Generate retro tracker music from prompts and presets.

Built for MilkyTracker, chiptune creators and demo scene enthusiasts.

## Overview

TrackerForge Composer is a prompt-driven retro music generator designed for creating melodic and bass-driven XM tracks for MilkyTracker. It combines preset-driven composition with a simple interface for generating chiptune-style ideas quickly.

## Features

- Prompt-based retro track generation
- Preset-inspired styles such as metal, punk, synthwave, ambient and chiptune
- Tempo, mood, key and bar-length controls
- XM export output for MilkyTracker
- Quick open-in-MilkyTracker workflow

## Installation

### From source

```bash
git clone https://github.com/AleksisLeipakivi/arc-ai-tracker-composer.git
cd arc-ai-tracker-composer
pip install -r requirements.txt
```

### Run the app

```bash
python arc_ai_tracker_gui_v03.py
```

## Quick Start

1. Launch the app.
2. Choose a preset or tune the style, mood, key and tempo.
3. Press Generate XM.
4. Open the produced file in MilkyTracker.

## Presets

Included presets cover a range of retro and demo-scene moods, including:

- Amiga 500 Demo
- Rambo 1985
- Miami Vice Sunset
- KiljuPaska-82
- Finnish Metal
- Cyberpunk Night Drive
- Goa Beach 1996
- Avaruusromua

## MilkyTracker workflow

The app is intended to generate `.xm` output and open it directly with MilkyTracker when available.

```text
Generate XM -> Open in MilkyTracker -> tweak instruments -> arrange and export
```

## Project goals

This project aims to make retro tracker composition feel approachable:

- fast experimentation with prompts and presets
- easy generation of short musical ideas
- output ready for MilkyTracker workflows

## Roadmap

- Better instrument generation and arrangement control
- More preset packs
- Export improvements and validation
- UI refinements and polish

## License

This project is currently unlicensed unless otherwise specified.

## Contributing

Pull requests and issue reports are welcome.
