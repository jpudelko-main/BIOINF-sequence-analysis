###POLECENIE:
###Utworz plik i zapisz do niego nastepujace uniprotid P10321,P04439,P01889,P17693,P13747
###Nastepnie napisz program ktory: 
###a)-dla kazdego z zapisanych w pliku wejsciowym UniprotID wyswietli
### jego odpowiednik w postaci KEGGID,
###b)-dla kazdego z zapisanych w pliku uniid pobierze sekwencje aa
### a nastepnie zapisze wszystkie pobrane dane w jednym pliku w formacie FASTA.


import requests
import json

with open("uniprot_id.txt","w") as f:
    f.write("P10321\nP04439\nP01889\nP17693\nP13747")
    print(f)
    
def getuniprotidfromfile():
    with open("uniprot_id.txt", "r") as g:
        file  = g.readlines()
        for i in range(len(file)):
            file[i] = file[i].strip("\n")
        #print(file)
        return file
    
def getkeggidformuniprotid(uniprotids):
    keggids = []
    for i in range(len(uniprotids)):
        uniprotid = uniprotids[i]
        url = f"https://rest.uniprot.org/uniprotkb/{uniprotid}.txt"
        resp = requests.get(url)
        resp = resp.text.split("\n")
        for j in range(len(resp)):
            line = resp[j]
            if line.startswith("DR   KEGG;"):  #11
                keggids.append(line[11:19])
                #print(keggids)
                break
    return keggids
        #if line.startsw1ith("DR   KEGG;"):   
def writefastatofile(uniprotids):
    fastas = []
    for i in range(len(uniprotids)):
        uniprotid = uniprotids[i]
        url = f"https://rest.uniprot.org/uniprotkb/{uniprotid}.fasta"
        resp = requests.get(url)
        resp = resp.text.split("\n")
        
        fasta = '>{uniprotid}\n'
        #print(resp)
        for j in range(1,len(resp)):
            fasta += resp[j]
        fastas.append(fasta)
    print(fastas)
    with open("fastaplik.txt", "w") as g:
        g.writelines(fastas)
        print(g)
        
def getsequencefromuniprotid(uniprotids):
    for i in range(len(uniprotids)):
        uniprotid = uniprotids[i]
        url = f"https://rest.uniprot.org/uniprotkb/{uniprotid}.json"
        resp = requests.get(url)
        resp = json.loads(resp.text)
        print(resp.keys())
        print(resp["sequence"].keys())
        with open("aminokwasjson.txt","a") as f:
            f.write(resp["sequence"]["value"] + "\n")
            f.write(str(resp["sequence"]["molWeight"])+"\n")
            
        #print(resp)
        
        #print(resp)
        
        

def main():
    uniprotids = getuniprotidfromfile()
    keggids = getkeggidformuniprotid(uniprotids)   
    writefastatofile(uniprotids)
    getsequencefromuniprotid(uniprotids)
    for i in range(len(uniprotids)):
        print(f"{uniprotids[i]}: {keggids[i]}")
main()