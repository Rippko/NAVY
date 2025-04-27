import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from fractal_computer import FractalComputer

class FractalViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fractal Viewer")
        self.geometry("820x1000")
        self.width, self.height = 800, 800
        self.x_min, self.x_max = -2.0, 1.0
        self.y_min, self.y_max = -1.5, 1.5
        self.max_iterations = 100
        self.current_fractal = "mandelbrot"  # výchozí fraktál
        self.julia_c = complex(-0.7, 0.27)  # výchozí hodnota pro Julia set
        self.fractal_computer = FractalComputer()
        self.fractal_computer.set_dimensions(self.width, self.height)
        self.fractal_computer.set_bounds(self.x_min, self.x_max, self.y_min, self.y_max)
        self.fractal_computer.set_iterations(self.max_iterations)
        self.fractal_computer.set_julia_parameter(self.julia_c)
        self.fractal_types = ["mandelbrot", "julia"]
        self.zoom_history = []
        self.save_current_view()
        self.setup_ui()
        self.render_image()
    
    def setup_ui(self):
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        

        ttk.Label(control_frame, text="Fractal:").pack(side=tk.LEFT, padx=5)
        set_var = tk.StringVar(value=self.current_fractal)
        set_dropdown = ttk.Combobox(control_frame, textvariable=set_var, 
                                   values=self.fractal_types, width=12, state="readonly")
        set_dropdown.pack(side=tk.LEFT, padx=5)
        set_dropdown.bind("<<ComboboxSelected>>", self.change_fractal)


        ttk.Label(control_frame, text="Iterations:").pack(side=tk.LEFT, padx=5)
        iter_var = tk.StringVar(value=str(self.max_iterations))
        iter_entry = ttk.Spinbox(control_frame, from_=10, to=1000, increment=10, 
                                textvariable=iter_var, width=5)
        iter_entry.pack(side=tk.LEFT, padx=5)
        iter_entry.bind("<Return>", lambda e: self.change_iterations(iter_var.get()))
        
        
        ttk.Button(control_frame, text="Reset", command=self.reset_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Back", command=self.go_back).pack(side=tk.LEFT, padx=5)
        
        
        self.julia_frame = ttk.LabelFrame(self, text="Julia Set Parameters")
        ttk.Label(self.julia_frame, text="Real part:").grid(row=0, column=0, padx=5, pady=5)
        self.julia_real_var = tk.StringVar(value=str(self.julia_c.real))
        julia_real_entry = ttk.Entry(self.julia_frame, textvariable=self.julia_real_var, width=10)
        julia_real_entry.grid(row=0, column=1, padx=5, pady=5)
        
        
        ttk.Label(self.julia_frame, text="Imaginary part:").grid(row=0, column=2, padx=5, pady=5)
        self.julia_imag_var = tk.StringVar(value=str(self.julia_c.imag))
        julia_imag_entry = ttk.Entry(self.julia_frame, textvariable=self.julia_imag_var, width=10)
        julia_imag_entry.grid(row=0, column=3, padx=5, pady=5)
        
        
        ttk.Button(self.julia_frame, text="Apply", 
                  command=self.update_julia_param).grid(row=0, column=4, padx=5, pady=5)
        
        if self.current_fractal == "julia":
            self.julia_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.bind("<ButtonPress-1>", self.start_zoom)
        self.canvas.bind("<B1-Motion>", self.update_zoom_box)
        self.canvas.bind("<ButtonRelease-1>", self.end_zoom)
        
        self.zoom_start = None
        self.zoom_rect = None
    
    def start_zoom(self, event):
        self.zoom_start = (event.x, event.y)
        if self.zoom_rect:
            self.canvas.delete(self.zoom_rect)
        self.zoom_rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y, outline='white', width=1)
    
    def update_zoom_box(self, event):
        if self.zoom_start and self.zoom_rect:
            x1, y1 = self.zoom_start
            self.canvas.coords(self.zoom_rect, x1, y1, event.x, event.y)
    
    def end_zoom(self, event):
        if self.zoom_start:
            x1, y1 = self.zoom_start
            x2, y2 = event.x, event.y

            if abs(x2 - x1) < 5 or abs(y2 - y1) < 5:
                if self.zoom_rect:
                    self.canvas.delete(self.zoom_rect)
                self.zoom_rect = None
                self.zoom_start = None
                return

            self.save_current_view()

            x_min_new = self.x_min + (self.x_max - self.x_min) * min(x1, x2) / self.width
            x_max_new = self.x_min + (self.x_max - self.x_min) * max(x1, x2) / self.width
            y_min_new = self.y_min + (self.y_max - self.y_min) * min(y1, y2) / self.height
            y_max_new = self.y_min + (self.y_max - self.y_min) * max(y1, y2) / self.height

            self.x_min, self.x_max = x_min_new, x_max_new
            self.y_min, self.y_max = y_min_new, y_max_new
            self.fractal_computer.set_bounds(self.x_min, self.x_max, self.y_min, self.y_max)

            if self.zoom_rect:
                self.canvas.delete(self.zoom_rect)
            self.zoom_rect = None
            self.zoom_start = None
            
            self.render_image()
    
    def save_current_view(self):
        view = {
            'x_min': self.x_min,
            'x_max': self.x_max,
            'y_min': self.y_min,
            'y_max': self.y_max,
            'fractal': self.current_fractal,
            'julia_c': self.julia_c,
            'iterations': self.max_iterations
        }
        self.zoom_history.append(view)
        if len(self.zoom_history) > 20:
            self.zoom_history.pop(0)
    
    def go_back(self):
        if len(self.zoom_history) > 1:
            self.zoom_history.pop()
            prev = self.zoom_history[-1]
            self.x_min = prev['x_min']
            self.x_max = prev['x_max']
            self.y_min = prev['y_min']
            self.y_max = prev['y_max']
            self.current_fractal = prev['fractal']
            self.julia_c = prev['julia_c']
            self.max_iterations = prev['iterations']
            self.fractal_computer.set_bounds(self.x_min, self.x_max, self.y_min, self.y_max)
            self.fractal_computer.set_iterations(self.max_iterations)
            self.fractal_computer.set_julia_parameter(self.julia_c)

            self.update_ui_from_state()
            self.render_image()
    
    def update_ui_from_state(self):
        if self.current_fractal == "julia":
            self.julia_frame.pack(fill=tk.X, padx=10, pady=5)
            self.julia_real_var.set(str(self.julia_c.real))
            self.julia_imag_var.set(str(self.julia_c.imag))
        else:
            self.julia_frame.pack_forget()
    
    def reset_view(self):
        self.save_current_view()
        if self.current_fractal == "mandelbrot":
            self.x_min, self.x_max = -2.0, 1.0
            self.y_min, self.y_max = -1.5, 1.5
        elif self.current_fractal == "julia":
            self.x_min, self.x_max = -1.5, 1.5
            self.y_min, self.y_max = -1.5, 1.5
        
        self.fractal_computer.set_bounds(self.x_min, self.x_max, self.y_min, self.y_max)
        self.render_image()
    
    def change_fractal(self, event):
        fractal_type = event.widget.get()
        if fractal_type != self.current_fractal:
            self.save_current_view()
            self.current_fractal = fractal_type

            if self.current_fractal == "julia":
                self.julia_frame.pack(fill=tk.X, padx=10, pady=5)
            else:
                self.julia_frame.pack_forget()
            
            self.reset_view()
    
    def change_iterations(self, value):
        try:
            iterations = int(value)
            if iterations != self.max_iterations and iterations > 0:
                self.save_current_view()
                self.max_iterations = iterations
                self.fractal_computer.set_iterations(self.max_iterations)
                self.render_image()
        except ValueError:
            pass
    
    def update_julia_param(self):
        try:
            real = float(self.julia_real_var.get())
            imag = float(self.julia_imag_var.get())
            new_c = complex(real, imag)
            if new_c != self.julia_c:
                self.save_current_view()
                self.julia_c = new_c
                self.fractal_computer.set_julia_parameter(self.julia_c)
                self.render_image()
        except ValueError:
            pass
    
    def render_image(self):
        start_time = time.time()
        self.status_var.set("Calculating...")
        self.update()
        iterations = self.fractal_computer.compute_fractal(self.current_fractal)
        colors = self.fractal_computer.create_color_palette()
        img = Image.new('RGB', (self.width, self.height), color='black')
        pixels = img.load()
        for x in range(self.width):
            for y in range(self.height):
                iter_count = iterations[y, x]
                pixels[x, y] = colors[iter_count] if iter_count < self.max_iterations else (0, 0, 0)
        
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        elapsed = time.time() - start_time
        fractal_name = self.current_fractal.capitalize()
        if self.current_fractal == "julia":
            fractal_name += f" (c={self.julia_c})"
        bounds = f"X: [{self.x_min:.6f}, {self.x_max:.6f}], Y: [{self.y_min:.6f}, {self.y_max:.6f}]"
        status = f"{fractal_name} | {bounds} | Iterations: {self.max_iterations} | Render time: {elapsed:.2f}s"
        self.status_var.set(status)