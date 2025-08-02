---

# 🎬 Quick Beat Saber Video Editor
A lightweight video editor tailored for Beat Saber gameplay editing. Trim videos, apply transitions, boost saturation, and overlay BeatSaver metadata.

https://github.com/user-attachments/assets/dec3492a-e5e1-4555-a033-7a73ccf7668e

---

## What is this?

This tool helps you quickly edit raw video clips of Beat Saber gameplay or map previews. It:

- Trims a video between two timestamps
- Applies fade-in and fade-out effects
- (Optionally) Boosts video saturation for good looking videos despite YouTube's evil compression
- (Optionally) Generates a map overlay with:
  - Song title
  - Mapper name
  - Cover image
-  Shows the overlay with a smooth slide animation

---

## How to use it?

### Option 1: For users familiar with running Python
This is the lightweight option if you just want the functional scripts.

> Requirements: Python 3.10+, `ffmpeg`, and `ffprobe` on your system PATH

1. Clone this repository
2. Install dependencies:

```bash (conda users)
conda env create -f videoediting_environment.yml
conda activate bsqve
```
or
```bash (pip + venv)
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the GUI:

```bash
python gui.py
```

---

### Option 2: For Windows users

Download the latest standalone `.exe`:

👉 [Download BS Quick Video Editor (Google Drive)](https://drive.google.com/file/d/1AGSYB_mrv-r2hQGeu459t1nMWWECA_ut/view?usp=sharing)

- Just double-click the `.exe`
- Select your video file
- Enter the desired video parameters
  - Trimming timestamps
  - File save location
  - (Optional) Map BeatSaver ID
  - (Optional) Saturation adjustment
- Wait for processing (this step might take several minutes depending on your video length and computer specs)
- Processed video will be saved to your selected folder

> All requirements are already bundled in the `.exe`, no other installations needed!

---

## What's included?

- `gui.py` – simple interface to enter video parameters
- `process_video.py` – core processing logic
- `overlay_creator.py` – generates overlay from BeatSaver data
- `environment.yml` – Conda environment
- `requirements.txt` – Pip + venv environment

---

## Suggestions
The tool is currently just made to suit my needs — I'm very open to suggestions for improvements or additions :D

The fastest way to reach me is on Discord @pan_vr

---

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
