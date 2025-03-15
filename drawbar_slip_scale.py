import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

# Function to calculate the drawbar coefficient
def calculate_drawbar_coeff(df):
    df['resultant_fx_fy'] = np.sqrt(df['f_x']**2 + df['f_y']**2)
    df['drawbar_coeff'] = df['resultant_fx_fy'] / df['f_z']
    return df['drawbar_coeff'].mean()

# Set up argument parsing
parser = argparse.ArgumentParser(description="Plot 2D graph of drawbar coefficient vs slip for different scale values.")
parser.add_argument('--csv', nargs='+', help="Paths to CSV files", required=True)
parser.add_argument('--scale', nargs='+', type=float, help="Scale factors for each CSV file", required=True)
parser.add_argument('--slip', nargs='+', type=float, help="Slip values for each CSV file", required=True)

args = parser.parse_args()

# Check if the number of CSV files, scale factors, and slip values match
if len(args.csv) != len(args.scale) or len(args.csv) != len(args.slip):
    print("Error: The number of CSV files, scale factors, and slip values must match.")
    sys.exit(1)

# Dictionary to store data for plotting, grouped by scale values
data = {}

# Process each CSV file
for csv_path, scale, slip in zip(args.csv, args.scale, args.slip):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Calculate the average drawbar coefficient
    avg_drawbar_coeff = calculate_drawbar_coeff(df)

    # Store the data grouped by scale value
    if scale not in data:
        data[scale] = {'slips': [], 'drawbar_coeffs': []}
    data[scale]['slips'].append(slip)
    data[scale]['drawbar_coeffs'].append(avg_drawbar_coeff)

# Create a 2D plot
plt.figure()

# Use a colormap for different scale values
colors = plt.cm.viridis(np.linspace(0, 1, len(data.keys())))

# Plot lines for each scale value
for scale, color in zip(sorted(data.keys()), colors):
    slips = np.array(data[scale]['slips'])
    drawbar_coeffs = np.array(data[scale]['drawbar_coeffs'])

    # Sort by slip value to ensure proper line connections
    sort_idx = np.argsort(slips)
    slips = slips[sort_idx]
    drawbar_coeffs = drawbar_coeffs[sort_idx]

    # Plot the line for this scale value
    plt.plot(slips, drawbar_coeffs, color=color, label=f'Scale {scale}')

# Add labels and legend
plt.xlabel('Slip Value')
plt.ylabel('Drawbar Coefficient')
plt.title('Drawbar Coefficient vs Slip for Different Scale Values')
plt.legend(title="Scale Factors")

# Show the plot
plt.show()

