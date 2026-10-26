from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "results" / "02_abundance" / "comparison.csv"
OUTPUT_DIR = BASE_DIR / "results" / "05_figures"
OUTPUT_FILE = OUTPUT_DIR / "enzyme_abundance.svg"

GROUPS = [
    (("M. formicicum", "methane metabolism"), [
        ("K2QYM4", "mcrA"), ("K2RAN9", "mcrB"), ("K2R3X9", "mer"),
        ("K2RSU0", "cdhA"), ("K2QYN3", "mvhD"),
    ]),
    (("S. zehnderi", "β-oxidation and energy"), [
        ("A0A0E4GEM6", "etfB"), ("A0A0E4G9L3", "fadA"),
        ("A0A0E3W2J0", "atpA"), ("A0A0E4G9E7", "atpD"),
    ]),
]


def read_table(path):
    df = pd.read_csv(path, sep=None, engine="python", index_col=0)

    def pick(sample, validation):
        for col in df.columns:
            is_validation = col.startswith("Validation")
            if sample.lower() in col.lower() and is_validation == validation and (validation or "[%]" in col):
                return col
        raise KeyError(f"No {'validation' if validation else 'abundance'} column for {sample}")

    return pd.DataFrame({
        "oleate": df[pick("Oleate", False)], "stearate": df[pick("Stearate", False)],
        "val_oleate": df[pick("Oleate", True)], "val_stearate": df[pick("Stearate", True)],
    })


def plot_enzymes(table, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns
        from matplotlib.patches import Patch
    except ImportError:
        print("matplotlib or seaborn is not installed: chart not generated")
        return

    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10
    plt.rcParams["hatch.linewidth"] = 0.5
    sns.set_theme(
        style="whitegrid",
        rc={
            "font.family": ["Linux Libertine", "Libertinus Serif", "DejaVu Serif"],
            "svg.fonttype": "none",
        },
    )
    sns.set_context("paper")

    colors = {"oleate": "#4c78a8", "stearate": "#e45756"}
    fig, ax = plt.subplots(figsize=(8.0, 3.4), dpi=150)

    x, labels, spans, pos = [], [], [], 0.0
    for title, members in GROUPS:
        start = pos
        for acc, gene in members:
            row = table.loc[acc]
            for offset, sample in ((-0.2, "oleate"), (0.2, "stearate")):
                value, validation = row[sample], row["val_" + sample]
                xi = pos + offset
                if pd.isna(value):
                    ax.text(xi, 0.4, "n.i.", ha="center", va="bottom", fontsize=6.5, color="gray", style="italic")
                    continue
                ax.bar(
                    xi, value, width=0.4, color=colors[sample], edgecolor="black", linewidth=0.4,
                    hatch="////" if validation == "Doubtful" else None,
                )
                if value == 0:
                    ax.text(xi, 0.4, "n.q.", ha="center", va="bottom", fontsize=6.5, color="gray", style="italic")
                else:
                    ax.text(xi, value + 0.4, f"{value:.1f}", ha="center", va="bottom", fontsize=6.5)
            x.append(pos)
            labels.append(gene)
            pos += 1.0
        spans.append((start - 0.45, pos - 1.0 + 0.45, title))
        pos += 0.8

    ax.set_ylim(0, table.loc[[a for _, m in GROUPS for a, _ in m], ["oleate", "stearate"]].max().max() * 1.12)
    ax.set_xticks(x, labels, style="italic")
    ax.set_xlim(spans[0][0] - 0.2, spans[-1][1] + 0.2)
    ax.set_ylabel("Relative abundance (%)", labelpad=4)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, color="gray", alpha=0.6)
    ax.grid(False, axis="x")
    ax.set_axisbelow(True)

    for left, right, title in spans:
        ax.plot([left, right], [-0.17, -0.17], transform=ax.get_xaxis_transform(),
                color="black", linewidth=0.6, clip_on=False)
        species, pathway = title
        ax.text((left + right) / 2, -0.20, species, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=8.5, style="italic")
        ax.text((left + right) / 2, -0.31, pathway, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=8.5)

    for spine in ax.spines.values():
        spine.set_linewidth(0.6)
        spine.set_color("black")

    handles = [
        Patch(facecolor=colors["oleate"], edgecolor="black", linewidth=0.4, label="Oleate"),
        Patch(facecolor=colors["stearate"], edgecolor="black", linewidth=0.4, label="Stearate"),
        Patch(facecolor="white", edgecolor="black", linewidth=0.4, hatch="////", label="Doubtful"),
    ]
    ax.legend(
        handles=handles, title=None, fontsize=8, frameon=False, loc="upper center",
        bbox_to_anchor=(0.5, 1.18), ncol=3, handlelength=1.0, columnspacing=1.0,
    )

    plt.tight_layout(pad=0.3)
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.savefig(Path(path).with_suffix(".png"), format="png", bbox_inches="tight", dpi=220)
    plt.close(fig)
    print("Chart saved to", path)


def main():
    table = read_table(INPUT_FILE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_enzymes(table, OUTPUT_FILE)


if __name__ == '__main__':
    main()