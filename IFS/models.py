model1_params = [
    [0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00],
    [0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24, 0.00, 0.80, 0.00],
    [-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24, 0.00, 0.22, 0.00],
    [0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84, 0.00, 0.80, 0.00]
]

model2_params = [
    [0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00],
    [0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.22, -0.45, 0.00, 1.00, 0.00],
    [-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45, 0.00, 1.25, 0.00],
    [0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49, 0.00, 2.00, 0.00]
]

model3_params = [
    [0.05, 0.00, 0.00, 0.00, 0.55, 0.00, 0.00, 0.00, 0.45, 0.00, 0.00, 0.00],
    [0.45, -0.32, 0.12, 0.32, 0.45, 0.12, -0.12, 0.12, 0.55, 0.00, 0.70, 0.10],
    [-0.35, 0.22, -0.15, 0.22, 0.35, 0.22, 0.15, -0.15, 0.45, 0.00, 1.25, 0.00],
    [0.46, -0.12, 0.28, 0.12, 0.46, 0.28, 0.08, -0.28, 0.46, 0.00, 1.80, 0.20]
]


all_models = {
    "model1": model1_params,
    "model2": model2_params,
    "model3": model3_params,
}

model_names = {
    "1": "Klasická kapradina",
    "2": "Druhá kapradina",
    "3": "Spirálová kapradina",
}

model_colors = {
    "1": "green",
    "2": "blue",
    "3": "purple",
}