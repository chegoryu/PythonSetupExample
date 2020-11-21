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
    # You may notice that creating a separate directory for helpers is not particularly necessary
    # and you can create a file helpers.py directly in the cli directory
    # this was done specifically to show what happens with two or more packages
    packages=find_packages(),

    # For this example we use external library 'click'
    install_requires=['click'],

    # Entry point for app
    # By default the startup script is installed in '/usr/local/bin' or something like that in other systems
    # To create startup script in installation dir run './setup.py install --install-scripts .'
    # after that startup script will be created in the installation directory
    # and can be run as './console_example <args>'
    entry_points={
        'console_scripts': [
            'console_example=cli:cli'
        ],
    }
)
