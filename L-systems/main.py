import tkinter as tk
from tkinter import messagebox, Frame, Canvas, Label, Entry, Button, Scale
import turtle
from collections import deque
import math
from functools import partial

class FractalLSystemGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Fractal L-System Generator")
        self.master.geometry("900x700")
        self.setup_layout()
        self.fractal_presets = [
            {
                "name": "Koch Variation",
                "axiom": "F+F+F+F",
                "rules": {"F": "F+F-F-FF+F+F-F"},
                "angle": 90
            },
            {
                "name": "Triangular Gosper",
                "axiom": "F++F++F",
                "rules": {"F": "F+F--F+F"},
                "angle": 60
            },
            {
                "name": "Plant Structure",
                "axiom": "F",
                "rules": {"F": "F[+F]F[-F]F"},
                "angle": math.degrees(math.pi/7)
            },
            {
                "name": "Branching Pattern",
                "axiom": "F",
                "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
                "angle": math.degrees(math.pi/8)
            }
        ]
        
        self.create_controls()
        self.create_preset_buttons()
        
        self._screen = None
        self._turtle = None
        self.initialize_turtle()
        self.canvas.config(scrollregion=(0, 0, 800, 600))
        self.set_default_values()
        
    def setup_layout(self):
        self.main_container = Frame(self.master)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas_container = Frame(self.main_container, bg="#eee")
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = Canvas(self.canvas_container, bg="white")
        
        self.x_scrollbar = tk.Scrollbar(self.canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.y_scrollbar = tk.Scrollbar(self.canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.x_scrollbar.grid(row=1, column=0, sticky="ew")
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas_container.grid_rowconfigure(0, weight=1)
        self.canvas_container.grid_columnconfigure(0, weight=1)

        self.control_container = Frame(self.main_container, bg="#f5f5f5", width=250)
        self.control_container.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
    def create_controls(self):
        row = 0
        padding = 5
        
        Label(self.control_container, text="L-System Parameters", 
              font=("Helvetica", 12, "bold"), bg="#f5f5f5").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=10)
        row += 1
        
        parameters = [
            ("start_x", "Starting X:"),
            ("start_y", "Starting Y:"),
            ("iterations", "Iterations:"),
            ("custom_axiom", "Custom Axiom:"),
            ("custom_rules", "Custom Rules:"),
            ("custom_angle", "Angle (degrees):")
        ]
        
        self.inputs = {}
        for param_id, label_text in parameters:
            Label(self.control_container, text=label_text, bg="#f5f5f5").grid(
                row=row, column=0, sticky="w", padx=padding, pady=padding)
            
            entry = Entry(self.control_container, width=15)
            entry.grid(row=row, column=1, sticky="ew", padx=padding, pady=padding)
            self.inputs[param_id] = entry
            row += 1
            
        Label(self.control_container, text="Line Length:", bg="#f5f5f5").grid(
            row=row, column=0, sticky="w", padx=padding, pady=padding)
        
        self.line_length_scale = Scale(self.control_container, from_=1, to=50, 
                                       orient=tk.HORIZONTAL, resolution=1)
        self.line_length_scale.grid(row=row, column=1, sticky="ew", padx=padding, pady=padding)
        row += 1
        
        Label(self.control_container, text="Line Width:", bg="#f5f5f5").grid(
            row=row, column=0, sticky="w", padx=padding, pady=padding)
        
        self.line_width_scale = Scale(self.control_container, from_=1, to=10, 
                                      orient=tk.HORIZONTAL, resolution=1)
        self.line_width_scale.grid(row=row, column=1, sticky="ew", padx=padding, pady=padding)
        row += 1
        
        # Action buttons
        Button(self.control_container, text="Generate Custom", bg="#4CAF50", fg="white",
               command=self.generate_custom).grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=padding, pady=padding*2)
        row += 1
        
        Button(self.control_container, text="Clear Canvas", bg="#f44336", fg="white",
               command=self.clear_canvas).grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=padding, pady=padding)
        row += 1
        
    def create_preset_buttons(self):
        preset_frame = Frame(self.control_container, bg="#f5f5f5")
        preset_frame.grid(row=99, column=0, columnspan=2, sticky="ew", pady=10)
        
        Label(preset_frame, text="Preset Patterns", 
              font=("Helvetica", 12, "bold"), bg="#f5f5f5").pack(anchor="w", pady=(10, 5))
        
        for i, preset in enumerate(self.fractal_presets):
            Button(preset_frame, text=preset["name"], bg="#2196F3", fg="white",
                  command=partial(self.generate_preset, i)).pack(fill=tk.X, pady=3)
    
    def initialize_turtle(self):
        if self._screen is None:
            self._screen = turtle.TurtleScreen(self.canvas)
            self._screen.bgcolor("white")
        
        if self._turtle is None:
            self._turtle = turtle.RawTurtle(self._screen)
            self._turtle.speed(0)  # Fastest speed
            self._turtle.hideturtle()
    
    def set_default_values(self):
        defaults = {
            "start_x": "0",
            "start_y": "0",
            "iterations": "3",
            "custom_axiom": "F",
            "custom_rules": """{"F": "F+F--F+F"}""",
            "custom_angle": "60"
        }
        
        for field, value in defaults.items():
            if field in self.inputs:
                self.inputs[field].delete(0, tk.END)
                self.inputs[field].insert(0, value)
        
        self.line_length_scale.set(5)
        self.line_width_scale.set(1)
    
    def expand_l_system(self, axiom, rules, iterations):
        current = axiom
        
        for _ in range(iterations):
            next_gen = ""
            for char in current:
                next_gen += rules.get(char, char)
            current = next_gen
            
        return current
    
    def render_l_system(self, l_string, angle, start_x, start_y, line_width, line_length):
        self._turtle.reset()
        self._turtle.pensize(line_width)
        self._turtle.speed(0)
        self._turtle.hideturtle()
        
        self._screen.tracer(0)
        self._turtle.penup()
        self._turtle.setposition(start_x, start_y)
        self._turtle.pendown()
        
        position_stack = deque()
        
        for i, char in enumerate(l_string):
            if char == 'F':  # Move forward and draw
                self._turtle.forward(line_length)
            elif char == 'b':  # Move without drawing
                self._turtle.penup()
                self._turtle.forward(line_length)
                self._turtle.pendown()
            elif char == '+':  # Turn right
                self._turtle.right(angle)
            elif char == '-':  # Turn left
                self._turtle.left(angle)
            elif char == '[':  # Save position and heading
                position_stack.append((self._turtle.position(), self._turtle.heading()))
            elif char == ']':  # Restore position and heading
                if position_stack:
                    pos, heading = position_stack.pop()
                    self._turtle.penup()
                    self._turtle.setposition(pos)
                    self._turtle.setheading(heading)
                    self._turtle.pendown()

        self._screen.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def generate_preset(self, preset_index):
        try:
            preset = self.fractal_presets[preset_index]
            iterations = int(self.inputs["iterations"].get())
            start_x = float(self.inputs["start_x"].get())
            start_y = float(self.inputs["start_y"].get())
            line_width = self.line_width_scale.get()
            line_length = self.line_length_scale.get()
            
            l_string = self.expand_l_system(preset["axiom"], preset["rules"], iterations)
            self.render_l_system(
                l_string, 
                preset["angle"], 
                start_x, 
                start_y,
                line_width, 
                line_length
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preset: {str(e)}")
    
    def generate_custom(self):
        try:
            axiom = self.inputs["custom_axiom"].get()
            rules_str = self.inputs["custom_rules"].get()
            angle = float(self.inputs["custom_angle"].get())
            iterations = int(self.inputs["iterations"].get())
            start_x = float(self.inputs["start_x"].get())
            start_y = float(self.inputs["start_y"].get())
            line_width = self.line_width_scale.get()
            line_length = self.line_length_scale.get()

            rules = eval(rules_str)
            
            l_string = self.expand_l_system(axiom, rules, iterations)
            self.render_l_system(
                l_string, 
                angle, 
                start_x, 
                start_y,
                line_width, 
                line_length
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate custom pattern: {str(e)}")
    
    def clear_canvas(self):
        if self._turtle:
            self._turtle.clear()
            self._screen.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = FractalLSystemGenerator(root)
    root.mainloop()