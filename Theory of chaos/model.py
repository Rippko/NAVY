import torch.nn as nn
import torch.nn.functional as F

class LogisticMap(nn.Module):
    def __init__(self, input_dim=2, hidden_dim=64, hidden_layers=3, output_dim=1, activation=F.relu):
        super().__init__()
        self.activation = activation
        layers = [nn.Linear(input_dim, hidden_dim)]
        for _ in range(hidden_layers - 1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
        self.hidden_layers = nn.ModuleList(layers)
        self.output_layer = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        for layer in self.hidden_layers:
            x = self.activation(layer(x))
        return self.output_layer(x)