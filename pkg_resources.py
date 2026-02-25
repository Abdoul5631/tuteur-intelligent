"""
Petit shim pour `pkg_resources` utilisé par certains paquets (ex: simplejwt)
Fournit `get_distribution(name)` et `DistributionNotFound` en utilisant
`importlib.metadata` quand c'est possible.

Ce fichier est un palliatif pour environnements où `pkg_resources`
n'est pas disponible (setuptools ne le fournit pas ici). Dès que
`pkg_resources` officiel est présent dans l'environnement, ce shim
peut être supprimé.
"""
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
