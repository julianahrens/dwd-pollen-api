import os
import sys

from setuptools import setup, find_packages


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author='Julian Ahrens',
    author_email='opensource@julianahrens.de',
    classifiers=[
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description='Asynchronous Python client for getting DWD pollen info.',
    include_package_data=True,
    install_requires=['aiohttp>=3.0.0'],
    keywords=['dwd', 'pollen', 'api', 'async', 'client'],
    license='MIT License',
    long_description_content_type='text/markdown',
    long_description=readme,
    name='dwd-pollen-api',
    packages=find_packages(include=['dwd-pollen-api']),
    url='https://github.com/julianahrens/dwd-pollen-api',
    version='1.0.1',
    zip_safe=False,
)
