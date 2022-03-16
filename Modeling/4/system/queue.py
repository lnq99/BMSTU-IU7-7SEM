from collections import deque


class Queue:

    def __init__(self, maxlen=None):
        self._queue = deque(maxlen=maxlen)
        self._len_max = 0
        self._len = 0

    def enqueue(self, item):
        self._queue.append(item)
        self._len += 1
        if self._len > self._len_max:
            self._len_max = self._len

    def dequeue(self):
        if self._len > 0:
            self._len -= 1
            return self._queue.pop()
        else:
            return None

    @property
    def is_empty(self):
        return self._len <= 0

    @property
    def len_max(self):
        return self._len_max

    @property
    def len(self):
        return self._len
