import fluteline


class Producer(fluteline.Producer):
    def produce(self):
        self.output.put(1)


class Consumer(fluteline.Consumer):
    def consume(self, item):
        self.output.put(item * 2)
