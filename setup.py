from setuptools import setup, find_packages

entry_points = """\
[console_scripts]
mdsim-plot=mdsim.plot_stats:main
mdsim-cell-size=mdsim.find_cell_size:main
mdsim-check-coords=mdsim.check_coordinates:main
mdsim-batch-config=mdsim.batch:main
mdsim-stride-stats=mdsim.stride:main
"""

package_data = {
    'mdsim.defaults': ['*.yaml'],
    'test.mdsim': ['*.dat'],
}

setup(
    name='mdsim',
    version='0',
    author='Alexander Smith',
    author_email='asmitl@gmu.edu',
    url='https://github.com/ajsmith/md-simulations',
    packages=find_packages('py'),
    package_dir={'': 'py'},
    package_data=package_data,
    include_package_data=True,
    zip_safe=True,
    entry_points=entry_points,
    install_requires=[
        'PyYAML',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
    ],
)
