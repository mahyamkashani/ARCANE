import sys
from pathlib import Path

# Make the pr2_controller package importable when running from results/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")  # headless: write a PNG without needing a display
import matplotlib.pyplot as plt
from pr2_controller.disruption_degradation import monotonic_degradation, exponential_degradation

TASK = "task"
GOAL = "goal"
ALPHA_BASE = 0.0                     # only critical devices contribute here
DEVICE_COUNTS = [1, 2, 3, 4, 5]
ALPHA_CRITS = [0.1, 0.2, 0.3, 0.4]
OUT_FILE = "monotonic_degradation.png"

PSI_FN = monotonic_degradation # exponential_degradation 



def psi_for_k_devices(k, alpha_crit):
    S = {f"d{i}" for i in range(k)}
    tau = {(d, TASK): 2 for d in S}  # level 2 => critical
    epsilon = {}
    return PSI_FN(S, tau, epsilon, TASK, GOAL, alpha_crit, ALPHA_BASE)


def main():
    plt.figure(figsize=(7, 5))

    for alpha_crit in ALPHA_CRITS:
        psis = [psi_for_k_devices(k, alpha_crit) for k in DEVICE_COUNTS]
        plt.plot(
            DEVICE_COUNTS, psis,
            marker="o",
            label=rf"$\alpha_{{crit}} = {alpha_crit}$",
        )

    plt.xlabel("Number of disrupted (critical) devices")
    plt.ylabel(r"$\psi$  (monotonic degradation)")
    plt.title(r"Monotonic degradation $\psi = \max(0,\ 1 - k\,\alpha_{crit})$")
    plt.xticks(DEVICE_COUNTS)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FILE, dpi=150)
    print(f"Saved {OUT_FILE}")


if __name__ == "__main__":
    main()
