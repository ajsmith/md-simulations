"""Utilities to generate batch configurations for production simulations.

"""
import argparse

import yaml


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


def make_trajectory_config(
        student_id, trajectory_id, experiment, steps, template):
    result = {
        'trajectory': trajectory_name(trajectory_id),
        'experiment': experiment,
        'config_template': template,
    }
    batch_configs = [
        make_batch_config(student_id, trajectory_id, i)
        for i in range(steps)
    ]
    result['batches'] = batch_configs
    return result


def make_simulation_config(student_id, trajectory_plan, steps):
    tr_configs = [
        make_trajectory_config(
            student_id, tr_id, tr_info['experiment'], steps, tr_info['template']
        )
        for (tr_id, tr_info) in trajectory_plan.items()
    ]
    return {'trajectories': tr_configs}


def save_yaml(file_name, sim_config):
    obj = {'simulation': sim_config}
    with open(file_name, 'w') as f:
        yaml.dump(obj, f)


def get_main_parser():
    parser = argparse.ArgumentParser()
    arg_map = {
        '--plan': {
            'dest': 'plan',
            'help': 'The plan file',
            'required': True,
        },
        '--out': {
            'dest': 'out',
            'help': 'The output file',
            'required': True,
        },
    }
    for (arg, arg_opts) in arg_map.items():
        parser.add_argument(arg, **arg_opts)
    return parser


def main(argv=None):
    parser = get_main_parser()
    if argv is not None:
        args = parser.parse_args(argv[1:])
    else:
        args = parser.parse_args()
    with open(args.plan, 'rb') as plan_file:
        plan_obj = yaml.load(plan_file, yaml.Loader)
        student_id = plan_obj['student_id']
        steps = plan_obj['steps']
        tr_plan = plan_obj['plan']
        sim_config = make_simulation_config(student_id, tr_plan, steps)
        save_yaml(args.out, sim_config)
