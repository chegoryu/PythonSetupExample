#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    # Some information about the app
    # You can write almost anything here
    name='console_example',
    version='1.0',
    url='https://github.com/chegoryu/PythonSetupExample',
    license='MIT',
    author='Egor Chunaev',
    author_email='none@none.com',
    description='Console example with setuptools',

    # Packages in this example are ['cli', 'cli.helpers']
    # We can specify them explicitly, but fortunately we have a special function
    packages=find_packages(),

    # For this example we use external library 'click'
    install_requires=['click'],

    # Entry point for app
    # After installation the app can be run as "console_example <args>"
    entry_points={
        'console_scripts': [
            'console_example=cli:cli'
        ],
    }
)
