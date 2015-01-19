import unittest

from tools import check_composite_widget_struct
from nose_parameterized import parameterized

class TestTools(unittest.TestCase):

    def setUp(self):
        self.required = dict(
            rpc = dict(
                host = str,
                port = int,
                path = str
            ),
            target_path = str
        )

    @parameterized.expand([
        (
            "mismatch_root_node_type",
            42,
            False
        ),(
            "missing_node",
            dict(
                target_path = ''
            ),
            False
        ),(
            "mismatch_node_type",
            dict(
                rpc = 42,
                target_path = ''
            ),
            False
        ),(
            "mismatch_value_type",
            dict(
                rpc = dict(
                    host = 42,
                    port = 42,
                    path = ''
                ),
                target_path = ''
            ),
            False
        ),(
            "everything_is_awesome",
            dict(
                rpc = dict(
                    host = '',
                    port = 42,
                    path = ''
                ),
                target_path = ''
            ),
            True
        )
    ])
    def test_check_composite_widget_struct(self, name, value, expected):
        self.assertEqual(check_composite_widget_struct(value, self.required), expected)
