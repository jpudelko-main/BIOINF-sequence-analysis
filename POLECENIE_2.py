# -*- coding: utf-8 -*-
# Skrypt:
# 1) Wczytuje KEGG ID z pliku i wypisuje chromosom + pozycję z bazy KEGG
# 2) Pobiera sekwencje nukleotydowe (ntseq) dla pierwszych 3 KEGG ID i robi MSA w Clustal Omega
# 3) Pobiera strukturę PDB (1LKX) i liczy HELIX / SHEET / ATOM

import requests
import time

# --- BLOK 1: Wczytanie listy KEGG ID z pliku ---

with open('kegg_id.txt', 'r') as f:
    content = f.read().strip()

# Tworzymy listę KEGG ID (jedno ID na linię, bez pustych wpisów)
keggids = [kid.strip() for kid in content.split("\n") if kid.strip()]
print(keggids)


# --- BLOK 2: Pobieranie danych o genie z KEGG (chromosom i pozycja) ---

def getDataFromKegg():
    """
    Dla każdego KEGG ID:
    - pobiera pełny wpis z KEGG (/get/<keggid>)
    - próbuje wyciągnąć fragment sekcji POSITION (chromosom i zakres pozycji)
    - wypisuje: <KEGG_ID>, chromosom X, pozycja Y
    """
    for keggid in keggids:
        url = f'https://rest.kegg.jp/get/{keggid}'
        response = requests.get(url)
        dane = response.text

        chromosom = "NA"
        pozycja = "NA"

        # Bezpieczna próba wyciągnięcia sekcji POSITION (między POSITION a MOTIF)
        if 'POSITION' in dane and 'MOTIF' in dane:
            try:
                fragment = dane.split('POSITION', 1)[1].split('MOTIF', 1)[0]
                parts = fragment.split(':', 1)
                chromosom = parts[0].strip()
                pozycja = parts[1].strip()
            except (IndexError, ValueError):
                # Jak coś nie wyjdzie w parsowaniu, zostaje "NA"
                pass

        print(f'{keggid}, chromosom {chromosom}, pozycja {pozycja}')


getDataFromKegg()


# --- BLOK 3: Pobieranie sekwencji nukleotydowych ntseq z KEGG ---

def getNtSeq(keggid):
    """
    Pobiera sekwencję nukleotydową (ntseq) dla danego KEGG ID
    z endpointu /get/<keggid>/ntseq
    """
    url = f'https://rest.kegg.jp/get/{keggid}/ntseq'
    response = requests.get(url)
    return response.text


# --- BLOK 4: Zapis ntseq dla pierwszych 3 KEGG ID do pliku ---

with open('ntseqkegg', 'w') as f:
    # Bierzemy maksymalnie pierwsze 3 ID z listy keggids
    for keggid in keggids[:3]:
        f.write(getNtSeq(keggid))

# --- BLOK 5: Wczytanie tych ntseq z pliku (będą wejściem do MSA) ---

with open('ntseqkegg', 'r') as f:
    danent = f.read()
    print(danent)


# --- BLOK 6: Wysłanie sekwencji do Clustal Omega i start MSA ---

def MSA(danent):
    """
    Wysyła sekwencje (danent) do serwera Clustal Omega (EBI)
    i zwraca jobID zadania MSA.
    """
    resp = requests.post(
        'https://www.ebi.ac.uk/Tools/services/rest/clustalo/run',
        data={
            "email": "mail@ug.edu.pl",
            "sequence": danent,
            "outfmt": "fa"  # chcemy wynik w formacie FASTA
        }
    )
    jobid = resp.text.strip()
    return jobid


jobId = MSA(danent)


# --- BLOK 7: Funkcje pomocnicze do obsługi statusu i wyników MSA ---

def getStatus(jobId):
    """
    Sprawdza status zadania MSA o danym jobId.
    Zwraca tekst: RUNNING / FINISHED / ERROR / ...
    """
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{jobId}"
    resp = requests.get(url)
    return resp.text.strip()


def getResults(jobId):
    """
    Pobiera wynik MSA (w formacie FASTA) dla danego jobId.
    """
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{jobId}/fa"
    resp = requests.get(url)
    return resp.text


# --- BLOK 8: Czekanie na zakończenie MSA i wypisanie wyniku ---

max_attempt = 20
for i in range(max_attempt):
    status = getStatus(jobId)
    if status == "FINISHED":
        results = getResults(jobId)
        print(results)
        break
    time.sleep(1)  # czekamy 1 sekundę przed kolejnym sprawdzeniem


# --- BLOK 9: Przygotowanie do analizy struktury PDB (ID: 1LKX) ---

pdb_id = '1LKX'


def getdatafromPDB():
    """
    Pobiera plik .pdb dla danego pdb_id z RCSB
    i zwraca jego zawartość jako tekst.
    Dodatkowo drukuje cały plik PDB.
    """
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"
    response = requests.get(url)
    tekst = response.text
    print(tekst)
    return tekst


# --- BLOK 10: Odczyt pliku PDB i wydzielenie nagłówka przed sekcją TITLE ---

pdb_text = getdatafromPDB()

# Nagłówek (wszystko przed pierwszym wystąpieniem słowa "TITLE")
header = pdb_text.split("TITLE")[0]
print(header)


# --- BLOK 11: Zliczanie HELIX, SHEET i ATOM w strukturze PDB ---

helixnumber = 0
sheetnumber = 0
atomnumber = 0

# Dzielimy plik PDB na linie i patrzymy po prefiksach
for line in pdb_text.split("\n"):
    if line.startswith("HELIX"):
        helixnumber += 1
    elif line.startswith("SHEET"):
        sheetnumber += 1
    elif line.startswith("ATOM"):
        atomnumber += 1

print(helixnumber, sheetnumber, atomnumber)
# Wypisuje: <liczba_helis> <liczba_arkuszy_beta> <liczba_atomów>
