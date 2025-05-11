import numpy as np
import torch
from torch.utils.data import TensorDataset, random_split

def generate_logistic_data(num_a=500, num_iter=1000, discard=100, x_init=0.5):
    a_values = np.linspace(0, 4, num=num_a)
    total_steps = num_iter - discard
    X = np.empty((num_a * total_steps, 2), dtype=np.float32)
    y = np.empty((num_a * total_steps,), dtype=np.float32)

    idx = 0
    for a in a_values:
        x = x_init
        # zahodíme prvních `discard` iterací
        for _ in range(discard):
            x = a * x * (1 - x)
        # sbíráme data
        for _ in range(total_steps):
            x_next = a * x * (1 - x)
            X[idx] = [a, x]
            y[idx] = x_next
            x = x_next
            idx += 1

    return X, y

def prepare_dataloaders(X, y, batch_size=128, split_ratio=0.8):
    dataset = TensorDataset(torch.from_numpy(X), torch.from_numpy(y).unsqueeze(1))
    train_size = int(split_ratio * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    return train_ds, val_ds