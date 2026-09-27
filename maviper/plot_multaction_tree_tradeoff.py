import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================
# INPUT CSV
# =========================

csv_path = "maviper/results/experiment5/regression_trees_2026_09_27_01_25_48.csv"

# Folder to save plots
output_dir = Path("maviper/data/experiment5")
output_dir.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv(csv_path)

# Each entry in "robot" now represents
# a specific robot/action combination:
#
# Titan_Linear
# Titan_Angular
# Spot_Linear
# Spot_Lateral
# Spot_Angular

action_types = df["robot"].unique()


# =========================
# HELPER FUNCTION
# =========================

def save_plot(filename):
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / filename, dpi=300)
    plt.show()
    plt.close()


# =========================
# GENERATE PLOTS FOR EACH
# ROBOT / ACTION TYPE
# =========================

for action_type in action_types:

    # Select and sort data for this action
    action_data = (
        df[df["robot"] == action_type]
        .sort_values("depth")
    )

    # Make nicer name for graph titles
    display_name = action_type.replace("_", " ")

    # Make safe lowercase name for filenames
    file_name = action_type.lower()


    # =========================
    # R2 vs DEPTH
    # =========================

    plt.figure()

    plt.plot(
        action_data["depth"],
        action_data["r2"],
        marker="o",
        label=display_name
    )

    plt.xlabel("Decision Tree Depth")
    plt.ylabel("R²")
    plt.title(f"R² vs Decision Tree Depth - {display_name}")

    save_plot(f"{file_name}_r2_vs_depth.png")


    # =========================
    # MAE vs DEPTH
    # =========================

    plt.figure()

    plt.plot(
        action_data["depth"],
        action_data["mae"],
        marker="o",
        label=display_name
    )

    plt.xlabel("Decision Tree Depth")
    plt.ylabel("MAE")
    plt.title(f"MAE vs Decision Tree Depth - {display_name}")

    save_plot(f"{file_name}_mae_vs_depth.png")


    # =========================
    # MSE vs DEPTH
    # =========================

    plt.figure()

    plt.plot(
        action_data["depth"],
        action_data["mse"],
        marker="o",
        label=display_name
    )

    plt.xlabel("Decision Tree Depth")
    plt.ylabel("MSE")
    plt.title(f"MSE vs Decision Tree Depth - {display_name}")

    save_plot(f"{file_name}_mse_vs_depth.png")


    # =========================
    # NODE COUNT vs DEPTH
    # =========================

    plt.figure()

    plt.plot(
        action_data["depth"],
        action_data["nodes"],
        marker="o",
        label=display_name
    )

    plt.xlabel("Decision Tree Depth")
    plt.ylabel("Node Count")
    plt.title(f"Decision Tree Complexity vs Depth - {display_name}")

    save_plot(f"{file_name}_nodes_vs_depth.png")


    # =========================
    # R2 vs NODE COUNT
    # =========================

    plt.figure()

    plt.plot(
        action_data["nodes"],
        action_data["r2"],
        marker="o",
        label=display_name
    )

    plt.xlabel("Decision Tree Complexity (Node Count)")
    plt.ylabel("R²")
    plt.title(f"R² vs Decision Tree Complexity - {display_name}")

    save_plot(f"{file_name}_r2_vs_nodes.png")


    # =========================
    # MAE vs NODE COUNT
    # =========================

    plt.figure()

    plt.plot(
        action_data["nodes"],
        action_data["mae"],
        marker="o",
        label=display_name
    )

    plt.xlabel("Decision Tree Complexity (Node Count)")
    plt.ylabel("MAE")
    plt.title(f"MAE vs Decision Tree Complexity - {display_name}")

    save_plot(f"{file_name}_mae_vs_nodes.png")


    # =========================
    # MSE vs NODE COUNT
    # =========================

    plt.figure()

    plt.plot(
        action_data["nodes"],
        action_data["mse"],
        marker="o",
        label=display_name
    )

    plt.xlabel("Decision Tree Complexity (Node Count)")
    plt.ylabel("MSE")
    plt.title(f"MSE vs Decision Tree Complexity - {display_name}")

    save_plot(f"{file_name}_mse_vs_nodes.png")