import argparse
import glob
import os
 
import pandas as pd
 
ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="*", help="user_ko file(s) downloaded from BlastKOALA")
ap.add_argument("-o", "--output-dir", default="results/04_blastkoala")
args = ap.parse_args()
files = args.files or sorted(glob.glob("data/04_blastkoala/user_ko_*.txt"))
os.makedirs(args.output_dir, exist_ok=True)
 
for path in files:
    ko = pd.read_csv(path, sep="\t", header=None, names=["Main_Accession", "KO"], usecols=[0, 1])
    ko["KO"] = ko["KO"].where(ko["KO"].str.fullmatch(r"K\d{5}", na=False), "NA")
    ko["Main_Accession"] = ko["Main_Accession"].str.replace(r"^\w+\|(\w+)\|.*", r"\1", regex=True)
 
    out = os.path.join(args.output_dir, os.path.splitext(os.path.basename(path))[0] + "_to_KO.txt")
    ko.to_csv(out, sep="\t", index=False)
    print(f"{os.path.basename(path)}: {(ko['KO'] != 'NA').sum()} of {len(ko)} proteins received a K number -> {out}")