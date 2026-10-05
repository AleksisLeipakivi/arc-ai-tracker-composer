import os
import sys
import random
import subprocess
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTextEdit,
    QSlider,
    QMessageBox,
    QSpinBox,
)

PRESETS = {

    "Custom": None,

    "Amiga 500 Demo": {
        "style": "chiptune",
        "mood": "bright",
        "key": "C",
        "tempo": 125,
        "bars": "64 - Extended",
    },

    "Rambo 1985": {
        "style": "metal",
        "mood": "dark",
        "key": "E",
        "tempo": 170,
        "bars": "64 - Extended",
    },

    "Miami Vice Sunset": {
        "style": "synthwave",
        "mood": "bright",
        "key": "F",
        "tempo": 118,
        "bars": "64 - Extended",
    },

    "KiljuPaska-82": {
        "style": "punk77",
        "mood": "energetic",
        "key": "E",
        "tempo": 195,
        "bars": "32 - Song",
    },

    "Vitun Pikku Prinssit": {
        "style": "punk77",
        "mood": "bright",
        "key": "A",
        "tempo": 185,
        "bars": "32 - Song",
    },

    "Avaruusromua": {
        "style": "ambient",
        "mood": "calm",
        "key": "C",
        "tempo": 90,
        "bars": "64 - Extended",
    },

    "Beastie Funk Punk": {
        "style": "punk77",
        "mood": "bright",
        "key": "E",
        "tempo": 186,
        "bars": "32 - Song",
    },

    "Cyberpunk Night Drive": {
        "style": "synthwave",
        "mood": "dark",
        "key": "C#",
        "tempo": 130,
        "bars": "64 - Extended",
    },

    "Goa Beach 1996": {
        "style": "goa",
        "mood": "bright",
        "key": "A",
        "tempo": 145,
        "bars": "64 - Extended",
    },

    "Finnish Metal": {
        "style": "metal",
        "mood": "dark",
        "key": "E",
        "tempo": 180,
        "bars": "64 - Extended",
    },
}


class ArcAiComposer(QWidget):

    def __init__(self):
        super().__init__()

        self.latest_file = None

        self.setWindowTitle("SemiTracker_Composer_v0.3")
        self.resize(750, 550)
        print("Window size set")

        self.setStyleSheet("""
        QWidget {
            background-color: #141824;
            color: #e8ecff;
            font-family: Segoe UI;
            font-size: 10pt;
        }

        QLabel {
            color: #7df9ff;
            font-weight: bold;
        }

        QComboBox {
            background-color: #20283a;
            color: white;
            border: 2px solid #00c8ff;
            border-radius: 6px;
            padding: 6px;
        }

        QSpinBox {
            background-color: #20283a;
            color: white;
            border: 2px solid #00c8ff;
            border-radius: 6px;
            padding: 6px;
        }

        QTextEdit {
            background-color: #0c1018;
            color: #00ff88;
            border: 2px solid #00c8ff;
            border-radius: 6px;
        }

        QPushButton {
            background-color: #00c8ff;
            color: black;
            border-radius: 8px;
            padding: 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #42dcff;
        }
        """)

        layout = QVBoxLayout()

        title = QLabel("TRACKERFORGE")
        title.setStyleSheet("""
            font-size: 22pt;
            font-weight: bold;
            color: #00c8ff;
        """)
        layout.addWidget(title)
        subtitle = QLabel(
            "Featuring KiljuPaska-82 Preset Pack"
        )

        subtitle.setStyleSheet("""
            color: #a0b8d8;
            font-size: 10pt;
        """)

        layout.addWidget(subtitle)

        layout.addWidget(QLabel("Preset"))

        self.preset = QComboBox()
        self.preset.addItems(list(PRESETS.keys()))
        self.preset.currentTextChanged.connect(
            self.load_preset
        )

        layout.addWidget(self.preset)

        layout.addWidget(QLabel("Style"))

        self.style = QComboBox()
        self.style.addItems([
            "metal",
            "punk77",
            "industrial",
            "synthwave",
            "ambient",
            "goa",
            "trance90s",
            "house90s",
            "jazz_lounge",
            "chiptune"
        ])
        layout.addWidget(self.style)

        layout.addWidget(QLabel("Mood"))

        self.mood = QComboBox()
        self.mood.addItems([
            "energetic",
            "dark",
            "bright",
            "calm"
        ])
        layout.addWidget(self.mood)

        layout.addWidget(QLabel("Key"))

        self.key = QComboBox()
        self.key.addItems([
            "A", "A#", "Ab",
            "B", "Bb",
            "C", "C#",
            "D", "D#", "Db",
            "E", "Eb",
            "F", "F#",
            "G", "G#", "Gb"
        ])
        self.key.setCurrentText("E")

        layout.addWidget(self.key)

        layout.addWidget(QLabel("Tempo"))

        self.tempo = QSlider(Qt.Horizontal)
        self.tempo.setRange(30, 300)
        self.tempo.setValue(180)

        self.tempo_label = QLabel("180 BPM")

        self.tempo.valueChanged.connect(
            lambda v: self.tempo_label.setText(f"{v} BPM")
        )

        layout.addWidget(self.tempo)
        layout.addWidget(self.tempo_label)

        layout.addWidget(QLabel("Bars"))

        self.bars = QComboBox()
        self.bars.addItems([
            "16 - Idea",
            "32 - Song",
            "64 - Extended"
        ])
        self.bars.setCurrentText("32 - Song")

        layout.addWidget(self.bars)

        layout.addWidget(QLabel("Seed"))

        self.seed = QSpinBox()
        self.seed.setRange(-2147483648, 2147483647)
        self.seed.setValue(666)

        layout.addWidget(self.seed)

        self.generate_btn = QPushButton("Generate XM")
        self.generate_btn.clicked.connect(
            self.generate_track
        )

        layout.addWidget(self.generate_btn)

        self.random_btn = QPushButton("🎲 Random Fantasy")
        self.random_btn.clicked.connect(
            self.random_preset
        )

        layout.addWidget(self.random_btn)

        self.open_btn = QPushButton("Open Latest XM")
        self.open_btn.clicked.connect(
            self.open_latest
        )

        layout.addWidget(self.open_btn)

        layout.addWidget(QLabel("Log"))

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.log)

        self.setLayout(layout)

    def load_preset(self, name):

        if name == "Custom":
            return

        preset = PRESETS[name]

        self.style.setCurrentText(
            preset["style"]
        )

        self.mood.setCurrentText(
            preset["mood"]
        )

        self.key.setCurrentText(
            preset["key"]
        )

        self.tempo.setValue(
            preset["tempo"]
        )

        self.bars.setCurrentText(
            preset["bars"]
        )

    def random_preset(self):

        presets = [
            p for p in PRESETS.keys()
            if p != "Custom"
        ]

        choice = random.choice(presets)

        self.preset.setCurrentText(choice)

        self.log.append(
            f"🎲 Random preset: {choice}"
        )

    def generate_track(self):

        style = self.style.currentText()
        mood = self.mood.currentText()
        key = self.key.currentText()
        tempo = self.tempo.value()
        bars = self.bars.currentText().split()[0]
        seed = self.seed.value()

        output = f"{style}_{tempo}.xm"

        cmd = [
            sys.executable,
            "-m",
            "arc_ai_tracker.cli",
            "generate",
            "--style", style,
            "--mood", mood,
            "--key", key,
            "--tempo", str(tempo),
            "--bars", str(bars),
            "--seed", str(seed),
            "--format", "xm",
            "--output", output,
        ]

        self.log.append("> " + " ".join(cmd))

        try:

            subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if Path(output).exists():

                self.latest_file = output

                self.log.append(
                    f"✅ Generated: {output}"
                )

                os.startfile(output)

            else:

                self.log.append(
                    f"❌ Failed: {output}"
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def open_latest(self):

        if (
            self.latest_file
            and Path(self.latest_file).exists()
        ):
            os.startfile(self.latest_file)

    def closeEvent(self, event):

        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ArcAiComposer()
    window.show()

    sys.exit(app.exec())