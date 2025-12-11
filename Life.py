import tkinter as tk
import numpy as np
import random

GRID_ROWS = 30
GRID_COLS = 50
CELL_SIZE = 20
UPDATE_DELAY = 100


class GameOfLifeGUI:
    def __init__(self, rows=GRID_ROWS, cols=GRID_COLS, cell_size=CELL_SIZE, delay=UPDATE_DELAY):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.delay = delay

        self.grid = np.full((self.rows, self.cols), False, dtype=bool)
        self.running = False
        self.after_id = None

        self.root = tk.Tk()
        self.root.title("Conway's Game of Life")

        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size

        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=5)

        # Buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.grid(row=1, column=0, sticky="ew")

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause)
        self.pause_button.grid(row=1, column=1, sticky="ew")

        self.step_button = tk.Button(self.root, text="Step", command=self.step_once)
        self.step_button.grid(row=1, column=2, sticky="ew")

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid)
        self.clear_button.grid(row=1, column=3, sticky="ew")

        self.random_button = tk.Button(self.root, text="Random", command=self.random_grid)
        self.random_button.grid(row=1, column=4, sticky="ew")

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.draw_grid()

    def count_neighbors(self, r, c):
        """Count alive neighbors of cell (r, c) with non-wrapping borders."""
        count = 0
        for rr in range(max(0, r - 1), min(self.rows - 1, r + 1) + 1):
            for cc in range(max(0, c - 1), min(self.cols - 1, c + 1) + 1):
                if rr == r and cc == c:
                    continue
                if self.grid[rr, cc]:
                    count += 1
        return count

    def next_generation(self):
        """Compute the next generation of the grid according to Game of Life rules."""
        new_grid = np.full((self.rows, self.cols), False, dtype=bool)
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(r, c)
                if self.grid[r, c]:
                    # Alive cell
                    if neighbors == 2 or neighbors == 3:
                        new_grid[r, c] = True
                    else:
                        new_grid[r, c] = False
                else:
                    # Dead cell
                    if neighbors == 3:
                        new_grid[r, c] = True
                    else:
                        new_grid[r, c] = False
        self.grid = new_grid

    def draw_grid(self):
        """Redraw the entire grid on the canvas."""
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.grid[r, c]:
                    fill = "black"
                else:
                    fill = "white"

                # Draw cell rectangle
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill,
                    outline="gray"
                )

    def on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row, col] = not self.grid[row, col]
            self.draw_grid()

    def start(self):
        """Start automatic simulation."""
        if not self.running:
            self.running = True
            self.run_simulation()

    def pause(self):
        """Pause automatic simulation."""
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def step_once(self):
        """Perform a single simulation step."""
        self.pause()  # make sure it's paused
        self.next_generation()
        self.draw_grid()

    def clear_grid(self):
        """Set all cells to dead."""
        self.pause()
        self.grid[:] = False
        self.draw_grid()

    def random_grid(self, density=0.2):
        """Fill grid with random live cells."""
        self.pause()
        self.grid = np.random.rand(self.rows, self.cols) < density
        self.draw_grid()

    def run_simulation(self):
        """Looped callback for automatic simulation."""
        if self.running:
            self.next_generation()
            self.draw_grid()
            self.after_id = self.root.after(self.delay, self.run_simulation)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GameOfLifeGUI()
    app.run()
