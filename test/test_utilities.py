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
        self.assertEqual(n1.output, n2.input)
        self.assertEqual(n2.output, n3.input)

    def test_logger(self):
        mock_logger = MockLogger()

        logger = fluteline.Logger(mock_logger)
        logger.start()

        logger.input.put('hello')
        logger.input.put('world')

        expected = ['hello', 'world']

        for output in expected:
            self.assertEqual(logger.output.get(), output)

        logger.stop()

        self.assertEqual(mock_logger.received, expected)
