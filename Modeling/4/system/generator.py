from numpy.random import default_rng


class IGenerator:
    generator = default_rng()

    def generate(self) -> float:
        raise NotImplementedError


class UniformGenerator(IGenerator):
    def __init__(self, low, high):
        if low > high: low, high = high, low
        self.low = low
        self.high = high

    def generate(self):
        return self.generator.uniform(self.low, self.high)


class NormalGenerator(IGenerator):
    def __init__(self, loc, scale):
        self.loc = loc
        self.scale = scale

    def generate(self):
        return self.generator.normal(self.loc, self.scale)


class RequestGenerator:
    def __init__(self, generator: IGenerator, n_task: int):
        self._generator = generator
        self._remaining_time = 0
        self._is_ready = False
        self._generated_tasks = 0
        self._n_task = n_task

    def generate(self):
        r = -1
        while r <= 0:
            r = self._generator.generate()
        self._remaining_time = r
        self._is_ready = True
        self._generated_tasks += 1
        return self._remaining_time

    def elapse(self, time):
        if not self._is_ready:
            if self._generated_tasks == self._n_task:
                return 0
            r = self._remaining_time - time
            if r <= 10e-4:
                r = self.generate() - r  # suppose >0
            self._remaining_time = r
            return self._remaining_time

    def pop(self):
        if self._is_ready:
            self._is_ready = False
            return self._generated_tasks    # task id
        return None

    @property
    def is_ready(self):
        return self._is_ready

    @property
    def generated_tasks(self):
        return self._generated_tasks
