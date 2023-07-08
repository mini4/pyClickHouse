from setuptools import find_packages, setup


setup(
    name='pyClickHouse',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
    ],
    extras_require={
        'dev': [
            'black',
            'coverage',
            'flake8',
            'isort',
            'pytest',
            'pytest-testmon',
            'pytest-watch',
        ]
    },
)
