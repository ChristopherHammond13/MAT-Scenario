try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'move and tag problem',
    'author': 'graphorn',
    'version': '0.1',
    'install_requires': ['nose', 'pyvisgraph'],
    'packages': ['mat_scenario'],
    'scripts': [],
    'name': 'mat_scenario'
}

setup(**config)
