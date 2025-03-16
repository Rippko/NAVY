import numpy as np
import matplotlib.pyplot as plt
from history import History
import sys

class ANN:
    def __init__(self, input_size=2, hidden_size=2, output_size=1, learning_rate=0.1, epochs=10000):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.history = History()
        
        np.random.seed(0) # Nastavení seedu pro reprodukovatelnost výsledků
        # Inicializace vah a biasů
        self.W1 = np.random.uniform(-1, 1, (self.input_size, self.hidden_size))
        self.W2 = np.random.uniform(-1, 1, (self.hidden_size, self.output_size))
        self.b1 = np.zeros((1, self.hidden_size))
        self.b2 = np.zeros((1, self.output_size))
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def print_learning_progress(self, epoch, sse):
        if epoch % 100 == 0:
            progress = int((epoch / self.epochs) * 50)  # Počet vybarvených bloků
            bar = '█' * progress + '-' * (50 - progress)  # Vytvoření progress baru
            sys.stdout.write(f"\rEpoch {epoch}/{self.epochs} [{bar}] Error: {sse:.9f}")
            sys.stdout.flush()
            
        if epoch == self.epochs - 1:
            bar = '█' * 50
            sys.stdout.write(f"\rEpoch {self.epochs}/{self.epochs} [{bar}] Error: {sse:.9f}\n")
            sys.stdout.flush()
    
    def train(self, X, y):
        """
        Trénování neuronové sítě.
        """
        for epoch in range(self.epochs):
            # Forward propagace
            hidden_input = np.dot(X, self.W1) + self.b1
            hidden_output = self.sigmoid(hidden_input)
            final_input = np.dot(hidden_output, self.W2) + self.b2
            final_output = self.sigmoid(final_input)
            
            # Chyba (SSE)
            sse = np.sum(1/2 * (np.square(y - final_output)))
            
            # Zpětná propagace
            d_output = (y - final_output) * self.sigmoid_derivative(final_output) # výpočet gradientu
            d_hidden = d_output.dot(self.W2.T) * self.sigmoid_derivative(hidden_output)
            
            # Aktualizace vah
            self.W2 += hidden_output.T.dot(d_output) * self.learning_rate
            self.b2 += np.sum(d_output, axis=0, keepdims=True) * self.learning_rate
            self.W1 += X.T.dot(d_hidden) * self.learning_rate
            self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * self.learning_rate
            
            # Uložení historie a výpis průběhu učení
            self.history.log(sse, [self.W1, self.W2], [self.b1, self.b2], [d_output, d_hidden])
            self.print_learning_progress(epoch, sse)
    
    def predict(self, X):
        hidden_input = np.dot(X, self.W1) + self.b1
        hidden_output = self.sigmoid(hidden_input)
        final_input = np.dot(hidden_output, self.W2) + self.b2
        return self.sigmoid(final_input)
    
    def plot_decision_boundary(self, X, y):
        """
        Vykreslí rozhodovací hranici neuronové sítě.
        """
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                                np.linspace(y_min, y_max, 100))

        # Předpověď pro každý bod mřížky
        grid_points = np.c_[xx.ravel(), yy.ravel()]
        Z = self.predict(grid_points)  
        Z = Z.reshape(xx.shape)

        # Vykreslení rozhodovací hranice
        plt.figure(figsize=(6, 5))
        plt.contourf(xx, yy, Z, levels=[-1, 0.5, 2], alpha=0.6, cmap='viridis')

        # Vykreslení trénovacích bodů
        plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), edgecolors='k', cmap='viridis', s=100)
        plt.xlabel("Input 1")
        plt.ylabel("Input 2")
        plt.title("Decision Boundary for XOR Problem")

if __name__ == "__main__":
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    # Inicializace a trénování
    ann = ANN()
    ann.train(X, y)
    
    print("\nANN output values:")
    predictions = ann.predict(X)
    
    for i, (x_val, pred) in enumerate(zip(X, predictions)):
        final_pred = int(np.round(pred[0]))
        print(final_pred)
        print(f"Input values: {x_val}")
        print(f"Predicted value: {pred[0]:.9f}")
        print(f"Final predict: {final_pred}\n")
    
    # Vizualizace chyby
    ann.history.plot_error()
    ann.plot_decision_boundary(X, y)
    plt.show()
