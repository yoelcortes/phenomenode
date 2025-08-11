# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2023, Yoel Cortes-Pena <yoelcortes@gmail.com>
#
# This module is under the UIUC open-source license. See
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
from setuptools import setup
setup(
    name='benchmark',
    packages=['benchmark'],
    license='MIT',
    version='0.0.1',
    description="Benchmark simulations and graph representations for phenomena-based decomposition approaches. ",
    long_description=open('README.md', encoding='utf-8').read(),
    author='Yoel Cortes-Pena',
    install_requires=['biosteam'],
    extras_require={
        'dev': [
        ]
    },
    package_data={
        'benchmark': []
    },
    python_requires='>=3.9',
    platforms=['Windows', 'Mac', 'Linux'],
    author_email='yoelcortes@gmail.com',
    url='https://github.com/yoelcortes/phenomenode',
    download_url='https://github.com/yoelcortes/phenomenode.git',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'License :: OSI Approved :: University of Illinois/NCSA Open Source License',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Chemistry',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Manufacturing',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: POSIX :: BSD',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Topic :: Education'],
    keywords=['thermodynamics', 'chemical engineering', 'mass and energy balance', 'material properties', 'phase equilibrium'],
)