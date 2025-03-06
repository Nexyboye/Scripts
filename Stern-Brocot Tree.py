import matplotlib.pyplot as plt
import numpy as np
import sys

tree_levels = 20

def progress_bar(
    current,
    total,
    length=100
    ):
    progress = int(length * current / total)
    bar = "#" * progress + "-" * (length - progress)
    sys.stdout.write("\r[%s] %d%%" % (bar, 100 * current / total))
    sys.stdout.flush()

def build_stern_brocot_tree(left, right, level, max_level, level_fractions):
    if level > max_level:
        return
    mediant_numer = left[0] + right[0]
    mediant_denom = left[1] + right[1]
    mediant = (mediant_numer, mediant_denom)
    level_fractions.setdefault(level, []).append(mediant)

    build_stern_brocot_tree(left, mediant, level + 1, max_level, level_fractions)
    build_stern_brocot_tree(mediant, right, level + 1, max_level, level_fractions)

def plot_stern_brocot_tree_and_density(max_level):
    level_fractions = {}
    left = (1, 1)
    right = (2, 1)
    mediant = (left[0] + right[0], left[1] + right[1])
    level_fractions[0] = [mediant]

    build_stern_brocot_tree(left, mediant, 1, max_level, level_fractions)
    build_stern_brocot_tree(mediant, right, 1, max_level, level_fractions)

    x_vals = []
    y_vals = []
    all_values = []
    print("\nGenerating..")
    for i, level in enumerate(sorted(level_fractions.keys())):
        fractions = level_fractions[level]
        for frac in fractions:
            value = frac[0] / frac[1]
            x_vals.append(value)
            y_vals.append(level)
            all_values.append(value)
        progress_bar(i+1, len(level_fractions.keys()))
    
    print(f"\n\nnumber of fractions: {len(y_vals)}")
    
    print("\n\nPlotting tree values..")
    
    plt.figure(figsize=(10, 6))
    plt.minorticks_on()
    plt.scatter(x_vals, y_vals, color='black', s=1, alpha=0.7)
    plt.xlabel('Value')
    plt.ylabel('Level')
    plt.grid(which='major', linestyle='-', linewidth=0.1, color='red')
    plt.grid(which='minor', linestyle=':', linewidth=0.25, color='red')
    plt.title('Stern-Brocot Tree')
    plt.gca().invert_yaxis()
    plt.show()

    print("\n\nPlotting density values..")

    plt.figure(figsize=(10, 6))
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth=0.1, color='red')
    plt.grid(which='minor', linestyle=':', linewidth=0.25, color='red')
    plt.hist(all_values, bins=5000, density=True, color='black', alpha=0.7)
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title('Density of Stern-Brocot Tree Values')
    plt.show()

plot_stern_brocot_tree_and_density(tree_levels)
