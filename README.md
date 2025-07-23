# 🎛️ VJing Grid Visualizer – Musikreaktive 3D-OpenGL-Visualisierung

Dieses Python-Projekt visualisiert ein animiertes 3D-Gitter (Grid) in OpenGL und erlaubt die manuelle sowie automatische Steuerung der Parameter über Musik – live über das Mikrofon. Es eignet sich hervorragend für VJing, interaktive Installationen oder kreative Experimente.

---

## 🔧 Features

- 🎛️ Steuerpanel mit Reglern für:
  - Amplitude
  - Frequenz
  - Wellengeschwindigkeit
  - Rotation
  - Zoom
  - Farbe (Hue)
  - Audio-Empfindlichkeit
- 🎚️ Umschaltbarer **Automatikmodus**:
  - 🎧 Bass → Amplitude
  - 🎨 Mitten → Farbe (Hue)
  - 💫 Gesamtlautstärke → Bewegung (Wellenanimation)
- 🔊 Live-Audio-Eingang über Mikrofon (kein Audio aus Datei)
- 🔬 Frequenzanalyse mittels FFT
- 🧠 Pegelglättung (für weiche Reaktionen)
- 🌀 Kameraperspektive zentral und flach (nicht von oben)

---

## 📦 Installation

1. Klone das Projekt oder lade die Dateien herunter:

git clone https://github.com/deinname/vjing_grid_visualizer.git
cd vjing_grid_visualizer


2. Erstelle eine virtuelle Umgebung (empfohlen):

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


3. Installiere die Abhängigkeiten:

pip install -r requirements.txt


4. Starten
python main.py