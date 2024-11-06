# main.py
# 内容：定义主程序入口，提供交互式功能

from signalpathwaysimulator import Simulator, DataManager, VisualizationManager
import numpy as np

def main():
    model_file = 'example_model.json'  # 示例模型文件路径

    # 初始化数据管理器、模拟器和可视化管理器
    data_manager = DataManager()
    simulator = Simulator(model_file)
    visualization_manager = VisualizationManager()

    # 导入模型数据
    network_data = data_manager.import_model(model_file)

    # 运行仿真
    initial_conditions = [1.0, 0.0, 0.0]  # 示例初始条件
    time_points = np.linspace(0, 10, 100)  # 示例时间点
    results = simulator.run_simulation(initial_conditions, time_points)

    # 可视化结果
    visualization_manager.plot_network(network_data)
    visualization_manager.plot_simulation_results(time_points, results)

if __name__ == '__main__':
    main()

