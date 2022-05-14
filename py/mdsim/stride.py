"""Statistical analysis of STRIDE data.

"""
import sys
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy.signal import savgol_filter


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
    return (helices, totals, helices / totals)


def process_files(file_paths):
    assert len(file_paths) > 0, 'No files given'

    helices = []
    totals = []
    helices_pcts = []
    for fpath in file_paths:
        ts_helix, ts_all, ts_pcts = process_file(fpath)
        helices.append(ts_helix)
        totals.append(ts_all)
        helices_pcts.append(ts_pcts)
    return (np.vstack(helices), np.vstack(totals), np.vstack(helices_pcts))


def process_contact_line(line):
    """Return the contact counts for a line of ibuContacts data."""
    return [int(field) for field in line.split()]


def process_contact_file(file_path):
    ts_contacts = []
    with open(file_path) as f:
        for line in f.readlines():
            ts_contacts.append(process_contact_line(line))
    return ts_contacts


def process_contact_files(file_paths):
    assert len(file_paths) > 0, 'No files given'

    contact_vecs = []
    for fpath in file_paths:
        contact_vecs.append(process_contact_file(fpath))
    return np.array(contact_vecs, dtype=np.uint)


def mean_residue_contact_frequency(contacts):
    return contacts.mean(axis=0)

def total_mean_residue_contact_frequency(contacts):
    x = np.array([mean_residue_contact_frequency(c) for c in contacts])
    return x.mean(axis=0)

def split_timeline(x, t_h):
    return (x[:t_h], x[t_h:])

def split_timeline_all(xs, t_h):
    timeline_pairs = [split_timeline(x, t_h) for x in xs]
    xs_initial = np.array([pair[0] for pair in timeline_pairs])
    xs_final = np.array([pair[1] for pair in timeline_pairs])
    return (xs_initial, xs_final)

def group_sum(matrix, cols):
    return matrix[cols].sum(axis=0)


def group_mean(matrix, cols):
    return matrix[cols].mean(axis=0)


def aggregate_group(helices, totals, cols):
    return np.vstack((group_sum(helices, cols), group_sum(totals, cols)))


def stats(ts_arrays):
    helices, totals = ts_arrays
    return {
        'y': helices / totals,
        'y_mean': (helices / totals).mean(),
        'var': helices.var(),
        'helix_count': helices.sum(),
        'structure_count': totals.sum(),
        'steps': len(totals)
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
        config['config_path'] = filepath
    return config


def canonicalize_file_paths(root, file_paths):
    path = Path(root)
    if path.is_file():
        path = path.parent
    return [str((path / fpath).resolve()) for fpath in file_paths]


def window_transform(x, window_size):
     k = window_size // 2
     return np.array([x[i-k:i+k].mean() for i in range(k, len(x), k)])


def apply_transforms(stats):
    result = dict(stats)
    result['y'] = savgol_filter(stats['y'], 100, 1)
    # result['y'] = window_transform(stats['y'], 100)
    return result


def smooth(x):
    return savgol_filter(x, 100, 1)
    # return window_transform(x, 100)


def make_plot(title, group_stats, output_file):
    nrows = len(group_stats)
    fig, axs = plt.subplots(nrows, sharey=True)
    for (ax, (name, st)) in zip(axs, group_stats.items()):
        st = apply_transforms(st)
        y = st['y']
        ax.plot(y, color='b')
        y_mean = st['y_mean']
        ax.axhline(y_mean, label=f'$<H_{{{name}}}>$', ls=':', color='m')
        ax.legend()
        ax.set_ylabel(f"$<H_{{{name}}}(t)>$")
    axs[-1].set_xlabel('t')
    fig.suptitle(title)
    fig.savefig(output_file)
    print('Saved plot:', output_file)


def helix_denature_time(helix_content, helix_fraction=0.4):
    result = 0
    for t, content in enumerate(helix_content):
        if content > 0.4:
            result = t
    return result


def plot_trajectory_helix_content(experiment, trajectory, y_raw, output_file):
    ncols = 2
    y_smooth = smooth(y_raw)
    y_mean = y_raw.mean()
    t_denatured = helix_denature_time(y_smooth)
    helix_mean = y_raw[:t_denatured].mean()
    denatured_mean = y_raw[t_denatured:].mean()
    # print(y_mean, t_denatured, output_file)
    # print(f'{t_denatured}: {y_mean:.3f} {helix_mean:.3f} {denatured_mean:.3f}')
    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(y_smooth, lw=1)
    ax1.set_ylabel(f"$<H_{{{trajectory}}}(t)>$")
    ax2.plot(y_raw, lw=1)
    ax2.set_ylabel(f"$<H_{{{trajectory}}}(t)> (raw)$")
    ax2.set_xlabel('t')
    for ax in (ax1, ax2):
        ax.axhline(y_mean, label=f'$<H_{{{trajectory}}}>$', lw=0.6, ls=':', color='m')
        ax.axvline(t_denatured, label=f'$t_{{h}}$', lw=0.6, ls=':', color='g')
        ax.set_ylim(ymax=1.2)
        ax.legend()
    fig.suptitle(f'Trajectory {trajectory}: {experiment} - Helix content (%)')
    fig.savefig(output_file)
    print('Saved plot:', output_file)


def plot_contacts(args):
    kaboom


def analyze_contacts_data(config):
    contact_file_paths = canonicalize_file_paths()
    kaboom


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
    output_dir_path = Path(config['output_dir'])
    title = config.get('title', '')

    group_configs = config['groups']
    helices, totals, helices_pcts = process_files(stride_file_paths)
    t_hs = np.array([
        helix_denature_time(smooth(x)) for x in helices_pcts
    ])
    print(t_hs)
    t_h_mean = t_hs.mean()

    print(f'Average t_h: {t_h_mean:.3f} ps')
    for group_config in group_configs:
        group_name = group_config['name']
        cols = group_config['cols']
        trajectories = group_config['trajectories']
        group_t_h_mean = group_mean(t_hs, cols)
        print(f'{group_name} t_h average: {group_t_h_mean:.3f} ps')
        for (col, trajectory) in zip(cols, trajectories):
            output_file = output_dir_path / f'stride-{group_name}-{trajectory}.png'
            plot_trajectory_helix_content(
                group_name, trajectory, helices_pcts[col], output_file)

    groups = dict(
        (conf['name'], aggregate_group(helices, totals, conf['cols']))
        for conf in group_configs
    )
    group_stats = dict((name, stats(data)) for (name, data) in groups.items())
    # plot_raw('Trajectory 01', 'ibu', helices[0], totals[0], output_file)
    make_plot(title, group_stats, output_dir_path / 'sstruture.png')
