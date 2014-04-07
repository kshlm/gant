
from setuptools import setup

setup(name='gant',
    version='0.0.1',
    description="The Gluster development helper ant",
    long_description="The Gluster development helper ant, gant for short, helps developer of GlusterFS by createing a standardized development and testing environment using Docker.",
    keywords='gluster docker utility development testing',
    author='Kaushal M',
    author_email='kshlmster@gmail.com',
    url='http://github.com/kshlm/gant',
    license='BSD',
    classifiers=[
        "Development Status :: 3 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
    ],
    packages=['gant'],
    install_requires=[
        "docker-py",
        "docopt",
        ],
    entry_points="""
        [console_scripts]
        gant = gant.main:main
    """,
    )
