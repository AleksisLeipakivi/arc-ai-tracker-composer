# TrackerForge Composer

> **Prompt-driven melody and bass composer for MilkyTracker XM**

Generate retro tracker music from presets and parameters. Built for MilkyTracker users, chiptune creators, and demo scene enthusiasts.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/AleksisLeipakivi/arc-ai-tracker-composer?include_prereleases)](https://github.com/AleksisLeipakivi/arc-ai-tracker-composer/releases)

---

## ✨ Features

- 🎵 **Prompt-based track generation** — generate XM tracks from style, mood, key, and tempo
- 🎼 **Preset library** — curated presets inspired by classic demo scene aesthetics
- ⚡ **Fast composition** — quick experimentation with melody and bass patterns
- 🎹 **MilkyTracker integration** — automatic detection + seamless open workflow
- 🎲 **Random generation** — hit "Random Fantasy" for unexpected inspiration
- 🔧 **Full control** — customize style, mood, tempo, key, bar length, and seed value

---

## 🚀 Quick Start

### Option 1: Download Executable (Windows)

1. Download the latest release from [Releases](https://github.com/AleksisLeipakivi/arc-ai-tracker-composer/releases)
2. Extract and run `TrackerForge.exe`
3. Ensure [MilkyTracker](https://milkytracker.org/) is installed

### Option 2: Install from Source

#### Requirements
- Python 3.8 or later
- [MilkyTracker](https://milkytracker.org/) (for playback/editing)

#### Installation

```bash
# Clone repository
git clone https://github.com/AleksisLeipakivi/arc-ai-tracker-composer.git
cd arc-ai-tracker-composer

# Install dependencies
pip install -r requirements.txt

# Run the application
python arc_ai_tracker_gui_v03.py
```

---

## 📖 Usage

### GUI Application

1. **Choose a preset** or customize manually:
   - **Preset**: Select from KiljuPaska-82, Finnish Metal, Cyberpunk, etc.
   - **Style**: metal, punk77, synthwave, ambient, chiptune, goa, etc.
   - **Mood**: energetic, dark, bright, calm
   - **Key**: A through G (with sharps/flats)
   - **Tempo**: 30–300 BPM
   - **Bars**: 16 (idea), 32 (song), 64 (extended)
   - **Seed**: integer for reproducible randomness

2. **Generate** by clicking "Generate XM"
   - The app creates an `.xm` file
   - **Automatically opens in MilkyTracker** if available
   - If MilkyTracker is not found, you'll see a clear error message

3. **Tweak and arrange** in MilkyTracker
   - Adjust instruments, effects, patterns
   - Arrange sections and save your track

### Presets Included

| Preset | Style | Mood | Tempo | Bars |
|--------|-------|------|-------|------|
| Amiga 500 Demo | chiptune | bright | 125 | 64 |
| Rambo 1985 | metal | dark | 170 | 64 |
| Miami Vice Sunset | synthwave | bright | 118 | 64 |
| KiljuPaska-82 | punk77 | energetic | 195 | 32 |
| Vitun Pikku Prinssit | punk77 | bright | 185 | 32 |
| Avaruusromua | ambient | calm | 90 | 64 |
| Beastie Funk Punk | punk77 | bright | 186 | 32 |
| Cyberpunk Night Drive | synthwave | dark | 130 | 64 |
| Goa Beach 1996 | goa | bright | 145 | 64 |
| Finnish Metal | metal | dark | 180 | 64 |

---

## 🔧 Workflow

```
[Generate XM] → [Auto-opens in MilkyTracker] → [Tweak Instruments] → [Arrange] → [Export]
```

1. **Generate** — create initial composition from presets
2. **Load** — automatic MilkyTracker open (if available)
3. **Edit** — adjust instruments, samples, effects in MilkyTracker
4. **Arrange** — rearrange patterns, add/remove bars
5. **Finish** — export or save as `.xm`

---

## 📁 Project Structure

```
arc-ai-tracker-composer/
├── arc_ai_tracker_gui_v03.py   # Main GUI application
├── setup.py                     # Package setup
├── pyproject.toml               # Modern Python packaging
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
└── .github/
    └── workflows/
        └── release.yml          # CI/CD for releases
```

---

## v0.4 Changes

**What's new:**
- ✅ Automatic MilkyTracker detection (multiple install paths supported)
- ✅ Robust error handling if MilkyTracker is not found
- ✅ No more self-launching when opening `.xm` files
- ✅ Better log messages and user feedback

**Supported MilkyTracker paths:**
- `C:\Program Files\MilkyTracker\MilkyTracker.exe`
- `C:\Program Files (x86)\MilkyTracker\MilkyTracker.exe`
- `%USERPROFILE%\Downloads\MilkyTracker.exe`
- `%USERPROFILE%\Desktop\MilkyTracker.exe`
- WinGet/Microsoft Store installations

---

## 🔄 Releases & Distribution

### Creating a Release

1. Tag a commit with semantic versioning:
   ```bash
   git tag -a v0.4.0 -m "Release v0.4.0"
   git push origin v0.4.0
   ```

2. GitHub Actions automatically:
   - Builds Python wheels and distributions
   - Generates OS-specific executables
   - Creates a GitHub Release with all artifacts

### Download Links

- **Latest Release**: [GitHub Releases](https://github.com/AleksisLeipakivi/arc-ai-tracker-composer/releases)
- **Source**: [Main Branch](https://github.com/AleksisLeipakivi/arc-ai-tracker-composer)

---

## 🛠️ Development

### Setup Dev Environment

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Style

```bash
black arc_ai_tracker_gui_v03.py
flake8 arc_ai_tracker_gui_v03.py
```

### Build Standalone Executable

```bash
pyinstaller --clean --onefile --windowed --name TrackerForge arc_ai_tracker_gui_v03.py
```

Then run:
```bash
.\dist\TrackerForge.exe
```

---

## 🗺️ Roadmap

- [ ] Settings window for custom MilkyTracker path
- [ ] Drum pattern generation
- [ ] More preset packs
- [ ] MIDI export
- [ ] Web UI (future)
- [ ] Better instrument control
- [ ] Undo/redo history

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📞 Support & Issues

- **Report Bugs**: [GitHub Issues](https://github.com/AleksisLeipakivi/arc-ai-tracker-composer/issues)
- **Email**: tukorama@gmail.com

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🎶 Acknowledgments

- Built with [PySide6](https://wiki.qt.io/Qt_for_Python) for the GUI
- Designed for [MilkyTracker](https://milkytracker.org/) XM format
- Inspired by the demo scene and retro chiptune community

---

**Happy composing! 🎵**
