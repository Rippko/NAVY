import matplotlib.pyplot as plt

class History:
    def __init__(self):
        self.error_history = []
        self.weights_history = []
        self.bias_history = []
        self.gradient_history = []
    
    def log(self, error, weights, biases, gradients):
        self.error_history.append(error)
        self.weights_history.append([w.copy() for w in weights])
        self.bias_history.append([b.copy() for b in biases])
        self.gradient_history.append([g.copy() for g in gradients])
    
    def plot_error(self):
        plt.plot(self.error_history)
        plt.xlabel("Epochs")
        plt.ylabel("Error")
        plt.title("Error Function Over Time")
        # plt.show()