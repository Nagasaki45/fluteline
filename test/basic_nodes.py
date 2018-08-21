import fluteline


class Producer(fluteline.Node):
    def generate(self):
        self.put(1)


class Consumer(fluteline.Node):
    def consume(self, item):
        self.put(item * 2)

