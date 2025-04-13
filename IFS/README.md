# 3D Fraktální Generátor s pomocí **Iterated Function Systems (IFS)**

## Jak to funguje?

Tento kód využívá konceptu **IFS**, kde se opakovaně aplikuje náhodně zvolená afinní transformace na bod v prostoru. Postupným opakováním vznikají složité fraktální útvary.

---

## Klíčové komponenty

### `iterate(num_iterations, starting_point=None)`

Tato metoda je jádrem generování fraktálu.

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

Tato metoda připraví transformační pravidla pro fraktál.

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

## Struktura

- `main.py`: Hlavní soubor programu
- `models.py`: Obsahuje definice modelů

---