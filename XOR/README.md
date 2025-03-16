# **Neuronová síť (ANN) v Pythonu**

Implementace jednoduché neuronové sítě (ANN) s jednou skrytou vrstvou. Síť je trénována pomocí zpětné propagace na logickou funkci XOR.

## **Popis kódu**
Neuronová síť obsahuje:
- **Vstupní vrstvu** (2 vstupy)
- **Skrytou vrstvu** (2 neurony)
- **Výstupní vrstvu** (1 neuron)

Síť používá **aktivační funkci sigmoid** a metodu **gradientního sestupu** pro optimalizaci vah.

## **Hlavní metody**
### `train(X, y)` - Trénování neuronové sítě  
### 1️⃣ Dopředná propagace (Forward propagation)  
- Vstupní data se vynásobí vahami a přičtou se biasy.  
- Použije se aktivační funkce sigmoid, která převede vstupy na výstupy skryté vrstvy.  
- Výstupy skryté vrstvy se použijí jako vstupy do výstupní vrstvy, kde se proces opakuje.  

### 2️⃣ Výpočet chyby (SSE - Sum of Squared Errors)  
- Chyba se vypočítá jako součet druhých mocnin rozdílů mezi skutečným a předpovězeným výstupem.  

### 3️⃣ Zpětná propagace (Backpropagation)  
- Spočítá se, jak moc se neuron spletl a jak tuto chybu opravit.  
- Pomocí derivace sigmoidové funkce se určí směr a velikost opravy. (gradient)
- Chyba se šíří zpět do skryté vrstvy, kde se opět počítají gradienty.  

### 4️⃣ Aktualizace vah a biasů  
- Každá váha a bias se upraví podle vypočítaných gradientů.  
- Úpravy probíhají podle nastavené rychlosti učení (`learning rate`).  

### 5️⃣ Sledování průběhu učení  
- Každou epochu se ukládá průběh chyb a upravené hodnoty vah.  
- Po každé epoše se vypisuje stav učení.  

---------------------------------------------------------------------

## `predict(X)` - Predikce výstupu neuronové sítě  
Tato metoda slouží k předpovědi výstupu na základě naučených vah a biasů.  

### 1️⃣ Výpočet vstupu do skryté vrstvy  
- Vstupní data `X` se vynásobí vahami první vrstvy `W1` a přičtou se biasy `b1`, které byly předem natrénovány.  

### 2️⃣ Aktivace skryté vrstvy  
- Použije se aktivační funkce **sigmoid**, která převede vstupy na hodnoty mezi 0 a 1.  
- Výstup skryté vrstvy (`hidden_output`) se pak posílá do výstupní vrstvy.  

### 3️⃣ Výpočet výstupu neuronové sítě  
- Výstupy skryté vrstvy se vynásobí vahami druhé vrstvy `W2` a přičtou se biasy `b2` (opět předtrénované hodnoty). 
- Výsledek je vstup pro finální výstupní neurony.  

### 4️⃣ Aktivace výstupu  
- Na finální výpočet se opět aplikuje **sigmoid**, aby se výstup převedl na hodnotu mezi 0 a 1.  
- Tato hodnota představuje pravděpodobnost, že výstup odpovídá určité třídě (například 0 nebo 1 u XOR problému).  

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.

