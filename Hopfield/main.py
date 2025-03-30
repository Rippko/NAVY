import numpy as np
import tkinter as tk
from tkinter import messagebox
import math

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        """ Trénuje síť na všech vzorech současně """
        self.weights.fill(0)
        for pattern in patterns:
            pattern = pattern.reshape(-1, 1)
            self.weights += pattern @ pattern.T
        np.fill_diagonal(self.weights, 0)

    def recover(self, pattern, method="synchronous", max_iter=1000):
        """ Obnovuje vstupní vzor na základě všech naučených vzorů s kontrolou energie """
        pattern = pattern.copy()
        previous_pattern = None

        for current_iter in range(max_iter):
            if method == "synchronous":
                pattern = np.sign(self.weights @ pattern)
            else:
                for i in range(self.size):
                    pattern[i] = np.sign(np.dot(self.weights[:, i], pattern))

            if previous_pattern is not None and np.array_equal(pattern, previous_pattern):
                break

            previous_pattern = pattern.copy()
        print(f"Iterations: {current_iter + 1}")
        return pattern

def draw_grid(canvas, grid):
    """ Vykresluje 5x5 mřížku v Tkinteru """
    canvas.delete("all")
    cell_size = 40
    for y in range(5):
        for x in range(5):
            color = "black" if grid[y, x] == 1 else "white"
            canvas.create_rectangle(
                x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size,
                fill=color, outline="gray"
            )

def on_click(event, grid, canvas):
    """ Přepíná černou/bílou barvu na mřížce po kliknutí """
    cell_size = 40
    x, y = event.x // cell_size, event.y // cell_size
    if 0 <= x < 5 and 0 <= y < 5:
        grid[y, x] = 1 - grid[y, x]
        draw_grid(canvas, grid)

def save_pattern(patterns, grid, network, canvas, root):
    """ Ukládá nový vzor do trénovací sady a trénuje síť """
    max_patterns = np.floor(network.size / (2 * math.log2(network.size)))
    
    if not grid.any():
        messagebox.showwarning("Blank Pattern", "Cannot save a blank pattern.")
        return

    pattern = grid.copy().flatten()
    pattern[pattern == 0] = -1
    patterns.append(pattern)
    network.train(patterns)
    grid.fill(0)
    draw_grid(canvas, grid)

    if len(patterns) > max_patterns:
        warning_label = tk.Label(root, text=f"Warning: Exceeding {int(max_patterns)} patterns may cause instability!",
                                 font=("Arial", 10, "bold"), fg="red")
        warning_label.pack(pady=5)
        root.after(2000, warning_label.destroy)

def restore_pattern(network, grid, canvas, method="synchronous"):
    """ Obnovuje aktuální vstupní vzor podle naučených vzorů """
    if len(patterns) == 0:
        messagebox.showwarning("No Patterns", "No saved patterns to restore.")
        return

    if not grid.any():
        messagebox.showwarning("Blank Grid", "The input grid is blank. Please draw a pattern before restoring.")
        return

    pattern = grid.copy().flatten()
    pattern[pattern == 0] = -1

    restored = network.recover(pattern, method=method)
    restored[restored == -1] = 0
    grid[:, :] = restored.reshape(5, 5)  # Changed to 5x5

    draw_grid(canvas, grid)

def remove_pattern(patterns, grid, network, canvas):
    """ Odstraňuje vzor z trénovací sady, pokud existuje """
    if len(patterns) == 0:
        messagebox.showwarning("No Patterns", "No saved patterns to remove.")
        return

    pattern = grid.copy().flatten()
    pattern[pattern == 0] = -1  # Hopfield network používá hodnoty -1 a 1

    # Find the matching pattern
    for saved_pattern in patterns:
        if np.array_equal(pattern, saved_pattern):
            patterns.remove(saved_pattern)
            network.train(patterns)
            grid.fill(0)
            draw_grid(canvas, grid)
            
            messagebox.showinfo("Pattern Removed", "The pattern has been removed successfully.")
            return

    messagebox.showwarning("Pattern Not Found", "The pattern is not in the saved patterns.")
    
def flush_patterns(patterns, network, canvas, grid):
    """ Clears all saved patterns and resets the network """
    if len(patterns) == 0:
        messagebox.showinfo("No Patterns", "There are no saved patterns to flush.")
        return

    patterns.clear()
    network.train(patterns)
    grid.fill(0)
    draw_grid(canvas, grid)

    messagebox.showinfo("Patterns Flushed", "All saved patterns have been cleared.")

def add_noise(grid, canvas, noise_level=0.1):
    """ Přidává šum do aktuální mřížky a aktualizuje zobrazení """
    noisy_grid = grid.copy()
    num_flips = int(noise_level * grid.size)
    indices = np.random.choice(grid.size, num_flips, replace=False)
    for idx in indices:
        noisy_grid.flat[idx] = 1 - noisy_grid.flat[idx]
    grid[:, :] = noisy_grid
    draw_grid(canvas, grid)

def show_saved_patterns(patterns, network, root):
    """ Zobrazuje uložené vzory v novém okně """
    if len(patterns) == 0:
        messagebox.showinfo("No Patterns", "There are no saved patterns to display.")
        return

    # Create a new window with adjusted size
    patterns_window = tk.Toplevel(root)
    patterns_window.title("Saved Patterns")
    patterns_window.geometry("1000x700")
    patterns_window.resizable(False, False)

    def display_pattern_details():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a pattern to view.")
            return
            
        idx = selected[0]
        pattern = patterns[idx]
        
        # Update canvas with pattern
        pattern_matrix = pattern.reshape(5, 5)
        matrix_without_zeros = np.where(pattern_matrix == -1, 1, pattern_matrix)
        
        # Calculate weight matrix for single pattern
        pattern_vector = pattern.reshape(-1, 1)
        single_pattern_weights = pattern_vector @ pattern_vector.T
        np.fill_diagonal(single_pattern_weights, 0)
        
        # Format matrices for better display
        pattern_matrix_str = np.array2string(pattern_matrix, prefix=' ', separator=',', precision=1)
        matrix_without_zeros_str = np.array2string(matrix_without_zeros, prefix=' ', separator=',', precision=1)
        pattern_vector_str = np.array2string(pattern, prefix=' ', separator=',', precision=1)
        weights_str = np.array2string(single_pattern_weights, prefix=' ', separator=',', precision=1)
        
        # Draw pattern on canvas
        pattern_canvas.delete("all")
        cell_size = 40
        for y in range(5):
            for x in range(5):
                color = "black" if pattern_matrix[y, x] == 1 else "white"
                pattern_canvas.create_rectangle(
                    x * cell_size, y * cell_size, 
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color, outline="gray"
                )
        
        # Updating text widget with details
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, f"Pattern {idx + 1} Details:\n\n")
        details_text.insert(tk.END, f"Pattern Matrix (5x5):\n{pattern_matrix_str}\n\n")
        details_text.insert(tk.END, f"Matrix Without Zeros:\n{matrix_without_zeros_str}\n\n")
        details_text.insert(tk.END, f"Pattern Vector (25x1):\n{pattern_vector_str}\n\n")
        details_text.insert(tk.END, f"Weight Matrix (25x25) for This Pattern:\n{weights_str}")
        details_text.config(state=tk.DISABLED)

    def forget_pattern():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a pattern to forget.")
            return
            
        idx = selected[0]
        patterns.pop(idx)
        network.train(patterns)
        
        listbox.delete(0, tk.END)
        for i in range(len(patterns)):
            listbox.insert(tk.END, f"Pattern {i + 1}")
            
        pattern_canvas.delete("all")
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.config(state=tk.DISABLED)
        
        if len(patterns) == 0:
            patterns_window.destroy()
            messagebox.showinfo("No Patterns", "All patterns have been forgotten.")

    # UI elements
    left_frame = tk.Frame(patterns_window, width=300)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20)
    left_frame.pack_propagate(False)
    
    right_frame = tk.Frame(patterns_window)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    listbox_label = tk.Label(left_frame, text="Saved Patterns", font=("Arial", 12, "bold"))
    listbox_label.pack(pady=5)
    
    listbox_frame = tk.Frame(left_frame)
    listbox_frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(listbox_frame, width=30, height=20, yscrollcommand=scrollbar.set,font=("Arial", 10))
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    
    listbox.bind('<<ListboxSelect>>', lambda e: display_pattern_details())

    preview_frame = tk.Frame(right_frame)
    preview_frame.pack(fill=tk.X)
    
    canvas_label = tk.Label(preview_frame, text="Pattern Preview", font=("Arial", 12, "bold"))
    canvas_label.pack(pady=5)
    
    pattern_canvas = tk.Canvas(preview_frame, width=200, height=200, bg="white", highlightthickness=1, highlightbackground="black")
    pattern_canvas.pack(pady=10)

    details_label = tk.Label(right_frame, text="Pattern Details", font=("Arial", 12, "bold"))
    details_label.pack(pady=5)
    
    details_frame = tk.Frame(right_frame)
    details_frame.pack(fill=tk.BOTH, expand=True)
    
    details_scroll = tk.Scrollbar(details_frame)
    details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    details_text = tk.Text(details_frame, height=15, width=50,
                          yscrollcommand=details_scroll.set,
                          font=("Courier", 10))  # Monospace font for better matrix display
    details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    details_scroll.config(command=details_text.yview)
    details_text.config(state=tk.DISABLED)

    button_frame = tk.Frame(right_frame)
    button_frame.pack(pady=15, fill=tk.X)
    
    button_style = {"font": ("Arial", 10), "width": 15, 
                   "bg": "#f0f0f0", "relief": "raised"}
    
    tk.Button(button_frame, text="Forget Pattern", 
              command=forget_pattern,
              **button_style).pack(side=tk.LEFT, padx=10)

    for i in range(len(patterns)):
        listbox.insert(tk.END, f"Pattern {i + 1}")

def main():
    root = tk.Tk()
    root.title("Hopfield Network")
    root.geometry("500x400")
    root.resizable(False, False)

    # Main container frames
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)
    
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)

    # Title
    title_label = tk.Label(left_frame, text="Hopfield Network", font=("Arial", 16, "bold"), fg="blue")
    title_label.pack(pady=(0, 10))

    # Grid canvas section
    canvas_frame = tk.Frame(left_frame)
    canvas_frame.pack(pady=10)

    canvas_label = tk.Label(canvas_frame, text="Pattern Grid", font=("Arial", 12, "bold"))
    canvas_label.pack()

    grid = np.zeros((5, 5), dtype=int)
    network = HopfieldNetwork(size=25)
    global patterns
    patterns = []

    canvas = tk.Canvas(canvas_frame, width=200, height=200, bg="white", highlightthickness=1, highlightbackground="black")
    canvas.pack(pady=5)
    canvas.bind("<Button-1>", lambda event: on_click(event, grid, canvas))
    draw_grid(canvas, grid)

    # Buttons section with grouping
    button_frame = tk.Frame(right_frame)
    button_frame.pack(fill=tk.BOTH, expand=True)

    # Button groups
    pattern_ops_frame = tk.LabelFrame(button_frame, text="Pattern Operations", font=("Arial", 10, "bold"))
    pattern_ops_frame.pack(fill=tk.X, pady=5)

    restore_frame = tk.LabelFrame(button_frame, text="Restore Operations", font=("Arial", 10, "bold"))
    restore_frame.pack(fill=tk.X, pady=5)

    utility_frame = tk.LabelFrame(button_frame, text="Utilities", font=("Arial", 10, "bold"))
    utility_frame.pack(fill=tk.X, pady=5)

    # Button style
    button_style = {
        "font": ("Arial", 10),
        "width": 20,
        "bg": "#f0f0f0",
        "relief": "raised"
    }

    # Pattern operation buttons
    tk.Button(pattern_ops_frame, text="Save Pattern",command=lambda: save_pattern(patterns, grid, network, canvas, root),**button_style).pack(pady=3)
    tk.Button(pattern_ops_frame, text="Show Saved Patterns",command=lambda: show_saved_patterns(patterns, network, root),**button_style).pack(pady=3)

    # Restore operation buttons
    tk.Button(restore_frame, text="Restore (Synchronous)",command=lambda: restore_pattern(network, grid, canvas, "synchronous"),**button_style).pack(pady=3)
    tk.Button(restore_frame, text="Restore (Asynchronous)",command=lambda: restore_pattern(network, grid, canvas, "asynchronous"),**button_style).pack(pady=3)

    # Utility buttons
    tk.Button(utility_frame, text="Add Noise",command=lambda: add_noise(grid, canvas, noise_level=0.1),**button_style).pack(pady=3)
    tk.Button(utility_frame, text="Flush Patterns",command=lambda: flush_patterns(patterns, network, canvas, grid),**button_style).pack(pady=3)
    root.mainloop()

if __name__ == "__main__":
    main()