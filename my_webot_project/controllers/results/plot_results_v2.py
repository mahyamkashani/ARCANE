"""
Presentation-quality plots for the resilience experiments  (ALL heatmaps).

Two families of heatmaps:
  DETERMINISTIC  -> the (k x theta_crit) -> gamma sweep. gamma is a pure
                    function of k and theta_crit (no variance). Shown as an
                    annotated gamma heatmap with the analytic boundary
                    theta_crit = psi = 1 - k * alpha_crit, plus a boundary
                    heatmap over (k x alpha_crit).
  STOCHASTIC     -> repeated runs (IDS detection is a Bernoulli trial, see
                    ids.py). Aggregated into heatmaps: mean metric per
                    (detection_rate x |S|), a metric-summary heatmap, and -
                    if you generate a per-run sweep CSV - P(gamma=0) and
                    mean-psi heatmaps over (k x theta_crit).

Run:  python plot_results_v2.py        (you are in vlm-env)
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# ----------------------------------------------------------------------
# Style + shared constants
# ----------------------------------------------------------------------
sns.set_theme(style="white", context="talk")

DATA_DIR = "task1"
ORANGE = "#f68838"   # gamma = 1  (tolerable)
RED = "#ee3e32"      # gamma = 0  (intolerable)
GAMMA_CMAP = ListedColormap([RED, ORANGE])   # 0 -> red, 1 -> orange


def _path(name):
    return os.path.join(DATA_DIR, name)


def _save(fig, name):
    out = f"{name}.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[saved] {out}")


# ======================================================================
# DETERMINISTIC HEATMAPS  (the k x theta_crit sweep)
# ======================================================================

def plot_gamma_heatmap(file="alpha_crit0.1_theta_crit_sweep.csv",
                       alpha_label=r"$\alpha_{crit}=0.1$"):
    """Annotated 0/1 gamma heatmap with the analytic boundary overlaid."""
    df = pd.read_csv(_path(file))
    pivot = df.pivot(index="k", columns="theta_crit", values="gamma")

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(
        pivot, cmap=GAMMA_CMAP, vmin=0, vmax=1, cbar=False,
        annot=True, fmt="d", linewidths=.5, linecolor="black",
        annot_kws={"fontsize": 9}, ax=ax,
        xticklabels=[round(float(t), 2) for t in pivot.columns],
    )
    ax.tick_params(axis="x", rotation=45)
    ax.invert_yaxis()  # k increasing upward

    # Analytic boundary: gamma flips to 0 when theta_crit > psi = 1 - k*alpha
    alpha = float(df["alpha_crit"].iloc[0])
    thetas = sorted(pivot.columns)
    ks = sorted(pivot.index)

    def theta_to_x(t):
        return float(np.interp(t, thetas, range(len(thetas))))
    bx = [theta_to_x(1 - k * alpha) for k in ks]
    by = [list(ks).index(k) for k in ks]
    ax.plot([x + 0.5 for x in bx], [y + 0.5 for y in by],
            color="black", lw=2, ls="--", marker="o",
            label=r"$\theta_{crit}=\psi=1-k\,\alpha_{crit}$")

    ax.set_xlabel(r"$\theta_{crit}$")
    ax.set_ylabel("Number of attacked devices  $k$")
    ax.set_title(f"Tolerable degradation $\\gamma$   ({alpha_label})")

    legend_red = plt.Line2D([0], [0], marker="s", color="w",
                            markerfacecolor=RED, markersize=12, label=r"$\gamma=0$")
    legend_org = plt.Line2D([0], [0], marker="s", color="w",
                            markerfacecolor=ORANGE, markersize=12, label=r"$\gamma=1$")
    boundary = plt.Line2D([0], [0], color="black", lw=2, ls="--",
                          label=r"$\theta_{crit}=1-k\,\alpha$")
    ax.legend(handles=[legend_org, legend_red, boundary],
              loc="upper right", fontsize=10, framealpha=.9)
    plt.tight_layout()
    _save(fig, "gamma_heatmap")
    plt.show()


def plot_gamma_facets(files=None):
    """Side-by-side gamma heatmaps for several alpha_crit values."""
    if files is None:
        files = {
            r"$\alpha_{crit}=0.1$": "alpha_crit0.1_theta_crit_sweep.csv",
            r"$\alpha_{crit}=0.2$": "alpha_crit0.2_theta_crit_sweep.csv",
            r"$\alpha_{crit}=0.3$": "alpha_crit0.3_theta_crit_sweep.csv",
        }
    fig, axes = plt.subplots(1, len(files), figsize=(6 * len(files), 5), sharey=True)
    if len(files) == 1:
        axes = [axes]
    for ax, (title, fname) in zip(axes, files.items()):
        df = pd.read_csv(_path(fname))
        pivot = df.pivot(index="k", columns="theta_crit", values="gamma")
        sns.heatmap(pivot, cmap=GAMMA_CMAP, vmin=0, vmax=1, cbar=False,
                    annot=True, fmt="d", linewidths=.5, linecolor="black",
                    annot_kws={"fontsize": 8}, ax=ax,
                    xticklabels=[round(float(t), 2) for t in pivot.columns])
        ax.tick_params(axis="x", rotation=45)
        ax.invert_yaxis()
        ax.set_title(title)
        ax.set_xlabel(r"$\theta_{crit}$")
    axes[0].set_ylabel("Number of attacked devices  $k$")
    plt.tight_layout()
    _save(fig, "gamma_facets")
    plt.show()


def plot_boundary_heatmap(files=None):
    """Heatmap of the tolerance boundary: max theta_crit still tolerable
    (= psi = 1 - k*alpha) over (k x alpha_crit). Replaces the line plot."""
    if files is None:
        files = {
            0.1: "alpha_crit0.1_theta_crit_sweep.csv",
            0.2: "alpha_crit0.2_theta_crit_sweep.csv",
            0.3: "alpha_crit0.3_theta_crit_sweep.csv",
        }
    rows = []
    for alpha, fname in files.items():
        df = pd.read_csv(_path(fname))
        for k in sorted(df.k.unique()):
            rows.append({"k": k, "alpha_crit": alpha, "psi": max(1 - k * alpha, 0)})
    grid = pd.DataFrame(rows).pivot(index="k", columns="alpha_crit", values="psi")

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(grid, cmap="viridis", annot=True, fmt=".2f",
                linewidths=.5, linecolor="white", ax=ax,
                cbar_kws={"label": r"max tolerable $\theta_{crit}=\psi$"})
    ax.invert_yaxis()
    ax.set_xlabel(r"$\alpha_{crit}$")
    ax.set_ylabel("Number of attacked devices  $k$")
    ax.set_title(r"Degradation-tolerance boundary  $\psi=1-k\,\alpha_{crit}$")
    plt.tight_layout()
    _save(fig, "boundary_heatmap")
    plt.show()


# ======================================================================
# STOCHASTIC HEATMAPS  (repeated detection runs)
# ======================================================================

def _load_detection(rates=(70, 80, 90)):
    frames = []
    for r in rates:
        f = _path(f"detection_{r}.csv")
        if os.path.exists(f):
            df = pd.read_csv(f)
            df["rate"] = r
            df["n_dev"] = df["devices"].fillna("{}").str.count("LW|RW")
            frames.append(df)
    if not frames:
        raise FileNotFoundError("No detection_*.csv files found.")
    return pd.concat(frames, ignore_index=True)


def plot_detection_metric_heatmap(metric="degradation"):
    """Mean metric over (detection_rate x number of compromised devices |S|).
    Empty (rate, |S|) combinations are left blank."""
    df = _load_detection()
    grid = df.pivot_table(index="rate", columns="n_dev", values=metric, aggfunc="mean")
    cnt = df.pivot_table(index="rate", columns="n_dev", values=metric, aggfunc="size")

    # annotate with "mean\n(n=..)"
    labels = grid.copy().astype(object)
    for i in grid.index:
        for j in grid.columns:
            v = grid.loc[i, j]
            n = cnt.loc[i, j] if (i in cnt.index and j in cnt.columns) else np.nan
            labels.loc[i, j] = "" if pd.isna(v) else f"{v:.1f}\n(n={int(n)})"

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(grid, cmap="rocket_r", annot=labels.values, fmt="",
                linewidths=.5, linecolor="white", ax=ax,
                annot_kws={"fontsize": 11},
                cbar_kws={"label": f"mean {metric}"})
    ax.set_xlabel(r"Number of compromised devices  $|S|$")
    ax.set_ylabel("IDS detection rate (%)")
    ax.set_title(f"Mean {metric} per detection rate and $|S|$")
    plt.tight_layout()
    _save(fig, f"detection_heatmap_{metric}")
    plt.show()


def plot_detection_summary_heatmap():
    """One heatmap summarising all metrics per detection rate.
    Columns have different units, so colour = per-column min-max normalised,
    but each cell is annotated with the real value."""
    df = _load_detection()
    g = df.groupby("rate").apply(lambda d: pd.Series({
        r"$P(\delta=0)$": (d.delta == 0).mean(),
        r"$P(\gamma=0)$": (d.gamma == 0).mean(),
        r"$P(\mathrm{resilient})$": (d.resilient == "RESILIENT").mean(),
        "mean time (s)": d.time.mean(),
        "std time (s)": d.time.std(),
        "mean degr (%)": d.degradation.mean(),
        "std degr (%)": d.degradation.std(),
    })).reset_index().set_index("rate")

    norm = (g - g.min()) / (g.max() - g.min()).replace(0, 1)  # per-column 0..1
    labels = g.copy()
    for c in g.columns:
        labels[c] = g[c].map(lambda v: f"{v:.2f}")

    fig, ax = plt.subplots(figsize=(11, 4.5))
    sns.heatmap(norm, cmap="mako", annot=labels.values, fmt="",
                linewidths=.5, linecolor="white", ax=ax,
                cbar_kws={"label": "per-column min-max (colour only)"},
                annot_kws={"fontsize": 11})
    ax.set_xlabel("")
    ax.set_ylabel("IDS detection rate (%)")
    ax.set_title("Resilience metrics per detection rate")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    _save(fig, "detection_summary_heatmap")
    plt.show()


# ----------------------------------------------------------------------
# STOCHASTIC SWEEP  (needs a per-run CSV: run_id,k,theta_crit,psi,gamma,...)
# ----------------------------------------------------------------------

def plot_pgamma_heatmap(file="sweep_runs.csv"):
    """P(gamma=0) over (k x theta_crit) -- the stochastic version of the
    deterministic gamma heatmap (continuous probability instead of 0/1)."""
    f = _path(file)
    if not os.path.exists(f):
        print(f"[skip] {f} not found - generate a per-run sweep first.")
        return
    df = pd.read_csv(f)
    agg = (df.groupby(["k", "theta_crit"])["gamma"]
             .apply(lambda g: (g == 0).mean())
             .reset_index(name="p_intolerable"))
    pivot = agg.pivot(index="k", columns="theta_crit", values="p_intolerable")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(pivot, cmap="Reds", vmin=0, vmax=1, annot=True, fmt=".2f",
                linewidths=.5, linecolor="white", ax=ax,
                cbar_kws={"label": r"$P(\gamma=0)$"})
    ax.invert_yaxis()
    ax.set_xlabel(r"$\theta_{crit}$")
    ax.set_ylabel("Number of attacked devices  $k$")
    ax.set_title(r"Probability of intolerable degradation")
    plt.tight_layout()
    _save(fig, "pgamma_heatmap")
    plt.show()


def plot_psi_heatmap(file="sweep_runs.csv"):
    """Mean remaining capacity psi over (k x theta_crit) across runs."""
    f = _path(file)
    if not os.path.exists(f):
        print(f"[skip] {f} not found - generate a per-run sweep first.")
        return
    df = pd.read_csv(f)
    pivot = df.pivot_table(index="k", columns="theta_crit", values="psi", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(pivot, cmap="viridis", annot=True, fmt=".2f",
                linewidths=.5, linecolor="white", ax=ax,
                cbar_kws={"label": r"mean $\psi$"})
    ax.invert_yaxis()
    ax.set_xlabel(r"$\theta_{crit}$")
    ax.set_ylabel("Number of attacked devices  $k$")
    ax.set_title(r"Mean remaining capacity $\psi$ across runs")
    plt.tight_layout()
    _save(fig, "psi_heatmap")
    plt.show()


# ======================================================================
if __name__ == "__main__":
    # --- deterministic heatmaps (work with your current data) ---
    plot_gamma_heatmap()
    plot_gamma_facets()
    plot_boundary_heatmap()

    # --- stochastic heatmaps from the detection_* runs ---
    plot_detection_metric_heatmap("degradation")
    plot_detection_metric_heatmap("time")
    plot_detection_summary_heatmap()

    # --- stochastic sweep heatmaps (only if sweep_runs.csv exists) ---
    plot_pgamma_heatmap()
    plot_psi_heatmap()
