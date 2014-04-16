from setuptools import setup

setup(name='gant',
    version='0.0.6',
    description="The Gluster development helper ant",
    long_description="The Gluster development helper ant, gant for short, helps in the development of GlusterFS by creating a standardized development and testing environment using Docker.",
    keywords='gluster docker utility development testing',
    author='Kaushal M',
    author_email='kshlmster@gmail.com',
    url='https://github.com/kshlm/gant',
    license='BSD',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
    ],
    packages=['gant', 'gant.utils'],
    install_requires=[
        "docker-py",
        "docopt",
        ],
    entry_points="""
        [console_scripts]
        gant = gant.main:main
    """,
    )
