"""
Exported modified file: pkg_resources.py (shim)
"""

# Full contents copied from current workspace

from importlib import metadata


class DistributionNotFound(Exception):
    pass


class _Dist:
    def __init__(self, name, version):
        self.project_name = name
        self.version = version


def get_distribution(name: str):
    try:
        ver = metadata.version(name)
        return _Dist(name, ver)
    except Exception as e:
        raise DistributionNotFound(name)
