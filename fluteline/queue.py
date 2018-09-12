try:
    import queue  # python 3
except ImportError:
    import Queue as queue


class Queue(object):
    '''
    Thread-safe input and output queue from nodes.
    '''
    def __init__(self):
        self._queue = queue.Queue()

    def empty(self):
        '''
        Return ``True`` if the queue is empty, ``False`` otherwise
        (not reliable!).
        '''
        return self._queue.empty()

    def put(self, item):
        '''
        Put an item into the queue.
        '''
        return self._queue.put(item)

    def get(self):
        '''
        Remove and return an item from the queue.
        '''
        return self._queue.get()
