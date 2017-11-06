from os import path
from unittest import TestCase
import mock

from .. import api

TEST_DIR = path.dirname(__file__)


@mock.patch(api.__name__ + ".mkdir")
def test_mkdir_if_not_exist(m_mkdir):
    dir_path = path.join(TEST_DIR, "dummy")
    api.mkdir_if_not_exist(dir_path)
    m_mkdir.assert_called_with(dir_path)


@mock.patch(api.__name__ + ".HOME_DIR", TEST_DIR)
class DataReaderTest(TestCase):

    def test_cache_dir(self):
        reader = api.DataReader()
        expected = path.join(TEST_DIR, "stock-data")
        self.assertEqual(reader.cache_dir, expected)
