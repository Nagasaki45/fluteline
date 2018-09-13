import unittest

import fluteline
from .basic_nodes import Producer, Consumer


class TestUtilities(unittest.TestCase):

    def test_connect(self):
        n1 = Producer()
        n2 = Consumer()
        n3 = Consumer()
        nodes = [n1, n2, n3]
        fluteline.connect(nodes)
        self.assertEqual(n1.output, n2)
        self.assertEqual(n2.output, n3)
        self.assertIsInstance(n3.output, fluteline.Queue)
