from __future__ import annotations
import unittest
from unittest.mock import MagicMock
from app.common.dtos.usecase import AuthCtx, AuthReq, AuthResp
from app.dao.session_dao import MemorySessionDao
from app.dao.user_dao import _hash_password
from app.facade.auth.impl import AuthFacadeImpl
from app.wf.WFAuth.impl import WFAuthImpl

class TestAuth(unittest.TestCase):
    def test_signin(self):
        salt, digest = _hash_password("pw")
        users = MagicMock()
        users.get_by_username.return_value = {
            "username": "u", "password_salt": salt, "password_hash": digest, "role": "operator"
        }
        facade = AuthFacadeImpl(wf=WFAuthImpl(user_dao=users, session_dao=MemorySessionDao()))
        out = facade.signin(AuthCtx(req=AuthReq(username="u", password="pw"), resp=AuthResp()))
        self.assertTrue(out.resp.ok)
        self.assertTrue(out.resp.token)

if __name__ == "__main__":
    unittest.main()
