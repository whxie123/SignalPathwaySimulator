import os
import unittest
import numpy as np

# Update this import path to match the actual location of your Simulator and VisualizationManager classes
# For example, if they are in a file named signalpathwaysimulator.py in the same directory:
# from signalpathwaysimulator import Simulator, VisualizationManager

from signalpathwaysimulator import Simulator, VisualizationManager


def create_simple_test_model(file_path):
    
    sbml_content = """<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4">
  <model id="simple_model" name="Simple Model">
    <listOfCompartments>
      <compartment id="cell" size="1" units="volume"/>
    </listOfCompartments>

    <listOfSpecies>
      <species id="A" name="A" compartment="cell" initialConcentration="10" boundaryCondition="false"/>
      <species id="B" name="B" compartment="cell" initialConcentration="0" boundaryCondition="false"/>
    </listOfSpecies>

    <listOfParameters>
      <parameter id="k" value="0.1"/>
    </listOfParameters>

    <listOfReactions>
      <reaction id="R1" reversible="false" name="A_to_B">
        <listOfReactants>
          <speciesReference species="A" stoichiometry="1"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="B" stoichiometry="1"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci>k</ci>
              <ci>A</ci>
            </apply>
          </math>
          <listOfParameters>
            <parameter id="k" value="0.1"/>
          </listOfParameters>
        </kineticLaw>
      </reaction>
    </listOfReactions>

  </model>
</sbml>
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sbml_content)


class TestSimpleModel(unittest.TestCase):

    def setUp(self):
        # Create a temporary SBML model file before each test
        self.model_file = 'simple_test_model.xml'
        create_simple_test_model(self.model_file)
    
    def tearDown(self):
        # Remove the model file after each test to avoid clutter
        if os.path.exists(self.model_file):
            os.remove(self.model_file)

    def test_simulation_runs(self):
        # Test if the simulation runs without errors and produces expected results
        simulator = Simulator(self.model_file)

        # Set initial conditions and time points (0 to 50 seconds with 500 points)
        initial_conditions = [species['initial_concentration'] for species in simulator.species]
        time_points = np.linspace(0, 50, 500)

        # Run the simulation
        results = simulator.run_simulation(initial_conditions, time_points)

        # Basic checks: results shape and monotonic trend (A should decrease, B should increase)
        self.assertEqual(results.shape, (500, 2), "Results array shape should be 500 x 2.")

        # Check that A decreases over time and B increases over time
        self.assertTrue(all(results[i,0] >= results[i+1,0] for i in range(499)), "Concentration of A should be non-increasing.")
        self.assertTrue(all(results[i,1] <= results[i+1,1] for i in range(499)), "Concentration of B should be non-decreasing.")

    def test_visualization(self):
        # Test visualization manager to ensure it runs without error
        simulator = Simulator(self.model_file)
        initial_conditions = [species['initial_concentration'] for species in simulator.species]
        time_points = np.linspace(0, 50, 500)
        results = simulator.run_simulation(initial_conditions, time_points)

        simulator.time_points = time_points
        simulator.concentrations = {species['id']: results[:, idx] for idx, species in enumerate(simulator.species)}

        visualization_manager = VisualizationManager(simulator)
        visualization_manager.create_reaction_network()

        # We won't check the output images here, but this ensures no exceptions occur during visualization
        try:
            visualization_manager.visualize()
        except Exception as e:
            self.fail(f"Visualization raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
