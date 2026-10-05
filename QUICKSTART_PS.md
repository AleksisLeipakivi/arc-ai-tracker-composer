# TrackerForge Composer – PowerShell Quick Start Guide

Tämä opas opettaa sinulle, miten käytät TrackerForge Compositoria PowerShellissä, vaihe vaiheelta.

---

## 📋 Ennakkovaatimukset

Sinulla täytyy olla:
- Windows 10 tai 11
- PowerShell (klikkaa Windows-nappia, kirjoita "PowerShell")
- Python 3.8 tai uudempi
- Internet-yhteys (lataamista varten)

---

## Vaihe 1: Tarkista Python

**Mitä tehdään**: Tarkistetaan, että Python on asennettu oikein.

Avaa **PowerShell** ja kirjoita:

```powershell
python --version
```

**Odotettu tulos**:
```
Python 3.10.5
```

Jos näet "python : The term 'python' is not recognized", Python ei ole asennettu. 
→ Asenna Python osoitteesta https://www.python.org/downloads/

---

## Vaihe 2: Lataa Projekti

**Mitä tehdään**: Ladataan TrackerForge-koodi GitHubista.

PowerShellissä kirjoita:

```powershell
git clone https://github.com/AleksisLeipakivi/arc-ai-tracker-composer.git
```

**Odotettu tulos**:
```
Cloning into 'arc-ai-tracker-composer'...
remote: Enumerating objects: 50, done.
remote: Counting objects: 100% (50/50), done.
```

Jos näet virheen "git : The term 'git' is not recognized", Git ei ole asennettu.
→ Asenna Git osoitteesta https://git-scm.com/

---

## Vaihe 3: Siirry Projektikansioon

**Mitä tehdään**: Menemme lataamasi projektin kansioon.

```powershell
cd arc-ai-tracker-composer
```

**Tarkista, että olet oikeassa paikassa**:

```powershell
dir
```

**Odotettu tulos** (näet nämä tiedostot):
```
Mode                 LastWriteTime         Length Name
----                 ----                  ------ ----
-a----        29.9.2026     16.52            1234 README.md
-a----        29.9.2026     16.52            5678 arc_ai_tracker_gui_v03.py
-a----        29.9.2026     16.52              50 requirements.txt
-a----        29.9.2026     16.52             999 LICENSE
```

---

## Vaihe 4: Asenna Riippuvuudet

**Mitä tehdään**: Asennetaan ohjelma tarvitsee Python-paketit (erityisesti PySide6).

```powershell
pip install -r requirements.txt
```

**Odotettu tulos**:
```
Collecting PySide6>=6.0
  Downloading PySide6-6.7.0-...
Installing collected packages: PySide6
Successfully installed PySide6-6.7.0
```

**Jos virheilmoitus**:
- Yritä: `pip install --upgrade pip`
- Sitten uudelleen: `pip install -r requirements.txt`

---

## Vaihe 5: Käynnistä Ohjelma

**Mitä tehdään**: Käynnistetään TrackerForge GUI.

```powershell
python arc_ai_tracker_gui_v03.py
```

**Odotettu tulos**:
- GUI-ikkuna avautuu ruudullesi
- Näet "TRACKERFORGE" otsikon
- Näet presetit, säätöjä, nappuloita

**Jos virheilmoitus**:
- Tarkista, että olet projektikansiossa (`cd arc-ai-tracker-composer`)
- Tarkista, että `requirements.txt` on asennettu (`pip install -r requirements.txt`)

---

## Vaihe 6: Käytä Ohjelmaa

**Mitä tehdään**: Luodaan ensimmäinen XM-tiedosto.

### 6.1 Valitse Preset

1. Klikkaa "Preset" -pudotusvalikko
2. Valitse esimerkiksi **"Finnish Metal"**
3. Näet, että Style, Mood, Key, Tempo päivittyvät automaattisesti

### 6.2 (Valinnainen) Säädä Asetuksia

Voit muuttaa:
- **Style**: metal, punk77, synthwave, ambient, chiptune...
- **Mood**: energetic, dark, bright, calm
- **Key**: A, A#, Ab, B, Bb, C, C#, D, D#, Db, E, Eb, F, F#, G, G#, Gb
- **Tempo**: 30–300 BPM (liikuttele slideria)
- **Bars**: 16 (idea), 32 (song), 64 (extended)
- **Seed**: mikä tahansa numero (sama numero = sama musiikki)

### 6.3 Generoi XM-tiedosto

1. Klikkaa **"Generate XM"** nappia
2. Odota 5–30 sekuntia
3. Log-tekstikenttään ilmestyy:
   ```
   > python -m arc_ai_tracker.cli generate --style metal --mood dark ...
   ✅ Generated: metal_180.xm
   ▶ Opened in MilkyTracker: metal_180.xm
   ```

**Mitä tapahtuu**:
- `metal_180.xm` tiedosto luodaan
- Jos MilkyTracker on asennettu, se avautuu automaattisesti

### 6.4 (Valinnainen) Avaa MilkyTrackerissa

Jos MilkyTracker ei auennut automaattisesti:

1. Klikkaa **"Open Latest XM"** nappia
2. MilkyTracker avautuu viimeisen tiedoston kanssa

---

## Vaihe 7: Katso Generoitu Tiedosto

**Mitä tehdään**: Tarkistetaan, että XM-tiedosto luotiin.

PowerShellissä (pidä TrackerForge avoimena):

```powershell
dir *.xm
```

**Odotettu tulos**:
```
Mode                 LastWriteTime         Length Name
----                 ----                  ------ ----
-a----        29.9.2026     17:05           12345 metal_180.xm
```

Jos näet tiedoston, se toimi! ✅

---

## Vaihe 8: Avaa MilkyTrackerissä (Manuaalisesti)

Jos haluat avata XM-tiedoston itse MilkyTrackerissa:

```powershell
# Korvaa polku omallasi, jos MilkyTracker on eri paikassa
& "C:\Users\tuukk\AppData\Local\Microsoft\WinGet\Packages\MilkyTracker.MilkyTracker_Microsoft.Winget.Source_8wekyb3d8bbwe\milkytracker-1.05.01-win64\MilkyTracker.exe" "metal_180.xm"
```

MilkyTracker avautuu ja lataa tiedoston.

---

## Vaihe 9: Kokeile "Random Fantasy"

**Mitä tehdään**: Luodaan satunnainen presetti.

1. Klikkaa **"🎲 Random Fantasy"** nappia
2. Preset valitaan satunnaisesti
3. Klikkaa **"Generate XM"**
4. Uusi tiedosto luodaan

---

## Vaihe 10: Kokeile Eri Presetejä

TrackerForgessa on 10 valmiiksi ladattua presettiä:

| Presetti | Tyyli | Mieli | Tempo | Palkit |
|----------|-------|-------|-------|--------|
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

Kokeile niitä kaikki! 🎵

---

## Vaihe 11: Sulje Ohjelma

Kun olet valmis:

1. Klikkaa GUI-ikkunan **X**-nappia
2. PowerShell palaa komentoriville

---

## 🔧 Virheiden Korjaus

### Ongelma: "python: The term 'python' is not recognized"

**Ratkaisu**:
1. Asenna Python: https://www.python.org/downloads/
2. **Tarkista "Add Python to PATH"** asennuksen aikana
3. Käynnistä PowerShell uudelleen

### Ongelma: "ModuleNotFoundError: No module named 'PySide6'"

**Ratkaisu**:
```powershell
pip install --upgrade PySide6
```

### Ongelma: "MilkyTracker not found"

**Ratkaisu**:
1. Asenna MilkyTracker: https://milkytracker.org/
2. Tai jätä se asennoimatta – ohjelma toimii silti, kunhan avaat .xm-tiedostot itse

### Ongelma: XM-tiedostoja ei luoda

**Ratkaisu**:
1. Tarkista, että olet projektikansiossa: `cd arc-ai-tracker-composer`
2. Tarkista log-tekstialueella mahdollisia virheilmoituksia
3. Tarkista, että levyllä on tilaa: `diskusage C:`

---

## 💡 Vinkkejä

- **Sama seed = sama musiikki**: Jos asitat Seed-kenttään 42 ja generoit kahdesti, saat saman kappaleen
- **Eri seed = eri musiikki**: Muuta Seed-numero saadaksesi uuden variation
- **Random Fantasy**: Klikkaa sitä monta kertaa saadaksesi erilaisia presetejä
- **MilkyTracker-muokkausta**: Kun olet avannut XM:n MilkyTrackerissa, voit muokata instrumentteja, efektejä ja malleita

---

## 📂 Tiedostojen Sijainti

Generoituja XM-tiedostoja säilytetään **projektikansiossa**:

```
C:\Käyttäjät\[sinun-käyttäjätunnuksesi]\...\arc-ai-tracker-composer\
    ├─ arc_ai_tracker_gui_v03.py (ohjelma)
    ├─ README.md
    ├─ requirements.txt
    ├─ metal_180.xm (generoitu tiedosto)
    ├─ synthwave_130.xm (generoitu tiedosto)
    └─ ...
```

Voit kopioida .xm-tiedostot mihin tahansa ja avata ne MilkyTrackerissa.

---

## ✅ Yhteenveto

Nämä ovat perusaskeleet:

1. ✅ Avaa PowerShell
2. ✅ `git clone https://github.com/AleksisLeipakivi/arc-ai-tracker-composer.git`
3. ✅ `cd arc-ai-tracker-composer`
4. ✅ `pip install -r requirements.txt`
5. ✅ `python arc_ai_tracker_gui_v03.py`
6. ✅ Valitse presetti
7. ✅ Klikkaa "Generate XM"
8. ✅ XM-tiedosto syntyy
9. ✅ MilkyTracker avautuu (jos asennettu)

Onnittelut! 🎵 Olet nyt käyttäjä TrackerForge Composerista.

---

## 🆘 Lisäohje

Jos sinulla on lisäkysymyksiä:

- Lue README.md
- Katso GitHub Issues: https://github.com/AleksisLeipakivi/arc-ai-tracker-composer/issues
- Ota yhteyttä: tukorama@gmail.com

---

**Happy composing!** 🎶
