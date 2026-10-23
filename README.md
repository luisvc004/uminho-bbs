# uminho-bbs

Scripts and data for the first practical assignment of Bioinformatics and Systems Biology (University of Minho): protein profiles of a syntrophic co-culture of *Syntrophomonas zehnderi* and *Methanobacterium formicicum* grown on oleate and on stearate.
 
Identification (Galaxy), annotation (UniProt ID Mapping) and K numbers (BlastKOALA) were done on their websites. Their downloads are in `data/` and the scripts that process them are in `scripts/`.

## Run
 
From the root of the repository:
 
```
pip install -r requirements.txt
python3 scripts/02_protein_abundance.py
python3 scripts/03_split_ids_by_organism.py
python3 scripts/04_ko_to_table.py
```
 
| Script | Input (`data/`) | Output (`results/`) |
|---|---|---|
| `02_protein_abundance.py` | `01_galaxy`, Protein Reports | `02_abundance`, relative abundances and comparison table |
| `03_split_ids_by_organism.py` | `03_uniprot`, ID Mapping tables | `03_uniprot`, IDs and annotation by organism |
| `04_ko_to_table.py` | `04_blastkoala`, user_ko files | `04_blastkoala`, protein to K number tables |
 
In the BlastKOALA file names, 120 is taxon 1204725 (*M. formicicum*) and 69 is taxon 690567 (*S. zehnderi*).

## Authors

Group 2

- Joana Junqueira
- [Luís Carmo](https://github.com/luisvc004/)
- [Miguel Cruz](https://github.com/migcruzz/)
- Matilde Monteiro