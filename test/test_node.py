import time
import unittest

import fluteline
from .basic_nodes import Producer, Consumer, SynchronousConsumer


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


class TestSynchronousConsumer(unittest.TestCase):

    def test_consume_item(self):
        sc = SynchronousConsumer()
        sc.output = fluteline.Queue()
        sc.put(1)
        self.assertEqual(sc.output.get(), 2)
        sc.stop()

    def test_enter_and_exit(self):
        sc = SynchronousConsumer()
        self.assertIsNone(sc.resource)
        sc.start()
        self.assertIsNotNone(sc.resource)
        sc.stop()
        self.assertIsNone(sc.resource)




if __name__ == '__main__':
    unittest.main()
