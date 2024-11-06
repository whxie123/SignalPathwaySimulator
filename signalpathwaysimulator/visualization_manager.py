# signalpathwaysimulator/visualization_manager.py
# 内容：定义可视化管理器类，负责生成图形化结果

import matplotlib.pyplot as plt

class VisualizationManager:
    def __init__(self):
        pass

    def plot_network(self, network_data):
        # 绘制反应网络图
        plt.figure()
        if 'species' in network_data and 'reactions' in network_data:
            for species in network_data['species']:
                plt.scatter(species['id'], 1, label=species['name'])
            for reaction in network_data['reactions']:
                plt.plot([reaction['reactants'][0], reaction['products'][0]], [1, 1], 'k-')
        else:
            print("Network data format not recognized.")
        plt.title('Reaction Network')
        plt.xlabel('Components')
        plt.ylabel('Presence')
        plt.legend()
        plt.show()

    def plot_simulation_results(self, time_points, results):
        # 绘制模拟结果的动力学曲线
        plt.figure()
        for i, result in enumerate(results.T):
            plt.plot(time_points, result, label=f'Component {i+1}')
        plt.xlabel('Time')
        plt.ylabel('Concentration')
        plt.legend()
        plt.title('Simulation Results')
        plt.show()
