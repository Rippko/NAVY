# 3D Fraktální Generátor s pomocí **Iterated Function Systems (IFS)**

## Jak to funguje?

Tento kód využívá konceptu **IFS**, kde se opakovaně aplikuje náhodně zvolená afinní transformace na bod v prostoru. Postupným opakováním vznikají složité fraktální útvary.

---

## Struktura

- `main.py`: Hlavní soubor programu
- `models.py`: Obsahuje definice modelů

---

## Klíčové komponenty

### `iterate(num_iterations, starting_point=None)`

```python
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
   ```

- **Co dělá:** 
  Opakovaně aplikuje náhodně vybrané afinní transformace (lineární + posun) na počáteční bod, čímž vytváří body fraktálu.

- **Parametry:**
  - `num_iterations`: Počet iterací = počet generovaných bodů.
  - `starting_point`: Volitelný počáteční bod (defaultně `[0, 0, 0]`).

- **Jak to funguje:**
  1. Náhodně se vygeneruje pole indexů transformací.
  2. Každý index určuje, kterou transformaci použít v dané iteraci.
  3. Body se vypočítají podle vzorce: `new_point = A @ point + b`.
---

### `create_model_transforms(model_params)`

```python
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
   ```

- **Co dělá:** 
  Převádí seznam parametrů modelu na konkrétní matice `A` (3×3) a vektory `b` (3×1), které se používají při generování bodů.

- **Parametry:**
  - `model_params`: Seznam 12-prvkových řádků (čísla určující jednotlivé transformace).

- **Vrací:** 
  Seznam dvojic `(A, b)`, kde `A` je transformační matice a `b` posunový vektor.

---

## Výstup

Po dokončení se vygenerovaný fraktál uloží jako interaktivní HTML soubor, který si můžete otevřít v libovolném prohlížeči.

---

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.

---
