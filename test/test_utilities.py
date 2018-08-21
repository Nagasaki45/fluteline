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
        self.assertEqual(n1._output, n2._input)
        self.assertEqual(n2._output, n3._input)
