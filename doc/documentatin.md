# Dokumentace projektu - RAM Price Predictor

**Autor:** Hynek Faktor 
**Kontakt:** h.faktor06@gmail.com
**Datum vypracování:** 10.4. 2026
**Škola:** Střední průmyslová škola elektrotechnická Ječná 30
**Typ projektu:** Školní projekt

---

## 1. Specifikace požadavků
### Funkční požadavky (Functional Requirements)
- **F1:** Uživatel zadá technické parametry RAM (kapacita, frekvence, typ).
- **F2:** Systém automaticky doplní latenci (CL) a napětí (V), pokud nejsou známy, na základě uživatelského profilu (Office/Gaming).
- **F3:** Systém provede predikci tržní ceny v USD pomocí strojového učení.
- **F4:** Grafické rozhraní zobrazí výsledek přehledně včetně použitých parametrů.
- **F5:** Aplikace umožní přepínání mezi modely pro PC a modely pro univerzální použití.

### Nefunkční požadavky (Non-functional Requirements)
- **N1:** Běh na operačním systému Windows (samostatný .exe soubor).
- **N2:** Rychlost predikce do 1 sekundy od odeslání požadavku.
- **N3:** Uživatelské rozhraní postavené na knihovně Tkinter (není vyžadována instalace Pythonu u koncového uživatele).

---

## 2. Architektura aplikace
Aplikace je postavena na architektuře **Modulární monolit** s využitím návrhového vzoru **Strategy** (výběr modelu podle kapacity RAM).

### Schéma architektury (Big Image)
1. **Prezenční vrstva (UI):** Modul `ui.py` – zpracovává vstupy od uživatele a zobrazuje výsledky.
2. **Logická vrstva (Controller):** Modul `main.py` – rozhoduje, který ML model použít, provádí čištění dat a volá predikční engine.
3. **Datová vrstva (Models):** Složky `models/` a `columns/` – obsahují serializované mozky stroje (soubory .pkl).
4. **Pomocné moduly:** Balíček `data_manipulation` – obsahuje logiku pro doplňování výchozích hodnot a transformaci dat.



---

## 3. Popis běhu aplikace (Activity Diagram)
Běh aplikace v typickém případě:
1. Uživatel spustí `ui.exe`.
2. Zadá parametry RAM (např. 16GB, 3200MHz, DDR4).
3. **Rozhodovací proces:** - Jsou vyplněny CL a Voltage? 
   - ANO -> Pokračuj. 
   - NE -> Doplň defaulty z `default_values.py` podle typu (Gaming/Office).
4. **Výběr modelu:** Program určí velikost RAM a vybere odpovídající model (PC / Small / Large).
5. **Predikce:** Model vypočítá cenu.
6. **Zobrazení:** Výsledek je vypsán do textového pole v UI.

---

## 4. Použité knihovny a rozhraní
Aplikace využívá následující knihovny třetích stran:
- **scikit-learn (1.2+):** Implementace algoritmů Random Forest.
- **pandas:** Manipulace s datovými rámci a strukturami.
- **numpy (< 2.0.0):** Matematické operace (základ pro ML knihovny).
- **joblib:** Serializace a načítání uložených modelů (.pkl).
- **matplotlib:** Podpora pro vizualizaci (volitelné součásti).
- **PyInstaller:** Nástroj pro kompilaci do spustitelného formátu.

---

## 5. Právní a licenční aspekty
- **Licence:** Projekt je šířen pod licencí **MIT**.
- **Autorská práva:** Kód je autorským dílem studenta. Použité knihovny (scikit-learn, pandas atd.) jsou open-source a jejich použití v tomto projektu je v souladu s jejich licencemi.
- **Data:** Trénovací data pocházejí z veřejně dostupných zdrojů a slouží výhradně pro edukační účely.

---

## 6. Konfigurace a instalace
### Instalace
Aplikace nevyžaduje instalaci. Je distribuována jako přenositelný (portable) soubor:
1. Stáhněte soubor `ui.exe`.
2. Spusťte soubor dvojklikem.

### Konfigurace
Program nevyžaduje externí konfigurační soubory (např. .ini nebo .env). Veškerá konfigurace (cesty k modelům) je řešena interně pomocí relativních cest skrze funkci `resource_path`.

---

## 7. Chybové stavy a jejich řešení
| Chyba | Příčina | Řešení |
| :--- | :--- | :--- |
| `FileNotFoundError` | Chybějící soubory modelů v `models/`. | Zkontrolovat integritu .exe souboru nebo přítomnost složek. |
| `ValueError` | Zadání textu do pole pro čísla. | UI automaticky ošetřuje vstupy, uživatel musí zadat číselnou hodnotu. |
| `Incompatibility Error` | Spuštění na nekompatibilní verzi OS. | Aplikace je určena pro Windows 10 a novější. |

---

## 8. Ověření a testování
Testování proběhlo formou **Unit testů** (ověření výpočtů v `main.py`) a **Manuálního akceptačního testování**:
- **Test 1:** Zadání standardní DDR4 16GB RAM -> Výsledek odpovídá tržní ceně (~40-60 USD).
- **Test 2:** Ponechání prázdných polí CL a V -> Ověřeno správné doplnění hodnot (např. 1.35V pro Gaming DDR4).
- **Validace:** Výsledky byly porovnány s aktuálními cenami na e-shopech (Amazon/Newegg), odchylka modelu se pohybuje v rozmezí 5–12 %.

---

## 9. Seznam verzí a známé chyby
- **v1.0 (Aktuální):** První stabilní verze.
- **Známé chyby:** - Při extrémně vysokých frekvencích (nad 8000 MHz) může model nadhodnocovat cenu kvůli nedostatku trénovacích dat pro tyto specifické moduly.
  - Aplikace nepodporuje historické typy RAM (DDR1, SDRAM).

---

## 10. Schéma importu/exportu
Aplikace neprovádí hromadný import dat. Vstupem je **objekt typu Dictionary** (v paměti), který obsahuje:
- `Capacity` (float, povinné)
- `Frequency` (float, povinné)
- `Latency` (float, volitelné)
- `Voltage` (float, volitelné)