# Double pendulum - dvojté kyvadlo

Tento program simuluje a animuje pohyb dvojitého kyvadla - fyzikálního systému, který vykazuje chaotické chování a je často používán pro demonstraci teorie chaosu.  
Dvojité kyvadlo je jedním z nejjednodušších příkladů chaotického systému.  
Přestože je popsáno jednoduchými rovnicemi, jeho chování je velmi složité.

## O co jde?

Dvojité kyvadlo se skládá ze dvou tyčí se závažími, kde druhá tyč je připevněna ke konci první tyče:
- Při malých výchylkách se chová předvídatelně
- Při větších výchylkách vykazuje chaotické chování
- Malé změny v počátečních podmínkách vedou k dramaticky odlišným trajektoriím

## Co program dělá

1. Vypočítá pohyb dvojitého kyvadla pomocí diferenciálních rovnic
2. Zobrazuje plynulou animaci pohybu kyvadla
3. Sleduje a zobrazuje trajektorii druhého závaží
4. Kontroluje zachování energie systému

### Parametry modelu
V kódu můžete upravit následující parametry:
- `L1`, `L2`: délky tyčí (v metrech)
- `m1`, `m2`: hmotnosti závaží (v kilogramech)
- `g`: gravitační zrychlení (m/s²)
- `y0`: počáteční podmínky [úhel1, rychlost1, úhel2, rychlost2]
- `tmax`: maximální doba simulace (v sekundách)
- `dt`: časový krok pro výpočet (v sekundách)
- `fps`: počet snímků za sekundu v animaci

### Lagrangeova formulace mechaniky

Rovnice pohybu dvojitého kyvadla vycházejí z Lagrangeovy mechaniky. Tento systém je definován jako:
L = T - V, kde:
- T je kinetická energie systému
- V je potenciální energie systému

### Pohybové rovnice v kódu

V programu jsou pohybové rovnice implementovány ve funkci `deriv`, která počítá časové derivace pro:
- `theta1`: úhel prvního kyvadla
- `z1`: úhlová rychlost prvního kyvadla
- `theta2`: úhel druhého kyvadla
- `z2`: úhlová rychlost druhého kyvadla

Tyto rovnice zahrnují:
- Gravitační sílu působící na obě závaží
- Odstředivé a Coriolisovy síly vznikající při pohybu
- Vzájemné působení obou kyvadel

Numerické řešení těchto rovnic pomocí `odeint` pak poskytuje časový vývoj všech proměnných, což umožňuje animovat celý systém.

### Vykreslování animace
Program používá modul `FuncAnimation` z knihovny Matplotlib pro vytvoření plynulé animace:
- Modré kolečko reprezentuje první závaží
- Červené kolečko reprezentuje druhé závaží
- Červená čára zobrazuje trajektorii druhého závaží za poslední sekundu
- Text v levém horním rohu ukazuje aktuální čas simulace

## Ukázka výstupu
![](/Double%20pendulum/screens/screenshot.PNG)


## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.



