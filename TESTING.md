# TrackerForge Composer v0.4 – Release Testing Checklist

**Version**: 0.4.0  
**Release Date**: 2026-10-05  
**Tester**: AleksisLeipakivi  
**Test Environment**: Windows 10/11, PowerShell, Python 3.8+

---

## 📋 Pre-Release Testing Protocol

This document outlines comprehensive testing for v0.4 release. Each test should be run in isolation and reported as **PASS** or **FAIL** with notes.

---

## 1️⃣ Environment Setup

### 1.1 Fresh PowerShell Session
- [ ] Open new PowerShell window as standard user (not admin)
- [ ] Navigate to project directory
- [ ] Run: `python --version` (should be 3.8+)
- [ ] Run: `pip list | findstr PySide6` (should find PySide6>=6.0)

**Status**: ___________

---

## 2️⃣ GUI Launch & Startup

### 2.1 Launch from Source Code
```powershell
python arc_ai_tracker_gui_v03.py
```

**Expected**:
- Window opens within 3 seconds
- Title bar shows "TrackerForge Composer v0.4"
- Subtitle shows "Featuring KiljuPaska-82 Preset Pack | v0.4 Patch"
- All UI elements visible and responsive
- No console errors

**Actual Result**: ___________

**Notes**: ___________

### 2.2 MilkyTracker Detection on Startup
**Expected**:
- Console shows MilkyTracker path found, OR
- Console shows "⚠️ MilkyTracker not found" (warning, not error)
- GUI launches successfully regardless

**Actual Result**: ___________

**Notes**: ___________

### 2.3 Window Resizing & Layout
**Expected**:
- Window is 750x550 pixels
- All buttons, sliders, text boxes fit without overflow
- No text cutoff or UI glitches
- Resizing window doesn't break layout

**Actual Result**: ___________

**Notes**: ___________

### 2.4 Theme & Styling
**Expected**:
- Dark theme applied (background #141824)
- Cyan text color (#7df9ff) on labels
- Cyan button borders (#00c8ff)
- Green text (#00ff88) in log
- Hover effects on buttons work

**Actual Result**: ___________

**Notes**: ___________

---

## 3️⃣ GUI Controls & Presets

### 3.1 Preset Selection
**Steps**:
1. Click "Preset" dropdown
2. Select each preset one by one: Amiga 500 Demo, Rambo 1985, KiljuPaska-82, Finnish Metal, etc.
3. Verify that Style, Mood, Key, Tempo, and Bars update automatically

**Expected**:
- All 10 presets load without errors
- Values change correctly for each preset
- "Custom" preset does nothing (correct behavior)

**Actual Result**: ___________

**Status by Preset**:
- [ ] Amiga 500 Demo: PASS/FAIL
- [ ] Rambo 1985: PASS/FAIL
- [ ] Miami Vice Sunset: PASS/FAIL
- [ ] KiljuPaska-82: PASS/FAIL
- [ ] Vitun Pikku Prinssit: PASS/FAIL
- [ ] Avaruusromua: PASS/FAIL
- [ ] Beastie Funk Punk: PASS/FAIL
- [ ] Cyberpunk Night Drive: PASS/FAIL
- [ ] Goa Beach 1996: PASS/FAIL
- [ ] Finnish Metal: PASS/FAIL

**Notes**: ___________

### 3.2 Manual Control Changes
**Steps**:
1. Change Style dropdown (cycle through all 10 options)
2. Change Mood dropdown (energetic, dark, bright, calm)
3. Change Key dropdown (A, A#, Ab, B, Bb, C, C#, D, D#, Db, E, Eb, F, F#, G, G#, Gb)
4. Change Tempo slider (min 30, max 300)
5. Change Bars dropdown (16 - Idea, 32 - Song, 64 - Extended)
6. Change Seed spinner (try -1, 0, 666, 999)

**Expected**:
- All dropdowns/sliders respond immediately
- No lag or freezes
- Tempo label updates correctly ("180 BPM" format)
- Seed accepts large integers without crashing

**Actual Result**: ___________

**Notes**: ___________

### 3.3 Random Fantasy Button
**Steps**:
1. Click "🎲 Random Fantasy" button 5 times
2. Observe log output and preset selection

**Expected**:
- Each click selects a random preset (not "Custom")
- Log shows "🎲 Random preset: [name]"
- Presets don't repeat on consecutive clicks (very rare but possible)
- No crashes

**Actual Result**: ___________

**Notes**: ___________

---

## 4️⃣ XM File Generation

### 4.1 Generate with Default Settings
**Steps**:
1. Leave all settings at default (Finnish Metal preset, E key, 180 BPM, 32 bars)
2. Click "Generate XM"
3. Wait for completion (watch log)

**Expected**:
- Log shows: "> [command line]"
- Log shows: "✅ Generated: metal_180.xm"
- File `metal_180.xm` created in project directory
- File size > 0 bytes
- No "❌ Failed" message
- **MilkyTracker opens automatically** (if installed)

**Actual Result**: ___________

**File Check**:
- [ ] File exists: metal_180.xm
- [ ] File size: __________ bytes
- [ ] File readable: PASS/FAIL

**Notes**: ___________

### 4.2 Generate with Different Styles
**Steps**:
Repeat 4.1 for these combinations:

| Style | Tempo | Bars | Expected Filename |
|-------|-------|------|-------------------|
| chiptune | 125 | 16 | chiptune_125.xm |
| punk77 | 195 | 32 | punk77_195.xm |
| synthwave | 130 | 64 | synthwave_130.xm |
| ambient | 90 | 64 | ambient_90.xm |

**Expected**:
- All files generate successfully
- Filenames match expected format: `{style}_{tempo}.xm`
- No naming conflicts or overwrites
- All files are valid XM format

**Actual Result**: ___________

**Status**:
- [ ] chiptune_125.xm: PASS/FAIL
- [ ] punk77_195.xm: PASS/FAIL
- [ ] synthwave_130.xm: PASS/FAIL
- [ ] ambient_90.xm: PASS/FAIL

**Notes**: ___________

### 4.3 Generate with Custom Seed
**Steps**:
1. Set Seed to 42
2. Generate XM → produces `test_42.xm`
3. Generate XM again with same seed (42) → produces `test_42.xm` (overwrite)
4. Set Seed to 99
5. Generate XM → produces `test_99.xm`

**Expected**:
- Same seed produces similar/identical compositions (reproducibility)
- Different seeds produce different variations
- No file corruption on overwrite
- Log clearly shows seed value used

**Actual Result**: ___________

**Notes**: ___________

### 4.4 XM File Format Validity
**Steps**:
1. Generate a test XM file
2. Open file in hex editor or check file header

**Expected**:
- File starts with "Extended Module:" header (or XM signature)
- File can be opened in MilkyTracker without corruption warnings
- File plays without artifacts

**Actual Result**: ___________

**Notes**: ___________

---

## 5️⃣ MilkyTracker Integration

### 5.1 Auto-Open in MilkyTracker
**Prerequisites**: MilkyTracker must be installed

**Steps**:
1. Generate XM file
2. Observe automatic opening behavior

**Expected**:
- MilkyTracker launches within 2 seconds
- Generated XM file loads automatically in MilkyTracker
- Log shows: "▶ Opened in MilkyTracker: {filename}"
- MilkyTracker window is in foreground

**Actual Result**: ___________

**Notes**: ___________

### 5.2 "Open Latest XM" Button (with MilkyTracker)
**Steps**:
1. Generate an XM file (e.g., `metal_180.xm`)
2. Keep MilkyTracker open or close it
3. Click "Open Latest XM" button
4. Repeat with different generated files

**Expected**:
- MilkyTracker launches/brings to front
- Latest file opens in MilkyTracker
- No "File not found" errors
- Log shows: "▶ Opened in MilkyTracker: {filename}"

**Actual Result**: ___________

**Notes**: ___________

### 5.3 MilkyTracker Not Found – Error Handling
**Prerequisites**: MilkyTracker not installed or path invalid

**Steps**:
1. Temporarily move/uninstall MilkyTracker
2. Generate an XM file
3. Click "Open Latest XM"

**Expected**:
- Error dialog appears: "MilkyTracker puuttuu" / "MilkyTracker.exe:tä ei löytynyt"
- XM file is NOT opened with default application
- XM file is NOT corrupted
- Log shows: "⚠️ MilkyTracker.exe not found"
- No crash

**Actual Result**: ___________

**Notes**: ___________

### 5.4 Multiple MilkyTracker Paths Tested
**If available**, test with MilkyTracker installed in:
- [ ] `C:\Program Files\MilkyTracker\` – PASS/FAIL
- [ ] `C:\Program Files (x86)\MilkyTracker\` – PASS/FAIL
- [ ] Downloads folder – PASS/FAIL
- [ ] WinGet/Microsoft Store – PASS/FAIL

**Expected**: App detects first available path and uses it

**Actual Result**: ___________

**Notes**: ___________

---

## 6️⃣ Log Output & User Feedback

### 6.1 Log Clarity & Messages
**Steps**:
1. Generate multiple XM files
2. Click buttons multiple times
3. Observe log text area

**Expected**:
- Log shows all commands executed ("> " prefix)
- Success messages use ✅ emoji
- Errors use ❌ emoji
- Warnings use ⚠️ emoji
- Playback indicators use ▶ emoji
- All messages are human-readable
- Log doesn't overflow or truncate

**Actual Result**: ___________

**Notes**: ___________

### 6.2 Error Messages Are Informative
**Steps**:
1. Trigger error scenarios (MilkyTracker not found, invalid file path, etc.)
2. Read error dialogs

**Expected**:
- Error messages explain the problem in plain language
- Error messages suggest solutions (e.g., "Install MilkyTracker")
- No cryptic stack traces shown to user
- Dialog buttons work (OK, Close)

**Actual Result**: ___________

**Notes**: ___________

### 6.3 No Duplicate or Conflicting Messages
**Steps**:
1. Generate files multiple times rapidly
2. Check for log spam or conflicting messages

**Expected**:
- One message per action
- No repeated identical messages
- Messages appear in correct order
- Timestamps or order is clear

**Actual Result**: ___________

**Notes**: ___________

---

## 7️⃣ File System Behavior

### 7.1 File Creation & Location
**Steps**:
1. Generate XM files
2. Check current working directory

**Expected**:
- XM files are created in project root (where app is run from)
- Files are visible in File Explorer
- File permissions allow user to delete/move files
- No hidden or system attributes set

**Actual Result**: ___________

**Notes**: ___________

### 7.2 Filename Collisions (Overwrite Behavior)
**Steps**:
1. Generate `metal_180.xm` (creates new file)
2. Generate `metal_180.xm` again (should overwrite)
3. Check file timestamp and size

**Expected**:
- File is overwritten without error
- No backup file created (expected behavior)
- File size may differ based on generation randomness
- Timestamp updates to current time
- No "file already exists" dialog

**Actual Result**: ___________

**Notes**: ___________

### 7.3 Long Filenames & Special Characters
**Steps**:
1. Set Style to something with underscores or numbers
2. Set Tempo to extreme values (30, 300)
3. Generate files for these combinations

**Expected**:
- Filenames follow `{style}_{tempo}.xm` format exactly
- No special characters in filenames (only alphanumeric, underscore, numbers, dot)
- No filename length issues
- All generated files are readable

**Actual Result**: ___________

**Notes**: ___________

### 7.4 Cleanup (No Temp Files Left Behind)
**Steps**:
1. Generate 10 XM files
2. Close application
3. Check directory for orphaned or temporary files

**Expected**:
- Only intended `.xm` files exist
- No `.tmp`, `.bak`, or other temporary files
- No Python cache files outside `__pycache__`
- Directory is clean

**Actual Result**: ___________

**Notes**: ___________

---

## 8️⃣ Performance & Stability

### 8.1 Startup Time
**Steps**:
1. Time application from launch to fully interactive

**Expected**:
- Startup < 5 seconds (Python interpreter + PySide6)
- All UI elements responsive within startup window
- No frozen/spinning cursor

**Actual Result**: ___________

**Startup Time**: __________ seconds

**Notes**: ___________

### 8.2 Generation Time
**Steps**:
1. Time XM generation from "Generate XM" click to completion

**Expected**:
- Generation < 30 seconds (depends on system)
- Log updates show progress
- No UI freezing during generation
- Cancel button exists (not yet implemented, but should not hang)

**Actual Result**: ___________

**Generation Time**: __________ seconds

**Notes**: ___________

### 8.3 Memory Usage
**Steps**:
1. Open Task Manager (Ctrl+Shift+Esc)
2. Find TrackerForge process
3. Note memory usage
4. Generate 5 XM files
5. Note memory usage again
6. Close app and repeat

**Expected**:
- Startup memory < 200 MB
- Memory doesn't grow excessively per generation
- No memory leaks on repeated generations
- Memory released on app close

**Actual Result**: ___________

**Startup Memory**: __________ MB  
**After 5 Generations**: __________ MB  
**Difference**: __________ MB

**Notes**: ___________

### 8.4 Rapid Clicking (Stability Under Load)
**Steps**:
1. Rapidly click "Generate XM" button 10 times without waiting
2. Observe behavior

**Expected**:
- Requests queue or later requests wait for earlier ones
- No crash or hang
- Log shows all commands (or shows queueing behavior)
- UI remains responsive
- Application recovers gracefully

**Actual Result**: ___________

**Notes**: ___________

---

## 9️⃣ Executable Build (EXE) Testing

### 9.1 Build Standalone Executable
```powershell
pyinstaller --clean --onefile --windowed --name TrackerForge arc_ai_tracker_gui_v03.py
```

**Expected**:
- Build completes without errors
- `dist\TrackerForge.exe` is created
- File size ~150-300 MB (PySide6 is large)
- No build warnings

**Actual Result**: ___________

**Build Time**: __________ seconds  
**EXE File Size**: __________ MB

**Notes**: ___________

### 9.2 Run Standalone Executable
**Steps**:
1. Navigate to `dist` directory
2. Run `.\TrackerForge.exe`
3. Repeat all GUI and generation tests above

**Expected**:
- EXE launches in ~10 seconds
- GUI appears and functions identically to source version
- All features work (generation, MilkyTracker open, etc.)
- Generates valid XM files
- No "missing DLL" or runtime errors

**Actual Result**: ___________

**Notes**: ___________

### 9.3 Run EXE from Different Directory
**Steps**:
1. Copy `TrackerForge.exe` to Desktop
2. Run from Desktop
3. Generate XM files

**Expected**:
- EXE runs successfully without working directory
- XM files generated in working directory (Desktop)
- All functionality works the same
- No file not found errors

**Actual Result**: ___________

**Notes**: ___________

### 9.4 Run EXE on Clean Windows (No Python)
**Prerequisites**: Test on machine with no Python installed

**Steps**:
1. Copy `dist\TrackerForge.exe` to USB or another computer
2. Run without Python installed
3. Generate XM files
4. Test MilkyTracker integration

**Expected**:
- EXE runs successfully
- All features work
- No Python/dependency errors

**Actual Result**: ___________

**Notes**: ___________

---

## 🔟 Error Scenarios & Edge Cases

### 10.1 No Disk Space
**Steps**:
1. Fill disk to nearly full
2. Try to generate XM

**Expected**:
- Clear error message about disk space
- No corrupted partial files left behind
- Application remains stable

**Actual Result**: ___________

**Notes**: ___________

### 10.2 Invalid File Path
**Steps**:
1. Run app from read-only directory (if possible)
2. Try to generate XM

**Expected**:
- Error message: "Cannot write to directory" or similar
- File not created
- App remains responsive

**Actual Result**: ___________

**Notes**: ___________

### 10.3 User Closes App During Generation
**Steps**:
1. Click "Generate XM"
2. Immediately click window close button (X)
3. Try to close app

**Expected**:
- App closes cleanly (may wait for generation to finish)
- Partial files cleaned up (or overwritten next time)
- No hanging processes

**Actual Result**: ___________

**Notes**: ___________

### 10.4 Window Minimized/Hidden During Generation
**Steps**:
1. Click "Generate XM"
2. Minimize window or switch to another app
3. Let generation complete
4. Bring window back

**Expected**:
- Generation continues in background
- Log updates visible when window restored
- MilkyTracker still opens automatically
- No frozen UI when restored

**Actual Result**: ___________

**Notes**: ___________

---

## 1️⃣1️⃣ Code Quality Checks

### 11.1 No Python Errors in Console
**Steps**:
1. Run app from PowerShell with console visible
2. Execute all tests above
3. Monitor console output

**Expected**:
- No red error messages
- No stack traces
- Only informational prints (window size, MilkyTracker path)
- Clean exit when window closes

**Actual Result**: ___________

**Console Output Sample**:
```
[Paste first 20 lines of console output]
```

**Notes**: ___________

### 11.2 Code Style Check
**Steps**:
```powershell
black arc_ai_tracker_gui_v03.py --check
flake8 arc_ai_tracker_gui_v03.py
```

**Expected**:
- No flake8 errors (warnings are okay)
- Black formatting is consistent

**Actual Result**: ___________

**Notes**: ___________

### 11.3 No Hardcoded Paths (Portability)
**Steps**:
1. Review `arc_ai_tracker_gui_v03.py` for hardcoded paths
2. Check: `/n "C:\Users\tuukk\"` or similar

**Expected**:
- No user-specific hardcoded paths (except as fallback in find_milkytracker)
- Uses `Path.home()` and environment variables
- App works on different Windows user accounts

**Actual Result**: ___________

**Findings**: ___________

**Notes**: ___________

---

## 1️⃣2️⃣ Documentation Review

### 12.1 README Accuracy
**Steps**:
1. Read README.md
2. Follow each instruction step by step
3. Verify examples work as documented

**Expected**:
- All install steps work
- Example commands run successfully
- Presets list is accurate
- Features list matches actual implementation

**Actual Result**: ___________

**Notes**: ___________

### 12.2 Comments in Code
**Steps**:
1. Open `arc_ai_tracker_gui_v03.py`
2. Check major functions for docstrings/comments
3. Verify v0.4 changes are documented

**Expected**:
- `find_milkytracker()` has clear docstring
- `open_with_milkytracker()` explains its purpose
- v0.4 changes noted in comments or README

**Actual Result**: ___________

**Notes**: ___________

---

## 1️⃣3️⃣ Compatibility & Dependencies

### 13.1 Python Version Compatibility
**Steps**:
1. Test on Python 3.8 (if available)
2. Test on Python 3.9 (if available)
3. Test on Python 3.10+ (current system)

**Expected**:
- All versions run without errors
- No Python version-specific syntax issues

**Actual Result**: ___________

**Python 3.8**: PASS/FAIL  
**Python 3.9**: PASS/FAIL  
**Python 3.10+**: PASS/FAIL

**Notes**: ___________

### 13.2 PySide6 Version
**Steps**:
```powershell
pip show PySide6
```

**Expected**:
- Version >= 6.0
- All GUI features work

**Actual Result**: ___________

**PySide6 Version**: __________

**Notes**: ___________

### 13.3 Dependencies List
**Steps**:
1. Check `requirements.txt`
2. Verify all dependencies are installed
3. Check for unused dependencies

```powershell
pip list
```

**Expected**:
- Only PySide6 required
- No bloat dependencies
- All specified versions satisfied

**Actual Result**: ___________

**Notes**: ___________

---

## Summary Report

### Overall Status
- **Total Tests**: 100+
- **Passed**: ________
- **Failed**: ________
- **Blocked/N/A**: ________

### Critical Issues Found
```
[List any FAIL results that block release]
```

### Minor Issues / Nice-to-Have Fixes
```
[List any minor FAIL results or improvements]
```

### Recommendation
- [ ] **APPROVED for v0.4 release** (all critical tests PASS)
- [ ] **NEEDS FIXES** before release (see critical issues above)
- [ ] **NEEDS REVIEW** (see notes section)

### Sign-Off
- **Tester**: AleksisLeipakivi
- **Test Date**: 2026-10-05
- **Next Steps**: ___________

---

**End of Release Testing Checklist**

