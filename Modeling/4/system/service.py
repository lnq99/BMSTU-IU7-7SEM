from .generator import IGenerator
from random import random


class Service:

    def __init__(self, generator: IGenerator, return_factor: float):
        self._generator = generator
        self._return_factor = return_factor
        self._remaining_time = 0
        self._completed_tasks = 0
        self._is_ready = True
        self._cur_task = 0
        self.count = 0

    def process(self, task):
        self._cur_task = task
        r = -1
        while r <= 0:
            r = self._generator.generate()
        self.count += r
        self._remaining_time = r
        self._is_ready = False
        return r

    def elapse(self, time):
        self._remaining_time -= time
        if self._remaining_time <= 10e-5 and not self._is_ready:
            # print(time)
            return self._remaining_time, self.done()
        return self._remaining_time, None

    def done(self):
        self._completed_tasks += 1
        self._is_ready = True
        if random() < self._return_factor:
            return self._cur_task  # re-enqueue

    @property
    def is_ready(self):
        return self._is_ready

    @property
    def completed_tasks(self) -> int:
        return self._completed_tasks
