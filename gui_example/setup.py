#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    # Some information about the app
    # You can write almost anything here
    name='gui_example',
    version='1.0',
    url='https://github.com/chegoryu/PythonSetupExample',
    license='MIT',
    author='Egor Chunaev',
    author_email='none@none.com',
    description='GUI example with setuptools',

    # Packages in this example is ['gui']
    # We can specify it explicitly, but fortunately we have a special function
    packages=find_packages(),

    # For this example we use external library 'kivy'
    install_requires=['kivy'],

    # Entry point for app
    # By default the startup script is installed in '/usr/local/bin' or something like that in other systems
    # To create startup script in installation dir run './setup.py install --install-scripts .'
    # after that startup script will be created in the installation directory
    # and can be run as './gui_example'
    # But it is recommended to install scripts in a separate directory './setup.py install --install-scripts ./scripts'
    # because in addition to the main scripts dependency scripts can also be installed
    entry_points={
        'gui_scripts': [
            'gui_example=gui:main'
        ],
    }
)
