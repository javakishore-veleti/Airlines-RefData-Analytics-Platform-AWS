from __future__ import annotations
import unittest
from app.dao.user_dao import _hash_password, verify_password

class TestHash(unittest.TestCase):
    def test_roundtrip(self):
        salt, digest = _hash_password("secret")
        self.assertTrue(verify_password("secret", salt, digest))
        self.assertFalse(verify_password("nope", salt, digest))

if __name__ == "__main__":
    unittest.main()
