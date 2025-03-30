import tkinter as tk
import numpy as np
import random
import time
from tkinter import messagebox, Toplevel, Text, Scrollbar

class FindTheCheeseGame:
    def __init__(self, root, rows=10, cols=10):
        self.root = root
        self.root.title("Find the Cheese - Q-Learning")
        
        self.rows = rows
        self.cols = cols
        
        self.cell_colors = {
            "*": "lightblue",   # walker
            "C": "gold",        # cheese
            "O": "red",         # hole
            "P": "lightgreen",  # path
            "": "white"         # empty
        }

        self.initial_pos = None
        self.walker_pos = None
        self.cheese_pos = None
        self.holes = []
        
        self.q_table = np.zeros((rows, cols, 4))  # Q-table: (row, col, action)
        self.actions = ['up', 'right', 'down', 'left']
        self.action_indices = {action: i for i, action in enumerate(self.actions)}
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        self.alpha = 0.1  # learning rate
        self.gamma = 0.9  # discount factor
        
        self.success_count = 0
        self.total_attempts = 0
        self.success_rate = 0.0
        
        self.move_reward = -1
        self.hole_reward = -100
        self.cheese_reward = 100
        
        self.iterations = 0
        self.is_training = False
        self.is_visualizing = False
        self.training_speed = 0  # in ms
        self.visualization_speed = 300  # in ms
        self.best_path = []

        self.create_ui()
        self.reset_grid()
    
    def create_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        self.grid_frame = tk.Frame(main_frame)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10)
        cell_size = 40
        # generating grid cells
        self.cells = []
        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                cell = tk.Frame(self.grid_frame, width=cell_size, height=cell_size, 
                              bg="white", highlightbackground="black", 
                              highlightthickness=1)
                cell.grid(row=r, column=c)
                cell.propagate(False)
                label = tk.Label(cell, bg="white", font=("Arial", 10), text="")  # Reduced font size
                label.place(relx=0.5, rely=0.5, anchor="center")
                
                cell.bind("<Button-1>", lambda event, r=r, c=c: self.cell_clicked(r, c))
                row_cells.append({"frame": cell, "label": label})
            self.cells.append(row_cells)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame)
        controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        
        # Object selection
        selection_frame = tk.LabelFrame(controls_frame, text="Place Objects")
        selection_frame.pack(fill="x", padx=5, pady=5)
        
        self.selection = tk.StringVar(value="walker")
        
        tk.Radiobutton(selection_frame, text="Walker (Start Position)", variable=self.selection, value="walker").pack(anchor="w")
        tk.Radiobutton(selection_frame, text="Cheese", variable=self.selection, value="cheese").pack(anchor="w")
        tk.Radiobutton(selection_frame, text="Hole", variable=self.selection, value="hole").pack(anchor="w")
        
        buttons_frame = tk.Frame(controls_frame)
        buttons_frame.pack(fill="x", padx=5, pady=10)
        
        self.train_button = tk.Button(buttons_frame, text="Start Learning", command=self.toggle_training)
        self.train_button.pack(fill="x", pady=2)
        
        self.visualize_button = tk.Button(buttons_frame, text="Visualize Best Path", command=self.visualize_best_path)
        self.visualize_button.pack(fill="x", pady=2)
        self.visualize_button.config(state=tk.DISABLED)  # Disabled initially
        
        tk.Button(buttons_frame, text="Single Step", command=self.single_step).pack(fill="x", pady=2)
        tk.Button(buttons_frame, text="Reset Learning", command=self.reset_learning).pack(fill="x", pady=2)
        tk.Button(buttons_frame, text="Display Q-Table", command=self.display_q_table).pack(fill="x", pady=2)
        tk.Button(buttons_frame, text="Clear Grid", command=self.reset_grid).pack(fill="x", pady=2)
        
        info_frame = tk.LabelFrame(controls_frame, text="Training Info")
        info_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(info_frame, text="Iterations:").grid(row=0, column=0, sticky="w")
        self.iter_label = tk.Label(info_frame, text="0")
        self.iter_label.grid(row=0, column=1, sticky="e")
        
        tk.Label(info_frame, text="Exploration rate:").grid(row=1, column=0, sticky="w")
        self.epsilon_label = tk.Label(info_frame, text=f"{self.epsilon:.2f}")
        self.epsilon_label.grid(row=1, column=1, sticky="e")
        
        tk.Label(info_frame, text="Success rate:").grid(row=2, column=0, sticky="w")
        self.success_label = tk.Label(info_frame, text="0%")
        self.success_label.grid(row=2, column=1, sticky="e")
        
        tk.Label(info_frame, text="Training speed:").grid(row=3, column=0, sticky="w")
        
        self.speed_slider = tk.Scale(info_frame, from_=1, to=500, orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_slider.set(self.training_speed)
        self.speed_slider.grid(row=3, column=1, sticky="e")
    
    def update_speed(self, val):
        speed = int(val)
        self.training_speed = speed
        self.visualization_speed = 300
    
    def cell_clicked(self, row, col):
        if self.is_training or self.is_visualizing:
            return
            
        selection = self.selection.get()
        
        if selection == "walker":
            if self.walker_pos:
                old_row, old_col = self.walker_pos
                self.update_cell(old_row, old_col, "")
            
            self.walker_pos = (row, col)
            self.initial_pos = (row, col)
            self.update_cell(row, col, "*")
            
        elif selection == "cheese":
            if self.cheese_pos:
                old_row, old_col = self.cheese_pos
                self.update_cell(old_row, old_col, "")
            
            self.cheese_pos = (row, col)
            self.update_cell(row, col, "C")
            
        elif selection == "hole":
            if (row, col) in self.holes:
                self.holes.remove((row, col))
                self.update_cell(row, col, "")
            else:
                self.holes.append((row, col))
                self.update_cell(row, col, "O")
    
    def update_cell(self, row, col, text):
        """Helper function to update cell appearance"""
        cell = self.cells[row][col]
        label = cell["label"]
        frame = cell["frame"]
        
        label.config(text=text)
        color = self.cell_colors.get(text)
        
        if text == "" and hasattr(self, 'q_table') and self.q_table is not None and not self.is_visualizing:
            q_values = self.q_table[row, col]
            max_q = np.max(q_values)
            if max_q > 0:
                intensity = min(255, int(200 * max_q / 100))
                color = f"#{255-intensity:02x}{255:02x}{255-intensity:02x}"
        
        frame.config(bg=color)
        label.config(bg=color)
    
    def reset_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.update_cell(r, c, "")
        
        self.walker_pos = None
        self.initial_pos = None
        self.cheese_pos = None
        self.holes = []
        self.q_table = np.zeros((self.rows, self.cols, 4))
        self.iterations = 0
        self.epsilon = 1.0
        self.success_count = 0
        self.total_attempts = 0
        self.success_rate = 0.0
        self.best_path = []
        self.visualize_button.config(state=tk.DISABLED)
        self.iter_label.config(text=str(self.iterations))
        self.epsilon_label.config(text=f"{self.epsilon:.2f}")
        self.success_label.config(text="0%")
    
    def reset_learning(self):
        """Reset learning progress while keeping grid layout"""
        if self.is_training or self.is_visualizing:
            return
        
        if messagebox.askyesno("Reset Learning", "Reset all learning progress while keeping the grid layout?"):
            self.q_table = np.zeros((self.rows, self.cols, 4))
            self.iterations = 0
            self.epsilon = 1.0
            self.success_count = 0
            self.total_attempts = 0
            self.success_rate = 0.0
            self.best_path = []
            
            # update UI elements
            self.visualize_button.config(state=tk.DISABLED)
            self.iter_label.config(text=str(self.iterations))
            self.epsilon_label.config(text=f"{self.epsilon:.2f}")
            self.success_label.config(text="0%")

            self.refresh_grid_display()
    
    def display_q_table(self):
        """Display the Q-table in a new window"""
        if not hasattr(self, 'q_table') or self.q_table is None:
            messagebox.showinfo("Q-Table", "No Q-table data available yet.")
            return
        
        q_window = Toplevel(self.root)
        q_window.title("Q-Table Values")
        q_window.geometry("800x600")
        
        frame = tk.Frame(q_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar_y = Scrollbar(frame)
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = Scrollbar(frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        text = Text(frame, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        text.pack(fill="both", expand=True)
        
        scrollbar_y.config(command=text.yview)
        scrollbar_x.config(command=text.xview)
        
        text.insert("1.0", "Q-Table Values (row, col): [Up, Right, Down, Left]\n")
        text.insert("end", "Highest value in each cell indicates the best action\n\n")
        
        for r in range(self.rows):
            for c in range(self.cols):
                q_values = self.q_table[r, c]
                cell_text = f"({r}, {c}): {q_values.round(2)}"
                
                # Mark special cells
                if (r, c) == self.initial_pos:
                    cell_text += " - START"
                elif (r, c) == self.cheese_pos:
                    cell_text += " - CHEESE"
                elif (r, c) in self.holes:
                    cell_text += " - HOLE"
                
                # Highlight the best action
                if np.max(q_values) > 0:
                    best_action = np.argmax(q_values)
                    action_name = self.actions[best_action]
                    cell_text += f" - Best: {action_name.upper()}"
                
                text.insert("end", cell_text + "\n")
        
        text.config(state="disabled")
    
    def toggle_training(self):
        if not self.walker_pos or not self.cheese_pos:
            messagebox.showwarning("Warning", "Please place both walker and cheese before training")
            return
        
        if self.is_visualizing:
            return
        
        self.is_training = not self.is_training
        
        if self.is_training:
            self.train_button.config(text="Stop Learning")
            self.train_step()
        else:
            self.train_button.config(text="Start Learning")
    
    def train_step(self):
        if not self.is_training:
            self.train_button.config(text="Start Learning")
            return
        
        if self.training_speed <= 10:
            iterations_per_update = 50
            for _ in range(iterations_per_update):
                if not self.is_training:
                    break
                self.single_step(update_ui=False)
            
            self.update_training_ui()
        else:
            self.single_step(update_ui=True)
        
        self.root.after(max(1, self.training_speed), self.train_step)
        
    def update_q_table(self, current_pos, action_idx, next_pos, reward):
        """Update the Q-table using the Q-learning formula"""
        current_q = self.q_table[current_pos[0], current_pos[1], action_idx]
        best_next_q = np.max(self.q_table[next_pos[0], next_pos[1]])
        new_q = current_q + self.alpha * (reward + self.gamma * best_next_q - current_q)
        self.q_table[current_pos[0], current_pos[1], action_idx] = new_q
    
    def single_step(self, update_ui=True):
        if not self.walker_pos or not self.cheese_pos or not self.initial_pos:
            messagebox.showwarning("Warning", "Please place both walker and cheese before training")
            return

        current_pos = self.walker_pos
        
        # epsilon-greedy policy
        if random.random() < self.epsilon:
            action_idx = random.randint(0, 3)
        else:
            action_idx = np.argmax(self.q_table[current_pos[0], current_pos[1]])
        
        # Take the action and get the next state and reward
        next_pos, reward, done = self.take_action(current_pos, action_idx)
        self.update_q_table(current_pos, action_idx, next_pos, reward)

        if update_ui:
            self.update_cell(current_pos[0], current_pos[1], "")
        
        self.walker_pos = next_pos
        
        # Check if next position is a hole
        is_hole = next_pos in self.holes
        
        if update_ui:
            self.update_cell(next_pos[0], next_pos[1], "*")
            
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) == self.walker_pos:
                        continue
                    elif (r, c) == self.cheese_pos:
                        self.update_cell(r, c, "C")
                    elif (r, c) in self.holes:
                        self.update_cell(r, c, "O")
                    else:
                        self.update_cell(r, c, "")
        
        # iteration counter
        self.iterations += 1
        if update_ui:
            self.iter_label.config(text=str(self.iterations))
        
        # Check if episode ended
        if done:
            self.total_attempts += 1
            
            # If found cheese
            if reward == self.cheese_reward:
                self.success_count += 1
                if update_ui:
                    self.flash_grid("green")
                
                # calculate best path -> enable visualization button
                self.calculate_best_path()
                
                if self.best_path:
                    self.visualize_button.config(state=tk.NORMAL)
                
                if self.success_count > 10:
                    self.epsilon = max(self.epsilon_min, self.epsilon * 0.95)
            
            # If hit a hole
            elif reward == self.hole_reward:
                if self.epsilon > self.epsilon_min:
                    self.epsilon *= self.epsilon_decay
                    if update_ui:
                        self.epsilon_label.config(text=f"{self.epsilon:.2f}")
                if update_ui:
                    self.flash_grid("red")
            
            # calculating success rate
            self.success_rate = (self.success_count / self.total_attempts) * 100
            if update_ui:
                self.success_label.config(text=f"{self.success_rate:.1f}%")
            
            # reseting walker to starting position
            if update_ui:
                self.update_cell(next_pos[0], next_pos[1], "O" if is_hole else "")
            
            self.walker_pos = self.initial_pos
            
            if update_ui:
                self.update_cell(self.initial_pos[0], self.initial_pos[1], "*")
                for hole_pos in self.holes:
                    if hole_pos != self.walker_pos:
                        self.update_cell(hole_pos[0], hole_pos[1], "O")
    
    def take_action(self, pos, action_idx):
        row, col = pos
        if action_idx == 0:  # Up
            new_row, new_col = max(0, row - 1), col
        elif action_idx == 1:  # Right
            new_row, new_col = row, min(self.cols - 1, col + 1)
        elif action_idx == 2:  # Down
            new_row, new_col = min(self.rows - 1, row + 1), col
        else:  # Left
            new_row, new_col = row, max(0, col - 1)
        
        # outcome based of action
        if (new_row, new_col) == self.cheese_pos:
            return (new_row, new_col), self.cheese_reward, True
        elif (new_row, new_col) in self.holes:
            return (new_row, new_col), self.hole_reward, True
        else:
            return (new_row, new_col), self.move_reward, False
    
    def calculate_best_path(self):
        """Calculate the best path from initial position to cheese based on Q-values"""
        if not self.initial_pos or not self.cheese_pos:
            return
        
        path = []
        current = self.initial_pos
        max_steps = self.rows * self.cols  # Prevent infinite loops
        step_count = 0
        
        while current != self.cheese_pos and step_count < max_steps:
            path.append(current)
            
            # best action from current position
            action_idx = np.argmax(self.q_table[current[0], current[1]])
            row, col = current
            if action_idx == 0:  # Up
                new_row, new_col = max(0, row - 1), col
            elif action_idx == 1:  # Right
                new_row, new_col = row, min(self.cols - 1, col + 1)
            elif action_idx == 2:  # Down
                new_row, new_col = min(self.rows - 1, row + 1), col
            else:  # Left
                new_row, new_col = row, max(0, col - 1)
            
            current = (new_row, new_col)
            step_count += 1
            
            if current in self.holes:
                break
        
        if current == self.cheese_pos:
            path.append(current)
            self.best_path = path
            
    def update_training_ui(self):
        """Update UI elements after batched training iterations"""
        self.iter_label.config(text=str(self.iterations))
        self.epsilon_label.config(text=f"{self.epsilon:.2f}")
        self.success_label.config(text=f"{self.success_rate:.1f}%")
        
        if self.best_path:
            self.visualize_button.config(state=tk.NORMAL)
        
        self.refresh_grid_display()
        self.root.update_idletasks()
    
    def visualize_best_path(self):
        """Visualize the best path found by the agent"""
        if not self.best_path or self.is_training:
            return
        
        self.is_visualizing = True
        self.train_button.config(state=tk.DISABLED)
        self.visualize_button.config(state=tk.DISABLED)
        self.original_pos = self.walker_pos
        self.refresh_grid_display()
        
        self.current_path_index = 0
        self.root.after(500, self.visualize_next_step)
        
    def visualize_next_step(self):
        """Process one step in the path visualization"""
        if not self.is_visualizing or self.current_path_index >= len(self.best_path):
            self.is_visualizing = False
            self.walker_pos = self.original_pos
            self.refresh_grid_display()
            self.train_button.config(state=tk.NORMAL)
            self.visualize_button.config(state=tk.NORMAL)
            return
        
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                if pos != self.cheese_pos and pos not in self.holes:
                    self.update_cell(r, c, "")
        
        for i in range(self.current_path_index):
            path_pos = self.best_path[i]
            if path_pos != self.cheese_pos and path_pos not in self.holes:
                self.update_cell(path_pos[0], path_pos[1], "P")
        
        current_pos = self.best_path[self.current_path_index]
        self.walker_pos = current_pos
        self.update_cell(current_pos[0], current_pos[1], "*")
        
        if self.cheese_pos:
            cheese_r, cheese_c = self.cheese_pos
            self.update_cell(cheese_r, cheese_c, "C")
        
        for hole_pos in self.holes:
            hole_r, hole_c = hole_pos
            self.update_cell(hole_r, hole_c, "O")
        
        self.current_path_index += 1
        self.root.after(300, self.visualize_next_step)
    
    def flash_grid(self, color):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c]["frame"].config(bg=color)
                self.cells[r][c]["label"].config(bg=color)
        
        self.root.update()
        time.sleep(0.2)
        self.refresh_grid_display()
                
    def refresh_grid_display(self):
        """Refreshes the entire grid display"""
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                if pos == self.walker_pos:
                    self.update_cell(r, c, "*")
                elif pos == self.cheese_pos:
                    self.update_cell(r, c, "C")
                elif pos in self.holes:
                    self.update_cell(r, c, "O")
                else:
                    self.update_cell(r, c, "")
                    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    game = FindTheCheeseGame(root)
    root.mainloop()