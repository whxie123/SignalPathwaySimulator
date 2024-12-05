import matplotlib.pyplot as plt
import pygraphviz as pgv

class VisualizationManager:
    def __init__(self, simulator):
        self.simulator = simulator

    def create_reaction_network(self):
        self.graph = pgv.AGraph(strict=False, directed=True)

        self.graph.graph_attr.update(layout='neato', nodesep='5', ranksep='5', splines='curved', overlap='false', sep='+5')
        self.graph.node_attr.update(shape='ellipse', style='filled', fillcolor='lightblue', fontsize='20')
        self.graph.edge_attr.update(fontsize='18', arrowType='normal')

        for species in self.simulator.species:
            name = species.get('name', species['id'])
            self.graph.add_node(name, label=name)

        for reaction in self.simulator.reactions:
            reactants = [self.get_species_name(r) for r in reaction['reactants']]
            products = [self.get_species_name(p) for p in reaction['products']]
            modifiers = [self.get_species_name(m) for m in reaction.get('modifiers', [])]
            reaction_label = reaction['name'].replace('phosphorylation', 'P')

            if not reactants or not products:
                print(f"Skipping reaction {reaction['name']} due to missing reactants or products.")
                continue

            for reactant in reactants:
                for product in products:
                    edge_color = 'black'  
                    label_color = 'black'  
                    print(reaction_label.lower())
                    if 'inactivation' in reaction_label.lower() or 'dep' in reaction_label.lower():
                        edge_color = 'red'
                        label_color = 'red'

                    if reaction['reversible']:
                        # Add two edges for reversible reactions
                        self.graph.add_edge(reactant, product, color=edge_color)
                        self.graph.add_edge(product, reactant, color=edge_color)
                        self.graph.get_edge(reactant, product).attr.update(xlabel=f"{reaction_label} (forward)", fontsize='16', fontcolor=label_color, labeldistance=3)
                        self.graph.get_edge(product, reactant).attr.update(xlabel=f"{reaction_label} (backward)", fontsize='16', fontcolor=label_color, labeldistance=3)
                    else:
                        # Add single edge for irreversible reaction
                        self.graph.add_edge(reactant, product, color=edge_color)
                        self.graph.get_edge(reactant, product).attr.update(xlabel=f"{reaction_label}", fontsize='16', fontcolor=label_color, labeldistance=3)

            # Add dashed lines for modifiers
            for modifier in modifiers:
                for reactant in reactants:
                    for product in products:
                        if self.graph.has_edge(reactant, product):
                            self.graph.add_edge(modifier, reactant, style='dashed', color='brown')

    def visualize(self):
        self.graph.layout(prog='neato')  
        self.graph.draw('reaction_network.png')
        img = plt.imread('reaction_network.png')
        plt.figure(figsize=(20, 20))  
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        plt.close()
        
        # Plot species concentrations after visualizing the reaction network
        self.plot_species_concentrations()

    def plot_species_concentrations(self):
        time_points = self.simulator.time_points
        concentrations = self.simulator.concentrations

        plt.figure(figsize=(12, 8))
        for species_id, conc_values in concentrations.items():
            species_name = self.get_species_name(species_id)
            plt.plot(time_points, conc_values, label=species_name)

        plt.xlabel('Time')
        plt.ylabel('Concentration')
        plt.title('Species Concentrations Over Time')
        plt.legend()
        plt.grid(True)
        plt.savefig('concentration.png')
        plt.show()
        plt.close()

    def get_species_name(self, species_id):
        for species in self.simulator.species:
            if species['id'] == species_id:
                return species.get('name', species_id)
        return species_id


