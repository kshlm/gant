
from setuptools import setup, find_packages
import sys, os

setup(name='gant',
    version='0.0.1',
    description="Development and testing environment for GlusterFS using Docker.",
    long_description="Development and testing environment for GlusterFS using Docker.",
    classifiers=[], 
    keywords='',
    author='Kaushal M',
    author_email='kshlmster@gmail.com',
    url='http://github.com/kshlm/gant',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        "docker-py",
        "aaargh",
        ],
    setup_requires=[],
    entry_points="""
    """,
    namespace_packages=[],
    )
