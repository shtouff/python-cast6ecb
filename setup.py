#!/usr/bin/env python3
from setuptools import setup, Extension
from subprocess import Popen, PIPE

VERSION = "0.3.1"


def one_liner_as_list(cmd_line):
    """
    this runs a cmd like the old `` fashion and return the 1st line of output as a list of words.
    """
    return Popen(cmd_line.split(), stdout=PIPE).communicate()[0].decode().strip().split(" ")

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
            define_macros=[("VERSION", '"%s"' % VERSION)],
            extra_compile_args=one_liner_as_list("libmcrypt-config --cflags"),
            extra_link_args=one_liner_as_list("libmcrypt-config --libs"),
        )
    ],
    classifiers=['Topic :: Security :: Cryptography'],
)
