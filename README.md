# Draw2Life

This project implements **Conway’s Game of Life** with a **Tkinter GUI** and adds **hand-gesture interaction** using **OpenCV + MediaPipe**.  
You can **draw live cells** on the grid using a pinch gesture and **clear the grid** using a hold gesture—no physical mouse required.
This is the final project for the Computer algebra class which we tried to push it further by using computer vision had_detection techniques using pretrained piplines from mediapipe.

---

## Features

- Conway’s Game of Life simulation (Tkinter GUI)
- Controls: Start, Pause, Step, Clear, Random
- Hand-tracked pointer (red highlight on the grid)
- Gesture-based drawing (thumb + middle finger pinch)
- Gesture-based clearing (open palm hold)
- Stable drawing logic (anti-flicker + “paint alive” behavior)

---

## Gestures Guide

### 1) Draw Cells (Paint Alive)
**Gesture:** Touch **thumb tip** to **middle finger tip** (pinch)  
**Effect:** While pinched, moving your hand over the grid will **paint cells alive**.

Notes:
- Drawing is active in **Draw mode** (or after you pause if your code switches mode back to Draw).
- The system paints cells alive (it does not toggle), so you will not get instant erase due to gesture flicker.

### 2) Clear the Grid
**Gesture:** Show an **open palm** (all fingers extended) and **hold** it for a short time  
**Effect:** Clears the entire grid.

Notes:
- Clearing is ignored while you are pinching (to avoid accidental clears).

---

## Project Structure

- `game_of_life_gui.py` — Tkinter Game of Life GUI + simulation logic
- `gesture_detection.py` — MediaPipe hand tracking and gesture detection (event mode)
- `app.py` — Integration layer (connects gestures to the Tkinter grid)
- `requirements.txt` — Python dependencies

---

## Installation

### 1) Create and activate a virtual environment (recommended)
Windows:
- `python -m venv venv`
- `venv\Scripts\activate`

macOS / Linux:
- `python3 -m venv venv`
- `source venv/bin/activate`

### 2) Install dependencies
- `pip install -r requirements.txt`

---

## Run

Start the full hand-controlled app:

- `python app.py`

You will typically see:
- A **Tkinter** window for the Game of Life grid
- An **OpenCV preview window** showing hand tracking (press **q** to hide the preview)

---

## How It Works

### Hand Tracking
- OpenCV reads webcam frames
- MediaPipe Hands detects landmarks
- Thumb position is used as a “pointer”
- Thumb–middle distance controls drawing (pinch)
- Open palm hold triggers clear

### Game of Life
- Grid is stored as a NumPy boolean array
- Each generation follows standard Conway rules:
  - Alive cell survives with 2–3 neighbors
  - Dead cell becomes alive with exactly 3 neighbors
- Tkinter Canvas renders the grid in real time

---

## Troubleshooting

- **Camera does not open**: try a different camera index in `app.py` / `virtual_mouse.py` (0, 1, 2).
- **Lag**: reduce camera resolution in `virtual_mouse.py` (e.g., 640×480) and/or disable landmark drawing.
- **Gesture drawing doesn’t work after Start/Pause**: ensure Pause switches back to Draw mode (or restrict drawing to when not running).

---

## More soon

There will be more updates and ideas coming to this project, soon (I hope)!
