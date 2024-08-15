#!/usr/bin/env python3
"""Script to increment the version number in pyproject.toml"""

import toml
from pathlib import Path


def increment_version(pyproject_path):
    pyproject = Path(pyproject_path)
    data = toml.load(pyproject)

    version = data['project']['version']
    major, minor, patch = map(int, version.split('.'))

    new_version = f'{major}.{minor}.{patch + 1}'
    data['project']['version'] = new_version

    with pyproject.open('w') as f:
        toml.dump(data, f)

    print(f"Version incremented to {new_version}")


if __name__ == "__main__":
    increment_version("pyproject.toml")