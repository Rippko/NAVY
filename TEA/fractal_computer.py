import numpy as np
import colorsys

class FractalComputer:
    def __init__(self):
        self.max_iterations = 100
        self.width = 800
        self.height = 800
        self.x_min = -2.0
        self.x_max = 1.0
        self.y_min = -1.5
        self.y_max = 1.5
        self.julia_c = complex(-0.7, 0.27)
    
    def set_dimensions(self, width, height):
        self.width = width
        self.height = height
    
    def set_bounds(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
    
    def set_iterations(self, max_iterations):
        self.max_iterations = max_iterations
    
    def set_julia_parameter(self, c):
        self.julia_c = c
    
    def compute_mandelbrot(self):
        re = np.linspace(self.x_min, self.x_max, self.width)
        im = np.linspace(self.y_min, self.y_max, self.height)
        X, Y = np.meshgrid(re, im)
        C = X + 1j * Y

        Z = np.zeros_like(C)
        iterations = np.zeros(C.shape, dtype=int)
        mask = np.ones(C.shape, dtype=bool)

        for i in range(self.max_iterations):
            Z[mask] = Z[mask]**2 + C[mask]
            mask_new = np.abs(Z) < 2.0
            iterations[mask & ~mask_new] = i
            mask = mask_new
        
        return iterations
    
    def compute_julia(self):
        re = np.linspace(self.x_min, self.x_max, self.width)
        im = np.linspace(self.y_min, self.y_max, self.height)
        X, Y = np.meshgrid(re, im)
        Z = X + 1j * Y

        iterations = np.zeros(Z.shape, dtype=int)
        mask = np.ones(Z.shape, dtype=bool)
        
        for i in range(self.max_iterations):
            Z[mask] = Z[mask]**2 + self.julia_c
            mask_new = np.abs(Z) < 2.0
            iterations[mask & ~mask_new] = i
            mask = mask_new
        
        return iterations
    
    def create_color_palette(self):
        colors = []
        for i in range(self.max_iterations):
            hue = i / self.max_iterations
            saturation = 0.8
            value = 1.0 if i < self.max_iterations - 1 else 0.0
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        
        return colors
    
    def compute_fractal(self, fractal_type):
        if fractal_type == "mandelbrot":
            return self.compute_mandelbrot()
        elif fractal_type == "julia":
            return self.compute_julia()
        else:
            raise ValueError(f"Nepodporovaný typ fraktálu: {fractal_type}")