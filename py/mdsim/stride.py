"""Statistical analysis of STRIDE data.

"""
import sys
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml


def process_line(line):
    """Return the structure frequencies for a line of STRIDE data."""
    result = {}
    for structure in line.split():
        result[structure] = result.get(structure, 0) + 1
    return result


def count_helices(d):
    """Return the helix count from structure freq data."""
    return d.get('H', 0) + d.get('G', 0) + d.get('I', 0)


def count_all(d):
    """Return the total count of all structures in the structure freq data."""
    return sum(d.values())


def process_file(file_path):
    ts_helix = []
    ts_all = []
    with open(file_path) as f:
        for line in f.readlines():
            structures = process_line(line)
            ts_helix.append(count_helices(structures))
            ts_all.append(count_all(structures))
    helices = np.array(ts_helix, dtype=np.uint)
    totals = np.array(ts_all, dtype=np.uint)
    return np.vstack((helices, totals))


def process_files(file_paths):
    assert len(file_paths) > 0, 'No files given'

    helices = []
    totals = []
    for fpath in file_paths:
        ts_helix, ts_all = process_file(fpath)
        helices.append(ts_helix)
        totals.append(ts_all)
    return np.vstack(helices), np.vstack(totals)


def aggregate_group(helices, totals, cols):
    return np.vstack((helices[cols].sum(axis=0), totals[cols].sum(axis=0)))


def stats(ts_arrays):
    helices, totals = ts_arrays
    return {
        'ts_mean': helices / totals,
        'mean': (helices / totals).mean(),
        'var': helices.var(),
        'N_helix': helices.sum(),
        'N': totals.sum(),
    }


def get_parser():
    parser = argparse.ArgumentParser()
    arg_map = {
        '--config': {
            'dest': 'config',
            'help': 'The configuration file',
            'required': True
        },
    }
    for (arg, arg_opts) in arg_map.items():
        parser.add_argument(arg, **arg_opts)
    return parser


def load_config(filepath=None):
    if not filepath:
        config = {}
    else:
        with open(filepath) as f:
            config = yaml.load(f, yaml.Loader)
    return config


def get_file_path(config, filepath):
    path = Path(config['config_path'])
    if path.is_file():
        path = path.parent
    path = path / filepath
    return path.resolve()


def canonicalize_file_paths(root, file_paths):
    path = Path(root)
    if path.is_file():
        path = path.parent
    return [str((path / fpath).resolve()) for fpath in file_paths]


def main():
    parser = get_parser()
    args = parser.parse_args()
    config = load_config(args.config)

    stride_file_paths = canonicalize_file_paths(
        args.config, config['stride_files'])
    (output_file,) = canonicalize_file_paths(
        args.config,
        [config.get('output_file', 'sstructure.png')],
    )

    group_configs = config['groups']
    helices, totals = process_files(stride_file_paths)
    groups = dict(
        (conf['name'], aggregate_group(helices, totals, conf['cols']))
        for conf in group_configs
    )
    group_stats = dict((name, stats(data)) for (name, data) in groups.items())
    fig, ax = plt.subplots()
    for (name, st) in group_stats.items():
        y = st['ts_mean']
        ax.plot(y[::500], ':', label=name)
    fig.savefig(output_file)
    print('Generated plot:', output_file)
