import argparse
import os

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="*", default=["data/03_uniprot/oleate_idmapping.tsv", "data/03_uniprot/stearate_idmapping.tsv"],
                help="tab-separated tables with 'From' and 'Organism (ID)' columns")
ap.add_argument("-o", "--output-dir", default="results/03_uniprot")
args = ap.parse_args()
os.makedirs(args.output_dir, exist_ok=True)

for path in args.files:
    sample = os.path.basename(path).split("_idmapping")[0]
    df = pd.read_csv(path, sep="\t", dtype=str)
 
    for org_id, group in df.groupby("Organism (ID)"):
        out = os.path.join(args.output_dir, f"{sample}_ids_organism_{org_id}.txt")
        ids = group["From"].drop_duplicates()
        ids.to_csv(out, index=False, header=False)
        print(f"{len(ids)} IDs -> {out}")
 
        annotation = os.path.join(args.output_dir, f"{sample}_annotation_organism_{org_id}.tsv")
        group.drop_duplicates("From").to_csv(annotation, sep="\t", index=False)