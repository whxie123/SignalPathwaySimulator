from setuptools import setup, find_packages

setup(
    name='SignalPathwaySimulator',
    version='0.1.0',
    author='Wenhui Xie',
    author_email='whxie@uw.edu',
    description='A Python tool for simulating and analyzing cellular signaling pathways.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/whxie123/SignalPathwaySimulator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy>=1.18.0',
        'scipy>=1.4.0',
        'matplotlib>=3.1.0',
        'libsbml>=5.18.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'signalpathwaysimulator=signalpathwaysimulator.cli:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/whxie123/SignalPathwaySimulator/issues',
        'Source': 'https://github.com/whxie123/SignalPathwaySimulator',
    },
)

