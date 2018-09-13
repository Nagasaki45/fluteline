import fluteline


class DeepThought(fluteline.Consumer):
    def consume(self, item):
        self.output.put(42)


deep_thought = DeepThought()
# We are talking low level here, so let's attach an output queue manually.
# It's easier to use fluteline.connect though. Check it out!
deep_thought.output = fluteline.Queue()
deep_thought.start()

# Put something in the input queue
deep_thought.input.put(
    'The Answer to the Ultimate Question of Life, The Universe, and Everything.'
)

# Get the output from the output queue
answer = deep_thought.output.get()

print('The answer is {}'.format(answer))

deep_thought.stop()
