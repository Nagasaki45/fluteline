import unittest

import fluteline
from .basic_nodes import Producer, Consumer


class MockLogger():
    def __init__(self):
        self.received = []

    def info(self, message):
        self.received.append(message)


class TestUtilities(unittest.TestCase):

    def test_connect(self):
        n1 = Producer()
        n2 = Consumer()
        n3 = Consumer()
        nodes = [n1, n2, n3]
        fluteline.connect(nodes)
        self.assertEqual(n1._output, n2._input)
        self.assertEqual(n2._output, n3._input)

    def test_logger(self):
        mock_logger = MockLogger()

        logger = fluteline.Logger(mock_logger)
        logger.start()

        logger._input.put('hello')
        logger._input.put('world')

        expected = ['hello', 'world']

        for output in expected:
            self.assertEqual(logger._output.get(), output)

        logger.stop()

        self.assertEqual(mock_logger.received, expected)
