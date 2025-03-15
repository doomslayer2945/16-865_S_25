import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import json


#  chronosimplotter.py 
def plot_chronosim_data(file_path):
    """Plot Chronosim data from a CSV file."""
    data = pd.read_csv(file_path)
    data.columns = [
        't', 'posX', 'posY', 'posZ', 'velX', 'velY', 'velZ', 
        'quatE0', 'quatE1', 'quatE2', 'quatE3', 
        'torqueLF', 'torqueRF', 'torqueLB', 'torqueRB', 'slip'
    ]

    # Create the first figure with two subplots: Position and Torque
    fig1, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

    # Position vs Time
    ax1.plot(data['t'], data[['posX', 'posY', 'posZ']])
    ax1.set_title("Position vs Time")
    ax1.set_ylabel("Position (m)")
    ax1.legend(["posX", "posY", "posZ"], loc="lower right")
    ax1.grid()

    # Torque vs Time
    ax2.plot(data['t'], data[['torqueLF', 'torqueRF', 'torqueLB', 'torqueRB']])
    ax2.set_title("Wheel Torques vs Time")
    ax2.set_ylabel("Torque (N*m)")
    ax2.legend(["lf", "rf", "lb", "rb"], loc="lower right")
    ax2.grid()

    plt.xlabel("Time (s)")
    plt.tight_layout()
    plt.show()

    # Create the second figure for Velocity
    fig2, ax3 = plt.subplots(figsize=(12, 8))

    # Velocity vs Time
    ax3.plot(data['t'], data[['velX', 'velY', 'velZ']])
    ax3.set_title("Velocity vs Time")
    ax3.set_ylabel("Velocity (m/s)")
    ax3.legend(["velX", "velY", "velZ"], loc="upper right")
    ax3.grid()
    ax3.set_ylim(-0.50, 1.00)

    plt.xlabel("Time (s)")
    plt.tight_layout()
    plt.show()

def analyze_chronosim_data(file_path, start_time=1, w_r=0.2, r_wheel=0.09):
    """Analyze Chronosim data to calculate slip and effective radius."""
    data = pd.read_csv(file_path)
    data.columns = [
        't', 'posX', 'posY', 'posZ', 'velX', 'velY', 'velZ', 
        'quatE0', 'quatE1', 'quatE2', 'quatE3', 
        'torqueLF', 'torqueRF', 'torqueLB', 'torqueRB', 'slip'
    ]

    # Slip Calculations
    start_id = data[data['t'] >= start_time].index[0]
    mean_vel_x = data['velX'].loc[start_id:].mean()
    expected_velocity = w_r * r_wheel
    slip = (1 - mean_vel_x / expected_velocity) * 100
    effective_radius = mean_vel_x / w_r

    return slip, effective_radius


#  drawbarplotter.py 
def plot_terramule_data():
    """Plot Terramule experimental data."""
    sand_data = np.genfromtxt("TerramuleData/Sand.csv", delimiter=",", skip_header=1, names=["slip", "drawbar"])
    fillite_data = np.genfromtxt("TerramuleData/Fillite.csv", delimiter=",", skip_header=1, names=["slip", "drawbar"])
    plt.plot(fillite_data["slip"], fillite_data["drawbar"], label="PHY-TERRA-FILLITE")
    plt.plot(sand_data["slip"], sand_data["drawbar"], label="PHY-TERRA-SAND")


def plot_drawbar_data():
    """Plot drawbar coefficient data."""
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(6.5, 6.5))

    plot_terramule_data()

    # Mass-adjusted terramule
    sim_terra_b = np.array([[-11, 0], [4, 0.3], [19, 0.5], [30, 0.6], [37, 0.7]])
    plt.plot(sim_terra_b[:, 0] + 11, sim_terra_b[:, 1], marker=".", linestyle="--", label="SIM-TERRA-GRC1, Adjusted")

    # Moonranger, Full Mass, Earth
    sim_mr_earth = np.array([[15.68, 0], [15.69, 0.0125], [18.08, 0.025], [21.33, 0.0375], [26.54, 0.05], [29.50, 0.1], [32.75, 0.15], [39.74, 0.20], [45.48, 0.25], [46.90, 0.3], [58.34, 0.5]])
    plt.plot(sim_mr_earth[:, 0] - 15.68, sim_mr_earth[:, 1], marker=".", linestyle="--", label="SIM-MR-EARTH-GRC1, Adjusted")

    # Moonranger, Full Mass, Moon
    sim_mr_moon = np.array([[-2.86, 0], [0.82, 0.05], [5.35, 0.1], [8.86, 0.15], [17.42, 0.2], [24.24, 0.25], [28.10, 0.3], [33.3, 0.4], [48.77, 0.5]])
    plt.plot(sim_mr_moon[:, 0] + 2.86, sim_mr_moon[:, 1], marker=".", linestyle="--", label="SIM-MR-MOON-GRC1, Adjusted")

    # Moonranger, Full Mass, Earth, Single Wheel, Experimental
    exp_mr_earth = np.array([[-0.01377441834, -0.02065071089], [0.04254638267, 0.06378585476], [0.09886718369, 0.126498084], [0.1551879847, 0.1628421714], [0.2115087857, 0.1764346278], [0.2678295868, 0.194016305]])
    error = np.fliplr([[0.003275811, 0.005570809, 0.002379257, 0.004441608, 0.003802956, 0.002151173], [0.00297384, 0.006661601, 0.002437128, 0.007362803, 0.006234711, 0.00191919]])
    plt.errorbar(exp_mr_earth[:, 0] * 100, exp_mr_earth[:, 1], yerr=error, marker=".", linestyle="-", label="EXP-MR-EARTH-BEST90, Adjusted")

    plt.xlabel("Slip (%)")
    plt.ylabel("Drawbar Coefficient")
    plt.xlim(0, 80)
    plt.ylim(0, 1)
    plt.title("Drawbar Coefficient vs Slip")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("drawbarplot.png")
    plt.show()


#  singlewheelplotter.py 
def plot_single_wheel_data(file_path):
    """
    Plot single wheel experimental data including forces, drawbar coefficient, and V_max.

    Parameters:
        file_path (str): Path to the CSV file containing the experimental data.
    """
    # Load data
    data = pd.read_csv(file_path)
    data.columns = [
        't', 'f_x', 'f_y', 'f_z', 'd_c', 'v_max', 
        'pos_x', 'pos_y', 'pos_z', 
        'oriq_x', 'oriq_y', 'oriq_z', 'oriq_w', 
        'vel_x', 'vel_y', 'vel_z'
    ]

    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    fig.suptitle("Single Wheel Experimental Data", fontsize=16)

    # Forces vs Time
    axs[0].plot(data['t'], data[['f_x', 'f_y', 'f_z']])
    axs[0].set_title("Forces vs Time")
    axs[0].set_ylabel("Force (N)")
    axs[0].legend(["f_x", "f_y", "f_z"], loc="upper right")
    axs[0].grid()

    # Drawbar Coefficient vs Time
    axs[1].plot(data['t'], data['d_c'])
    axs[1].set_title("Drawbar Coefficient vs Time")
    axs[1].set_ylabel("D_c")
    axs[1].grid()
    axs[1].set_ylim(-0.5, 0.5)

    # V_max vs Time
    axs[2].plot(data['t'], data['v_max'])
    axs[2].set_title("V_max vs Time")
    axs[2].set_ylabel("V_max (m/s)")
    axs[2].set_xlabel("Time (s)")
    axs[2].grid()
    
    plt.show()

#  starttimetesting.py 
def batch_process_data(main_folder, output_directory="SimulatedData", start_time=10, end_time=20, save_output=False):
    """
    Process batch data from a main folder containing multiple wheel test subfolders.
    Each subfolder should contain a params.json and output.csv file.
    """
    print(f"Starting batch processing for main folder: {main_folder}")
    print(f"Output directory: {output_directory}")
    print(f"Time range for analysis: {start_time} to {end_time} seconds")
    print(f"Save output: {save_output}")

    # Create output directory if it doesn't exist
    if save_output and not os.path.exists(output_directory):
        print(f"Creating output directory: {output_directory}")
        os.makedirs(output_directory)
    elif save_output:
        print(f"Output directory already exists: {output_directory}")

    all_slip_drawbar = []

    # Iterate through each subfolder in the main folder
    for subdir in sorted(os.listdir(main_folder)):
        subdir_path = os.path.join(main_folder, subdir)
        print(f"\nProcessing subfolder: {subdir_path}")

        # Skip if it's not a directory
        if not os.path.isdir(subdir_path):
            print(f"Skipping non-directory: {subdir_path}")
            continue

        # Check if params.json and output.csv exist
        params_path = os.path.join(subdir_path, "params.json")
        output_csv_path = os.path.join(subdir_path, "output.csv")

        if not os.path.exists(params_path):
            print(f"Error: {params_path} does not exist")
            continue
        if not os.path.exists(output_csv_path):
            print(f"Error: {output_csv_path} does not exist")
            continue

        # Load slip value from params.json
        with open(params_path) as params_fp:
            params = json.load(params_fp)
            slip = float(params["slip"])
            print(f"Loaded slip value: {slip} from {params_path}")

        # Read the output data
        print(f"Reading data from {output_csv_path}")
        data = pd.read_csv(output_csv_path, skipinitialspace=True)

        try:
            # Debug: Print the columns in the CSV file
            print(f"Columns in CSV: {data.columns}")

            # Debug: Print the time range
            print(f"Time range in CSV: min={data['t'].min()}, max={data['t'].max()}")

            # Find start and end indices
            start_id = data[data['t'] >= start_time].index[0]
            end_id = data[data['t'] <= end_time].index[-1]
            print(f"Time range for analysis: start={data['t'][start_id]}, end={data['t'][end_id]}")

            # Calculate mean drawbar coefficient
            mean_d_c = data['d_c'].loc[start_id:end_id].mean()
            print(f"Calculated mean drawbar coefficient: {mean_d_c} for slip {slip}")

            # Append to slip_drawbar
            all_slip_drawbar.append([slip, mean_d_c])
            print(f"Updated slip_drawbar: {all_slip_drawbar}")
        except Exception as e:
            print(f"Error processing {subdir_path}: {e}")

    # Convert to numpy array and ensure it's 2D
    all_slip_drawbar = np.atleast_2d(all_slip_drawbar)
    print(f"Final slip_drawbar data: {all_slip_drawbar}")

    # Plot the data (only if slip_drawbar is not empty)
    if all_slip_drawbar.size > 0:
        print("\nPlotting data")
        plt.plot(all_slip_drawbar[:, 0], all_slip_drawbar[:, 1], marker="o", linestyle="--")
        plt.xlabel("Slip")
        plt.ylabel("Drawbar Coefficient")
        plt.title("Drawbar Coefficient vs Slip")
        plt.grid()
        plt.show()

        # Save output if enabled
        if save_output:
            output_file = os.path.join(output_directory, "slip_drawbar.txt")
            print(f"Saving output to: {output_file}")
            np.savetxt(output_file, all_slip_drawbar, header="Slip, Drawbar")
    else:
        print("No valid data found for plotting.")
#  Main 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python combined_plotter.py <functionality> [arguments]")
        print("Available functionalities:")
        print("1. plot_chronosim <file_path>")
        print("2. plot_drawbar")
        print("3. plot_single_wheel <file_path>")
        print("4. plot_start_time_testing <directory>")
        print("5. batch_process <main_folder> [output_directory] [start_time] [end_time] [save_output]")
        sys.exit(1)

    functionality = sys.argv[1]

    if functionality == "plot_chronosim":
        if len(sys.argv) < 3:
            print("Usage: python combined_plotter.py plot_chronosim <file_path>")
            sys.exit(1)
        file_path = sys.argv[2]
        plot_chronosim_data(file_path)
        slip, effective_radius = analyze_chronosim_data(file_path)
        print(f"Slip: {slip:.2f}%")
        print(f"Effective Radius: {effective_radius:.4f}")

    elif functionality == "plot_drawbar":
        plot_drawbar_data()

    elif functionality == "plot_single_wheel":
        if len(sys.argv) < 3:
            print("Usage: python combined_plotter.py plot_single_wheel <file_path>")
            sys.exit(1)
        file_path = sys.argv[2]
        plot_single_wheel_data(file_path)

    elif functionality == "batch_process":
        if len(sys.argv) < 3:
            print("Usage: python combined_plotter.py batch_process <main_folder> [output_directory] [start_time] [end_time] [save_output]")
            sys.exit(1)
        main_folder = sys.argv[2]
        output_directory = sys.argv[3] if len(sys.argv) > 3 else "SimulatedData"
        start_time = float(sys.argv[4]) if len(sys.argv) > 4 else 10
        end_time = float(sys.argv[5]) if len(sys.argv) > 5 else 20
        save_output = sys.argv[6].lower() == "true" if len(sys.argv) > 6 else False
        batch_process_data(main_folder, output_directory, start_time, end_time, save_output)

    else:
        print(f"Unknown functionality: {functionality}")
        print("Available functionalities:")
        print("1. plot_chronosim <file_path>")
        print("2. plot_drawbar")
        print("3. plot_single_wheel <file_path>")
        print("4. batch_process <main_folder> [output_directory] [start_time] [end_time] [save_output]")
        sys.exit(1)

