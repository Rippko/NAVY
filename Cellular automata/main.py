import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

class ForestFire:
    EMPTY = 0
    TREE = 1
    BURNING = 2
    BURNT = 3
    
    def __init__(self, width=100, height=100, p=0.05, f=0.001, density=0.5, burnout_prob=0.8, use_moore=False):
        self.width = width
        self.height = height
        self.p = p  # pravděpodobnost růstu nového stromu
        self.f = f  # pravděpodobnost spontánního vznícení
        self.density = density  # hustota stromů při inicializaci
        self.burnout_prob = burnout_prob  # pravděpodobnost vyhoření hořícího stromu
        self.use_moore = use_moore  # použití Moorova okolí (8 sousedů)
        self.grid = np.zeros((height, width), dtype=int)
        self.initialize_forest()
        
    def initialize_forest(self, add_initial_fires=False):
        """Inicializuje les s danou hustotou stromů"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        # Efektivnější způsob inicializace s využitím náhodnosti Numpy
        random_values = np.random.random((self.height, self.width))
        self.grid = np.where(random_values < self.density, self.TREE, self.EMPTY)

        if add_initial_fires:
            # Přidání počátečních požárů
            for _ in range(3):
                i, j = np.random.randint(0, self.height), np.random.randint(0, self.width)
                if self.grid[i, j] == self.TREE:
                    self.grid[i, j] = self.BURNING
    
    def update(self):
        """Aktualizuje stav lesa podle pravidel"""
        new_grid = np.copy(self.grid)

        for i in range(self.height):
            for j in range(self.width):
                cell_state = self.grid[i, j]
                
                if cell_state == self.EMPTY or cell_state == self.BURNT:
                    # Pravděpodobnost, že na prázdném místě nebo spáleném místě vyroste nový strom
                    if np.random.random() < self.p:
                        new_grid[i, j] = self.TREE

                elif cell_state == self.TREE:
                    # Buď se strom vznítí od souseda, nebo spontánně
                    if self.has_burning_neighbor(i, j) or np.random.random() < self.f:
                        new_grid[i, j] = self.BURNING

                elif cell_state == self.BURNING:
                    # Hořící strom má určitou pravděpodobnost vyhoření
                    if np.random.random() < self.burnout_prob:
                        new_grid[i, j] = self.BURNT

        self.grid = new_grid
        return self.grid
    
    def has_burning_neighbor(self, i, j):
        """Kontroluje, zda má buňka hořícího souseda"""
        if self.use_moore:
            # Moorovo okolí (8 směrů)
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.height and 0 <= nj < self.width and self.grid[ni, nj] == self.BURNING:
                        return True
        else:
            # Von Neumannovo okolí (4 směry)
            neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for ni, nj in neighbors:
                if 0 <= ni < self.height and 0 <= nj < self.width and self.grid[ni, nj] == self.BURNING:
                    return True
        return False
    
    def get_stats(self):
        """Vrací statistiky o aktuálním stavu lesa"""
        total_cells = self.width * self.height
        tree_count = np.sum(self.grid == self.TREE)
        burning_count = np.sum(self.grid == self.BURNING)
        burnt_count = np.sum(self.grid == self.BURNT)
        
        return {
            "tree": tree_count / total_cells,
            "burning": burning_count / total_cells,
            "burnt": burnt_count / total_cells
        }

    def save_animation(self, gif_filename='forest_fire.gif', frames=200):
        """Uloží animaci simulace jako GIF soubor"""
        colors = ['brown', 'green', 'orange', 'black']
        cmap = mcolors.ListedColormap(colors)
        
        fig, ax = plt.figure(figsize=(8, 8)), plt.axes()
        ax.set_title('Model lesního požáru')
        img = ax.imshow(self.grid, cmap=cmap, vmin=0, vmax=3)

        def animate(frame):
            self.update()
            img.set_array(self.grid)
            return [img]
        
        anim = FuncAnimation(fig, animate, frames=frames, interval=100, blit=True)
        anim.save(gif_filename, writer='pillow')
        print(f"Animace uložena jako {gif_filename}")
        plt.close(fig)


class ForestFireSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulátor lesního požáru")
        self.root.geometry("1000x600")
        
        # Parametry simulace
        self.width = 100
        self.height = 100
        self.density = 0.5
        self.growth_prob = 0.05
        self.ignition_prob = 0.001
        self.burnout_prob = 0.8
        self.update_interval = 100  # ms
        self.use_moore = False
        self.running = False
        
        # Vytvoření simulace
        self.simulator = ForestFire(
            width=self.width, 
            height=self.height, 
            p=self.growth_prob, 
            f=self.ignition_prob, 
            density=self.density,
            burnout_prob=self.burnout_prob,
            use_moore=self.use_moore
        )
        
        self.setup_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """Zastaví simulaci a zavře aplikaci"""
        self.running = False
        self.root.destroy()
        sys.exit(0)
        
    def setup_gui(self):
        # Hlavní rozložení
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Rozdělení na hlavní rámce
        self.control_frame = ttk.Frame(main_frame, padding="10", width=310)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.control_frame.pack_propagate(False)
        
        self.plot_frame = ttk.Frame(main_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Statistiky dole vlevo
        self.stat_frame = ttk.Frame(self.control_frame, padding="5")
        self.stat_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Vytvoření sliderů pro parametry
        self.create_slider("Hustota lesa:", 0.0, 1.0, self.density, self.update_density, format_func=lambda x: f"{x:.2f}")
        self.create_slider("Pravděpodobnost růstu:", 0.0, 0.2, self.growth_prob, self.update_growth_prob, format_func=lambda x: f"{x:.3f}")
        self.create_slider("Pravděpodobnost vznícení:", 0.0, 0.01, self.ignition_prob, self.update_ignition_prob, format_func=lambda x: f"{x:.4f}")
        self.create_slider("Pravděpodobnost vyhoření:", 0.0, 1.0, self.burnout_prob, self.update_burnout_prob, format_func=lambda x: f"{x:.2f}")
        self.create_slider("Rychlost simulace (ms):", 10, 500, self.update_interval, self.update_speed, format_func=lambda x: f"{int(x)}")
        
        # Checkbox pro typ sousedství
        self.moore_var = tk.BooleanVar(value=self.use_moore)
        self.moore_check = ttk.Checkbutton(
            self.control_frame,
            text="Moorovo okolí (8 sousedů)",
            variable=self.moore_var,
            command=self.toggle_moore
        )
        self.moore_check.pack(anchor=tk.W, pady=10)
        
        # Tlačítka
        self.button_frame = ttk.Frame(self.control_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.toggle_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(self.button_frame, text="Uložit GIF", command=self.save_gif)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Statistiky
        self.stats_var = tk.StringVar(value="Stromy: 0%, Hořící: 0%, Spálené: 0%")
        ttk.Label(self.stat_frame, text="Statistiky:").pack(anchor=tk.W)
        self.stats_label = ttk.Label(
            self.stat_frame, 
            textvariable=self.stats_var,
            font=("Arial", 10)
        )
        self.stats_label.pack(anchor=tk.W, pady=5)
        
        # Nastavení grafu
        self.setup_plot()
        self.update_stats()
    
    def create_slider(self, label_text, min_val, max_val, default_val, callback, format_func=None):
        """Pomocná metoda pro vytvoření slideru s popiskem a hodnotou"""
        slider_frame = ttk.Frame(self.control_frame)
        slider_frame.pack(fill=tk.X, pady=5)
        ttk.Label(slider_frame, text=label_text).pack(anchor=tk.W)
        
        slider_value_frame = ttk.Frame(slider_frame)
        slider_value_frame.pack(fill=tk.X)
        
        slider = ttk.Scale(
            slider_value_frame, 
            from_=min_val, 
            to=max_val, 
            value=default_val
        )
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        value_label = ttk.Label(slider_value_frame, text=format_func(default_val) if format_func else str(default_val))
        value_label.pack(side=tk.RIGHT, padx=5)
        
        # Uložení referencí pro pozdější použití v callbacku
        slider.value_label = value_label
        slider.format_func = format_func or (lambda x: str(x))
        slider.configure(command=lambda val: self.slider_callback(slider, val, callback))
        return slider
    
    def slider_callback(self, slider, value, callback):
        """Obecný callback pro slidery"""
        value = float(value)
        slider.value_label.config(text=slider.format_func(value))
        callback(value)
        
    def setup_plot(self):
        """Nastaví graf pro zobrazení simulace"""
        self.fig = plt.Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Model lesního požáru")
        
        colors = ['brown', 'green', 'orange', 'black']  # prázdno, strom, hoří, spálený
        self.cmap = mcolors.ListedColormap(colors)
        
        self.img = self.ax.imshow(self.simulator.grid, cmap=self.cmap, vmin=0, vmax=3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def update_density(self, value):
        """Aktualizuje hustotu lesa"""
        self.density = value
        
    def update_growth_prob(self, value):
        """Aktualizuje pravděpodobnost růstu nových stromů"""
        self.growth_prob = value
        self.simulator.p = value
        
    def update_ignition_prob(self, value):
        """Aktualizuje pravděpodobnost spontánního vznícení"""
        self.ignition_prob = value
        self.simulator.f = value
        
    def update_burnout_prob(self, value):
        """Aktualizuje pravděpodobnost vyhoření hořícího stromu"""
        self.burnout_prob = value
        self.simulator.burnout_prob = value
        
    def update_speed(self, value):
        """Aktualizuje rychlost simulace"""
        self.update_interval = int(value)
        
    def toggle_moore(self):
        """Přepíná mezi Von Neumannovým a Moorovým okolím"""
        self.use_moore = self.moore_var.get()
        self.simulator.use_moore = self.use_moore
        
    def update_simulation(self):
        """Aktualizuje simulaci a zobrazení"""
        if self.running:
            self.simulator.update()
            self.img.set_array(self.simulator.grid)
            self.canvas.draw()
            self.update_stats()
            self.root.after(self.update_interval, self.update_simulation)
            
    def update_stats(self):
        """Aktualizuje statistiky o lese"""
        stats = self.simulator.get_stats()
        self.stats_var.set(
            f"Stromy: {stats['tree']:.1%}, "
            f"Hořící: {stats['burning']:.1%}, "
            f"Spálené: {stats['burnt']:.1%}"
        )
            
    def toggle_simulation(self):
        """Spouští nebo zastavuje simulaci"""
        self.running = not self.running
        if self.running:
            self.start_button.config(text="Stop")
            self.update_simulation()
        else:
            self.start_button.config(text="Start")
            
    def reset_simulation(self):
        """Resetuje simulaci s aktuálními parametry"""
        self.simulator = ForestFire(
            width=self.width, 
            height=self.height, 
            p=self.growth_prob, 
            f=self.ignition_prob, 
            density=self.density,
            burnout_prob=self.burnout_prob,
            use_moore=self.use_moore
        )
        self.simulator.initialize_forest()
        self.img.set_array(self.simulator.grid)
        self.canvas.draw()
        self.update_stats()
        
    def save_gif(self):
        """Uloží animaci jako GIF soubor"""
        was_running = self.running
        if was_running:
            self.toggle_simulation()
            
        temp_simulator = ForestFire(
            width=self.width,
            height=self.height,
            p=self.growth_prob,
            f=self.ignition_prob,
            density=self.density,
            burnout_prob=self.burnout_prob,
            use_moore=self.use_moore
        )
        temp_simulator.initialize_forest(add_initial_fires=True)
        temp_simulator.save_animation(gif_filename="screens/forest_fire_simulation.gif")
        
        if was_running:
            self.toggle_simulation()


def main():
    root = tk.Tk()
    app = ForestFireSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()