import time
import unittest

import fluteline
from .basic_nodes import Producer, Consumer


class TestProducer(unittest.TestCase):

    def setUp(self):
        self.producer = Producer()
        self.producer.output = fluteline.Queue()
        self.producer.start()

    def tearDown(self):
        self.producer.stop()

    def test_producer(self):
        item = self.producer.output.get()
        self.assertEqual(item, 1)


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.producer = Producer()
        self.consumer = Consumer()
        self.consumer.output = fluteline.Queue()
        self.producer.output = self.consumer
        self.producer.start()
        self.consumer.start()

    def tearDown(self):
        self.producer.stop()
        self.consumer.stop()

    def test_pipeline(self):
        item = self.consumer.output.get()
        self.assertEqual(item, 2)


if __name__ == '__main__':
    unittest.main()
