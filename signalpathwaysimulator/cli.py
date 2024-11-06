
# signalpathwaysimulator/cli.py
# Defines the command line interface and is responsible for processing user input

import argparse
from .simulator import Simulator
from .data_manager import DataManager
from .visualization_manager import VisualizationManager
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='SignalPathwaySimulator: Simulate cellular signaling pathways.')
    parser.add_argument('model_file', type=str, help='Path to the model file (e.g., SBML or JSON).')
    parser.add_argument('--simulate', action='store_true', help='Run the simulation.')
    parser.add_argument('--visualize', action='store_true', help='Visualize the model and results.')
    args = parser.parse_args()

    data_manager = DataManager()
    simulator = Simulator(args.model_file)
    visualization_manager = VisualizationManager()

    results = None

    if args.simulate:
        # Define initial conditions and time points
        initial_conditions = [1.0, 0.0, 0.0]  # Example Initial Conditions
        time_points = np.linspace(0, 10, 100)  # Example time point
        results = simulator.run_simulation(initial_conditions, time_points)
        print('Simulation completed.')

    if args.visualize:
        # Example visualization results
        network_data = data_manager.import_model(args.model_file)
        visualization_manager.plot_network(network_data)
        if results is not None:
            visualization_manager.plot_simulation_results(time_points, results)
