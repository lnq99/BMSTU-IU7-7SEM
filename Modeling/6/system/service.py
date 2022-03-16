from .generator import IGenerator
from .model import GNode
from .queue import Queue


class Service(GNode):
    def __init__(self, generator: IGenerator, *args, **kwargs):
        super().__init__(generator, *args, **kwargs)
        self._cur_task = None

    def handle(self, task):
        if self._is_ready:
            task.add_log(self.name, self.timer, 'принят')
            self._cur_task = task
            self.start_process()
        else:
            self.fail(task)

    def elapse(self, time):
        if not self._is_ready:
            self._remaining_time -= time
            if self._remaining_time <= self.EPS:
                self.next(self._cur_task)
                self._is_ready = True


class QueueService(Service):
    def __init__(self, generator: IGenerator, queue: Queue, *args, **kwargs):
        super().__init__(generator, *args, **kwargs)
        self.queue = queue

    def handle(self, task):
        pass
        # self.queue.enqueue(task)

    def elapse(self, time):
        super().elapse(time)
        if self._is_ready:
            if not self.queue.is_empty:
                task = self.queue.dequeue()
                task.add_log(self.name, self.timer, 'принят')
                self._cur_task = task
                self.start_process()
