import torch
from model import LogisticMap
from data import generate_logistic_data, prepare_dataloaders
from train import train
from visualize import (generate_trajectory, predict_trajectory,
                       plot_trajectories, show_diagrams)
from config import DEVICE, EPOCHS, BATCH_SIZE, MODEL_PATH
import os

def main():
    X, y = generate_logistic_data()
    train_ds, val_ds = prepare_dataloaders(X, y, BATCH_SIZE)
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = torch.utils.data.DataLoader(val_ds, batch_size=BATCH_SIZE)

    model = LogisticMap().to(DEVICE)
    if not os.path.exists(MODEL_PATH):
        print("Training new model...")
        train(model, train_loader, val_loader, epochs=EPOCHS)
        print("Training completed.")
    else:
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval()
        print("Loaded pre-trained model.")

    # Prediction and Visualization
    a_test, x0, steps = 3.7, 0.5, 1000
    true_vals = generate_trajectory(a_test, x0, steps)
    pred_vals = predict_trajectory(model, a_test, x0, steps)
    plot_trajectories(true_vals, pred_vals, a_test)
    show_diagrams(model)

if __name__ == "__main__":
    main()