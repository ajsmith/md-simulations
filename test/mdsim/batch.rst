====================================
Setup and running production batches
====================================

Production simulations are typically very long running processes,
which if interrupted could lead to the loss of hours, days, or even
weeks of work. Thus, production simulations are broken down into a
batch smaller segments. The output of one segment becomes the input to
the next, and this way we can provide some fault tolerance. The
`mdsim.batch` module provides utilities for working with such batches.

The following data is used in configuring a batch.

    >>> student_id = 6
    >>> trajectory_id = 1
    >>> step_id = 0

Let's get the random seed for the first, second, and third segments.

    >>> from mdsim.batch import make_seed
    >>> make_seed(student_id, trajectory_id, step_id)
    '60100'
    >>> make_seed(student_id, trajectory_id, step_id + 1)
    '60101'
    >>> make_seed(student_id, trajectory_id, step_id + 2)
    '60102'

Now let's generate the configuration for a three-step batch.

    >>> from mdsim.batch import make_batch_config
    >>> batch_configs = [
    ...     make_batch_config(student_id, trajectory_id, step_id + i)
    ...     for i in range(3)
    ... ]
    >>> from pprint import pprint
    >>> for config in batch_configs:
    ...     pprint(config)
    {'batch': '00', 'previous_batch': None, 'seed': '60100'}
    {'batch': '01', 'previous_batch': '00', 'seed': '60101'}
    {'batch': '02', 'previous_batch': '01', 'seed': '60102'}

Now let's configure a trajectory with three steps. Trajectory configs
also specify a configuration template to use.

    >>> from mdsim.batch import make_trajectory_config
    >>> config_template = 'quench.namd.j2'
    >>> tr_config = make_trajectory_config(
    ...     student_id, trajectory_id, 3, config_template)
    >>> list(sorted(tr_config.keys()))
    ['batches', 'config_template', 'trajectory']
    >>> tr_config['trajectory']
    '01'
    >>> tr_config['config_template']
    'quench.namd.j2'
    >>> for batch_config in tr_config['batches']:
    ...     pprint(batch_config)
    {'batch': '00', 'previous_batch': None, 'seed': '60100'}
    {'batch': '01', 'previous_batch': '00', 'seed': '60101'}
    {'batch': '02', 'previous_batch': '01', 'seed': '60102'}
