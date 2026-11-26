"""Compare archived torque-component choices for the same simulation run."""
from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def read_peaks(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return {row["joint"]: row for row in csv.DictReader(stream)}


def main():
    old = read_peaks(ROOT / "data/original/motor_capacity_summary.csv")
    current = read_peaks(ROOT / "results/motor_capacity_summary.csv")
    joints = ["J1_Base", "J2_Shoulder", "J3_Elbow", "J4_Wrist1", "J5_Wrist2", "J6_Wrist3"]
    if set(old) != set(joints) or set(current) != set(joints):
        raise ValueError("Expected the same six joints in both summaries")
    if any(current[j]["axis_component"] != "TZ" for j in joints):
        raise ValueError("Corrected torque must use local TZ for every joint")
    before = [float(old[j]["required_peak_abs_torque_Nm"]) for j in joints]
    after = [float(current[j]["required_peak_abs_torque_Nm"]) for j in joints]
    fig, ax = plt.subplots(figsize=(11, 3.8), constrained_layout=True)
    fig.set_facecolor("#ffffff")
    for offset, values, color, label in [(-0.19, before, "#94a3b8", "Previous component choice"),
                                        (0.19, after, "#176b91", "Corrected: local TZ")]:
        bars = ax.bar([i + offset for i in range(6)], values, width=0.36, color=color, label=label)
        ax.bar_label(bars, labels=[f"{v:.3f}" for v in values], padding=3, fontsize=10)
    ax.set_xticks(range(6), [j.replace("_", "\n") for j in joints])
    ax.set_ylabel("Sampled peak |torque| (N m)")
    ax.set_ylim(0, 68)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.set_title("UR3 torque review | same 0-18.5 s run, 901 samples per joint", loc="left", pad=12)
    fig.savefig(ROOT / "assets/torque_comparison.png", dpi=180, facecolor="white")
    plt.close(fig)
    print("assets/torque_comparison.png")


if __name__ == "__main__":
    main()
