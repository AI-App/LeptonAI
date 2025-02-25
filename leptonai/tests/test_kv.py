import random
import string

from loguru import logger

from leptonai.api import workspace as workspace_api
from leptonai.kv import KV
import unittest


def random_name():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(8))


@unittest.skipIf(
    workspace_api.WorkspaceInfoLocalRecord.get_current_workspace_id() is None,
    "No login info. Skipping test.",
)
class TestKV(unittest.TestCase):
    def setUp(self):
        self.prefix = "testws-" + random_name()
        logger.debug(f"Setting up test with namespace name {self.prefix}")
        self.kv_instance = KV(self.prefix, create_if_not_exists=True)
        logger.debug("Namespace created")

    def tearDown(self):
        logger.debug(f"Tearing down test with namespace name {self.prefix}")
        KV.delete_kv(self.kv_instance)
        logger.debug("Namespace deleted")

    def test_create_delete_kv(self):
        logger.debug("Testing create/delete")
        logger.debug("Testing create/delete with existing namespace")
        with self.assertRaises(ValueError):
            _ = KV(self.prefix, create_if_not_exists=False, error_if_exists=True)
        logger.debug("Testing create/delete with non-existing namespace")
        with self.assertRaises(ValueError):
            _ = KV(self.prefix + "2", create_if_not_exists=False, error_if_exists=False)

    def test_put_get_kv(self):
        logger.debug("Testing put/get")
        key = self.prefix + "-key"
        value = (self.prefix + "-value").encode("utf-8")
        logger.debug("Testing get with non-existing key")
        with self.assertRaises(KeyError):
            self.kv_instance.get(key)
        logger.debug("Testing put")
        self.kv_instance.put(key, value)
        logger.debug("Testing get")
        self.assertEqual(self.kv_instance.get(key), value)
        logger.debug("Testing delete")
        self.kv_instance.delete(key)
        logger.debug("Testing get with deleted key")
        with self.assertRaises(KeyError):
            self.kv_instance.get(key)


if __name__ == "__main__":
    unittest.main()
