import time
import unittest

from fluteline import _TerminationMessage
from .basic_nodes import Producer, Consumer


class TestProducer(unittest.TestCase):

    def setUp(self):
        self.producer = Producer()
        self.producer.start()

    def tearDown(self):
        self.producer.stop()

    def test_producer(self):
        item = self.producer._output.get()
        self.assertEqual(item, 1)

    def test_cascade_reaches_the_output(self):
        self.producer.stop(cascade=True)
        start = time.time()
        while time.time() - start < 1:  # 1 second timeout
            item = self.producer._output.get()
            if isinstance(item, _TerminationMessage):
                self.assertTrue(item.cascade)
                break
        else:
            raise AssertionError('No termination message in output')


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.producer = Producer()
        self.consumer = Consumer()
        self.producer.connect(self.consumer)
        self.producer.start()
        self.consumer.start()

    def tearDown(self):
        self.producer.stop()
        self.consumer.stop()

    def test_pipeline(self):
        item = self.consumer._output.get()
        self.assertEqual(item, 2)


if __name__ == '__main__':
    unittest.main()
