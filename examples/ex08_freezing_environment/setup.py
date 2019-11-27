from setuptools import setup, find_packages

setup(
    name = 'Demo',
    version = '0.1.0',
    packages = find_packages(),
    install_requires = ('kickoff'),
    entry_points = {
        'console_scripts': ['demo = demo.__main__:main'],
        },
)
