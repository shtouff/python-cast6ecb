#!/usr/bin/env python3
import unittest
import random

# Add build directory to search path
import os
if os.path.exists("build"):
    from distutils.util import get_platform
    import sys
    s = "build/lib.%s-%.3s" % (get_platform(), sys.version)
    s = os.path.join(os.getcwd(), s)
    sys.path.insert(0, s)

from cast6ecb import encrypt, decrypt, block_size


def random_ascii(size):
    return ''.join([ chr(random.randint(32, 126)) for _ in range(size) ])


class Cast6EbcTestCase(unittest.TestCase):
    key = 'foo bar'.ljust(32, "\0")

    def test_encrypt(self):
        self.assertEqual(
            encrypt(self.key, 'baz qux'),
            b'\x4a\x95\x5c\xd5\x68\xe2\xd6\x78\x50\xfc\x26\xaf\xec\xb2\x7c\x47'
        )

    def test_encrypt_block_padded(self):
        self.assertEqual(
            encrypt(self.key, 'baz qux'.ljust(block_size(), "\0")),
            b'\x4a\x95\x5c\xd5\x68\xe2\xd6\x78\x50\xfc\x26\xaf\xec\xb2\x7c\x47'
        )

    def test_decrypt(self):
        self.assertEqual(
            str(decrypt(
                self.key,
                b'\x6d\xcc\x2d\xe2\xf0\x6b\xce\x27\x86\x0c\x92\x66\x20\xaa\x1f\x4f').decode('utf-8').rstrip('\0')
            ),
            'qux baz'
        )

    def test_decrypt_no_padded_when_plaintext_is_block_size_long(self):
        plaintext = random_ascii(block_size())
        secret = encrypt(self.key, plaintext)

        ret = decrypt(self.key, secret)
        self.assertEqual(
            ret.decode(),
            plaintext
        )

    def test_invalid_key_size(self):
        key = 'foobarfoobarfoobarfoobarfoobarfoo' # 33 chars long, max is 32 for CAST-256

        with self.assertRaises(ValueError):
            encrypt(key, 'barbaz')

    def test_invalid_encrypt_params(self):
        with self.assertRaises(TypeError):
            encrypt()
        with self.assertRaises(TypeError):
            encrypt('foobar')

    def test_invalid_decrypt_params(self):
        with self.assertRaises(TypeError):
            decrypt()
        with self.assertRaises(TypeError):
            decrypt('foobar')


if __name__ == "__main__":
    unittest.main()
