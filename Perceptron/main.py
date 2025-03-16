import numpy as np
import matplotlib.pyplot as plt

# Generování 100 bodů
np.random.seed(42)
X = np.random.uniform(-10, 10, 100)  # Náhodné souřadnice pro x
Y = np.random.uniform(-10, 10, 100)  # Náhodné souřadnice pro y

# Cílové hodnoty (labely)
labels = np.where(Y > 3*X + 2, 1, -1)

# Inicializace váh perceptronu
w = np.random.rand(2)
b = np.random.rand(1)
learning_rate = 0.01

# Trénování perceptronu
for _ in range(100):
    for i in range(len(X)):
        x_vec = np.array([X[i], Y[i]])
        pred = np.sign(np.dot(w, x_vec) + b)
        if pred != labels[i]:  # Pokud je špatná predikce, upravíme váhy
            w += learning_rate * labels[i] * x_vec
            b += learning_rate * labels[i]

# Vizualizace
plt.figure(figsize=(8,6))
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle="--", linewidth=0.5)

# Původní přímka y = 3x + 2
x_line = np.linspace(-10, 10, 100)
y_line = 3*x_line + 2
plt.plot(x_line, y_line, 'k-', label="y = 3x + 2")

# Barvy bodů podle klasifikace
colors = ['red' if label == 1 else 'blue' for label in labels]
plt.scatter(X, Y, c=colors, edgecolors='black')

plt.legend()
plt.show()
