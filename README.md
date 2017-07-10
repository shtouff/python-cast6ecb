[![Build Status](https://www.travis-ci.org/shtouff/python-cast6ecb.svg?branch=master)](https://www.travis-ci.org/shtouff/python-cast6ecb)

# Purpose
This extension is aimed at helping people who still needs a binding to libmcrypt because they need to use CAST-256 (CAST6) algorithm, in ECB mode.

As far as I know (I may be wrong at this point, feel free to correct me if it's the case), none of the other python crypto libs (either semi-native like pycrypto or Cpython like openssl) still implement this algorithm. Even libsodium, which was chosen by the PHP community as a replacement for mcrypt in php72, does not implement it.

Since I needed to decrypt some specific things that were encrypted with this algo, using python3, I created this extension to achieve that very specific goal. It is focused on CAST-256-ECB because that was my need, and I hope this will be very temporary. 

I strongly advise people to upgrade both the algorithm they use (CAST-256 to AES for example) and the underlying library too (libmcrypt to openssl or libsodium).

# Build the extension

## Build locally
```
$ python3 setup.py build
```

Run the tests:
```
$ python3 setup.py test
```

## Push to pypi

First, check your $HOME/.pypirc:

```
[pypi]
username = <username>
password = <password>
```
I had trouble with quoted user/password and password containing a '%'.

Then, run:
```
$ python3 setup.py sdist bdist_wheel upload
```
