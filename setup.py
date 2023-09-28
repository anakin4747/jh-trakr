from setuptools import setup, find_packages

with open("requirements.txt", "r") as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name="jh_trakr",
    version="1.0",
    description=(
        "A tool for keeping track of job applications from the command line"
    ),
    author="Anakin",
    author_email="anakin@childerhose.ca",
    url="https://github.com/anakin4747/jh-trakr/",
    packages=find_packages(exclude=('tests*',)),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'jh_trakr = jh_trakr.main:main',
        ],
    },
)
