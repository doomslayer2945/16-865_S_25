import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

# Set up argument parsing
parser = argparse.ArgumentParser(description="Plot pos_x vs time and pos_y vs time for different scale values.")
parser.add_argument('--csv', nargs='+', help="Paths to CSV files", required=True)
parser.add_argument('--scale', nargs='+', type=float, help="Scale factors for each CSV file", required=True)
parser.add_argument('--slip', type=float, help="Constant slip value for all CSV files", required=True)

args = parser.parse_args()

# Check if the number of CSV files and scale factors match
if len(args.csv) != len(args.scale):
    print("Error: The number of CSV files and scale factors must match.")
    sys.exit(1)

# Use a colormap for different scale values
colors = plt.cm.viridis(np.linspace(0, 1, len(args.scale)))

# Function to create a plot with two subplots (pos_x vs t and pos_y vs t)
def create_plot(df, scale, color, title):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle(title, fontsize=16)

    # Plot pos_x vs time
    ax1.plot(df['t'], df['pos_x'], color=color, label=f'pos_x (Scale {scale})')
    ax1.set_xlabel('Time (t)')
    ax1.set_ylabel('pos_x')
    ax1.legend()

    # Plot pos_y vs time
    ax2.plot(df['t'], df['pos_y'], color=color, label=f'pos_y (Scale {scale})')
    ax2.set_xlabel('Time (t)')
    ax2.set_ylabel('pos_y')
    ax2.legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the suptitle
    plt.show()

# Process each CSV file and create individual plots
for csv_path, scale, color in zip(args.csv, args.scale, colors):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Create a plot for this scale value
    create_plot(df, scale, color, title=f'pos_x and pos_y vs Time (Scale {scale}, Slip = {args.slip})')

# Create the combined plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle(f'Combined pos_x and pos_y vs Time (Slip = {args.slip})', fontsize=16)

for csv_path, scale, color in zip(args.csv, args.scale, colors):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Plot pos_x vs time
    ax1.plot(df['t'], df['pos_x'], color=color, label=f'pos_x (Scale {scale})')
    # Plot pos_y vs time
    ax2.plot(df['t'], df['pos_y'], color=color, label=f'pos_y (Scale {scale})')

# Add labels and legends for the combined plot
ax1.set_xlabel('Time (t)')
ax1.set_ylabel('pos_x')
ax1.legend()

ax2.set_xlabel('Time (t)')
ax2.set_ylabel('pos_y')
ax2.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the suptitle
plt.show()