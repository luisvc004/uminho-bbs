# uminho-bbs

Scripts and data for the first practical assignment of Bioinformatics and Systems Biology (University of Minho): protein profiles of a syntrophic co-culture of *Syntrophomonas zehnderi* and *Methanobacterium formicicum* grown on oleate and on stearate.

Identification (Galaxy), annotation (UniProt ID Mapping) and K numbers (BlastKOALA) were done on their websites. Their downloads are in `data/` and the scripts that process them are in `scripts/`. The complete comparison table is available at https://luisvc004.github.io/uminho-bbs/ (the page is in `docs/`).

## Run

From the root of the repository:

```
pip install .
python3 scripts/02_protein_abundance.py
python3 scripts/03_split_ids_by_organism.py
python3 scripts/04_ko_to_table.py
python3 scripts/05_enzyme_barplot.py
python3 scripts/05_highlighted_barplot.py
```

| Script | Input | Output |
|---|---|---|
| `02_protein_abundance.py` | `data/01_galaxy`, Protein Reports | `results/02_abundance`, relative abundances and comparison table |
| `03_split_ids_by_organism.py` | `data/03_uniprot`, ID Mapping tables | `results/03_uniprot`, IDs and annotation by organism |
| `04_ko_to_table.py` | `data/04_blastkoala`, user_ko files | `results/04_blastkoala`, protein to K number tables |
| `05_enzyme_barplot.py` | `results/02_abundance`, comparison table | `results/05_figures`, bar chart of selected enzymes |
| `05_highlighted_barplot.py` | `data/plots`, Excel files with the highlighted proteins | `results/05_figures_v2`, wide bar chart of the highlighted proteins |

Tested with Python 3.12.13, pandas 3.1.0, matplotlib 3.11.2, seaborn 0.13.2 and openpyxl 3.1.5.

In the BlastKOALA file names, 120 is taxon 1204725 (*M. formicicum*) and 69 is taxon 690567 (*S. zehnderi*).

## Authors

Group 2

- Joana Junqueira
- [Luís Carmo](https://github.com/luisvc004/)
- [Miguel Cruz](https://github.com/migcruzz/)
- Matilde Monteiro