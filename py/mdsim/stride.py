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


def split_contact_timeline(x, t_h):
    return (x[:t_h], x[t_h:])


def split_contact_timeline_all(xs, t_h):
    timeline_pairs = [split_contact_timeline(x, t_h) for x in xs]
    xs_initial = [pair[0] for pair in timeline_pairs]
    xs_final = [pair[1] for pair in timeline_pairs]
    return (xs_initial, xs_final)


def split_helix_timeline(x, t_h=None):
    if t_h is None:
        t_h = int(helix_denature_time(x))
    return (x[:t_h], x[t_h:])


def split_helix_timeline_all(xs, t_h=None):
    timeline_pairs = [split_helix_timeline(x, t_h) for x in xs]
    xs_initial = [pair[0] for pair in timeline_pairs]
    xs_final = [pair[1] for pair in timeline_pairs]
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
    result['y'] = smooth(stats['y'])
    return result


def smooth(x, window_size=100):
    window_size = min(window_size, len(x) // 2)
    return savgol_filter(x, window_size, 1)
    # return window_transform(x, window_size)


def save_plot(fig, output_file):
    fig.savefig(output_file)
    print('Saved plot:', output_file)


def make_plot(title, group_stats, output_file):
    nrows = len(group_stats)
    fig, axs = plt.subplots(nrows, sharey=True)
    for (ax, (name, st)) in zip(axs, group_stats.items()):
        st = apply_transforms(st)
        y = st['y']
        ax.plot(y)
        y_mean = st['y_mean']
        ax.axhline(y_mean, label=f'$<H_{{{name}}}>$', ls=':', color='m')
        ax.legend()
        ax.set_ylabel(f"$<H_{{{name}}}(t)>$")
    axs[-1].set_xlabel('t')
    fig.suptitle(title)
    save_plot(fig, output_file)


def plot_average_helix_all(helices_pcts, output_file):
    fig, ax = plt.subplots()
    y = smooth(helices_pcts.mean(axis=0))
    ax.plot(y)
    y_mean = y.mean()
    ax.axhline(y_mean, label='$<H_{all}>$', ls=':', color='m')
    ax.legend()
    ax.set_ylabel('$<H_{all}(t)>$')
    ax.set_xlabel('t')
    fig.suptitle('Average helix structure (%) for all trajectories')
    save_plot(fig, output_file)


def helix_denature_time(helix_content, helix_fraction=0.4):
    result = 0
    for t, content in enumerate(smooth(helix_content)):
        if content > 0.4:
            result = t
    return result


def plot_trajectory_helix_content(experiment, trajectory, y_raw, output_file):
    ncols = 2
    y_smooth = smooth(y_raw)
    y_mean = y_raw.mean()
    t_denatured = helix_denature_time(y_raw)
    helix_mean = y_raw[:t_denatured].mean()
    denatured_mean = y_raw[t_denatured:].mean()
    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(y_smooth, lw=1)
    ax1.set_ylabel(f"$<H_{{{trajectory}}}(t)>$")
    ax2.plot(y_raw, lw=1)
    ax2.set_ylabel(f"$<H_{{{trajectory}}}(t)> (raw)$")
    ax2.set_xlabel('t')
    for ax in (ax1, ax2):
        ax.axhline(y_mean, label=f'$<H_{{{trajectory}}}>$', lw=0.6, ls=':', color='m')
        ax.axvline(t_denatured, label=f'$t_{{h,{trajectory}}}$', lw=0.6, ls=':', color='g')
        ax.set_ylim(ymax=1.2)
        ax.legend()
    fig.suptitle(f'Trajectory {trajectory}: {experiment} - Helix content (%)')
    save_plot(fig, output_file)


def plot_contacts(y_all, y_initial, y_final):
    fig, ax = plt.subplots()
    x = list(range(1, len(y_all) + 1))
    ys = (y_all, y_initial, y_final)
    labels = ('$<C_{all}>$', '$<C_{initial}>$', '$<C_{final}>$')
    for (y, label) in zip(ys, labels):
        ax.plot(x, y, marker='o', lw=1, label=label)
    ax.set_ylabel('<C(i)>')
    ax.set_xlabel('i')
    ax.legend()
    return fig


def analyze_contacts(config, t_h):
    contact_file_paths = canonicalize_file_paths(
        config['config_path'],
        config['ibuContact_files'],
    )
    output_dir_path = Path(config['output_dir'])
    output_file = output_dir_path / 'contacts.png'
    title = 'Average Ibuprofin Contacts'
    contacts = process_contact_files(contact_file_paths)
    contacts_initial, contacts_final = split_contact_timeline_all(contacts, t_h)
    y_all = total_mean_residue_contact_frequency(contacts)
    y_initial = total_mean_residue_contact_frequency(contacts_initial)
    y_final = total_mean_residue_contact_frequency(contacts_final)
    fig = plot_contacts(y_all, y_initial, y_final)
    fig.suptitle(title)
    save_plot(fig, output_file)


def plot_t_h(t_h_data):
    fig, ax = plt.subplots()
    labels = ['$t_{h,ibu}$', '$t_{h,water}$']
    data = [t_h_data['ibu_t_h'], t_h_data['water_t_h']]
    ax.boxplot(data, labels=labels)
    ax.set_ylabel('t')
    fig.suptitle('Helix dissolution time of Ibuprofen and Water systems')
    return fig


def calculate_t_h(group_configs, helices_pcts):
    result = {}
    result['t_h'] = t_h = np.array([
        helix_denature_time(x) for x in helices_pcts
    ])
    result['t_h_mean'] = t_h.mean()
    for group_config in group_configs:
        name = group_config['name']
        cols = group_config['cols']
        trajectories = group_config['trajectories']
        result[f'{name}_t_h'] = t_h[cols]
        result[f'{name}_t_h_mean'] = group_mean(t_h, cols)
    return result


def helix_timeline_means(helices_pcts):
    ys_initial, ys_final = split_helix_timeline_all(helices_pcts)
    ys_initial = [y.mean() for y in ys_initial]
    ys_final = [y.mean() for y in ys_final]
    return (ys_initial, ys_final)


def analyze_helix_timelines(config, helices_pcts):
    output_dir_path = Path(config['output_dir'])
    output_file = output_dir_path / 't_h_batch_compare.png'
    ibu_config, water_config = config['groups']
    ibu_cols = ibu_config['cols']
    water_cols = water_config['cols']
    labels = ['Ibu', 'Water']

    y1, y2 = helix_timeline_means(helices_pcts)
    y1 = np.array(y1)
    y2 = np.array(y2)
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True)

    data1 = [y1[ibu_cols], y1[water_cols]]
    ax1.boxplot(data1, labels=labels)
    ax1.set_ylabel('$<H_{initial}>$')

    data2 = [y2[ibu_cols], y2[water_cols]]
    ax2.boxplot(data2, labels=labels)
    ax2.set_ylabel('$<H_{final}>$')

    fig.suptitle(
        'Average helical structure before and after helix dissolution, '
        '$t_{h,m}$'
    )
    save_plot(fig, output_file)


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
    output_dir_path.mkdir(parents=True, exist_ok=True)

    group_configs = config['groups']
    helices, totals, helices_pcts = process_files(stride_file_paths)
    t_h_data = calculate_t_h(group_configs, helices_pcts)
    t_h_mean = t_h_data['t_h_mean']
    print(t_h_data['t_h'])
    print(f'Average t_h: {t_h_mean:.3f} ps')
    fig = plot_t_h(t_h_data)
    save_plot(fig, output_dir_path / 't_h.png')

    for group_config in group_configs:
        group_name = group_config['name']
        cols = group_config['cols']
        trajectories = group_config['trajectories']
        group_t_h_mean = t_h_data[f'{group_name}_t_h_mean']
        print(f'{group_name} t_h average: {group_t_h_mean:.3f} ps')
        for (col, trajectory) in zip(cols, trajectories):
            file_name = f'stride-{group_name}-{trajectory}.png'
            output_file_path = output_dir_path / file_name
            plot_trajectory_helix_content(
                group_name, trajectory, helices_pcts[col], output_file_path)

    groups = dict(
        (conf['name'], aggregate_group(helices, totals, conf['cols']))
        for conf in group_configs
    )
    group_stats = dict((name, stats(data)) for (name, data) in groups.items())
    title = 'Average helix structure (%) of IBU and Water systems'
    make_plot(title, group_stats, output_dir_path / 'stride-groups.png')
    plot_average_helix_all(helices_pcts, output_dir_path / 'stride-all.png')

    analyze_helix_timelines(config, helices_pcts)

    ibu_t_h = int(t_h_data['ibu_t_h_mean'])
    analyze_contacts(config, ibu_t_h)
