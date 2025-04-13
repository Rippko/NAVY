# **Fractal L-System**

Tato aplikace umožňuje generovat fraktální vzory pomocí **L-systémů** (Lindenmayerových systémů) s interaktivním grafickým rozhraním v Pythonu. Používá knihovny `tkinter` pro GUI a `turtle` pro vykreslování vzorů.

---

##  **Hlavní komponenty**

### 1. **`expand_l_system(axiom, rules, iterations)`**

Tato metoda slouží k **postupné tvorbě řetězce, který reprezentuje fraktální vzor**. Začíná se s výchozím řetězcem (*axiom*) a v každé iteraci se **každý znak nahradí podle zadaných pravidel (rules)**. Tento proces se opakuje tolikrát, kolik určuje parametr `iterations`.

Metoda vrací finální řetězec, který slouží jako vstup pro kreslení pomocí turtle grafiky.

#### Příklad:
```python
axiom = "F"
rules = {"F": "F+F--F+F"}
iterations = 2
```

Vývoj řetězce:
- Iterace 0: `F`
- Iterace 1: `F+F--F+F`
- Iterace 2: `F+F--F+F+F+F--F+F--F+F--F+F+F+F--F+F`

```python
def expand_l_system(self, axiom, rules, iterations):
    current = axiom
    for _ in range(iterations):
        next_gen = ""
        for char in current:
            next_gen += rules.get(char, char)
        current = next_gen
    return current
```

---

### 2. **`render_l_system(l_string, angle, start_x, start_y, line_width, line_length)`**

Tato metoda **vykreslí finální řetězec L-systému pomocí `turtle`**. Každý znak ve vstupním řetězci reprezentuje určitou akci:

- `F`: posun dopředu s kreslením
- `b`: posun dopředu bez kreslení
- `+`: otočení doprava o daný úhel
- `-`: otočení doleva o daný úhel
- `[`: uložení aktuální pozice a směru
- `]`: obnovení poslední uložené pozice a směru


```python
def render_l_system(self, l_string, angle, start_x, start_y, line_width, line_length):
    self._turtle.reset()
    self._turtle.pensize(line_width)
    self._turtle.speed(0)
    self._turtle.hideturtle()

    self._screen.tracer(0)
    self._turtle.penup()
    self._turtle.setposition(start_x, start_y)
    self._turtle.pendown()

    position_stack = deque()

    for char in l_string:
        if char == 'F':
            self._turtle.forward(line_length)
        elif char == 'b':
            self._turtle.penup()
            self._turtle.forward(line_length)
            self._turtle.pendown()
        elif char == '+':
            self._turtle.right(angle)
        elif char == '-':
            self._turtle.left(angle)
        elif char == '[':
            position_stack.append((self._turtle.position(), self._turtle.heading()))
        elif char == ']':
            if position_stack:
                pos, heading = position_stack.pop()
                self._turtle.penup()
                self._turtle.setposition(pos)
                self._turtle.setheading(heading)
                self._turtle.pendown()

    self._screen.update()
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))
```

---

## **GUI komponenty (stručně)**

Aplikace obsahuje grafické uživatelské rozhraní, kde lze:
- Zadávat vlastní axiom, pravidla a úhel
- Vybrat počet iterací
- Měnit tloušťku a délku čar
- Spouštět přednastavené fraktály
- Vyčistit plátno

Všechny tyto ovládací prvky jsou implementovány pomocí knohovny `tkinter`.

---

## **Ukázka výstupů:**

![Example01](/L-systems/screens/example01.PNG)
![Example02](/L-systems/screens/example02.PNG)

---
## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.

---