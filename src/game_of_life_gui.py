import tkinter as tk
import numpy as np

class GameOfLifeGUI:
    def __init__(self, rows=30, cols=50, cell_size=20, delay=100):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.delay = delay

        self.grid = np.zeros((self.rows, self.cols), dtype=bool)

        self.running = False
        self.after_id = None

        self.hand_cursor_rect = None

        self.root = tk.Tk()
        self.root.title("Conway's Game of Life (Tkinter)")

        canvas_w = self.cols * self.cell_size
        canvas_h = self.rows * self.cell_size

        self.canvas = tk.Canvas(self.root, width=canvas_w, height=canvas_h, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=6)

        tk.Button(self.root, text="Start", command=self.start).grid(row=1, column=0, sticky="ew")
        tk.Button(self.root, text="Pause", command=self.pause).grid(row=1, column=1, sticky="ew")
        tk.Button(self.root, text="Step", command=self.step_once).grid(row=1, column=2, sticky="ew")
        tk.Button(self.root, text="Clear", command=self.clear_grid).grid(row=1, column=3, sticky="ew")
        tk.Button(self.root, text="Random", command=self.random_grid).grid(row=1, column=4, sticky="ew")

        self.mode_var = tk.StringVar(value="Draw")
        tk.OptionMenu(self.root, self.mode_var, "Draw", "Simulate").grid(row=1, column=5, sticky="ew")

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_grid()

    def count_neighbors(self, r, c):
        count = 0
        for rr in range(max(0, r - 1), min(self.rows - 1, r + 1) + 1):
            for cc in range(max(0, c - 1), min(self.cols - 1, c + 1) + 1):
                if rr == r and cc == c:
                    continue
                if self.grid[rr, cc]:
                    count += 1
        return count

    def next_generation(self):
        new_grid = np.zeros((self.rows, self.cols), dtype=bool)
        for r in range(self.rows):
            for c in range(self.cols):
                n = self.count_neighbors(r, c)
                if self.grid[r, c]:
                    new_grid[r, c] = (n == 2 or n == 3)
                else:
                    new_grid[r, c] = (n == 3)
        self.grid = new_grid

    def draw_grid(self):
        self.canvas.delete("cell")
        for r in range(self.rows):
            y1 = r * self.cell_size
            y2 = y1 + self.cell_size
            for c in range(self.cols):
                x1 = c * self.cell_size
                x2 = x1 + self.cell_size
                fill = "black" if self.grid[r, c] else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray", tags="cell")

    def highlight_cell(self, row: int, col: int):
        """Draw or move a rectangle showing the current hand 'cursor' cell."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            if self.hand_cursor_rect is not None:
                self.canvas.delete(self.hand_cursor_rect)
                self.hand_cursor_rect = None
            return

        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        if self.hand_cursor_rect is None:
            self.hand_cursor_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="red",
                width=2
            )
        else:
            self.canvas.coords(self.hand_cursor_rect, x1, y1, x2, y2)

    def toggle_cell(self, row: int, col: int):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row, col] = ~self.grid[row, col]

    def set_cell(self, row: int, col: int, alive: bool):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row, col] = alive

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        self.toggle_cell(row, col)
        self.draw_grid()

    def start(self):
        self.running = True
        self.mode_var.set("Simulate")
        self._loop()

    def pause(self):
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.mode_var.set("Draw")

    def step_once(self):
        self.pause()
        self.next_generation()
        self.draw_grid()

    def clear_grid(self):
        self.pause()
        self.grid[:, :] = False
        self.draw_grid()

    def random_grid(self, density=0.2):
        self.pause()
        self.grid = (np.random.rand(self.rows, self.cols) < density)
        self.draw_grid()

    def _loop(self):
        if self.running:
            self.next_generation()
            self.draw_grid()
            self.after_id = self.root.after(self.delay, self._loop)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GameOfLifeGUI(rows=30, cols=50, cell_size=20, delay=100)
    app.run()
