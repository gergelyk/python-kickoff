from setuptools import setup, find_packages
from pathlib import Path

this_dir_path = Path(__file__).parent
readme_path = this_dir_path / 'README.rst'

with open(readme_path) as fh:
    long_description = fh.read()

setup(
    name = 'kickoff',
    version = '0.3.2',
    description = 'Turns your Python script or module into an application with decent CLI.',
    author = 'Grzegorz Krason',
    author_email = 'grzegorz.krason@gmail.com',
    url = 'https://github.com/gergelyk/python-kickoff',
    license = 'MIT',
    packages = find_packages(),
    keywords = 'cli cui argparse optparse docopt click fire invoke runfile'.split(),
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    python_requires = '~=3.6',
    entry_points = {
        'console_scripts': ['kickoff = kickoff.__main__:main'],
        },
    install_requires = [
        'click',
        'click-didyoumean',
        'click-repl',
        'python-box',
    ],
    classifiers = [
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Other Environment',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'License :: OSI Approved :: MIT License',
        'Operating System :: iOS',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
