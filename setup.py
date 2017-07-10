#!/usr/bin/env python3
from setuptools import setup, Extension

VERSION = "0.2.1"

setup(
    name="cast6ecb",
    version=VERSION,
    description="Python3 interface to mcrypt library, only for CAST-256 (CAST6) algorithm, with ECB mode.",
    author="Remi Paulmier",
    author_email="pypi-ops@blablacar.com",
    license="LGPL",
    url="https://github.com/shtouff/python-cast6ecb",
    long_description= \
        """
        Partial python3 interface to mcrypt library. This can be used only for CAST-256 (CAST6) algorithm, with ECB mode.
        """,
    ext_modules=[
        Extension(
            "cast6ecb",
            ["cast6ecb.c"],
            libraries=["mcrypt"],
            define_macros=[("VERSION", '"%s"' % VERSION)]
        )
    ],
    classifiers=['Topic :: Security :: Cryptography'],
)
