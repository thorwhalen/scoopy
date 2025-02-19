"""Utility functions for Scoopy."""

import os
from functools import partial

from i2 import get_app_data_folder

import dol

pkg_name = 'scoopy'

_root_app_data_dir = get_app_data_folder()
app_data_dir = os.environ.get(
    f'{pkg_name.upper()}_APP_DATA_DIR',
    os.path.join(_root_app_data_dir, pkg_name),
)
app_data_dir = dol.ensure_dir(app_data_dir, verbose=f'Making app dir: {app_data_dir}')
djoin = partial(os.path.join, app_data_dir)


def get_config(key):
    """Get a configuration value from the environment or raise an error if missing."""
    val = os.getenv(key)
    if val is None:
        raise ValueError(f"Missing environment variable: {key}")
    return val
