import tkinter as tk
import random

class GameOfLife:
    def __init__(self, root, rows=50, cols=50, cell_size=12):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.running = False
        self.delay = 100  # Milliseconds between generations

        # State: 1 for alive, 0 for dead
        self.grid = [[random.choice([0, 0, 0, 1]) for _ in range(cols)] for _ in range(rows)]
        
        self.setup_gui()
        self.render_all()

    def setup_gui(self):
        """Initialize the GUI components."""
        self.canvas = tk.Canvas(
            self.root, 
            width=self.cols * self.cell_size, 
            height=self.rows * self.cell_size, 
            bg='#1e1e1e',
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        # Create rectangle items for each cell once
        self.rects = []
        for r in range(self.rows):
            row_rects = []
            for c in range(self.cols):
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                rect = self.canvas.create_rectangle(
                    x0, y0, x1, y1, 
                    fill='#1e1e1e', 
                    outline='#333333'
                )
                row_rects.append(rect)
            self.rects.append(row_rects)

        # Controls
        self.controls = tk.Frame(self.root, bg='#2d2d2d')
        self.controls.pack(fill=tk.X, side=tk.BOTTOM)

        btn_style = {'padx': 10, 'pady': 5, 'bg': '#444444', 'fg': 'white', 'relief': tk.FLAT}

        self.start_btn = tk.Button(self.controls, text="▶ Start", command=self.start, **btn_style)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_btn = tk.Button(self.controls, text="⏸ Stop", command=self.stop, **btn_style)
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.reset_btn = tk.Button(self.controls, text="↻ Reset", command=self.reset, **btn_style)
        self.reset_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_btn = tk.Button(self.controls, text="⌧ Clear", command=self.clear_grid, **btn_style)
        self.clear_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_label = tk.Label(self.controls, text="Stopped", bg='#2d2d2d', fg='#aaaaaa')
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Bindings for interaction
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_paint)

    def handle_click(self, event):
        """Toggle cell state on click."""
        self._apply_mouse_action(event, toggle=True)

    def handle_paint(self, event):
        """Set cell to alive on drag."""
        self._apply_mouse_action(event, toggle=False, state=1)

    def _apply_mouse_action(self, event, toggle=False, state=1):
        """Update a cell based on mouse coordinates."""
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if toggle:
                self.grid[r][c] = 1 - self.grid[r][c]
            else:
                self.grid[r][c] = state
            self.render_cell(r, c)

    def render_cell(self, r, c):
        """Update the visual state of a single cell."""
        color = '#4caf50' if self.grid[r][c] == 1 else '#1e1e1e'
        self.canvas.itemconfig(self.rects[r][c], fill=color)

    def render_all(self):
        """Update the visual state of all cells."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.render_cell(r, c)

    def get_neighbors(self, r, c):
        """Count live neighbors with wrap-around boundaries."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = (r + dr) % self.rows, (c + dc) % self.cols
                count += self.grid[nr][nc]
        return count

    def update_logic(self):
        """Apply Conway's rules to calculate the next generation."""
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        changes = []
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.get_neighbors(r, c)
                if self.grid[r][c] == 1:
                    if neighbors in [2, 3]:
                        new_grid[r][c] = 1
                else:
                    if neighbors == 3:
                        new_grid[r][c] = 1
                
                if new_grid[r][c] != self.grid[r][c]:
                    changes.append((r, c))
        
        self.grid = new_grid
        return changes

    def tick(self):
        """Main animation loop step."""
        if self.running:
            changes = self.update_logic()
            for r, c in changes:
                self.render_cell(r, c)
            self.root.after(self.delay, self.tick)

    def start(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Running", fg='#4caf50')
            self.tick()

    def stop(self):
        self.running = False
        self.status_label.config(text="Stopped", fg='#aaaaaa')

    def reset(self):
        self.stop()
        self.grid = [[random.choice([0, 0, 0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
        self.render_all()

    def clear_grid(self):
        """Set all cells to dead."""
        self.stop()
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.render_all()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life")
    root.configure(bg='#2d2d2d')
    game = GameOfLife(root)
    root.mainloop()
