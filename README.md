# Draw2Life

This project extends the classic Conway’s Game of Life by introducing a gesture-based control system using webcam hand tracking. Instead of manipulating the grid with a mouse, users interact with the Game of Life through real-time hand movements detected by MediaPipe. This merges cellular automata, computer vision, and graphical user interface programming into a single interactive system.

## Overview

Conway’s Game of Life is a two-dimensional cellular automaton where simple rules create complex emergent behaviors. Our implementation provides a Tkinter-based GUI for visualization and simulation control. In addition, we built a virtual mouse using MediaPipe and OpenCV that maps hand positions to cursor movement and uses gesture-based clicks. The long-term goal is to integrate both systems so users can draw cell patterns and interact with the simulation using only hand gestures.

## Features

- Tkinter GUI for Conway’s Game of Life  
- Real-time simulation with Start, Pause, Step, Clear, and Random controls  
- Clickable grid for toggling cell states  
- Webcam-based hand tracking using MediaPipe  
- Virtual mouse controlled entirely by hand gestures  
- Gesture-based clicking (thumb–pinky for left-click)  
- Smooth cursor movement using interpolation  
- Planned integration: draw Game of Life patterns using hand gestures instead of the physical mouse

## Project Structure

- **virtual_mouse.py** – Webcam hand tracking and virtual mouse controller  
- **game_of_life_gui.py** – Tkinter-based Game of Life implementation  
- **README.md** – Project documentation  

## Tech Stack

- Python 3.x  
- OpenCV – Webcam capture and image processing  
- MediaPipe – Real-time hand landmark detection  
- PyAutoGUI – Cursor movement  
- pynput – Mouse press/release actions  
- NumPy – Grid operations for Game of Life  
- Tkinter – GUI rendering of the automaton

## Installation

1. Clone the repository.  
2. (Recommended) create a virtual environment.  
3. Install dependencies: OpenCV, MediaPipe, PyAutoGUI, pynput, NumPy.  
4. Make sure your system has:  
   - A working webcam  
   - Python GUI support (for Tkinter)  
   - OS permissions for camera access  

## Usage

### 1. Virtual Mouse (Hand Tracking)

Run `virtual_mouse.py` to enable hand-controlled cursor movement.  

Gestures:  
- Thumb–index close → activate movement  
- Thumb–pinky close → left-click press  
- Thumb–pinky separate → release click  

Movement is mapped to screen coordinates and smoothed to reduce jitter. Press `q` in the OpenCV window to exit.

### 2. Game of Life GUI

Run `game_of_life_gui.py` to open the cellular automaton.  

Controls:  
- **Start** – Begin continuous simulation  
- **Pause** – Stop simulation  
- **Step** – Advance one generation  
- **Clear** – Reset the grid  
- **Random** – Fill randomly with live cells  
- **Click any cell** to toggle alive/dead  

### 3. (Planned) Fully Integrated Gesture-Controlled Game of Life

The goal is to combine both modules so that:  
- The virtual mouse no longer controls the OS cursor  
- Instead, hand coordinates directly control the Tkinter grid  
- Gesture-based clicks toggle cell states  
- Users can “draw” initial patterns with their hands  
- Additional gestures may control Start/Pause/Clear modes  

This will transform the Game of Life into an interactive, gesture-driven simulator.

## How It Works

### Hand Tracking System

1. OpenCV captures webcam frames  
2. Frames are mirrored and passed into MediaPipe  
3. MediaPipe extracts 21 hand landmarks  
4. Distances between finger tips determine gestures  
5. Thumb position is mapped to screen coordinates  
6. Cursor movement is smoothed for stability  
7. pynput and PyAutoGUI produce click and movement events  

### Game of Life Engine

1. A 2D NumPy grid stores alive/dead states  
2. For each cell, neighbors are counted with boundary checks  
3. Conway’s rules determine the next generation  
4. Grid is redrawn on a Tkinter Canvas using rectangles  
5. Tkinter’s `after()` method animates simulation smoothly  

## Roadmap

- Full integration of hand tracking + Game of Life  
- Gesture-based grid editing  
- Gesture-based mode switching (start, pause, clear)  
- Overlay of the Game of Life grid directly on webcam feed (optional)  
- Multi-hand support or pinch-to-zoom (optional)

## Known Limitations

- Hand tracking depends on lighting and camera quality  
- Gesture thresholds may require tuning  
- Virtual mouse uses OS-level cursor (until integration is complete)  
- Tkinter rendering speed may limit extremely large grids  


