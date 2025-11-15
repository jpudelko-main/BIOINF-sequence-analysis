###POLECENIE:
###Utworz plik i zapisz do niego nastepujace uniprotid P10321,P04439,P01889,P17693,P13747
###Nastepnie napisz program ktory: 
###a)-dla kazdego z zapisanych w pliku wejsciowym UniprotID wyswietli
### jego odpowiednik w postaci KEGGID,
###b)-dla kazdego z zapisanych w pliku uniid pobierze sekwencje aa
### a nastepnie zapisze wszystkie pobrane dane w jednym pliku w formacie FASTA.
###c)-Wykona analize MSA dla pobranych sekwencji i wyswietli wynik dzialania algorytmu.
###d)-Wypisze ile jest gap(-) w calym dopasowaniu. 

import requests
import time


#wczytujemy plik uniprot_id
with open('uniprot_id', 'r') as uniprot_id_file:
        lista_kegg_id = uniprot_id_file.read() #czytamy dane z pliku
        lista_kegg_id = lista_kegg_id.split('\n') #dzielimy je linijka po linijce


#pobieramy dane z kegga, konwertujemy uniprot_id na kegg_id
def convertUniprotIDtoKeggId(operation, argument1, argument2, id):
    url = f"https://rest.kegg.jp/{operation}/{argument1}/{argument2}:{id}"

    resp = requests.get(
        url
    )

    if resp.ok:
        return resp.text

#deklaracja listy
kegg_ids = []

#dla kazdego kegg_id w liscie
for element in lista_kegg_id:
    kegg_id = convertUniprotIDtoKeggId('conv', 'genes', 'uniprot', element) #konwertujemy UP_id do Kegg_id
    kegg_id = kegg_id.split('\t')[1] #bierzemy prawą strone
    kegg_id = kegg_id.strip('\n') #usuwamy znak nowej linii z konca
    kegg_ids.append(kegg_id) #dodajemy kegg_id do listy zawierajacej kegg_id

print(kegg_ids)

#pobieramy sekwencje aminokwasowa
def getAminoacidSequence(operation, id, option):
    url = f"https://rest.kegg.jp/{operation}/{id}/{option}"

    response = requests.get(
        url
    )

    return response.text

#deklarujemy liste sekwencji aminokwasowych
aasequences = []

with open('podpunktB', 'w') as file: #otwieramy plik NAJPIERW
#dla kazdego kegg_id w liste z kegg_id
    for kegg_id in kegg_ids:
    
        data = getAminoacidSequence('get', kegg_id, 'aaseq')#pobieramy sekwekwencje aminokwasowa
        aasequences.append(data)#dodajemy to do listy z sekwencjami aminokwasowymi
        file.write(data)#dopisujemy to wszystko do pliku z sekwencjami aminokwasowymi


#wysylamy do api sekwencje do clustala omega
def MSAAnalysis(sequence_in_fasta):
    url = f'https://www.ebi.ac.uk/Tools/services/rest/clustalo/run'
    response = requests.post(url,
                  data={
                       "email": "j.pudelko.970@studms.ug.edu.pl",
                       'sequence': sequence_in_fasta,
                       'outfmt': 'fa'
                  })
    
    jobID = response.text
    return jobID

jobID = MSAAnalysis('\n'.join(aasequences)) #zapisujemy jobID


#sprawdzamy czy nasze zapytanie jest spelnione
def checkStatusMSA(jobID):
    url = f'https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{jobID}'
    response = requests.get(
        url
    )

    return response.text


#pobieramy wynik naszego zapytania
def getMSAResult(jobID, resultType):
    url = f'https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{jobID}/{resultType}'
    response = requests.get(
        url
    )

    return response.text



#sprawdzamy pare razy czy juz sie zrobilo
for i in range(20):
    if checkStatusMSA(jobID) == 'FINISHED':#jesli tak to pokazujemy wyniki
        MSAResult = getMSAResult(jobID, 'fa')
        print(MSAResult)
        time.sleep(1)
        break
    else:#jesli nie to czekamy
        time.sleep(1)

gaps = MSAResult.split('\n')
print('\n',gaps)

#deklarujemy liste z linijkami wyniku MSA
lista_linijek_z_wynikami_MSA = []

#sprawdzamy czy indeks linijki jest podzielny przez 8, tzn. mamy do czynienia z headerem
for i in range(len(gaps)):
    if i % 8 == 0: #jesli tak, to go pomijamy
        continue
    else:#jesli nie to zapisujemy dana linijke w liscie
        lista_linijek_z_wynikami_MSA.append(gaps[i])

#laczymy wszystkie elementy listy w jeden dlugi string
long_sequence = ''.join(lista_linijek_z_wynikami_MSA)

#wypisujemy liczbe "-" w dlugiej sekwencji
print(long_sequence.count('-'))