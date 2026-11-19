import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "connectors" / "market-rule-mysql.json"


class ConnectorConfigTest(unittest.TestCase):
    def test_connector_json_exists_and_targets_market_rule(self):
        self.assertTrue(CFG.is_file(), f"missing {CFG}")
        data = json.loads(CFG.read_text())
        self.assertEqual(data["name"], "arfd-market-rule-mysql")
        cfg = data["config"]
        self.assertEqual(cfg["connector.class"], "io.debezium.connector.mysql.MySqlConnector")
        self.assertEqual(cfg["table.include.list"], "market_db.market_rule")
        self.assertEqual(cfg["topic.prefix"], "arfd")
        self.assertIn("database.hostname", cfg)
        self.assertIn("database.user", cfg)
        self.assertIn("database.server.id", cfg)


if __name__ == "__main__":
    unittest.main()
