import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.signal import savgol_filter  # For Savitzky-Golay filtering

# Function to calculate the drawbar coefficient
def calculate_drawbar_coeff(df):
    df['resultant_fx_fy'] = np.sqrt(df['f_x']**2 + df['f_y']**2)
    df['drawbar_coeff'] = df['resultant_fx_fy'] / df['f_z']
    return df

# Function to apply smoothing
def smooth_data(y, method='moving_average', window_size=5, polyorder=2):
    if method == 'moving_average':
        return y.rolling(window=window_size, center=True, min_periods=1).mean()  # Moving average
    elif method == 'savgol':
        return savgol_filter(y, window_length=window_size, polyorder=polyorder)  # Savitzky-Golay filter
    else:
        return y  # No smoothing

# Set up argument parsing
parser = argparse.ArgumentParser(description="Plot 2D graph of drawbar coefficient vs time for different scale values.")
parser.add_argument('--csv', nargs='+', help="Paths to CSV files", required=True)
parser.add_argument('--scale', nargs='+', type=float, help="Scale factors for each CSV file", required=True)
parser.add_argument('--slip', type=float, help="Constant slip value for all CSV files", required=True)
parser.add_argument('--smooth', type=str, default='moving_average', choices=['moving_average', 'savgol', 'none'],
                    help="Smoothing method: 'moving_average', 'savgol', or 'none'")
parser.add_argument('--window_size', type=int, default=5,
                    help="Window size for smoothing (must be an odd integer for Savitzky-Golay)")
parser.add_argument('--polyorder', type=int, default=2,
                    help="Polynomial order for Savitzky-Golay filter")

args = parser.parse_args()

# Check if the number of CSV files and scale factors match
if len(args.csv) != len(args.scale):
    print("Error: The number of CSV files and scale factors must match.")
    sys.exit(1)

# Create a 2D plot
plt.figure()

# Use a colormap for different scale values
colors = plt.cm.viridis(np.linspace(0, 1, len(args.scale)))

# Process each CSV file
for csv_path, scale, color in zip(args.csv, args.scale, colors):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Calculate the drawbar coefficient
    df = calculate_drawbar_coeff(df)

    # Apply smoothing to the drawbar coefficient data
    if args.smooth != 'none':
        if args.smooth == 'moving_average':
            df['drawbar_coeff_smooth'] = smooth_data(
                df['drawbar_coeff'], method='moving_average', window_size=args.window_size
            )
        elif args.smooth == 'savgol':
            df['drawbar_coeff_smooth'] = smooth_data(
                df['drawbar_coeff'], method='savgol', window_size=args.window_size, polyorder=args.polyorder
            )
        y_values = df['drawbar_coeff_smooth']
    else:
        y_values = df['drawbar_coeff']

    # Plot drawbar coefficient vs time (using the 't' column)
    plt.plot(df['t'], y_values, color=color, label=f'Scale {scale} ({scale*20}x scaled)')

# Add labels and legend
plt.xlabel('Time (t)')
plt.ylabel('Drawbar Coefficient')
plt.title(f'Drawbar Coefficient vs Time (Slip = {args.slip})')
plt.legend(title="Scale Factors")

# Show the plot
plt.show()