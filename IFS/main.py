import numpy as np
import plotly.graph_objects as go
from models import all_models, model_names, model_colors
import time

class FractalFern3D:
    def __init__(self, transforms):
        self.transforms = transforms
        self.points = []
    
    def iterate(self, num_iterations, starting_point=None):
        current_point = np.zeros(3) if starting_point is None else np.array(starting_point)
        
        points = np.zeros((num_iterations + 1, 3))
        points[0] = current_point
        
        transform_indices = np.random.randint(0, len(self.transforms), num_iterations)
        
        for i in range(num_iterations):
            A, b = self.transforms[transform_indices[i]]
            current_point = A @ current_point + b
            points[i+1] = current_point
            
        self.points = points
    
    def plot(self, figure_title, color='green', opacity=0.8, size=2):
        fig = go.Figure(data=[go.Scatter3d(
            x=self.points[:, 0],
            y=self.points[:, 1],
            z=self.points[:, 2],
            mode='markers',
            marker=dict(
                size=size,
                color=color,
                opacity=opacity
            )
        )])
        
        fig.update_layout(
            title=figure_title,
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='data'
            ),
            width=900,
            height=800,
            margin=dict(l=0, r=0, b=0, t=40)
        )
        
        return fig

def create_model_transforms(model_params):
    transforms = []
    for params in model_params:
        a, b, c, d, e, f, g, h, i, j, k, l = params
        
        A = np.array([
            [a, b, c],
            [d, e, f],
            [g, h, i]
        ])
        b = np.array([j, k, l])
        transforms.append((A, b))
    
    return transforms

def main():    
    print("=== 3D Fraktální Generátor ===")
    print("Dostupné modely:")
    
    for model_id, model_name in model_names.items():
        print(f"{model_id}. {model_name}")

    while True:
        model_choice = input(f"\nVyberte číslo modelu (1-{len(all_models)}): ")
        if model_choice in model_names.keys():
            break
        print(f"Neplatná volba. Vyberte číslo mezi 1-{len(all_models)}.")

    selected_model_params = all_models[f"model{model_choice}"]
    model_name = model_names[model_choice]
    model_color = model_colors[model_choice]

    try:
        num_input = input("Počet bodů (výchozí: 50000): ")
        num_points = int(num_input) if num_input.strip() else 50000
        if num_points <= 0:
            raise ValueError("Počet bodů musí být kladné číslo")
    except ValueError as e:
        print(f"Neplatný počet bodů: {e}. Použiji výchozí hodnotu 50000.")
        num_points = 50000

    custom_color = input(f"Barva (výchozí: {model_color}): ")
    if custom_color.strip():
        model_color = custom_color
    

    try:
        size_input = input("Velikost bodů (výchozí: 1.5): ")
        point_size = float(size_input) if size_input.strip() else 1.5
        if point_size <= 0:
            raise ValueError("Velikost bodů musí být kladné číslo")
    except ValueError as e:
        print(f"Neplatná velikost bodů: {e}. Použiji výchozí hodnotu 1.5.")
        point_size = 1.5
    

    try:
        opacity_input = input("Průhlednost (0-1, výchozí: 0.8): ")
        opacity = float(opacity_input) if opacity_input.strip() else 0.8
        if opacity < 0 or opacity > 1:
            raise ValueError("Průhlednost musí být mezi 0 a 1")
    except ValueError as e:
        print(f"Neplatná průhlednost: {e}. Použiji výchozí hodnotu 0.8.")
        opacity = 0.8
    
    file_name = input(f"Název výstupního souboru (výchozí: fern_model{model_choice}.html): ")
    if not file_name.strip():
        file_name = f"fern_model{model_choice}.html"
    elif not file_name.endswith(".html"):
        file_name += ".html"
    
    print(f"\n--- Generuji model: {model_name} ---")
    
    transforms = create_model_transforms(selected_model_params)
    fern = FractalFern3D(transforms)
    
    print(f"Generuji {num_points} bodů...")
    start_time = time.time()
    
    fern.iterate(num_points)
    
    end_time = time.time()
    print(f"Generování dokončeno za {end_time - start_time:.2f} sekund.")
    
    fig = fern.plot(f"3D Fraktál - {model_name}", color=model_color, opacity=opacity, size=point_size)
    fig.write_html(file_name)
    print(f"Model uložen jako '{file_name}'")
    
    if input("Zobrazit model v prohlížeči? (a/n): ").lower() in ['a', 'ano', 'y', 'yes']:
        fig.show()
    
    if input("\nChcete generovat další model? (a/n): ").lower() in ['a', 'ano', 'y', 'yes']:
        main()
    else:
        print("https://www.youtube.com/watch?v=C27NShgTQE4&ab_channel=NSYNCVEVO")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram přerušen uživatelem.")
    except Exception as e:
        print(f"\nDošlo k chybě: {e}")