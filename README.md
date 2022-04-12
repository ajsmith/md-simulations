# md-simulations

Tools for running molecular dynamics simulations.

This project is a mess of utility and analysis scripts implemented in
Python and Ansible.


# Python Tools

Python executables provided by this project have the "mdsim-"
prefix. They're generally useful for analyzing NAMD output and
manipulating configuration files for running simulations.


## Installation

This project can be pip installed into your environment.

```shell
pip install -e .
```

For convenience, the `install.sh` script will create a Python
virtualenv in the current directory if one doesn't already exist, then
pip install this project into it. This is stored in the "venv"
directory. A first time setup and use might look like

```shell
```


# Automation & Batch Running

pip
