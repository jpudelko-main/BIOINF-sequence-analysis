import json
from sys import argv, exit
import requests

def getDataFromUniProt(uniprot_id):
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}"

    resp = requests.get(
        url, headers={"Accept": "application/json"}
    )

    if resp.ok:
        data = json.loads(resp.text)
        return data

    print(f"Uniprot id: {uniprot_id} does not exist")
    exit(1)

if __name__ == "__main__":
    try:
        uniprot_id = argv[1]
        data = getDataFromUniProt(uniprot_id)

        print(data["organism"]["names"][0]["value"])

        print(data["gene"][0]['name']['value'])

        print(data['sequence']['sequence'])

    except IndexError:
        print("Hey! Please provide uniprot id")
    