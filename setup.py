from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sauce_storage_api',
    author='Augusto Vilela',
    url='https://github.com/avilela/SauceLabsApplicationStorageApi',
    author_email='avilelateixeira@gmail.com',
    version='1.0.3',
    description='Lib to use saucelabs Application Storage API - https://wiki.saucelabs.com/display/DOCS/Application+Storage',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keyword=['saucelabs', 'application storage'],
    install_requires=['requests'],
    python_requires='>=3.6'
)
