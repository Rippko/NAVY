import tkinter as tk
from tkinter import ttk
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

class FractalTerrainGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generátor fraktálního terénu")
        self.root.geometry("800x600")

        self.dimension_var = tk.StringVar(value="2D")
        self.iterations_var = tk.IntVar(value=5)
        self.roughness_var = tk.DoubleVar(value=0.6)
        self.create_widgets()
        
    def create_widgets(self):
        settings_frame = ttk.LabelFrame(self.root, text="Nastavení")
        settings_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(settings_frame, text="Dimenze:").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(settings_frame, text="2D", variable=self.dimension_var, value="2D").pack(anchor=tk.W)
        ttk.Radiobutton(settings_frame, text="3D", variable=self.dimension_var, value="3D").pack(anchor=tk.W)
        
        ttk.Label(settings_frame, text="Počet iterací:").pack(anchor=tk.W, pady=5)
        ttk.Scale(settings_frame, from_=3, to=10, variable=self.iterations_var, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        ttk.Label(settings_frame, text="Drsnost terénu:").pack(anchor=tk.W, pady=5)
        ttk.Scale(settings_frame, from_=0.1, to=1, variable=self.roughness_var, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        ttk.Button(settings_frame, text="Generovat terén", command=self.generate_terrain).pack(pady=20)

        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig = plt.Figure(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def generate_2d_terrain(self, iterations, roughness):
        # Začátek s přímkou (x = 0 až 1, y = 0.5)
        points = [(0, 0.5), (1, 0.5)]

        for i in range(iterations):
            new_points = []
            scale = roughness ** i

            for j in range(len(points) - 1):
                new_points.append(points[j])
                mid_x = (points[j][0] + points[j+1][0]) / 2
                mid_y = (points[j][1] + points[j+1][1]) / 2
                displacement = random.uniform(-scale, scale)
                new_mid_y = mid_y + displacement
                new_points.append((mid_x, new_mid_y))

            new_points.append(points[-1])
            points = new_points

        x_values = [p[0] for p in points]
        y_values = [p[1] for p in points]
        
        return x_values, y_values
    
    def generate_3d_terrain(self, iterations, roughness):
        size = 2 ** iterations + 1
        terrain = np.zeros((size, size))
        terrain[0, 0] = 0
        terrain[0, size-1] = 0
        terrain[size-1, 0] = 0
        terrain[size-1, size-1] = 0

        step = size - 1
        while step > 1:
            half_step = step // 2

            for x in range(0, size-1, step):
                for y in range(0, size-1, step):
                    avg = (terrain[x, y] + terrain[x+step, y] + 
                           terrain[x, y+step] + terrain[x+step, y+step]) / 4
                    
                    displacement = random.uniform(-roughness, roughness)
                    terrain[x+half_step, y+half_step] = avg + displacement
            
            for x in range(0, size-1, half_step):
                for y in range(0, size-1, half_step):
                    if (x % step == 0 and y % step == 0) or (x % step == half_step and y % step == half_step):
                        continue

                    count = 0
                    avg = 0
                    
                    if x >= half_step:
                        avg += terrain[x-half_step, y]
                        count += 1
                    
                    if x + half_step < size:
                        avg += terrain[x+half_step, y]
                        count += 1
                    
                    if y >= half_step:
                        avg += terrain[x, y-half_step]
                        count += 1
                    
                    if y + half_step < size:
                        avg += terrain[x, y+half_step]
                        count += 1
                    
                    avg /= count
                    
                    displacement = random.uniform(-roughness, roughness)
                    terrain[x, y] = avg + displacement
            
            step = half_step
            roughness *= 0.5
        
        return terrain
    
    def generate_terrain(self):
        dimension = self.dimension_var.get()
        iterations = self.iterations_var.get()
        roughness = self.roughness_var.get()
        self.fig.clear()

        if dimension == "2D":
            colors = ['darkgreen', 'black', 'saddlebrown']
            height_positions = [0.7, 0.4, 0.2]
            ax = self.fig.add_subplot(111)
            size = 2**iterations + 1
            x_values = np.linspace(0, 1, size)
            all_terrains = []
            
            for i in range(3):
                y_values = []
                current_points = [(0, 0.5), (1, 0.5)]
                
                for iter in range(iterations):
                    new_points = []
                    scale = roughness ** iter

                    for j in range(len(current_points) - 1):
                        new_points.append(current_points[j])
                        mid_x = (current_points[j][0] + current_points[j+1][0]) / 2
                        mid_y = (current_points[j][1] + current_points[j+1][1]) / 2
                        displacement = random.uniform(-scale, scale)
                        new_mid_y = mid_y + displacement
                        new_points.append((mid_x, new_mid_y))

                    new_points.append(current_points[-1])
                    current_points = new_points

                y_values = [p[1] * 0.25 + height_positions[i] for p in current_points]
                all_terrains.append(y_values)

            for i in range(2, -1, -1):
                y_terrain = all_terrains[i]
                y_bottom = [0] * len(y_terrain) if i == 2 else all_terrains[i+1]
                xy_polygon = []

                for j in range(len(x_values)):
                    xy_polygon.append((x_values[j], y_terrain[j]))

                for j in range(len(x_values)-1, -1, -1):
                    xy_polygon.append((x_values[j], y_bottom[j]))

                polygon = plt.Polygon(xy_polygon, closed=True, facecolor=colors[i], edgecolor='none')
                ax.add_patch(polygon)
            
            ax.set_title("2D vrstvený fraktální terén")
            ax.set_xlabel("Vzdálenost")
            ax.set_ylabel("Výška")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.grid(False)
            
        else:
            terrain = self.generate_3d_terrain(iterations, roughness)
            x = np.linspace(0, 1, terrain.shape[0])
            y = np.linspace(0, 1, terrain.shape[1])
            X, Y = np.meshgrid(x, y)
            ax = self.fig.add_subplot(111, projection='3d')
            height_levels = [0.3, 0.6]
            colors = ['blue', 'green', 'brown']
            terrain_colors = np.zeros(terrain.shape + (3,))
            
            for i in range(terrain.shape[0]):
                for j in range(terrain.shape[1]):
                    height = terrain[i, j]
                    if height < height_levels[0]:
                        terrain_colors[i, j] = [0, 0, 1]  # modrá
                    elif height < height_levels[1]:
                        terrain_colors[i, j] = [0, 0.5, 0]  # zelená
                    else:
                        terrain_colors[i, j] = [0.5, 0.25, 0]  # hnědá
            
            ax.plot_surface(X, Y, terrain, facecolors=terrain_colors, rstride=1, cstride=1, 
                                   shade=True, antialiased=False)
            
            ax.set_title("3D fraktální terén")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Výška")
            ax.set_zlim(-1, 1)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FractalTerrainGenerator(root)
    root.mainloop()