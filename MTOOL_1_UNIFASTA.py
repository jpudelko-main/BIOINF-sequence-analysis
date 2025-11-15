from sys import argv
import requests

def getDataFromUniProt(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    
    resp = requests.get(
        url
    )

    if resp.ok:
        print(resp.text)
        return
    
    print(f"UniProt id: {uniprot_id} does not exist")

if __name__ == "__main__":
    try:
        uniprot_id = argv[1]
        getDataFromUniProt(uniprot_id)

    except IndexError:
        print("Hey! Please provide uniprot id")
    