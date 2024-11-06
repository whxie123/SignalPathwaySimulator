# signalpathwaysimulator/data_manager.py
# 内容：定义数据管理器类，负责导入、导出模型数据

import os
import json

class DataManager:
    def __init__(self):
        pass

    def import_model(self, filepath):
        # 导入 SBML 文件或者 JSON 文件
        if filepath.endswith('.sbml'):
            # 处理 SBML 文件的导入逻辑（需要额外的 SBML 解析库，如 libsbml）
            try:
                import libsbml
                reader = libsbml.SBMLReader()
                document = reader.readSBML(filepath)
                if document.getNumErrors() > 0:
                    raise ValueError("Error reading SBML file.")
                model = document.getModel()
                return self._parse_sbml_model(model)
            except ImportError:
                raise ImportError("libsbml package is required to parse SBML files.")
        elif filepath.endswith('.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data
        else:
            raise ValueError("Unsupported file format. Only SBML and JSON are supported.")

    def export_model(self, data, filepath):
        # 导出模型为 JSON 文件
        with open(filepath, 'w') as f:
            json.dump(data, f)

    def _parse_sbml_model(self, model):
        # 将 SBML 模型解析为 Python 数据结构
        # 这里实现解析逻辑，例如提取物种、反应等信息
        parsed_data = {
            'species': [],
            'reactions': []
        }
        for species in model.getListOfSpecies():
            parsed_data['species'].append({
                'id': species.getId(),
                'name': species.getName(),
                'initial_concentration': species.getInitialConcentration()
            })
        for reaction in model.getListOfReactions():
            parsed_data['reactions'].append({
                'id': reaction.getId(),
                'name': reaction.getName(),
                'reactants': [r.getSpecies() for r in reaction.getListOfReactants()],
                'products': [p.getSpecies() for p in reaction.getListOfProducts()]
            })
        return parsed_data

