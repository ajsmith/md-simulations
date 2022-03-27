import importlib.resources
import yaml


def _load_yaml(name):
    resource = importlib.resources.open_text('mdsim.defaults', name)
    return yaml.load(resource, yaml.Loader)


def load_plot_stats():
    return _load_yaml('plot_stats.yaml')
