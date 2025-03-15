import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Plot pos_z vs time for a given slip value with vertical lines at multiples of 1.47 seconds.")
parser.add_argument('--csv', nargs='+', help="Paths to CSV files", required=True)
parser.add_argument('--scale', nargs='+', type=float, help="Scale factors for each CSV file", required=True)
parser.add_argument('--slip', type=float, help="Slip value for all CSV files", required=True)

args = parser.parse_args()

# Check if the number of CSV files and scale factors match
if len(args.csv) != len(args.scale):
    print("Error: The number of CSV files and scale factors must match.")
    sys.exit(1)

# Create a 2D plot
plt.figure()

# Use a colormap for different scale values
colors = plt.cm.viridis(np.linspace(0, 1, len(args.scale)))

# Process each CSV file and plot pos_z vs time
for csv_path, scale, color in zip(args.csv, args.scale, colors):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Plot pos_z vs time (using the 't' column)
    plt.plot(df['t'], df['pos_z'], color=color, label=f'Scale {scale}')

# Add vertical red lines at multiples of 1.47 seconds and label them
max_time = max([pd.read_csv(csv_path)['t'].max() for csv_path in args.csv])  # Find the maximum time across all files
multiples = np.arange(0, max_time + 1.47, 1.47)  # Generate multiples of 1.47 seconds
for multiple in multiples:
    plt.axvline(x=multiple, color='red', linestyle='--', alpha=0.5)
    plt.text(multiple, plt.ylim()[0], f'{multiple:.2f}', color='red', rotation=90, verticalalignment='bottom', horizontalalignment='right')

# Add labels and legend
plt.xlabel('Time (t)')
plt.ylabel('pos_z')
plt.title(f'pos_z vs Time (Slip = {args.slip})')
plt.legend(title="Scale Factors")

# Show the plot
plt.show()