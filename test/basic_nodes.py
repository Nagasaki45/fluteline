import fluteline


class Producer(fluteline.Producer):
    def produce(self):
        self.put(1)


class Consumer(fluteline.Consumer):
    def consume(self, item):
        self.put(item * 2)

