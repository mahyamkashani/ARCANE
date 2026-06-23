from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent

FILES = {
    "90%": HERE / "task1" / "detection_90_attackall.csv",
    "80%": HERE / "task1" / "detection_80_attackall.csv",
    "70%": HERE / "task1" / "detection_70_attackall.csv",
}

CATEGORIES = ["None", "One", "Both"]
COLORS = ["#D55E00", "#E69F00", "#009E73"]   # None=vermillion, One=amber, Both=bluish-green
HATCHES = ["//", "..", "xx"]           

OUT_PDF = HERE / "detection_rates_distribution.pdf"
OUT_PNG = HERE / "detection_rates_distribution.png"


def classify(devices) -> str:
    """Map a detected-device set string to None / One / Both (by LW, RW)."""
    s = str(devices).replace("{", "").replace("}", "").strip()
    if s == "" or s.lower() == "nan":
        return "None"
    parts = {p.strip() for p in s.split(",")}
    n = sum(w in parts for w in ("LW", "RW"))
    return {0: "None", 1: "One", 2: "Both"}[n]


def category_fractions(path: Path) -> pd.Series:
    df = pd.read_csv(path)
    if "devices" not in df.columns:          # fall back to last column
        df = df.rename(columns={df.columns[-1]: "devices"})
    cats = df["devices"].apply(classify)
    fracs = cats.value_counts(normalize=True)
    return fracs.reindex(CATEGORIES).fillna(0.0)


def main():
    plt.rcParams.update({
        "hatch.linewidth": 1.0,   # crisp hatching for print
        "font.size": 15,        
        "axes.titlesize": 18,
        "axes.labelsize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
    })
    fig, axes = plt.subplots(1, len(FILES), figsize=(13, 4.6), sharey=True)

    for ax, (label, path) in zip(axes, FILES.items()):
        fracs = category_fractions(path)
        print(f"{label}: " + ", ".join(f"{c}={fracs[c]*100:.1f}%" for c in CATEGORIES))

        bars = ax.bar(CATEGORIES, fracs.values, color=COLORS,
                      edgecolor="black", linewidth=0.8)
        for bar, hatch in zip(bars, HATCHES):
            bar.set_hatch(hatch)
        for bar, val in zip(bars, fracs.values):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.01,
                    f"{val*100:.1f}%", ha="center", va="bottom", fontsize=13)

        ax.set_title(f"IDS Detection Rate {label}")
        ax.set_xlabel("Detected Devices")
        ax.set_ylim(0, 1.1)
        ax.grid(axis="y", linestyle="--", alpha=0.6)

    axes[0].set_ylabel("Probability")
    fig.tight_layout()
    fig.savefig(OUT_PDF)
    fig.savefig(OUT_PNG, dpi=150)
    print(f"Saved {OUT_PDF}")
    print(f"Saved {OUT_PNG}")
    plt.show()


if __name__ == "__main__":
    main()
