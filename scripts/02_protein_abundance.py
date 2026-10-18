import argparse
import os

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="*", default=["data/01_galaxy/Oleate_Protein_Report.tabular", "data/01_galaxy/Stearate_Protein_Report.tabular"],
                help="Protein Report of sample 1 and sample 2")
ap.add_argument("-o", "--output", default="results/02_abundance/comparison.csv")
args = ap.parse_args()
if len(args.files) != 2:
    ap.error("give exactly two Protein Reports")

os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
base, ext = os.path.splitext(args.output)
sep = "," if ext.lower() == ".csv" else "\t"

abundances, validations = [], []
for path in args.files:
    name = os.path.splitext(os.path.basename(path))[0]
    df = pd.read_csv(path, sep="\t")
    df = df[~df["Main Accession"].str.startswith("cRAP")]
    df = df[df["Validation"].isin(["Confident", "Doubtful"])]

    s = df.set_index("Main Accession")["Spectrum Counting"]
    out = pd.DataFrame({
        "Spectrum Counting": s,
        "Relative abundance [%]": s / s.sum() * 100,
        "Validation": df.set_index("Main Accession")["Validation"],
    })
    out.index.name = "Main_Accession"
    fname = f"{base}_{name}{ext}"
    out.sort_values("Relative abundance [%]", ascending=False).to_csv(
        fname, sep=sep, float_format="%.4f"
    )
    print(f"{len(out)} proteins -> {fname}")

    abundances.append(out["Relative abundance [%]"].rename(f"{name}[%]"))
    validations.append(out["Validation"].rename(f"Validation_{name}"))

    ids_name = f"{base}_{name}_ids.txt"
    with open(ids_name, "w") as fh:
        fh.write("\n".join(out.index) + "\n")
    print(f"IDs -> {ids_name}")

ab = pd.concat(abundances, axis=1)
comparison = pd.concat([ab, pd.concat(validations, axis=1)], axis=1)
comparison.index.name = "Main_Accession"
comparison.sort_values(list(ab.columns), ascending=False).to_csv(
    args.output, sep=sep, na_rep="NA", float_format="%.4f"
)
print(f"{len(comparison)} unique proteins -> {args.output}")