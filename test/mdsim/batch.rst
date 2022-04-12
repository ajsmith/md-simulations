==========================================
Configuring and running production batches
==========================================

Production simulations are typically very long running processes,
which if interrupted could lead to the loss of hours, days, or even
weeks of work. Thus, production simulations are broken down into a
batch smaller segments. The output of one segment becomes the input to
the next, and this way we can provide some fault tolerance. The
`mdsim.batch` module provides utilities for working with such batches.

The following data is used in configuring a batch::

    >>> student_id = 6
    >>> trajectory_id = 1
    >>> step_id = 0

Let's get the random seed for the first, second, and third segments::

    >>> from mdsim.batch import make_seed
    >>> make_seed(student_id, trajectory_id, step_id)
    '60100'
    >>> make_seed(student_id, trajectory_id, step_id + 1)
    '60101'
    >>> make_seed(student_id, trajectory_id, step_id + 2)
    '60102'

Now let's generate the configuration for a three-step batch::

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
also specify a configuration template to use::

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

In a very simple sense, a simulation plan is a map of trajectory ids
to configuration templates. Along with the student id and step count,
we can generate all the configuration items needed for several
simulation trajectories.

    >>> sim_plan = {
    ...     1: 'ibu.namd.j2',
    ...     2: 'ibu.namd.j2',
    ...     3: 'water.namd.j2',
    ...     4: 'water.namd.j2',
    ... }
    >>> from mdsim.batch import make_simulation_config
    >>> sim_config = make_simulation_config(student_id, sim_plan, 3)
    >>> list(sim_config.keys())
    ['trajectories']
    >>> for trajectory in sim_config['trajectories']:
    ...     print('Trajectory:', trajectory['trajectory'])
    ...     print('Template', trajectory['config_template'])
    ...     for batch_config in trajectory['batches']:
    ...         pprint(batch_config)
    Trajectory: 01
    Template ibu.namd.j2
    {'batch': '00', 'previous_batch': None, 'seed': '60100'}
    {'batch': '01', 'previous_batch': '00', 'seed': '60101'}
    {'batch': '02', 'previous_batch': '01', 'seed': '60102'}
    Trajectory: 02
    Template ibu.namd.j2
    {'batch': '00', 'previous_batch': None, 'seed': '60200'}
    {'batch': '01', 'previous_batch': '00', 'seed': '60201'}
    {'batch': '02', 'previous_batch': '01', 'seed': '60202'}
    Trajectory: 03
    Template water.namd.j2
    {'batch': '00', 'previous_batch': None, 'seed': '60300'}
    {'batch': '01', 'previous_batch': '00', 'seed': '60301'}
    {'batch': '02', 'previous_batch': '01', 'seed': '60302'}
    Trajectory: 04
    Template water.namd.j2
    {'batch': '00', 'previous_batch': None, 'seed': '60400'}
    {'batch': '01', 'previous_batch': '00', 'seed': '60401'}
    {'batch': '02', 'previous_batch': '01', 'seed': '60402'}

This configuration is most useful when stored in a file, so let's save
it as a YAML file.

    >>> from tempfile import NamedTemporaryFile
    >>> tmp = NamedTemporaryFile(prefix='test-mdsim.batch-')
    >>> from mdsim.batch import save_yaml
    >>> save_yaml(tmp.name, sim_config)
    >>> with open(tmp.name) as f:
    ...     print(f.read())
    simulation:
      trajectories:
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60100'
        - batch: '01'
          previous_batch: '00'
          seed: '60101'
        - batch: '02'
          previous_batch: '01'
          seed: '60102'
        config_template: ibu.namd.j2
        trajectory: '01'
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60200'
        - batch: '01'
          previous_batch: '00'
          seed: '60201'
        - batch: '02'
          previous_batch: '01'
          seed: '60202'
        config_template: ibu.namd.j2
        trajectory: '02'
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60300'
        - batch: '01'
          previous_batch: '00'
          seed: '60301'
        - batch: '02'
          previous_batch: '01'
          seed: '60302'
        config_template: water.namd.j2
        trajectory: '03'
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60400'
        - batch: '01'
          previous_batch: '00'
          seed: '60401'
        - batch: '02'
          previous_batch: '01'
          seed: '60402'
        config_template: water.namd.j2
        trajectory: '04'


 And of course, it's helpful if we can run this all from the command
 line by feeding it a YAML file which describes the simulation plan.

    >>> from mdsim.batch import main
    >>> tmp1 = NamedTemporaryFile(prefix='test-mdsim.batch-')
    >>> tmp2 = NamedTemporaryFile(prefix='test-mdsim.batch-')
    >>> plan_yaml = """\
    ... student_id: 6
    ... steps: 3
    ... plan:
    ...   1: ibu.namd.j2
    ...   2: ibu.namd.j2
    ...   3: water.namd.j2
    ...   4: water.namd.j2
    ... """
    >>> _ = tmp1.write(plan_yaml.encode('utf8'))
    >>> tmp1.flush()
    >>> main(argv=['test', '--plan', tmp1.name, '--out', tmp2.name])
    >>> with open(tmp2.name, 'r') as f:
    ...     print(f.read())
    simulation:
      trajectories:
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60100'
        - batch: '01'
          previous_batch: '00'
          seed: '60101'
        - batch: '02'
          previous_batch: '01'
          seed: '60102'
        config_template: ibu.namd.j2
        trajectory: '01'
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60200'
        - batch: '01'
          previous_batch: '00'
          seed: '60201'
        - batch: '02'
          previous_batch: '01'
          seed: '60202'
        config_template: ibu.namd.j2
        trajectory: '02'
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60300'
        - batch: '01'
          previous_batch: '00'
          seed: '60301'
        - batch: '02'
          previous_batch: '01'
          seed: '60302'
        config_template: water.namd.j2
        trajectory: '03'
      - batches:
        - batch: '00'
          previous_batch: null
          seed: '60400'
        - batch: '01'
          previous_batch: '00'
          seed: '60401'
        - batch: '02'
          previous_batch: '01'
          seed: '60402'
        config_template: water.namd.j2
        trajectory: '04'
