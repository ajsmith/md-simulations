#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt

COL_TS = 1
COL_KINETIC = 10
COL_POTENTIAL = 13
COL_TEMP = 12
COL_TOTAL = 11
COL_VOLUME = 18


def get_parser():
    parser = argparse.ArgumentParser()
    arg_map = {
        '--min-out': {
            'dest': 'min_out',
            'help': 'The minimization step output file.'
        },
        '--heat-out': {
            'dest': 'heat_out',
            'help': 'The heating step output file.'
        },
        '--equil-out': {
            'dest': 'equil_out',
            'help': 'The equilibration step output file.'
        },
        '--quench-out': {
            'dest': 'quench_out',
            'help': 'The production step output file.'
        },
    }
    for (arg, arg_opts) in arg_map.items():
        parser.add_argument(arg, **arg_opts)
    return parser


def plot_minimzation(filepath):
    with open(filepath) as f:
        ts = []
        energy = []
        for line in f.readlines():
            if line.startswith('ENERGY:'):
                cols = line.split()
                ts.append(int(cols[COL_TS]))
                energy.append(float(cols[COL_POTENTIAL]))
        fig, ax = plt.subplots()
        ax.plot(ts, energy)
        ax.set_title('NAMD Minimization - Potential Energy')
        ax.set_xlabel('ts')
        ax.set_ylabel(r'$E_{pot}$')
        fig.tight_layout()
        fig.savefig('minimization.png')


def plot_heating(filepath):
    with open(filepath) as f:
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
        ax1.set_title('NAMD Heating - Potential Energy')
        ax1.set_ylabel(r'$E_{pot}$')
        ax2.plot(ts, temp)
        ax2.set_title('NAMD Heating - Temperature')
        ax2.set_xlabel('ts')
        ax2.set_ylabel('temperature')
        fig.tight_layout()
        fig.savefig('heating.png')


def plot_equilibration(filepath):
    with open(filepath) as f:
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
        ax1.set_title('NAMD Equilibration - Temperature')
        ax1.set_ylabel('temperature')
        ax2.plot(ts, cell_size)
        ax2.set_title('NAMD Equilibration - Unit Cell Size')
        ax2.set_xlabel('ts')
        ax2.set_ylabel('Unit Cell Size')
        fig.tight_layout()
        fig.savefig('equilibration.png')


def plot_production(filepath):
    with open(filepath) as f:
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
        ax1.set_title('NAMD Production - Total Energy')
        ax1.set_ylabel(r'$E_{total}$')
        ax2.plot(ts, temp)
        ax2.set_title('NAMD Production - Temperature')
        ax2.set_xlabel('ts')
        ax2.set_ylabel('temperature')
        fig.tight_layout()
        fig.savefig('production.png')


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.min_out:
        plot_minimzation(args.min_out)
    if args.heat_out:
        plot_heating(args.heat_out)
    if args.equil_out:
        plot_equilibration(args.equil_out)
    if args.quench_out:
        plot_production(args.quench_out)


if __name__ == '__main__':
    main()
