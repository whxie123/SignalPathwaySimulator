Data Manager: Manages the import, export, and storage of pathway data, supporting import of models in SBML format.

Simulation Manager: Responsible for handling the dynamic simulation of signaling pathways, using the ODE solver from SciPy for numerical integration.

Visualization Manager: Generates reaction network diagrams and concentration change curves to help users intuitively understand the model results.

Component Interaction: Users import model data via the Data Manager, the Simulation Manager performs the simulation, and finally, the Visualization Manager displays the results.
