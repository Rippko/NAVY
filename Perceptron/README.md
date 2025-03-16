# Perceptron - Klasifikace
Perceptron pro klasifikaci náhodně generovaných bodů v rovině. Cílem je rozdělit body do dvou tříd podle toho, na které straně přímky y = 3x + 2 leží. Perceptron se učí pomocí metody přírůstků a na základě chyb v predikci aktualizuje své váhy.

- Kód generuje 100 náhodných bodů v rovině, kde X a Y jsou souřadnice bodů.
- Na základě rovnice přímky y = 3x + 2 jsou body klasifikovány do dvou tříd:
- **Třída 1 (červená):** Body, které leží nad přímkou y = 3x + 2.
- **Třída -1 (modrá):** Body, které leží pod přímkou y = 3x + 2.

## Inicializace perceptronu:

Perceptron je inicializován s náhodnými váhami a biasem. Váhy a bias jsou použity pro rozhodování o klasifikaci bodů.

## Trénování perceptronu:

Postupně prochází všechny generované body a na základě jejich souřadnic predikuje, zda budou patřit do třídy 1 nebo -1.
Pokud je predikce špatná, perceptron upraví své váhy a bias na základě pravidla přírůstků.
Pokud je predikce špatná, váhy se aktualizují o součin učební míry (`learning_rate`), skutečné třídy bodu (`labels[i]`) a souřadnic bodu (`x_vec`).

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.