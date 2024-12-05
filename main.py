from signalpathwaysimulator import Simulator, VisualizationManager
import numpy as np

def main():
    # Load the SBML model
    model_file = 'D:/BIOEN 537/SignalPathwaySimulator/examples/BIOMD0000000010_url.xml' 
    simulator = Simulator(model_file)

    # Set initial conditions and time points
    initial_conditions = [species['initial_concentration'] for species in simulator.species]
    time_points = np.linspace(0, 4000, 40000)  # Define time points for simulation

    # Run the simulation
    results = simulator.run_simulation(initial_conditions, time_points)
    
    # Store the results in the simulator for visualization purposes
    simulator.time_points = time_points
    simulator.concentrations = {species['id']: results[:, idx] for idx, species in enumerate(simulator.species)}
    
    # Visualize the reaction network
    visualization_manager = VisualizationManager(simulator)
    visualization_manager.create_reaction_network()
    visualization_manager.visualize()

if __name__ == "__main__":
    main()