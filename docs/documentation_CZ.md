# PRG I - Duplicitní soubory

## Milan Abrahám

## Zadání

Program prohledá zadaný adresář včetně pod-adresářů a vypíše seznam shodných souborů. Uživatel zvolí, které vlastnosti souborů se mají porovnávat. Mezi volitelné vlastnosti patří jméno, datum a čas, velikost a obsah souboru.

## Úvod

Tento program napsaný v jazyce Python slouží jako pomocník při vyhledávání duplicitních souborů v uživateli zvoleném adresáři a všech v něm vnořených adresářích. Je určen k použití v příkazové řádce. 

Uživatel vybírá porovnávané vlastnosti pomocí argumentů a zvolí, kam se má zobrazit výstup. Výstup, rozdělený do skupin podle identických vlastností, je buďto vypisován přímo do příkazové řádky nebo uložen do textového souboru. Program porovnává soubory jakéhokoliv typu a to i obsahově (např. obrázky, videa a dokumenty). 

## Porovnávané vlastnosti

Soubory lze porovnávat podle názvu, velikosti, data a obsahu. Název je porovnáván  včetně přípony souboru (.txt, .jpg...). Datum je závislý na operačním systém. Na systému Windows je to datum vytvoření souboru, na Linuxu datum poslední úpravy. Porovnání obsahu se provádí pomocí zahashování celého obsahu algoritmem SHA-256 a porovnáním hashů.

### Argumenty

Argumenty jsou zadávány v příkazové řádce. Jsou zpracovány knihovnou **argparse**, která je standardně obsažena v Pythonu. 

| ARGUMENT       | POPIS                                           |
| -------------- | ----------------------------------------------- |
| -s (--size)    | Porovnání souborů podle velikosti               |
| -n (--name)    | Porovnávní souborů podle názvu (včetně přípony) |
| -d (--date)    | Porovnání souborů podle data a času             |
| -c (--content) | Porovnání douborů podle obsahu                  |
| -f (--file)    | Výstup do souboru                               |

**Příklad použití:**

`python dupefiles.py TestFiles/ -n -f Dokumenty/`

Použití argumentů je podrobněji popsáno v Uživatelské příručce.

## Porovnávání souborů

Vyhledání duplicitních souborů probíhá ve dvou krocích. Nejdříve se rekurzivně projdou všechny adresáře a všechny v nich obsažené soubory. Informace o všech souborech se uloží do slovníku (type **dict**). Jako klíče se použijí vlastnosti souborů. V druhém kroku se celý slovník projde a naleznou se soubory uložené pod stejnými klíči (vlastnostmi).

### Skenování adresáře

K průchodu celým adresářem je použita knihovna **os**, konkrétně její funkce **os.scandir**. Tato funkce umožňuje iteraci přes všechny soubory v adresáři. Kombinovaná s rekurzí projde i všechny pod-adresáře. Funkce **os.scandir** vrací i všechny potřebné vlastnosti souboru. 

Cesty k souborům jsou ukládány do slovníku, jako klíče slouží vlastnosti souborů. Jelikož počet klíčů (hloubka slovníku) není pevně stanoven a závisí na zvolených vlastnostech, bylo potřeba použít rekurzivní funkci.

Při porovnávání obsahu se ovšem nehashuje každý soubor, ale místo toho se porovnávají soubory podle velikosti (jelikož soubory se stejným obsahem musí mít nutně stejnou velikost). Důvodem je časová náročnost čtení a hashování obsahu. Porovnání hashů se provádí až v další funkci jen u souborů se shodnou velikostí.

**Příklad slovníku** při porovnávání podle velikosti a data. Lze nahlédnout, že duplicitní soubory jsou uloženy ve stejném seznamu:

```json
{
    "764176B": {
        "2020_02_22 18:05": [
            "TestFiles/Music/song.mp3",
            "TestFiles/Music/song1.mp3"
        ]
    },
    "1087849B": {
        "2020_02_22 18:07": [
            "TestFiles/Music/song1_longer.mp3"
        ]
    }
}
```

### Vyhledání duplicitních souborů ve slovníku

Výsledný slovník je předán druhé funkci. Ta nejdříve zpracuje cestu k souboru s výsledky (pokud uživatel zvolil výstup do souboru) a soubor vytvoří. Poté projde celý slovník a vypíše cesty souborů, které jsou duplicitní (jsou uloženy pod stejnými klíčy). V případě porovnávání obsahu, vytvoří pomocný slovník, do kterého uloží hashe souborů, které mají stejné ostatní vlastnosti. 

**Ukázka výstupu:**

```
[2]bestsongever.mp3 764176B
 - TestFiles/Music/bestsongever.mp3
 - TestFiles/Folder123/Archived/Hidden/Photos/bestsongever.mp3
[2]hello_world.txt 14B
 - TestFiles/hello_world.txt
 - TestFiles/Folder123/hello_world.txt
[3]cake.png 7523B
 - TestFiles/Photos/cake.png
 - TestFiles/Folder123/SecretFolder/cake.png
 - TestFiles/Folder123/Archived/Hidden/Photos/cake.png
```

### Hashování obsahu

Pro hashování souborů je použita knihovna **hashlib**. Zvolil jsem hashovací algoritmus SHA-256. Důvodem je, že nejsou známe žádné kolize. Tudíž je velice malá (téměř nulová) pravděpodobnost, že dva různé soubory budou mít stejný hash. Existují i novější algoritmy, například SHA3, ale výhodou je jen bezpečnost, které při porovnávání není potřeba. SHA3 je dokonce pomalejší a při porovnání je důležitá rychlost. Výstupem je hash dlouhý 32 bytů v hexadecimální podobě. Soubor je čten po blocích dlouhých 64KB, ty jsou předávány objektu **sha256** knihovny hashlib, která následně vrátí hash v textové podobě.

## Složitost algoritmů

### Časová

Předpokládejme, že N je počet souborů v adresáři. První funkce skenující adresář  jej projde v N krocích, v každém kroce provede konstatní počet operací (zjištení vlastností a uložení do slovníku). Druhá funkce procházející slovník ho prochází také v N krocích a provede konstatní počet operací (vypsání stejných hodnot, případně hashování při porovnání obsahu). Algoritmy v obou funkcích mají tedy **lineární** časovou složitost O(N). 

### Prostorová

Program při běhu vytvoří v nejhorším případě, pokud není žádný ze souborů duplicitní, slovník s N záznamy. Při porovnání obsahu ještě vytváří pomocný slovník s velikostí porovnávaných souborů. V nejhorším případě by se tedy nacházeli v paměty 2 slovníky o velikosti N (což je ale velice nepravděpodobné). Prostorová složitost je tedy také lineární O(N).

## Vývoj

Původně jsem vytvořil algoritmus, který pro každý soubor ukládal vlastnosti do jednoho velkého pole. Poté porovnával každý soubor s každým, což se ukázalo velice časově neefektivní (O(N<sup>2</sup>)). Použití slovníku zlepšil časovou složitost na lineární. Nejdříve jsem implementoval jen výstup do příkazového řádku, což se ale při větším množství souborů ukázalo nepřehledné, a proto jsem přidal i výstup do souboru. Uvažoval jsem i o možnosti mazání souborů, ale tu jsem zavrhl, protože jsem nechtěl riskovat možnost výskytu chyby a smazání špatných souborů.

## Testovací data

Před vytvořením programu jsem vytvořil adresář plný rozličných typů souborů, abych na něm mohl v průběhu vývoje testovat funkčnost. Obsahuje textové soubory, obrázky, zvukové soubory a dokumenty v různých adresářích. Testovací adresář je přiložený v komprimovaném formátu .zip. 

## Závěr

Cílem práce bylo vytvořit funkční program na vyhledávání duplicitních souborů. Podařilo se mi splnit celé zadání. Navíc jsem doplnil výstup do souboru. Program byl otestován na více počítačích, na operačních systémech Windows i Linux. Vývoj mi umožnil získání nových znalostí v oblastech práce se soubory a hashování. Kód včetně komentářů jsem napsal v anglickém jazyce, uživatelskou příručku v anglickém i českém jazyce, aby program případně mohl používat kdokoliv. Je volně dostupný ve webové službě [GitHub](https://github.com/milan252525/DuplicateFiles).


