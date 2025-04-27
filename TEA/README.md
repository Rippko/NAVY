# TEA

TEA je aplikace pro generování a prozkoumávání fraktálních obrazců. Umožňuje interaktivní zobrazení Mandelbrotovy a Juliovy množiny s možností přiblížení a úpravy parametrů.

## Obsah aplikace

Aplikace se skládá ze tří hlavních souborů:

1. `fractal_computer.py` - Obsahuje třídu pro matematické výpočty fraktálů
2. `fractal_viewer.py` - Obsahuje třídu pro uživatelské rozhraní a interakci
3. `main.py` - Jednoduchý spouštěcí soubor

## Základní principy

### Mandelbrotova množina

Mandelbrotova množina je definována pomocí rekurzivního vzorce:

```
Z_{n+1} = Z_n^2 + C
```

kde Z a C jsou komplexní čísla. Výpočet začíná s Z_0 = 0 a C je pozice v komplexní rovině pro každý pixel. Pro každý bod C sledujeme, zda posloupnost Z_n zůstane omezená (patří do množiny) nebo diverguje k nekonečnu. 

Bod C je součástí Mandelbrotovy množiny, pokud posloupnost zůstává omezená i po nekonečném počtu iterací. V praxi je omezený počet iterací pro každý pixel, kde testujeme podmínku |Z| < 2. Pokud |Z| překročí hodnotu 2, víme že posloupnost diverguje.

### Juliova množina

Juliova množina používá stejný rekurzivní vzorec jako Mandelbrotova množina:

```
Z_{n+1} = Z_n^2 + C
```

Rozdíl je v tom, že při výpočtu Juliovy množiny je C konstantní pro celý obraz a Z_0 se mění podle pozice pixelu. Každá hodnota C vytváří jedinečnou Juliovu množinu, což umožňuje velkou variabilitu obrazců.

## Implementace výpočtů

### Třída FractalComputer


#### Klíčové metody:

- `compute_mandelbrot()` - Vypočítá Mandelbrotovu množinu pomocí NumPy pro efektivní výpočty.
- `compute_julia()` - Vypočítá Juliovu množinu pro zadanou konstantu C.
- `create_color_palette()` - Vytváří paletu barev založenou na HSV modelu pro vizualizaci fraktálů.

#### Algoritmus pro výpočet Mandelbrotovy množiny:

1. Vytvoříme mřížku komplexních čísel odpovídající každému pixelu.
2. Pro každý bod C (pixel) inicializujeme Z = 0.
3. Iterativně aplikujeme vzorec Z = Z^2 + C maximálně `max_iterations` krát.
4. Sledujeme, kdy |Z| překročí hodnotu 2, a uložíme počet iterací.
5. Podle počtu iterací přiřadíme barvu každému pixelu.

- Provádí vektorové výpočty pro celou mřížku bodů najednou
- Používá masky pro sledování bodů, které ještě nebyly určeny jako divergentní
- Minimalizuje čas výpočtu i pro velké rozlišení obrazů

## Uživatelské rozhraní

Třída `FractalViewer` implementuje grafické rozhraní pomocí knihovny Tkinter. Umožňuje:

- Přepínání mezi Mandelbrotovou a Juliovou množinou
- Nastavení počtu iterací (ovlivňuje detaily a rychlost vykreslení)
- Nastavení parametru C pro Juliovu množinu
- Interaktivní přibližování pomocí výběru oblasti myší
- Návrat na předchozí zobrazení
- Reset do výchozího zobrazení
- Aplikace ukládá historii zobrazení (pozice, měřítko, parametry), což umožňuje navigaci zpět pomocí tlačítka "Back".


## Ukázky výstupu
### Mandelbrotova množina
![](/TEA/screens/example01.PNG)

### Julia množina
![](/TEA/screens/example02.PNG)

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.

