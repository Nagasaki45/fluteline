import fluteline


class DeepThought(fluteline.Consumer):
    def consume(self, item):
        self.put(42)


deep_thought = DeepThought()
deep_thought.start()

# Put something in the input queue
deep_thought.input.put(
    'The Answer to the Ultimate Question of Life, The Universe, and Everything.'
)

# Get the output from the output queue
answer = deep_thought.output.get()

print('The answer is {}'.format(answer))

deep_thought.stop()
