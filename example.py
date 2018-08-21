import random
import time

import fluteline


class RandomNumberGenerator(fluteline.Node):
    def generate(self):
        number = random.random()
        self.put(number)


class Max(fluteline.Node):
    def enter(self):
        self.max_ = None

    def consume(self, item):
        if self.max_ is None or item > self.max_:
            self.put(item)
            self.max_ = item


class Printer(fluteline.Node):
    def consume(self, item):
        print(item)


def main():
    nodes = [
        RandomNumberGenerator(),
        Max(),
        Printer(),
    ]
    fluteline.connect(nodes)
    fluteline.start(nodes)

    time.sleep(5)

    fluteline.stop(nodes)


if __name__ == '__main__':
    main()
