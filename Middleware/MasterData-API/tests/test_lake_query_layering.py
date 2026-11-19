from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path

from app.common.dtos.usecase import LakeQueryCtx, LakeQueryReq, LakeQueryResp
from app.dao.lake_dao import JsonLakeDao
from app.facade.lake_query.impl import LakeQueryFacadeImpl
from app.wf.WFLakeQuery.impl import WFLakeQueryImpl


class TestLakeQuery(unittest.TestCase):
    def test_list_and_get(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "rule_id=7.json").write_text(json.dumps({"rule_id": 7, "name": "x"}))
            dao = JsonLakeDao(lake_root=root)
            facade = LakeQueryFacadeImpl(wf=WFLakeQueryImpl(dao=dao))
            out = facade.query(LakeQueryCtx(req=LakeQueryReq(limit=10), resp=LakeQueryResp()))
            self.assertEqual(out.resp.count, 1)
            one = facade.query(LakeQueryCtx(req=LakeQueryReq(rule_id=7), resp=LakeQueryResp()))
            self.assertEqual(one.resp.items[0]["rule_id"], 7)


if __name__ == "__main__":
    unittest.main()
