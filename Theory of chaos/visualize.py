import numpy as np
import matplotlib.pyplot as plt
import torch
from config import DEVICE

def generate_trajectory(a, x0=0.5, steps=100):
    x_vals = np.empty(steps + 1, dtype=np.float32)
    x_vals[0] = x = x0
    for i in range(1, steps + 1):
        x = a * x * (1 - x)
        x_vals[i] = x
    return x_vals.tolist()

def predict_trajectory(model, a, x0=0.5, steps=100):
    x_vals = np.empty(steps + 1, dtype=np.float32)
    x_vals[0] = x = x0
    model.eval()

    for i in range(1, steps + 1):
        inp = torch.tensor([a, x], dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            x = model(inp).item()
        x_vals[i] = x

    return x_vals.tolist()

def plot_trajectories(true_vals, pred_vals, a):
    plt.figure(figsize=(12, 4))
    plt.plot(true_vals, label="True", linewidth=2)
    plt.plot(pred_vals, label="Predicted", linestyle="--")
    plt.title(f"Trajectory at a = {a}")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_origin_diagram(num_a=1000, num_iter=1000, discard=100):
    a_values = np.linspace(0, 4, num=num_a)
    x_init = 0.5
    data = []
    for a in a_values:
        x = x_init
        for _ in range(discard):
            x = a * x * (1 - x)
        for _ in range(num_iter - discard):
            x = a * x * (1 - x)
            data.append([a, x])
    data = np.array(data)
    plt.figure(figsize=(10, 6))
    plt.scatter(data[:, 0], data[:, 1], s=0.1, color="black")
    plt.title("True Bifurcation Diagram")
    plt.xlabel("a")
    plt.ylabel("x")
    plt.grid(True)

def plot_predicted_diagram(model, num_a=1000, num_iter=200):
    a_values = np.linspace(0, 4, num=num_a)
    x_init = 0.5
    data = []
    model.eval()
    for a in a_values:
        x = x_init
        for _ in range(num_iter):
            inp = torch.tensor([[a, x]], dtype=torch.float32).to(DEVICE)
            with torch.no_grad():
                x = model(inp).item()
            data.append([a, x])
    data = np.array(data)
    plt.figure(figsize=(10, 6))
    plt.scatter(data[:, 0], data[:, 1], s=0.1, color="blue")
    plt.title("Predicted Bifurcation Diagram")
    plt.xlabel("a")
    plt.ylabel("x")
    plt.grid(True)
    
def show_diagrams(model):
    plot_origin_diagram()
    plot_predicted_diagram(model)
    plt.show()