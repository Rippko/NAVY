# Find the Cheese - Q-Learning

## Úvod
Tato aplikace interaktivně vizualizuje proces učení Q-learningu tím, že ukazuje, jak se agent (chodec) postupně učí navigovat v mřížkovém prostředí, aby dosáhl cíle (sýr) a vyhnul se překážkám (díry). Učení probíhá v reálném čase, což umožňuje uživatelům sledovat, jak se agentovo rozhodování postupně zlepšuje.

## Funkce

- Interaktivní mřížka, kde mohou uživatelé umístit agenta, sýr a překážky
- Vizualizace procesu Q-learningu v reálném čase
- Nastavitelná rychlost učení
- Vizuální reprezentace naučené strategie pomocí intenzity barev
- Vizualizace nejlepší nalezené cesty
- Podrobné zobrazení Q-tabulky
- Sledování statistik tréninku

## Jak to funguje ?

Q-learning jakožto algoritmus posilovaného učení, který se učí hodnotu akcí ve stavech tím, že zažívá výsledky a aktualizuje své znalosti. Agent udržuje Q-tabulku, která ukládá očekávanou užitečnost provedení konkrétní akce v konkrétním stavu.

V této implementaci:
- **Stavy**: Každá buňka v mřížce představuje stav (řádek, sloupec)
- **Akce**: Agent se může pohybovat ve čtyřech směrech (nahoru, doprava, dolů, doleva)
- **Odměny**: 
  - Přesun na prázdnou buňku: -1 (malá penalizace pro podporu hledání nejkratší cesty)
  - Pád do díry: -100 (významná penalizace)
  - Nalezení sýra: +100 (cílová odměna)

### Klíčové komponenty implementace

#### 1. Nastavení prostředí

Třída `FindTheCheeseGame` inicializuje prostředí mřížky s:
```python
self.q_table = np.zeros((rows, cols, 4))  # Q-tabulka: (řádek, sloupec, akce)
self.actions = ['up', 'right', 'down', 'left']
```

#### 2. Parametry Q-Learningu

Algoritmus používá několik parametrů, které řídí proces učení:
```python
self.epsilon = 1.0
self.epsilon_decay = 0.99
self.epsilon_min = 0.01
self.alpha = 0.1
self.gamma = 0.9
```

- **Epsilon (ε)**: Řídí poměr průzkumu vs. využívání už známých cest. Vysoká hodnota podporuje náhodné akce (průzkum), zatímco nízká hodnota podporuje následování nejlépe známé cesty (využívání).
- **Epsilon Decay**: Postupně snižuje průzkum, jak se agent učí.
- **Alpha (α)**: Rychlost učení, která určuje, jak moc nové informace přepisují staré informace.
- **Gamma (γ)**: Diskontní faktor, který určuje důležitost budoucích odměn.

#### 3. Mechanismus aktualizace Q-tabulky

Jádrem Q-learningu je pravidlo aktualizace implementované v metodě `update_q_table`:

```python
def update_q_table(self, current_pos, action_idx, next_pos, reward):
    current_q = self.q_table[current_pos[0], current_pos[1], action_idx]
    best_next_q = np.max(self.q_table[next_pos[0], next_pos[1]])
    new_q = current_q + self.alpha * (reward + self.gamma * best_next_q - current_q)
    self.q_table[current_pos[0], current_pos[1], action_idx] = new_q
```

Tato funkce implementuje vzorec Q-learningu:

Q(s,a) ← Q(s,a) + α[r + γ max<sub>a'</sub> Q(s',a') - Q(s,a)]

Kde:
- s, a jsou aktuální stav a akce
- s', a' jsou následující stav a potenciální akce
- r je odměna
- α je rychlost učení
- γ je diskontní faktor

#### 4. Výběr akce pomocí Epsilon-Greedy strategie

Používáme tzv. epsilon-greedy strategii k vyvážení průzkumu a využívání:

```python
# epsilon-greedy strategie
if random.random() < self.epsilon:
    action_idx = random.randint(0, 3)
else:
    action_idx = np.argmax(self.q_table[current_pos[0], current_pos[1]])
```

- S pravděpodobností ε vybere náhodnou akci (průzkum)
- S pravděpodobností 1-ε vybere akci s nejvyšší Q-hodnotou (využívání)

#### 5. Proces tréninku

Proces tréninku je implementován v metodách `single_step` a `train_step`:

```python
def train_step(self):
    if not self.is_training:
        self.train_button.config(text="Start Learning")
        return
    
    if self.training_speed <= 10:
        iterations_per_update = 50
        for _ in range(iterations_per_update):
            if not self.is_training:
                break
            self.single_step(update_ui=False)
        
        self.update_training_ui()
    else:
        self.single_step(update_ui=True)
    
    self.root.after(max(1, self.training_speed), self.train_step)
```

Trénink může být:
- Vizualizován krok za krokem s nastavitelnou rychlostí
- Spuštěn v dávkovém režimu pro rychlejší učení
- Monitorován prostřednictvím úspěšnosti, počtu iterací a míry průzkumu

#### 6. Výpočet a vizualizace cesty

Po tréninku je nejlepší cesta vypočítána na základě naučených Q-hodnot:

```python
def calculate_best_path(self):
    path = []
    current = self.initial_pos
    
    while current != self.cheese_pos and step_count < max_steps:
        path.append(current)
        
        # nejlepší akce z aktuální pozice
        action_idx = np.argmax(self.q_table[current[0], current[1]])
        # Výpočet nové pozice na základě akce
        # ...
        
        current = (new_row, new_col)
        
        if current in self.holes:
            break
```

Tato cesta je poté vizualizována, aby se demonstrovalo, co se agent naučil.

#### 7. Vizuální zpětná vazba
- Barvy buněk odrážejí nejvyšší Q-hodnoty (silnější barvy indikují silnější preference)
- Míra úspěšnosti ukazující procento úspěšných epizod
- Aktuální míra průzkumu (epsilon)
- Počet trénovacích iterací

### Ovládání

- **Start/Stop Learning**: Spouští nebo pozastavuje proces Q-learningu
- **Visualize Best Path**: Zobrazuje nejlepší cestu nalezenou agentem po tréninku (dostupné pouze pokud agent našel správnou cestu, alespoň 1x)
- **Single Step**: Provede jeden krok učení
- **Reset Learning**: Vymaže naučená data, ale zachová nastavení mřížky
- **Display Q-Table**: Zobrazuje aktuální Q-hodnoty pro každý pár stav-akce
- **Clear Grid**: Resetuje celé prostředí
- **Speed Slider**: Upravuje rychlost vizualizace tréninku (nedoporučuji měnit trénování je poté extrémně zdlouhavé)


## Pokročilé nastavení
### Úprava parametrů učení

Můžeme experimentovat s různými parametry učení úpravou následujících proměnných:
- `self.alpha`: Rychlost učení (jak rychle nové informace přepisují staré)
- `self.gamma`: Diskontní faktor (důležitost budoucích odměn)
- `self.epsilon`, `self.epsilon_decay`, `self.epsilon_min`: Řídí strategii průzkumu

### Odměny agenta za jednotlivé akce

Strukturu odměn lze upravit změnou:
- `self.move_reward`: Odměna za přesun na prázdnou buňku
- `self.hole_reward`: Odměna za pád do díry
- `self.cheese_reward`: Odměna za nalezení sýra

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.
