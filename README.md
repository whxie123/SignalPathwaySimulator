# SignalPathwaySimulator

## Author
**Wenhui Xie**

---

**Final Project, BIOEN 537: Computational Systems Biology. University of Washington, Seattle**

---

## Description
A Python package designed to simulate and visualize biochemical signal transduction pathways defined in SBML format.

---

## Version Information
- **CURRENT ACTIVE VERSION**: 0.1.0  
- **LAST UPDATED**: 12/07/2024

---

## Notice
This package is still in an early stage of development. While the simulation outputs are based on standard ODE solvers and SBML parsing, some advanced visualization features may have compatibility issues with certain graphing libraries.  
If you encounter errors or unexpected behaviors, please consider these as known limitations and report them as issues on the project repository.

---

## Background
Biochemical signal transduction pathways are central to understanding cellular decision-making, homeostasis, and responses to stimuli.  
Accurate computational modeling and simulation of these pathways can help researchers:
- Predict system responses to perturbations
- Design synthetic pathways
- Assist in drug target identification  

This package aims to streamline pathway analysis and support hypothesis-driven research by:
- Providing a stable simulation environment
- Creating clear visualizations of reaction networks  

Key features include:
- Using SBML files as input
- Reading species, parameters, and reactions
- Simulating dynamics over time using ODE solvers
- VisualizationManager for creating network diagrams and plotting temporal concentration changes  

**Assumptions:**  
- Well-mixed conditions  
- Kinetic laws defined in the SBML model (e.g., mass-action or Michaelis-Menten kinetics)

---

## Installation and Use

### Pre-requisites
Ensure you have the following Python packages installed:
- `numpy`
- `pygraphviz`
- `matplotlib`
- `python-libsbml` (for SBML parsing)

Install all dependencies with one command:
```bash
pip install numpy pygraphviz matplotlib python-libsbml signalpathwaysimulator
```

## RUNNING A SIMULATION
Once installed, you can run a simulation by creating a Python script:
```bash
import numpy as np
from signalpathwaysimulator import Simulator

sim = Simulator('path_to_sbml_model.xml')
initial_conditions = [spec['initial_concentration'] for spec in sim.species]
time_points = np.linspace(0, 50, 500)
results = sim.run_simulation(initial_conditions, time_points)
results is a numpy array with species concentrations over time.
```
## USING THE VISUALIZATION FEATURES
To visualize reaction networks or plot simulation results:
```bash
from signalpathwaysimulator import VisualizationManager

vis = VisualizationManager(sim)
vis.create_reaction_network()  # Creates a reaction network graph
vis.visualize()  # Generates and displays plots
Ensure Graphviz is installed and PyGraphviz is correctly configured.
```
## GUI/ADDITIONAL TOOLS (FUTURE WORK)
A GUI or web-based dashboard for interactive model loading, simulation configuration, and visualization is under consideration. This would allow parameter changes and re-simulation on the fly.

## USING INDIVIDUAL FUNCTIONS
You can leverage the core functions from Simulator and VisualizationManager for customized workflows:
```bash
Simulator.run_simulation(initial_conditions, time_points)
VisualizationManager.create_reaction_network()
VisualizationManager.visualize()
```
## GUI COMPONENTS AND FUNCTION NOTES (PLANNED)
Future versions may include a GUI that can:
- Load SBML models directly.
- Allow users to modify parameters, initial conditions, and simulation duration.
- Interactively plot species concentrations and reaction networks.
- Export results to various formats (CSV, images, SBML variants).

## AUTHOR'S NOTES
This package was developed as a course project and may be extended to include more sophisticated features, such as stochastic simulations (Gillespie algorithm), parameter estimation, and sensitivity analysis. It currently provides a robust foundation for deterministic ODE-based modeling and rapid visualization.

## RESOURCES
GitHub Link: [https://github.com/whxie123/SignalPathwaySimulator.git]

These provide introductory examples on running simulations and visualizing results. Feel free to clone, modify, or contribute to this project. Feedback and pull requests are welcome!
