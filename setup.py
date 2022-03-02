#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['caproto']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Ronald J Pandolfi",
    author_email='ronpandolfi@lbl.gov',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="A caproto-based IOC for control of the fastccd power supply",
    entry_points={
        'console_scripts': [
            'fastccd_psu_ioc=fastccd_psu_ioc.fastccd_psu_ioc:main'
        ],
    },
    extras_require={
        "docs": ["sphinx", "recommonmark", "sphinx_bootstrap_theme", ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    include_package_data=True,
    keywords='fastccd_psu_ioc',
    name='fastccd_psu_ioc',
    packages=find_packages(include=['fastccd_psu_ioc', 'fastccd_psu_ioc.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lbl-camera/fastccd_psu_ioc',
    version='0.1.0',
    zip_safe=False,
)
