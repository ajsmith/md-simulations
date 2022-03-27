#!/usr/bin/env python

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import yaml

import mdsim.defaults


COL_TS = 1
COL_KINETIC = 10
COL_POTENTIAL = 13
COL_TEMP = 12
COL_TOTAL = 11
COL_VOLUME = 18


def get_parser():
    parser = argparse.ArgumentParser()
    arg_map = {
        '--config': {
            'dest': 'config',
            'help': 'The configuration file',
        },
    }
    for (arg, arg_opts) in arg_map.items():
        parser.add_argument(arg, **arg_opts)
    return parser


DEFAULTS = mdsim.defaults.load_plot_stats()


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


def file_path_pair(config, section):
    """Return input and output file paths for a config section."""
    input_path = get_file_path(config, config[section]['input'])
    output_path = get_file_path(config, config[section]['output'])
    return (input_path, output_path)


def print_plot_step(config, section):
    suptitle = config[section].get('suptitle', section)
    print(f'* Generating plot: {suptitle}')
    input_path, output_path = file_path_pair(config, section)
    print(f'    Plotting {input_path}')
    print(f'    Saving plot to {output_path}')


def plot_minimzation(config):
    suptitle = config['min'].get('suptitle', 'Minimization')
    input_file, output_file = file_path_pair(config, 'min')
    print_plot_step(config, 'min')
    with open(input_file) as f:
        ts = []
        energy = []
        for line in f.readlines():
            if line.startswith('ENERGY:'):
                cols = line.split()
                ts.append(int(cols[COL_TS]))
                energy.append(float(cols[COL_POTENTIAL]))
        fig, ax = plt.subplots()
        ax.plot(ts, energy)
        ax.set_title(r'$E_{pot}$')
        ax.set_xlabel('ts')
        ax.set_ylabel(r'$E_{pot}$')
        fig.suptitle(suptitle)
        fig.tight_layout()
        fig.savefig(output_file)



def plot_heating(config):
    section = 'heat'
    suptitle = config[section].get('suptitle', 'Heating')
    input_file, output_file = file_path_pair(config, section)
    print_plot_step(config, section)
    with open(input_file) as f:
        ts = []
        energy = []
        temp = []
        for line in f.readlines():
            if line.startswith('ENERGY:'):
                cols = line.split()
                ts.append(int(cols[COL_TS]))
                temp.append(float(cols[COL_TEMP]))
                energy.append(float(cols[COL_POTENTIAL]))
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(ts, energy)
        ax1.set_title('Potential Energy')
        ax1.set_ylabel(r'$E_{pot}$')
        ax2.plot(ts, temp)
        ax2.set_title('Temperature')
        ax2.set_xlabel('ts')
        ax2.set_ylabel('temperature')
        fig.suptitle(suptitle)
        fig.tight_layout()
        fig.savefig(output_file)


def plot_equilibration(config):
    section = 'equil'
    suptitle = config[section].get('suptitle', 'Equilibration')
    input_file, output_file = file_path_pair(config, section)
    print_plot_step(config, section)
    with open(input_file) as f:
        ts = []
        temp = []
        cell_size = []
        for line in f.readlines():
            if line.startswith('ENERGY:'):
                cols = line.split()
                ts.append(int(cols[COL_TS]))
                temp.append(float(cols[COL_TEMP]))
                cell_size.append(float(cols[COL_VOLUME])**(1/3.0))
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(ts, temp)
        ax1.set_title('Temperature')
        ax1.set_ylabel('temperature')
        ax2.plot(ts, cell_size)
        ax2.set_title('Unit Cell Size')
        ax2.set_xlabel('ts')
        ax2.set_ylabel('Unit Cell Size')
        fig.suptitle(suptitle)
        fig.tight_layout()
        fig.savefig(output_file)


def plot_production(config):
    section = 'quench'
    suptitle = config[section].get('suptitle', 'Quench')
    input_file, output_file = file_path_pair(config, section)
    print_plot_step(config, section)
    with open(input_file) as f:
        ts = []
        energy = []
        temp = []
        for line in f.readlines():
            if line.startswith('ENERGY:'):
                cols = line.split()
                ts.append(int(cols[COL_TS]))
                temp.append(float(cols[COL_TEMP]))
                energy.append(float(cols[COL_TOTAL]))
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(ts, energy)
        ax1.set_title('Total Energy')
        ax1.set_ylabel(r'$E_{total}$')
        ax2.plot(ts, temp)
        ax2.set_title('Temperature')
        ax2.set_xlabel('ts')
        ax2.set_ylabel('temperature')
        fig.suptitle(suptitle)
        fig.tight_layout()
        fig.savefig('production.png')


def main():
    parser = get_parser()
    args = parser.parse_args()
    config = load_config(args.config)
    if args.config:
        config['config_path'] = args.config
    else:
        config['config_path'] = Path.cwd()

    if 'min' in config:
        plot_minimzation(config)

    if 'heat' in config:
        plot_heating(config)

    if 'equil' in config:
        plot_equilibration(config)

    if 'quench' in config:
        plot_production(config)


if __name__ == '__main__':
    main()
