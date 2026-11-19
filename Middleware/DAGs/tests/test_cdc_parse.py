import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.cdc_parse import map_debezium_op


class CdcParseTest(unittest.TestCase):
    def test_create(self):
        op = map_debezium_op({"op": "c", "after": {"rule_id": 1, "name": "a"}, "before": None})
        self.assertEqual(op.op, "insert")
        self.assertEqual(op.rule_id, 1)

    def test_update(self):
        op = map_debezium_op({"op": "u", "after": {"rule_id": 2, "weight": 9}, "before": {"rule_id": 2}})
        self.assertEqual(op.op, "update")

    def test_delete(self):
        op = map_debezium_op({"op": "d", "before": {"rule_id": 3}, "after": None})
        self.assertEqual(op.op, "delete")
        self.assertIsNone(op.row)

    def test_snapshot_read(self):
        op = map_debezium_op({"op": "r", "after": {"rule_id": 4, "name": "snap"}})
        self.assertEqual(op.op, "insert")


if __name__ == "__main__":
    unittest.main()
