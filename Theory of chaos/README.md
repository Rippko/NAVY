# Theory of chaos: Logistic map, chaotic numbers and their prediction

Implementace neuronové sítě pro predikci chování logistické mapy - fundamentálního modelu v teorii chaosu. Kód demonstruje, jak lze pomocí neuronových sítí modelovat a potenciálně předvídat chaotické chování.

## O logistické mapě

Logistická mapa je jednoduchá nelineární diferenční rovnice s komplexním chováním:

```
x_{n+1} = a * x_n * (1 - x_n)
```

kde:
- `a` je parametr, který řídí chování systému (obvykle v rozmezí 0 až 4)
- `x` je hodnota v intervalu [0, 1]

Chování logistické mapy se mění s hodnotou parametru `a`:
- Pro `a < 3`, systém konverguje k jednomu bodu
- Pro `3 < a < ~3.57`, systém osciluje mezi několika body (dochází k bifurkacím)
- Pro `a > ~3.57`, systém začíná vykazovat chaotické chování

## Struktura projektu

- `config.py` - Konfigurační parametry
- `data.py` - Generování a příprava dat z logistické mapy
- `model.py` - Definice neuronové sítě
- `train.py` - Trénovací funkce
- `visualize.py` - Vizualizace trajektorií a bifurkačních diagramů
- `main.py` - Hlavní skript spojující všechny komponenty

## Jak to funguje

1. **Generování dat**: Vytváříme data pomocí logistické mapy pro různé hodnoty parametru `a`
2. **Trénování modelu**: Používáme neuronovou síť k naučení mapování ze stavu `[a, x_n]` na následující stav `x_{n+1}`
3. **Predikce**: Model predikuje trajektorie pro různé hodnoty parametru `a`
4. **Vizualizace**: Porovnání skutečných a predikovaných trajektorií a bifurkačních diagramů


## Podrobný popis komponent

### 1. Generování dat (`data.py`)
Generujeme data z iterací logistické mapy pro různé hodnoty parametru `a`. Pro každou hodnotu parametru:
- Začínáme s `x = 0.5`
- Provádíme počáteční iterace pro ustálení systému, které následně zahazujeme
- Zaznamenáváme dvojice `([a, x_n], x_{n+1})` pro trénování

### 2. Model (`model.py`)
Implementujeme neuronovou síť s následujícími vlastnostmi:
- Vstup: 2 neurony (pro hodnoty `a` a `x_n`)
- Několik skrytých vrstev (v našem případě 3)
- Výstup: 1 neuron (predikce `x_{n+1}`)

### 3. Trénování (`train.py`)
Rozdělujeme data na trénovací a validační sady, trénujeme neuronovou síť minimalizací MSE mezi skutečnými a predikovanými hodnotami.

### 4. Vizualizace (`visualize.py`)
Implementujeme dvě hlavní vizualizace:
- **Trajektorie**: Porovnání skutečných a predikovaných trajektorií pro konkrétní hodnotu `a`
- **Bifurkační diagram**: Grafické znázornění dlouhodobého chování systému pro různé hodnoty parametru `a`

## Ukázky výstupů

### 1. Trajektorie pro a = 3.7
![](/Theory%20of%20chaos/screens/trajectory.png)

### 2. Skutečný bifurkační diagram
![](/Theory%20of%20chaos/screens/original_diagram.png)

### 3. Predikovaný bifurkační diagram
- Model s 64 neurony

![](/Theory%20of%20chaos/screens/64_model.png)

- Model se 128 neurony

![](/Theory%20of%20chaos/screens/128_model.png)

- Model s 256 neurony

![](/Theory%20of%20chaos/screens/256_model.png)

## Interpretace výsledků

### Co můžeme pozorovat:
- Pro nižší hodnoty `a`, neuronová síť dokáže dobře předpovídat chování logistické mapy
- Pro chaotické režimy (např. `a > 3.57`), predikce se stává obtížnější
- Model je schopen zachytit základní strukturu bifurkačního diagramu, ale s určitými nepřesnostmi

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.
