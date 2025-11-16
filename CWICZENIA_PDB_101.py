import requests
url = "https://files.rcsb.org/view/4GHP.pdb"
def getDataFromRCSB(url):
    resp = requests.get(url)
    
    return resp.text
pdb_4GHP = getDataFromRCSB(url)
type(pdb_4GHP)
print(pdb_4GHP)
for line in pdb_4GHP.split('\n'):
    if line.startswith('HEADER'):
        print(line)
def getSEQRESData(pdb_data):
    seq = []
    
    for line in pdb_data.split('\n'):
        if line.startswith('SEQRES'):
            seq.extend(
                line[19:].split()
            )
            
    seq = '-'.join(seq)
    
    return seq
sequence_long = getSEQRESData(pdb_4GHP)
symbol = {
    "ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F", "GLY": "G", "HIS": "H", "ILE": "I",
    "LYS": "K", "LEU": "L", "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R", "SER": "S",
    "THR": "T", "TRP": "W", "VAL": "V", "TYR": "Y"
}
def getSequence(sequence_long):
    sequence = ''
    for aa in sequence_long.split('-'):
        try:
            sequence += symbol[aa]
        except KeyError:
            sequence += "X"
            
    return sequence
getSequence(sequence_long)
# sequence_test = ''.join([symbol[aa] for aa in sequence_long.split('-')])
fake_sequence = "MET-ALA-XYZ-MET-GLU"
getSequence(fake_sequence)
def countHelixAndSheet(pdb_data):
    helix = 0
    sheet = 0
    
    for line in pdb_data.split('\n'):
        if line.startswith('HELIX'):
            helix += 1
            continue
        
        if line.startswith('SHEET'):
            sheet += 1
            continue
            
    print(
        f'HELIX: {helix} SHEET: {sheet}'
    )
countHelixAndSheet(pdb_4GHP)
def getCAATOMS(pdb_data):
    for line in pdb_data.split('\n'):
        if line.startswith('ATOM'):
            atom_type = line[12:16].strip()
            if atom_type == "CA":
                print(line)
getCAATOMS(pdb_4GHP)
