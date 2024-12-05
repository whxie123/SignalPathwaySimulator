import numpy as np
from scipy.integrate import odeint
import sympy as sp
from libsbml import readSBML
import re

class Simulator:
    def __init__(self, model_file):
        self.species = []
        self.reactions = []
        self.parameters = {}
        self.symbol_map = {}
        self.load_model_data(model_file)

    # Load model data from an XML (SBML) file.        
    def load_model_data(self, model_file):
        document = readSBML(model_file)
        if document.getNumErrors() > 0:
            raise ValueError(f"Error reading the SBML file: {document.getErrorLog().toString()}")

        model = document.getModel()
        if model is None:
            raise ValueError("Model could not be loaded. Please check the XML file.")

        # Extract species and information
        for species in model.getListOfSpecies():
            if species is not None:
                # Remove underscores and hyphens from species ID and name
                species_id_no_special_chars = species.getId().replace("_", "").replace("-", "")
                species_name_no_special_chars = species.getName().replace("_", "").replace("-", "")
                
                # Create a valid Python symbol for the species
                species_symbol = sp.symbols(species_id_no_special_chars)
                
                # Add species information
                self.symbol_map[species.getId()] = species_symbol
                self.species.append({
                    'original_id': species.getId(),  # Keep original ID for reference
                    'id': species_id_no_special_chars,  # Store the cleaned ID
                    'name': species_name_no_special_chars,
                    'initial_concentration': species.getInitialConcentration(),
                    'compartment': species.getCompartment(),  # Add compartment information
                    'symbol': species_symbol
                })
                
        # Extract reactions
        for reaction in model.getListOfReactions():
            if reaction is not None:
                kinetic_law = reaction.getKineticLaw()
                rate_law = kinetic_law.getFormula() if kinetic_law is not None else None

                # Extract parameters from the kinetic law
                parameter_values = {}
                if kinetic_law is not None:
                    for parameter in kinetic_law.getListOfParameters():
                        parameter_id = parameter.getId().replace("_", "").replace("-", "")
                        parameter_value = parameter.getValue()
                        parameter_values[parameter_id] = parameter_value

                # Remove underscores and hyphens from rate law expression
                if rate_law is not None:
                    rate_law = rate_law.replace("_", "").replace("-", "")

                # Replace parameter IDs in the rate law with their corresponding values
                if rate_law is not None:
                    for param_id, param_value in parameter_values.items():
                        rate_law = rate_law.replace(param_id, str(param_value))

                # Extract reactants, products, and modifiers, and remove special characters
                reactants = [r.getSpecies().replace("_", "").replace("-", "") for r in reaction.getListOfReactants()]
                products = [p.getSpecies().replace("_", "").replace("-", "") for p in reaction.getListOfProducts()]
                modifiers = [m.getSpecies().replace("_", "").replace("-", "") for m in reaction.getListOfModifiers()]

                # Add reaction to the list only if there are reactants and products
                if reactants and products:
                    self.reactions.append({
                        'id': reaction.getId(),
                        'name': reaction.getName(),
                        'reactants': reactants,
                        'products': products,
                        'modifiers': modifiers,
                        'reversible': reaction.getReversible(),
                        'rate_law': rate_law
                    })
                else:
                    print(f"Skipping reaction {reaction.getId()} due to missing reactants or products.")

    def evaluate_rate_law(self, rate_law, y):
        if rate_law is None:
            return 0
        rate_law_str = rate_law
        rate_law_str = rate_law_str.replace("_", "").replace("-", "")
        rate_law_str = rate_law_str.replace("^", "**")

        species_mapping = {species['id']: i for i, species in enumerate(self.species)}
        sorted_species = sorted(species_mapping.items(), key=lambda x: len(x[0]), reverse=True)

        # Replace species symbols with corresponding y[i]
        for species_id, index in sorted_species:
            # Use word boundary `\b` to ensure we replace the entire species ID, avoiding partial replacements
            rate_law_str = re.sub(rf'\b{species_id}\b', f'y[{index}]', rate_law_str)

        # Use sympy to safely evaluate the expression
        try:
            param_values = {
                'uVol': 1.0
            }
            # Create a list of symbols for y, like y0, y1, y2, ..., yN
            y_symbols = sp.symbols(f'y0:{len(y)}')
            print(f"y_symbols: {y_symbols}")  

            # Replace y[i] with the appropriate symbol name (e.g., y0, y1, y2, ...)
            for i, symbol in enumerate(y_symbols):
                rate_law_str = rate_law_str.replace(f"y[{i}]", str(symbol))
            print("Rate law string after replacement:", rate_law_str)  

            # Replace parameter values in rate_law_str
            for param, value in param_values.items():
                rate_law_str = rate_law_str.replace(param, str(value))
            print("Rate law string with parameters replaced:", rate_law_str)  

            # Transform the rate law string into a sympy expression
            rate_expr = sp.sympify(rate_law_str)
            print("Rate expression:", rate_expr)  

            # Create a lambda function with the list of y symbols
            rate_func = sp.lambdify(y_symbols, rate_expr, modules='math')
            print("Rate function:", rate_func)  

            # Evaluate rate by unpacking the list y into individual values
            rate = rate_func(*y)
            print("Rate:", rate) 
           
        except Exception as e:
            print(f"Error evaluating rate law {rate_law_str}: {e}")

            rate = 0

        return rate

    # get the concentration instantaneous rate of change 
    def model_equations(self, y, t):
        print(f"Calculating model equations at time {t}")  
        dydt = np.zeros(len(y))
        
        for reaction in self.reactions:
            print(f"Evaluating reaction: {reaction['name']}")  
            rate = self.evaluate_rate_law(reaction['rate_law'], y)
            print(f"Time {t}: Reaction {reaction['name']} rate = {rate}")

            # Get indices of reactants and products
            reactant_indices = [self.get_species_index(reactant) for reactant in reaction['reactants']]
            product_indices = [self.get_species_index(product) for product in reaction['products']]

            # Update rate of change for reactants and products
            for idx in reactant_indices:
                if idx != -1:
                    dydt[idx] -= rate
            for idx in product_indices:
                if idx != -1:
                    dydt[idx] += rate

        return dydt


    def get_species_index(self, species_id):
        species_id_no_special_chars = species_id.replace("_", "").replace("-", "")
        for i, species in enumerate(self.species):
            if species['id'] == species_id_no_special_chars:
                return i
        return -1

    def get_species_name(self, species_id):
        species_id_no_special_chars = species_id.replace("_", "").replace("-", "")
        for species in self.species:
            if species['id'] == species_id_no_special_chars:
                return species['name']
        return species_id_no_special_chars  
    
    # get concentration
    def run_simulation(self, initial_conditions, time_points):
        if len(initial_conditions) != len(self.species):
            raise ValueError("Initial conditions must match the number of species.")

        results = odeint(self.model_equations, initial_conditions, time_points)

        return results
