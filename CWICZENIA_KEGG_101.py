import requests
def keggINFO(database):
    url = f"https://rest.kegg.jp/info/{database}"
    
    resp = requests.get(url)
    
    print(resp.text)

def keggLIST(database):
    url = f"https://rest.kegg.jp/list/{database}"
    
    resp = requests.get(url)
    
    return resp.text
def keggFIND(database, query):
    url = f"https://rest.kegg.jp/find/{database}/{query}"
    
    resp = requests.get(url)
    
    return resp.text
def keggGET(dbentries):
    url = f"https://rest.kegg.jp/get/{dbentries}"
    
    resp = requests.get(url)
    
    return resp.text
print(
    keggFIND("drug", "cocaine")
)
print(
    keggFIND("compound", "cocaine")
)
print(
    keggGET("dr:D00110")
)
print(
    keggGET("cpd:C01416")
)
print(
    keggGET("R06727+R06728+R06745+R08430")
)
print(
    keggGET("K01044")
)
print(
    keggGET("hsa:1066")
)
