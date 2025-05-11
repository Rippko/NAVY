import torch
import torch.nn as nn
from config import DEVICE, MODEL_PATH
from tqdm import tqdm

def train_one_epoch(model, dataloader, optimizer, loss_fn):
    model.train()
    total_loss = 0
    for X_batch, y_batch in tqdm(dataloader, desc="Training", leave=False):
        X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
        optimizer.zero_grad()
        preds = model(X_batch)
        loss = loss_fn(preds, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)

def validate(model, dataloader, loss_fn):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
            preds = model(X_batch)
            total_loss += loss_fn(preds, y_batch).item()
    return total_loss / len(dataloader)

def train(model, train_loader, val_loader, epochs=10):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()
    best_loss = float('inf')
    history = []

    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        train_loss = train_one_epoch(model, train_loader, optimizer, loss_fn)
        val_loss = validate(model, val_loader, loss_fn)

        history.append((train_loss, val_loss))

        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"Validation loss improved: {val_loss:.6f} → model saved.")
        else:
            print(f"Validation loss: {val_loss:.6f}")

        print(f"Training loss: {train_loss:.6f}")

    return history
