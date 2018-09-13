import fluteline


class Producer(fluteline.Producer):
    def produce(self):
        self.output.put(1)


class Consumer(fluteline.Consumer):
    def consume(self, item):
        self.output.put(item * 2)


class SynchronousConsumer(fluteline.SynchronousConsumer):
    def __init__(self):
        super(SynchronousConsumer, self).__init__()
        self.resource = None

    def enter(self):
        self.resource = 'my resource'

    def exit(self):
        self.resource = None

    def consume(self, item):
        self.output.put(item * 2)
