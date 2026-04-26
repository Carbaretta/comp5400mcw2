from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set the input and output folders.
experiments_folder = Path("experiments")
figures_folder = Path("figures")
figures_folder.mkdir(exist_ok=True)

# These are the variables and levels used throughout the plots.
variables = ["separation", "alignment", "cohesion", "fear", "contagion", "noise"]
levels = ["minimum", "baseline", "medium", "maximum"]

# Turn an experiment title into the matching csv filename.
def experiment_to_filename(experiment_title):
    return experiments_folder/f"experiment_{experiment_title}.csv"

# Load one csv and prepare the time values for plotting.
def load_experiment(experiment_title):
    file_path = experiment_to_filename(experiment_title)
    df = pd.read_csv(file_path)

    # Round time to the nearest whole second for cleaner plotting.
    df["Time Rounded (s)"] = df["Time (s)"].round(0).astype(int)

    return df

# Get the final prey population from one experiment.
def final_prey_population(experiment_title):
    df = load_experiment(experiment_title)
    return float(df["Prey Population"].iloc[-1])

# Convert final prey population into a survival percemtage.
def final_survival_percentage(experiment_title, initial_population=150):
    final_population = final_prey_population(experiment_title)
    return (final_population/initial_population) * 100.0

# Stre the five baseline conditions in one list.
baseline_experiments = [
    "predator_1_nearest_baseline",
    "predator_1_cluster_baseline",
    "predator_25_nearest_baseline",
    "predator_25_cluster_baseline",
    "predator_0_baseline"
]

# Build an experiment title for a parameter test.
def parameter_experiment_title(predator_count, targeting, variable, level):
    return f"predator_{predator_count}_{targeting}_{variable}_{level}"

# Build the baseline title for a predator-present condition.
def predator_baseline_title(predator_count, targeting):
    return f"predator_{predator_count}_{targeting}_baseline"

# Use clearer display names in the plot titles.
def variable_display_name(variable):
    names = {
        "separation": "Separation",
        "alignment": "Alignment",
        "cohesion": "Cohesion",
        "fear": "Predator Fear Response",
        "contagion": "Panic Contagion",
        "noise": "Organic Noise"
    }
    
    return names[variable]

# Use clearer labels on the x-axis labels.
def level_display_name(level):
    names = {
        "minimum": "Minimum",
        "baseline": "Baseline",
        "medium": "Medium",
        "maximum": "Maximum"
    }
    
    return names[level]

# Plot prey population over time for the five baseline conditions.
def plot_baseline_population_over_time():
    plt.figure(figsize=(8, 5))

    # Use clearer labels for the legened.
    labels = {
        "predator_0_baseline": "0 Predators",
        "predator_1_nearest_baseline": "1 Predator: Nearest Strategy",
        "predator_1_cluster_baseline": "1 Predator: Cluster Strategy",
        "predator_25_nearest_baseline": "25 Predators: Nearest Strategy",
        "predator_25_cluster_baseline": "25 Predators: Cluster Strategy",
    }

    # Plot one line for each baseline experiment.
    for title in baseline_experiments:
        df = load_experiment(title)

        # Make the no-predator line easier to distinguish.
        if title == "predator_0_baseline":
            plt.plot(df["Time Rounded (s)"], df["Prey Population"], label=labels[title], linestyle="--")
        else:
            plt.plot(df["Time Rounded (s)"], df["Prey Population"], label=labels[title])

    plt.xlabel("Time (s)")
    plt.ylabel("Prey Population")
    plt.title("Baseline Prey Population over Time")
    plt.grid(True, alpha=0.5)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(figures_folder/"baseline_prey_population_over_time.png", dpi=300)
    plt.close()

# Plot average nearest-neighbour distance over time for the baseline conditions.
def plot_baseline_average_nearest_neighbour_distance_over_time():
    plt.figure(figsize=(8, 5))

    # Use clearer labels for the legened.
    labels = {
        "predator_0_baseline": "0 Predators",
        "predator_1_nearest_baseline": "1 Predator: Nearest Strategy",
        "predator_1_cluster_baseline": "1 Predator: Cluster Strategy",
        "predator_25_nearest_baseline": "25 Predators: Nearest Strategy",
        "predator_25_cluster_baseline": "25 Predators: Cluster Strategy",
    }

    # Plot one line for each baseline experiment.
    for title in baseline_experiments:
        df = load_experiment(title)

        # Make the no-predator line easier to distinguish.
        if title == "predator_0_baseline":
            plt.plot(df["Time Rounded (s)"], df["Avg Nearest Neighbor Distance"], label=labels[title], linestyle="--")
        else:
            plt.plot(df["Time Rounded (s)"], df["Avg Nearest Neighbor Distance"], label=labels[title])

    plt.xlabel("Time (s)")
    plt.ylabel("Average Nearest-Neighbor Distance")
    plt.title("Baseline Average Nearest-Neighbor Distance over Time")
    plt.grid(True, alpha=0.5)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(figures_folder/"baseline_average_nearest_neighbor_distance_over_time.png", dpi=300)
    plt.close()

# Plot how parameter changes affect survival for one predator count.
def plot_parameter_effects_on_survival(predator_count, output_name):
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    axes = axes.flatten()

    # Set the x-axis positions and labels once.
    x_labels = [level_display_name(level) for level in levels]
    x = np.arange(len(x_labels))

    # Each subplot is for one variable.
    for ax, variable in zip(axes, variables):
        nearest_values = []
        cluster_values = []

        # Get the four survival values for this variables across the x-axis levels.
        for level in levels:
            if level == "baseline":
                nearest_title = predator_baseline_title(predator_count, "nearest")
                cluster_title = predator_baseline_title(predator_count, "cluster")
            else:
                nearest_title = parameter_experiment_title(predator_count, "nearest", variable, level)
                cluster_title = parameter_experiment_title(predator_count, "cluster", variable, level)

            nearest_values.append(final_survival_percentage(nearest_title))
            cluster_values.append(final_survival_percentage(cluster_title))

        # Plot nearest and cluster targeting on the same subplot.
        ax.plot(x, nearest_values, marker="o", label="Nearest")
        ax.plot(x, cluster_values, marker="o", label="Cluster")
        ax.set_title(variable_display_name(variable))
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, rotation=20)
        ax.set_ylabel("Final Survival (%)")
        ax.grid(True, alpha=0.5)

    # Use one shared legend for the whole figure.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", ncol=2)

    # Set the overall figure title based on predator count.
    if predator_count == 1:
        fig_title = "Effect of Flocking Parameters on Survival with 1 Predator"
    elif predator_count == 25:
        fig_title = "Effect of Flocking Parameters on Survival with 25 Predators"

    fig.suptitle(fig_title)
    plt.tight_layout()
    fig.savefig(figures_folder/output_name, dpi=300)
    plt.close(fig)

# Build the condition labels used in the targeting comparison.
def matched_conditions():
    conditions = ["baseline"]

    # Add each variable-level combination after baseline.
    for variable in variables:
        for level in ["minimum", "medium", "maximum"]:
            conditions.append(f"{variable}_{level}")

    return conditions

# Turn one matched condition into a full experiment title.
def experiment_title_from_condition(predator_count, targeting, condition):
    if condition == "baseline":
        return predator_baseline_title(predator_count, targeting)
    
    # Split a condition into variable and level.
    variable, level = condition.rsplit("_", 1)
    
    return parameter_experiment_title(predator_count, targeting, variable, level)

# Compre nearest and cluster targeting across matched conditions.
def plot_targeting_strategy_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    
    # Make one subplot for 1 predator and one for 25 predators.
    for ax, predator_count in zip(axes, [1, 25]):
        conditions = matched_conditions()

        nearest_values = []
        cluster_values = []

        # Collect the final survival values for each matched condition.
        for condition in conditions:
            nearest_title = experiment_title_from_condition(predator_count, "nearest", condition)
            cluster_title = experiment_title_from_condition(predator_count, "cluster", condition)

            nearest_values.append(final_survival_percentage(nearest_title))
            cluster_values.append(final_survival_percentage(cluster_title))

        x = np.arange(len(conditions))

        # Plot the two targeting strategies on the same subplot.
        ax.plot(x, nearest_values, marker="o", label="Nearest")
        ax.plot(x, cluster_values, marker="o", label="Cluster")

        if predator_count == 1:
            ax.set_title("1 Predator")
        elif predator_count == 25:
            ax.set_title("25 Predators")
            
        ax.set_xlabel("Matched Condition")
        ax.set_xticks(x)
        ax.set_xticklabels(range(1, len(conditions) + 1))
        ax.set_ylabel("Final Survival (%)")
        ax.grid(True, alpha=0.5)

    # Use one shared legend for the whole figure.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", ncol=2)
    fig.suptitle("Overall Comparison of Predator Targeting Strategies")
    plt.tight_layout()
    fig.savefig(figures_folder/"targeting_strategy_comparison.png", dpi=300)
    plt.close(fig)

# Save a key for the numbered conditions used in the targeting comparison plot.
def save_targeting_condition_key():
    rows = []

    # Save the condition numbers for both predator counts.
    for predator_count in [1, 25]:
        conditions = matched_conditions()
        
        for i, condition in enumerate(conditions, start=1):
            rows.append({
                "Predator Count": predator_count,
                "Condition Number": i,
                "Condition": condition
            })

    df = pd.DataFrame(rows)
    df.to_csv(figures_folder/"targeting_strategy_condition_key.csv", index=False)

# Run all plotting functins and save all output files.
def main():
    plot_baseline_population_over_time()
    plot_baseline_average_nearest_neighbour_distance_over_time()
    plot_parameter_effects_on_survival(1, "parameter_effects_on_survival_1_predator.png")
    plot_parameter_effects_on_survival(25, "parameter_effects_on_survival_25_predators.png")
    plot_targeting_strategy_comparison()
    save_targeting_condition_key()
    print("All figures saved in the 'figures' folder.")

if __name__ == "__main__":
    main()
