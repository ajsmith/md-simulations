#!/usr/bin/env python

import matplotlib.pyplot as plt

COL_TS = 1
COL_KINETIC = 10
COL_POTENTIAL = 13
COL_TEMP = 12
COL_TOTAL = 11
COL_VOLUME = 18


def plot_minimzation():
    with open('output/val_min.out') as f:
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


def plot_heating():
    with open('output/val_heat.out') as f:
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


def plot_equilibration():
    with open('output/val_equil.out') as f:
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


def plot_production():
    with open('output/val_quench.out') as f:
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
    plot_minimzation()
    plot_heating()
    plot_equilibration()
    plot_production()

if __name__ == '__main__':
    main()
