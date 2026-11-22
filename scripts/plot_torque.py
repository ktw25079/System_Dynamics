"""Plot stored local-axis torque samples; does not run the dynamics solver."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]

def main():
    series = {}
    with (ROOT / "results/torque_timeseries.csv").open(newline="") as stream:
        for row in csv.DictReader(stream):
            if row["axis_component"] != "TZ":
                raise ValueError("Expected local rotation-axis component TZ")
            series.setdefault(row["joint"], []).append(
                (float(row["time_s"]), float(row["axis_torque_Nm"])))
    if len(series) != 6:
        raise ValueError("Expected six joints")
    fig, axes = plt.subplots(3, 2, figsize=(12, 8), sharex=True, constrained_layout=True)
    for ax, (joint, samples) in zip(axes.flat, sorted(series.items())):
        times, torques = zip(*samples)
        peak = max(range(len(torques)), key=lambda i: abs(torques[i]))
        ax.plot(times, torques, color="#176b91", linewidth=1.3)
        ax.scatter(times[peak], torques[peak], color="#c85028", s=20, zorder=3)
        ax.set_title(f"{joint.replace('_', ' ')} | peak |TZ| = {abs(torques[peak]):.3f} N m", loc="left", fontsize=11)
        ax.axhline(0, color="#8c98a3", linewidth=0.6)
        ax.set_ylabel("Torque (N m)")
        ax.set_xlim(0, 18.5)
        ax.grid(alpha=0.2)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    for ax in axes[-1]:
        ax.set_xlabel("Time (s)")
    fig.suptitle("UR3 joint torque · stored RecurDyn simulation\nLocal TZ · 901 samples per joint · independent vertical scales", fontsize=14)
    target = ROOT / "assets/joint_torque.png"
    fig.savefig(target, dpi=150, facecolor="white")
    plt.close(fig)
    print(target.relative_to(ROOT))

if __name__ == "__main__":
    main()
