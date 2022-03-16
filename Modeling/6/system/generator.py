from .model import IGenerator, Task, GNode


class Const(IGenerator):
    def __init__(self, c):
        self.c = c

    def generate(self):
        return self.c


class Uniform(IGenerator):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def generate(self):
        return self.generator.uniform(self.low, self.high)


class Normal(IGenerator):
    def __init__(self, loc, scale):
        self.loc = loc
        self.scale = scale

    def generate(self):
        return self.generator.normal(self.loc, self.scale)


class RequestGenerator(GNode):
    _task_id = 0

    def __init__(self, generator: IGenerator, max_tasks: int, *args, **kwargs):
        super().__init__(generator, *args, **kwargs)
        self.max_tasks = max_tasks

    def handle(self, task):
        pass

    def elapse(self, time):
        if self.n_succeed < self.max_tasks:
            self._remaining_time -= time
            if self._remaining_time <= self.EPS:
                RequestGenerator._task_id += 1
                task = Task(self._task_id)
                task.add_log(self.name, self.timer, 'сгенерирован')
                self.next(task)
                self._is_ready = True
            if self._is_ready and self.n_succeed < self.max_tasks:
                self.start_process()
