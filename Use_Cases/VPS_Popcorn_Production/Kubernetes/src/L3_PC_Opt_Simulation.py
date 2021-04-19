import os
from scipy.optimize import differential_evolution
from math import ceil
import pickle
import numpy as np

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


from classes.KafkaPC import KafkaPC


env_vars = {'config_path': os.getenv('config_path'),
            'config_section': os.getenv('config_section')}
"""
env_vars = {'kafka_broker_url': os.getenv('KAFKA_BROKER_URL'),
            'in_topic': os.getenv('IN_TOPIC'),
            'in_group': os.getenv('IN_GROUP'),
            'in_schema_file': os.getenv('IN_SCHEMA_FILE'),
            'out_topic': os.getenv('OUT_TOPIC'),
            'out_schema_file': os.getenv('OUT_SCHEMA_FILE')}

env_vars = {'in_topic': 'AB_model_data',
            'in_group': 'model_appl',
            'in_schema_file': './schema/model.avsc',
            'out_topic': 'AB_model_application',
            'out_schema_file': './schema/model_appl.avsc'
            }
"""

# configuration constants
N_INITIAL_DESIGN = 5
N_OPTIMIZATION_BUDGET = 200
N_POP_SIZE = 20
N_MAX_ITER = ceil(N_OPTIMIZATION_BUDGET / N_POP_SIZE)

X_MIN = 4000
X_MAX = 10100

bounds = [(X_MIN, X_MAX)]

new_pc = KafkaPC(**env_vars)

print("INIT: Optimization of Simulations module")

for msg in new_pc.consumer:
    """
    "name": "Simulation",
    "fields": [
        {"name": "id", "type": ["int"]},
        {"name": "simulation", "type": ["byte"]},

        ]
    """

    new_sim = new_pc.decode_avro_msg(msg)

    objFunction = pickle.loads(new_sim['simulation'])
    result = differential_evolution(objFunction, bounds, maxiter=N_MAX_ITER, popsize=N_POP_SIZE)
    best_x = result.x[0]
    best_y = result.fun

    print(f"The optimization suggests "
          f"x={round(best_x, 3)}, y={round(best_y, 3)}")

    """
    "name": "Model_Application",
    "fields": [
        {"name": "phase", "type": ["enum"], "symbols": ["init", "observation"]},
        {"name": "model_name", "type": ["string"]},
        {"name": "id_x", "type": ["int"]},
        {"name": "n_data_points", "type": ["int"]},
        {"name": "id_start_x", "type": ["int"]},
        {"name": "model_size", "type": ["int"]},
        {"name": "x", "type": ["float"]},
        {"name": "pred_y", "type": ["float"]},
        {"name": "rmse", "type": ["null, float"]},
        {"name": "mae", "type": ["null, float"]},
        {"name": "rsquared", "type": ["null, float"]},
        {"name": "CPU_ms", "type": ["float"]},
        {"name": "RAM", "type": ["float"]}
        ]
    """
    # model_appl_data = {'phase': new_model['phase'],
    #                    'model_name': new_model['model_name'],
    #                    'id': new_model['id'],
    #                    'n_data_points': new_model['n_data_points'],
    #                    'id_start_x': new_model['id_start_x'],
    #                    'model_size': new_model['model_size'],
    #                    'x': surrogate_x,
    #                    'pred_y': surrogate_y,
    #                    'rmse': new_model['rmse'],
    #                    'mae': new_model['mae'],
    #                    'rsquared': new_model['rsquared'],
    #                    'CPU_ms': new_model['CPU_ms'],
    #                    'RAM': new_model['RAM']
    #                    }

    # new_pc.send_msg(model_appl_data)
