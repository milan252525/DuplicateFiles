# PRG I - Duplikátní soubory

## Uživatelská dokumentace

### Úvod

Program slouží k prohledání zadaného adresáře a nalezení duplicitních souborů. Lze ho použít v příkazové řádce. Výstup je vypsán přímo do příkazového řádku nebo do souboru.

Uživatel má možnost zvolit, které z následujících vlastností bude program porovnávat. 

- velikost

- název

- datum a čas

- obsah



### Použítí

Program se spouští v příkazové řádce následovně:

`python cesta/dupefiles.py cesta/adresar/ argumenty`

`cesta/adresar/` - cesta k prohledávanému adresáři

### Argumenty

| ARGUMENT       | POPIS                                           |
| -------------- | ----------------------------------------------- |
| -s (--size)    | Porovnání souborů podle velikosti               |
| -n (--name)    | Porovnávní souborů podle názvu (včetně přípony) |
| -d (--date)    | Porovnání souborů podle data a času\*           |
| -c (--content) | Porovnání douborů podle obsahu                  |
| -f (--file)    | Výstup do souboru                               |

\*Windows - datum vytvoření, Linux - datum poslední úpravy

Na pořadí argumentů nezáleží.

Všechny možnosti lze také zobrazit pomocí ``python dupefiles.py --help`.

**Argument -f**

Lze ponechat samotný nebo doplnit o parametr s cestou, kam se má soubor uložit.

Pokud není doplněn o cestu, výstup je uložen do adresáře, ze kterého je vykonáván příkaz.

Implicitní název souboru: `duplicate_files_DATUM.txt`

### Příklady použití

`python dupefiles.py TestFiles/ -n -c`

Nalezne všechny soubory se stejným názvem a obsahem.

`python dupefiles.py TestFiles/ --date --size`

Nalezne všechny soubory se stejným datem a velikostí.

`python dupefiles.py TestFiles/ -c -d -f`

Nalezne všechny soubory se stejným datem a obsahem, výsledek vypíše do souboru v adresáři ze kterého je vykonáván příkaz pod názvem duplicate_files_DATUM.txt.

`python dupefiles.py TestFiles/ -n -f Dokumenty/`

Nalezne všechny soubory se stejným názvem, výsledek vypíše do adresáře Dokumenty/ pod názvem duplicate_files_DATUM.txt.

`python dupefiles.py TestFiles/ -n -f Dokumenty/vysledek.txt`

Nalezne všechny soubory se stejným názvem, výsledek vypíše do adresáře Dokumenty/ pod názvem vysledek.txt.

### Řešení problémů

**Chybějící knihovny**

Všechny použité knihovny jsou distribuovány s jazykem Python. Pokud by i přesto hlásil program chybu, lze je doinstalovat pomocí příkazu:

`pip install --user hashlib argparse`


