'''
Zadanie 4.

a) W pliku "unirpot_ids.list" znajdują się unikalne numery id dla wybranych rekordów z bazy danych UniProt. Pobierz sekwencje aminokwasowe białek, do których odwołują się wspomniane numery id i zapisz sekwencje w formacie FASTA. Następnie przefiltruj sekwencje tak, aby były dostepne jedynie te, które należą do białek z grupy "SsrA-binding protein". [5 pkt]

b) W pliku "kegg_ids.list" znajdują się unikalne numery id dla wybranych rekordów z bazy danych KEGG. Pobierz sekwencje aminokwasowe tych białek i przedstaw je zgodnie z danymi zapisanymi w formacie fasta. [4 pkt]

c) Wykonaj wspólną analizę MSA dla sekwencji otrzymanych z podpunktów a) oraz b) [4 pkt]
a) Uniprot → sekwencje AA → filtr „SsrA-binding protein”
b) KEGG ID → sekwencje AA (FASTA)
c) wspólne MSA dla sekwencji z a) i b
'''

with open('uniprot_id.txt', 'r') as uniprot_id_file:
    uniprot_id_list = uniprot_id_file.readlines()

    clean_uniprot_id_list = []

    for x in uniprot_id_list:
        clean_uniprot_id_list.append(x.strip('\n'))
    print(clean_uniprot_id_list)

import requests
import pandas as pd


def getDataFromKegg(operation, argument):
    url = f"https://rest.kegg.jp/{operation}/{argument}"

    resp = requests.get(
        url
    )

    if resp.ok:
        return resp.text
    
'''def getAASeq(uniprot_id):
    kegg_id_data = getDataFromKegg(
        "conv", f"genes/uniprot:{uniprot_id}"
    )

    kegg_id = kegg_id_data.strip().split("\t")[1]

    gene = getDataFromKegg(
        "get", f"{kegg_id}/aaseq"
    )

    gene = "".join(gene.split("\n")[1:])

    return gene'''


def convUniprotToKegg(uniprot_id):
    url = f'https://rest.kegg.jp/conv/genes/uniprot:{uniprot_id}'

    response = requests.get(url)

    ids = response.text

    kegg_id = ids.split('\t')[1].strip('\n')

    return kegg_id

def getAAFromKegg(kegg_id):
    url = f'https://rest.kegg.jp/get/{kegg_id}/aaseq'

    response = requests.get(url)

    return response.text

'''with open('fastaKegg.txt', 'w') as f:
    for x in clean_uniprot_id_list:
        f.write(getAAFromKegg(convUniprotToKegg(x)))'''

lista_klas = []

with open('fastaKegg.txt', 'r') as f:
    jedenDuzyString = f.read()

    listaElementow = jedenDuzyString.split('>')

    for x in listaElementow:
        if 'class II' in x:
            lista_klas.append(x)

print(lista_klas)

with open('kegg_id.txt', 'r') as f:
    lista = f.readlines()

    for index, element in enumerate(lista):
        lista[index] = element.strip('\n')

    #czysta_lista = lista.split('\n')

    print(lista)

msaList = []

for x in lista:
    msaList.append(getAAFromKegg(x))

msaString = '\n'.join(msaList)




def runClustal(sequecnes_in_fasta):
    resp = requests.post(
        'https://www.ebi.ac.uk/Tools/services/rest/clustalo/run',
        data={
            "email": "marcel.thiel@ug.edu.pl",
            "sequence": sequecnes_in_fasta,
            "outfmt": "fa"
        }
    )
    jobid = resp.text

    return jobid


def getStatus(jobId):
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{jobId}"
    
    resp = requests.get(
        url
    )

    return resp.text


def getResults(jobId):
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{jobId}/fa"

    resp = requests.get(
        url
    )

    return resp.text


jobid = runClustal(msaString)

import time

for x in range(30):
    if getStatus(jobid) == 'FINISHED':
        print(getResults(jobid))
        break

    else:
        time.sleep(1)
