import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, random_split
import torch.nn.functional as F
import matplotlib.pyplot as plt
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# --- Data Generation ---
def generate_logistic_regression_data(num_a=500, num_iter=1000, discard=100):
    a_values = np.linspace(0, 4, num=num_a)
    x_init = 0.5
    X = []
    y = []

    for a in a_values:
        x = x_init
        for _ in range(discard):
            x = a * x * (1 - x)
        for _ in range(num_iter - discard):
            x_next = a * x * (1 - x)
            X.append([a, x])
            y.append(x_next)
            x = x_next

    return np.array(X), np.array(y)

# --- Neural Network ---
class LogisticMapRegressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        return self.fc4(x)

# --- Training Function ---
def train_model(model, train_loader, val_loader, epochs=10):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    prev_val_loss = float('inf')
    for epoch in range(epochs):
        model.train()
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            preds = model(X_batch)
            loss = criterion(preds, y_batch)
            loss.backward()
            optimizer.step()

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                preds = model(X_batch)
                val_loss += criterion(preds, y_batch).item()
        if val_loss < prev_val_loss:
            prev_val_loss = val_loss
            print(f"Epoch {epoch + 1}: Validation Loss Improved to {val_loss / len(val_loader):.6f}")
            torch.save(model.state_dict(), "best_model.pth")

# --- Prediction & Visualization ---
def generate_true_trajectory(a, x0=0.5, steps=100):
    x_vals = [x0]
    x = x0
    for _ in range(steps):
        x = a * x * (1 - x)
        x_vals.append(x)
    return x_vals

def predict_trajectory(model, a, x0=0.5, steps=100):
    model.eval()
    x_vals = [x0]
    x = x0
    for _ in range(steps):
        inp = torch.tensor([[a, x]], dtype=torch.float32).to(device)
        with torch.no_grad():
            x = model(inp).item()
        x_vals.append(x)
    return x_vals

def plot_trajectories(true_vals, pred_vals, a):
    plt.figure(figsize=(100, 10))
    plt.plot(true_vals, label='True Logistic Map', linewidth=2)
    plt.plot(pred_vals, label='Model Prediction', linestyle='--')
    plt.title(f'Logistic Map Prediction (a = {a})')
    plt.xlabel('Step')
    plt.ylabel('x')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_true_bifurcation_diagram(num_a=1000, num_iter=1000, discard=100):
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
    plt.scatter(data[:, 0], data[:, 1], s=0.1, color='black')
    plt.title("True Bifurcation Diagram")
    plt.xlabel("a")
    plt.ylabel("x")
    plt.grid(True)
    plt.show()


def plot_predicted_bifurcation_diagram(model, num_a=1000, num_iter=200, discard=0):
    a_values = np.linspace(0, 4, num=num_a)
    x_init = 0.5
    data = []
    model.eval()
    
    # Create the figure just once before the loop
    plt.figure(figsize=(10, 6))
    plt.title("Predicted Bifurcation Diagram (Neural Net)")
    plt.xlabel("a")
    plt.ylabel("x")
    plt.xlim(0, 4)
    plt.ylim(0, 1)
    plt.grid(True)
    
    for i, a in enumerate(a_values):
        x = x_init
        for _ in range(discard):
            inp = torch.tensor([[a, x]], dtype=torch.float32).to(device)
            with torch.no_grad():
                x = model(inp).item()
        
        for _ in range(num_iter - discard):
            inp = torch.tensor([[a, x]], dtype=torch.float32).to(device)
            with torch.no_grad():
                x = model(inp).item()
            data.append([a, x])
        
        current_data = np.array(data)
        plt.clf()
        plt.title(f"Predicted Bifurcation Diagram (Progress: {i+1}/{num_a})")
        plt.xlabel("a")
        plt.ylabel("x")
        plt.xlim(0, 4)
        plt.ylim(0, 1)
        plt.grid(True)
        plt.scatter(current_data[:, 0], current_data[:, 1], s=0.1, color='blue')
        plt.pause(0.0001)
    
    plt.title("Predicted Bifurcation Diagram (Neural Net)")
    plt.show()


# --- Main ---
def main():
    # Generate data
    X_data, y_data = generate_logistic_regression_data()
    X_tensor = torch.tensor(X_data, dtype=torch.float32)
    y_tensor = torch.tensor(y_data, dtype=torch.float32).unsqueeze(1)

    dataset = TensorDataset(X_tensor, y_tensor)
    train_size = int(0.8 * len(dataset))
    train_dataset, val_dataset = random_split(dataset, [train_size, len(dataset) - train_size])
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=128)

    if not os.path.exists('best_model.pth'):
        # Initialize and train the model
        print("Training new model...")
        model = LogisticMapRegressor().to(device)
        train_model(model, train_loader, val_loader, epochs=10)
        print("Training completed. Model saved as 'best_model.pth'.")
    else:
        model = LogisticMapRegressor().to(device)
        model.load_state_dict(torch.load('best_model.pth'))
        model.eval()
        print("Loaded existing model.")

    # Predict & Plot
    a_test = 3.7
    x0 = 0.5
    steps = 1000
    true_vals = generate_true_trajectory(a_test, x0, steps)
    pred_vals = predict_trajectory(model, a_test, x0, steps)
    plot_trajectories(true_vals, pred_vals, a_test)

    plot_true_bifurcation_diagram()
    plot_predicted_bifurcation_diagram(model)

if __name__ == '__main__':
    main()