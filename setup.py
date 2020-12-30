from setuptools import setup, find_packages

setup(
    name='sauce_storage_api',
    author='Augusto Vilela',
    author_email='avilelateixeira@gmail.com',
    version='1.0.0',
    description='Lib to use saucelabs Application Storage API - https://wiki.saucelabs.com/display/DOCS/Application+Storage',
    packages=find_packages(),
    keyword=['saucelabs', 'application storage'],
    install_requires=['httpx']
)
