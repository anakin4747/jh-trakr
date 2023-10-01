
from setuptools import setup, find_packages

setup(
    name='jh-trakr',
    version='0.1.0',
    license='MIT',
    description='Command line job application tracker',

    author='Anakin Childerhose',
    author_email='anakin@childerhose.ca',
    url='https://github.com/anakin4747/jh-trakr',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['pyfzf', 'tabulate'],

    entry_points={
        'console_scripts': [
            'jh-trakr = jh_trakr.main:main',
        ]
    },
)
