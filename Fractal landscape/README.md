# Fractal landscape
Aplikace vytváří náhodně generovaný terén. Můžeme si vybrat mezi 2D a 3D zobrazením, nastavit počet iterací (které určují detailnost terénu) a drsnost, která ovlivňuje, jak moc členitý bude výsledný terén.

## Jak to funguje

Aplikace používá algoritmus "Midpoint Displacement" (přesouvání středového bodu), což je jednoduchá, ale efektivní metoda pro generování realisticky vypadajících přírodních útvarů:

### 2D terén

1. Začínáme s přímkou (od bodu 0 do bodu 1)
2. V každé iteraci:
   - Pro každý úsek přímky najdeme jeho střed
   - Posuneme tento střed nahoru nebo dolů o náhodnou hodnotu
   - Velikost posunu se s každou iterací zmenšuje (podle nastaveného parametru `roughness`)
3. Ve 2D zobrazení vytváříme 3 vrstvy (hory, kopce a nížina) pro lepší vizuální efekt

### 3D terén

1. Začínáme se čtvercem, kde máme definované výšky pouze v rozích
2. V každé iteraci:
   - Nejprve zpracujeme středy čtverců
   - Pak zpracujeme středy hran
   - Náhodně posuneme výšku každého nového bodu
   - Velikost posunu se s každou iterací zmenšuje
3. Nakonec obarvíme terén podle výškových úrovní (modrá pro vodu, zelená pro nížiny, hnědá pro hory)

## Hlavní metody

### `generate_2d_terrain(iterations, roughness)`

Tato metoda vytváří 2D fraktální terén:
- **Průběh**: Začíná s přímkou a postupně přidává body tím, že nachází střed mezi každými dvěma sousedními body a náhodně jej posouvá
- **Výstup**: Dvě pole - x-ové a y-ové souřadnice bodů terénu

### `generate_3d_terrain(iterations, roughness)`

Tato metoda vytváří 3D fraktální terén:
- **Průběh**: 
  1. Vytvoří mřížku o velikosti 2^iterations + 1
  2. Nastaví výšky v rozích
  3. Postupně zpracovává čtverce poloviční velikosti v každé iteraci
  4. Nejprve vypočítá výšku ve středu každého čtverce
  5. Poté vypočítá výšky na středech hran
- **Výstup**: 2D pole reprezentující výšky v jednotlivých bodech terénu

### `generate_terrain()`

Hlavní metoda, která se volá po stisknutí tlačítka "Generovat terén":
- Získá aktuální nastavení z uživatelského rozhraní
- Podle vybrané dimenze zavolá příslušnou metodu pro generování terénu
- Pro 2D vytvoří tři vrstvy terénu s různými barvami
- Pro 3D vytvoří terén a obarví jej podle výškových úrovní
- Zobrazí výsledek v grafu

## Ukázky výstupů
![](/Fractal%20landscape/screens/example01.PNG)
![](/Fractal%20landscape/screens/example02.PNG)
![](/Fractal%20landscape/screens/example03.PNG)

## **Použití**
```python
python main.py # pro spuštění chodu programu
```

## **requirements.txt**
- Všechny potřebné knihovny pro spuštění lze nalézt zde.
