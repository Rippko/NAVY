# Hopfieldova síť

## Popis projektu
Implementace **Hopfieldovy neuronové síť** v jazyce Python s použitím knihovny Tkinter pro vizualizaci a interakci. 

Síť je schopna naučit se binární vzory, uložit je a následně obnovit poškozené nebo šumem ovlivněné vstupy.

---

## **Třída HopfieldNetwork**
Třída **HopfieldNetwork** obsahuje metody pro trénování sítě a obnovu vzorů.

## 1. **Inicializace sítě**

```python
class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))
```
### Jak to funguje?
- `size` – Určuje počet neuronů v síti. V našem případě 5×5 obrázku máme **25 neuronů**.
- `weights` – Vytváří **matici vah** mezi neurony. Každý neuron je propojen s každým jiným neuronem (ale ne sám se sebou). Na začátku mají všechny spoje váhu **0**.

## 2. **Trénování sítě (na základě uložených vzorů)**

```python
    def train(self, patterns):
        self.weights.fill(0)
        for pattern in patterns:
            pattern = pattern.reshape(-1, 1)
            self.weights += pattern @ pattern.T
        np.fill_diagonal(self.weights, 0)
```
1. **Inicializace vah na nulu** – Před učením vynulujeme všechny váhy.
2. **Hebbovo pravidlo** – Pro každý vzor provedeme maticový součin `pattern @ pattern.T` samotného patternu a jeho transponované verze pro výpočet matice váh.
3. **Nastavení diagonály na nulu** – Neuron nemůže ovlivňovat sám sebe, proto nastavíme **diagonální prvky** váhové matice na nulu.

## 3. **Obnova vzoru**

```python
    def recover(self, pattern, method="synchronous", max_iter=1000):
        pattern = pattern.copy()
        previous_pattern = None

        for current_iter in range(max_iter):
            if method == "synchronous":
                pattern = np.sign(self.weights @ pattern)
            else:
                for i in range(self.size):
                    pattern[i] = np.sign(np.dot(self.weights[:, i], pattern))
            
            if previous_pattern is not None and np.array_equal(pattern, previous_pattern):
                break
            
            previous_pattern = pattern.copy()
        print(f"Iterations: {current_iter + 1}")
        return pattern
```

### Jak to funguje?
1. **Metoda `recover` obdrží poškozený vzor**, který chceme opravit ze vstupu.
2. **Synchronní aktualizace**: Pokud je zvolená metoda **synchronous**, aktualizují se všechny neurony současně v jednom kroku.
3. **Asynchronní aktualizace**: Pokud je metoda **asynchronous**, aktualizujeme neurony **jeden po druhém**.
4. **Podmínka zastavení**:
   - Pokud vzor **zůstane stejný jako v předchozím kroku**, algoritmus se zastaví.
   - Pokud dosáhneme maximálního počtu iterací (`max_iter`), také se zastavíme.
5. **Vracíme opravený vzor** a vypíšeme počet provedených iterací.


## 4. **Shrnutí**
- Síť se učí podle **Hebbova pravidla** a ukládá vzory do váhové matice.  
- Síť je schopná obnovovat vzor buď **synchronně** nebo **asynchronně**.
- Proces se zastaví, pokud se vzor přestane měnit respektive je obnoven správně nebo po dosažení maximálního počtu iterací.
- Síť umí opravovat správně vzory pokud se nepřekročí stanovená hranice pro maximální počet uložených vzorů dle:

# Maximální kapacita sítě

```python
max_patterns = np.floor(network.size / (2 * math.log2(network.size)))
```

Matematicky vyjádřeno:

$$ M_{max} = \left\lfloor\frac{N}{2\log_2(N)}\right\rfloor $$

kde:
- $M_{max}$ je maximální počet vzorů, které síť dokáže spolehlivě uložit a fungovat korektně
- $N$ je počet neuronů v síti (v našem případě N = 25 pro mřížku 5×5)
- $\lfloor \rfloor$ označuje funkci floor (zaokrouhlení dolů)

Pro naši implementaci s mřížkou 5×5:
$$ M_{max} = \left\lfloor\frac{25}{2\log_2(25)}\right\rfloor $$

> **Poznámka**: V původní definici Hopfieldovy sítě se často používá přirozený logaritmus $\ln$, 
> ale v mé implementaci používám $\log_2$ dle [definice Hopfieldovy sítě](https://en.wikipedia.org/wiki/Hopfield_network).

---

## **GUI aplikace**
Aplikace využívá **Tkinter** k vizualizaci vzorů a interakci s uživatelem.

### **Hlavní funkce aplikace**

#### **Vykreslování mřížky**
```python
def draw_grid(canvas, grid):
```
- Vykresluje **5x5 mřížku**, kde černá buňka = 1, bílá buňka = 0.

#### **Uložení vzoru**
```python
def save_pattern(patterns, grid, network, canvas, root):
```
- Ukládá vzor do seznamu naučených vzorů a přetrénuje síť.

#### **Obnova vzoru**
```python
def restore_pattern(network, grid, canvas, method="synchronous"):
```
- Používá síť k obnově vstupního vzoru.

#### **Přidání šumu**
```python
def add_noise(grid, canvas, noise_level=0.1):
```
- Náhodně otočí **určitý počet pixelů**, čímž do vzoru přidá šum.

#### **Zobrazení uložených vzorů**
```python
def show_saved_patterns(patterns, network, root):
```
- Otevře nové okno se seznamem vzorů a jejich detaily.

---

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.

---

