import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================
# INPUT CSV
# =========================

csv_path = "maviper/results/experiment9/regression_trees_2026_10_01_01_24_56-D2.csv"

# Folder to save plots
output_dir = Path("maviper/data/experiment9")
output_dir.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv(csv_path)

# Separate Titan and Spot
titan = df[df["robot"].str.lower() == "titan"].sort_values("depth")
spot = df[df["robot"].str.lower() == "spot"].sort_values("depth")


# =========================
# HELPER FUNCTION
# =========================

def save_plot(filename):
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / filename, dpi=300)
    plt.show()


# =========================
# R2 vs DEPTH
# =========================

plt.figure()

plt.plot(
    titan["depth"],
    titan["r2"],
    marker="o",
    label="Titan"
)

plt.plot(
    spot["depth"],
    spot["r2"],
    marker="o",
    label="Spot"
)

plt.xlabel("Decision Tree Depth")
plt.ylabel("R²")
plt.title("R² vs Decision Tree Depth")

save_plot("r2_vs_depth.png")


# =========================
# MAE vs DEPTH
# =========================

plt.figure()

plt.plot(
    titan["depth"],
    titan["mae"],
    marker="o",
    label="Titan"
)

plt.plot(
    spot["depth"],
    spot["mae"],
    marker="o",
    label="Spot"
)

plt.xlabel("Decision Tree Depth")
plt.ylabel("MAE")
plt.title("MAE vs Decision Tree Depth")

save_plot("mae_vs_depth.png")


# =========================
# MSE vs DEPTH
# =========================

plt.figure()

plt.plot(
    titan["depth"],
    titan["mse"],
    marker="o",
    label="Titan"
)

plt.plot(
    spot["depth"],
    spot["mse"],
    marker="o",
    label="Spot"
)

plt.xlabel("Decision Tree Depth")
plt.ylabel("MSE")
plt.title("MSE vs Decision Tree Depth")

save_plot("mse_vs_depth.png")


# =========================
# NODE COUNT vs DEPTH
# =========================

plt.figure()

plt.plot(
    titan["depth"],
    titan["nodes"],
    marker="o",
    label="Titan"
)

plt.plot(
    spot["depth"],
    spot["nodes"],
    marker="o",
    label="Spot"
)

plt.xlabel("Decision Tree Depth")
plt.ylabel("Node Count")
plt.title("Decision Tree Complexity vs Depth")

save_plot("nodes_vs_depth.png")


# =========================
# R2 vs NODE COUNT
# =========================

plt.figure()

plt.plot(
    titan["nodes"],
    titan["r2"],
    marker="o",
    label="Titan"
)

plt.plot(
    spot["nodes"],
    spot["r2"],
    marker="o",
    label="Spot"
)

plt.xlabel("Decision Tree Complexity (Node Count)")
plt.ylabel("R²")
plt.title("R² vs Decision Tree Complexity")

save_plot("r2_vs_nodes.png")


# =========================
# MAE vs NODE COUNT
# =========================

plt.figure()

plt.plot(
    titan["nodes"],
    titan["mae"],
    marker="o",
    label="Titan"
)

plt.plot(
    spot["nodes"],
    spot["mae"],
    marker="o",
    label="Spot"
)

plt.xlabel("Decision Tree Complexity (Node Count)")
plt.ylabel("MAE")
plt.title("MAE vs Decision Tree Complexity")

save_plot("mae_vs_nodes.png")


# =========================
# MSE vs NODE COUNT
# =========================

plt.figure()

plt.plot(
    titan["nodes"],
    titan["mse"],
    marker="o",
    label="Titan"
)

plt.plot(
    spot["nodes"],
    spot["mse"],
    marker="o",
    label="Spot"
)

plt.xlabel("Decision Tree Complexity (Node Count)")
plt.ylabel("MSE")
plt.title("MSE vs Decision Tree Complexity")

save_plot("mse_vs_nodes.png")