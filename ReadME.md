                            Combined Plotter Tool (combined_plotter.py)

This repository contains a Python script that provides various functionalities for plotting and analyzing data from single-wheel experimental data. The script is designed to be modular and easy to use, allowing users to visualize and analyze data with minimal setup.

Features:

Chronosim Data Plotting:

    Plot position, velocity, and wheel torques over time.

    Analyze slip and effective radius based on the provided data.

Drawbar Coefficient Plotting:

    Plot experimental and simulated drawbar coefficient data for different terrains (e.g., sand, fillite).

    Compare results from different simulations (e.g., Moonranger on Earth vs. Moon).

Single Wheel Experimental Data Plotting:

    Plot forces, drawbar coefficient, and maximum velocity over time for single-wheel experiments.

Batch Processing:

    Process multiple datasets from subfolders, calculate mean drawbar coefficients, and plot results.

    Save processed data for further analysis.



Requirements
Python 3.x

Required Python packages:

numpy
pandas
matplotlib

You can install the required packages using pip:
pip install numpy pandas matplotlib


Usage
The script is designed to be run from the command line. Below are the available functionalities and their usage:

1. Plot Chronosim Data
python combined_plotter.py plot_chronosim <file_path>


2. Plot Drawbar Coefficient Data
python combined_plotter.py plot_drawbar


3. Plot Single Wheel Experimental Data
python combined_plotter.py plot_single_wheel <file_path>
s will generate plots for forces, drawbar coefficient, and maximum velocity over time.

4. Batch Process Data
To process multiple datasets from subfolders:


                        Drawbar Slip Scale Tool (drawbar_slip_scale.py)

This Python script generates a 3D scatter plot to visualize the relationship between time, drawbar coefficient (d_c), and scale factors for multiple datasets. 

Each dataset corresponds to a specific file, and the points in the plot are color-coded based on the slip factor (0.000, 0.100, or 0.200). The script uses command-line arguments to accept a list of data files, their corresponding scale factors, and slip factors. 

It processes the data, ensures the required columns (t for time and d_c for drawbar coefficient) are present, and creates an interactive 3D plot using matplotlib. 

The plot helps analyze how the drawbar coefficient varies over time and across different scale factors, with slip factors providing additional context through color differentiation

Example:
python script_name.py file1.csv file2.csv file3.csv --scale_factors 1.0 1.5 2.0 --slip_factors 0.000 0.100 0.200



                        Multiple Scale Plotter (multiple_scale.py)

This script creates a 3D scatter plot to visualize the relationship between time, force magnitude, and scale factors across multiple datasets. It processes CSV files containing force components (f_x, f_y, f_z) and time (t), computes the force magnitude, and plots the data in 3D. Points are color-mapped based on scale factors for better visualization

Example:
python script_name.py file1.csv file2.csv --scale_factors 1.0 2.0


