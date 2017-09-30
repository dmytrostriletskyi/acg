"""
Setup.
"""
from setuptools import find_packages, setup


setup(
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="API client generator.",
    entry_points={
        "console_scripts": [
            "acg = acg.acg:acg",
        ]
    },
    install_requires=[
        "PyYAML>=3.12",
    ],
    license="MIT",
    name="acg",
    packages=find_packages(),
    include_package_data=True,
    version="0.1.0",
)
