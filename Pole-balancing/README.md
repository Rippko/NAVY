# Trénink agenta pomocí Deep Q-Learning pro prostředí CartPole

Implementace algoritmu Deep Q-Learning (DQN) pro řešení problému CartPole z knihovny OpenAI Gym. Cílem je natrénovat agenta, který dokáže udržet tyč ve vzpřímené poloze co nejdéle.

## O problému CartPole

CartPole je klasický problém z oblasti posilovaného učení (reinforcement learning), kde se agent snaží udržet tyč balancující na vozíku. Agent může v každém kroku posunout vozík doleva nebo doprava. Cílem je udržet tyč ve vzpřímené poloze co nejdéle, přičemž epizoda končí, když:
- Tyč se nakloní o více než 15 stupňů od vertikální polohy
- Vozík vyjede z definovaného prostoru
- Je dosaženo maximálního počtu kroků (500 v prostředí CartPole-v1)

## Klíčové komponenty kódu

### 1. DQN Agent
Agent používá hlubokou neuronovou síť (QNetwork) k aproximaci Q-hodnot pro jednotlivé akce. Při tréninku využívá následující techniky:
- **Epsilon-greedy strategie**: Vyvažuje exploraci (průzkum) a exploitaci (využívání naučeného). Hodnota epsilon postupně klesá z 1.0 na 0.01.
- **Experience Replay**: Ukládá zkušenosti (stavy, akce, odměny) do paměti a učí se z náhodných dávek těchto zkušeností.

### 2. Neuronová síť (QNetwork)
Jednoduchá plně propojená neuronová síť s architekturou:
- Vstupní vrstva: velikost stavu (4 hodnoty pro CartPole)
- 2 skryté vrstvy s 24 neurony a ReLU aktivací
- Výstupní vrstva: velikost akčního prostoru (2 akce pro CartPole)

### 3. ReplayBuffer
Paměť pro ukládání zkušeností agenta, ze které se náhodně vzorkují dávky pro trénink.

### 4. Vizualizace
Kód obsahuje funkce pro:
- Vizualizaci natrénovaného agenta v prostředí
- Vykreslení grafu vývoje skóre během tréninku

## Parametry tréninku

```
EPISODES = 500         # Maximální počet epizod tréninku
GAMMA = 0.99           # Diskontní faktor pro budoucí odměny
EPSILON_START = 1.0    # Počáteční hodnota epsilon (pravděpodobnost náhodné akce)
EPSILON_END = 0.01     # Koncová hodnota epsilon
EPSILON_DECAY = 0.995  # Rychlost poklesu epsilon
MEMORY_SIZE = 10000    # Velikost paměti pro zkušenosti
BATCH_SIZE = 64        # Velikost dávky pro učení
LEARNING_RATE = 0.001  # Rychlost učení
```

## Jak to funguje

1. **Inicializace**: Vytvoření prostředí, agenta a jeho neuronové sítě.
2. **Trénink**:
   - V každé epizodě agent interaguje s prostředím, vybírá akce a získává odměny.
   - Zkušenosti se ukládají do ReplayBuffer.
   - Agent se pravidelně učí z náhodných dávek zkušeností.
   - Hodnota epsilon postupně klesá, což vede k menšímu průzkumu a většímu využívání naučené strategie.
3. **Ukončení tréninku**: Trénink končí dosažením maximálního počtu epizod nebo když agent dosáhne průměrného skóre 295+ bodů za posledních 100 epizod.
4. **Vizualizace**: Po tréninku se spustí vizualizace natrénovaného agenta a vykreslí se graf vývoje skóre.

## Vývoj skóre během tréninku

- **Vývoj skóre během tréninku**

![](/Pole-balancing/screens/training_results.png)

Graf ukazuje, jak se postupně zlepšovala schopnost agenta udržet tyč ve vzpřímené poloze. Vyšší hodnoty znamenají delší dobu balancování tyče.

## Ukázka balancingu

![](/Pole-balancing/screens/cartpole_solution.gif)

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.