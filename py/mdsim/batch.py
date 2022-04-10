import argparse
import sys
from pathlib import Path

import yaml

import mdsim.defaults


def make_seed(student_id, trajectory_id, step_id):
    result = f'{student_id}'
    result += trajectory_name(trajectory_id)
    result += step_name(step_id)
    return result


def step_name(step_id):
    return f'{step_id:02}'


def trajectory_name(trajectory_id):
    return f'{trajectory_id:02}'


def make_batch_config(student_id, trajectory_id, step_id):
    result = {}
    result['batch'] = step_name(step_id)
    result['seed'] = make_seed(student_id, trajectory_id, step_id)
    if step_id > 0:
        prev_id = step_id - 1
        result['previous_batch'] = step_name(prev_id)
    else:
        result['previous_batch'] = None

    return result


def make_trajectory_config(student_id, trajectory_id, steps, config_template):
    result = {
        'trajectory': trajectory_name(trajectory_id),
        'config_template': config_template,
    }
    batch_configs = [
        make_batch_config(student_id, trajectory_id, i)
        for i in range(steps)
    ]
    result['batches'] = batch_configs
    return result
