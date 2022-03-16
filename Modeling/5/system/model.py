from __future__ import annotations

from numpy.random import default_rng


class IGenerator:
    generator = default_rng()

    def generate(self) -> float:
        raise NotImplementedError


class Task:
    def __init__(self, task_id):
        self.task_id = task_id
        self.log = []

    def add_log(self, node_name, time, event):
        self.log.append([node_name, time, event])

    def __str__(self):
        res = f'Task {self.task_id}:\t'
        for e in self.log:
            res += f't={e[1]:.2f}\t{e[0]}, {e[2]}\n\t\t\t'
        return res


class Node:
    timer = 0

    def __init__(self, next_node: Node = None, fail_node: Node = None, name: str = ''):
        self.next_node = next_node
        self.fail_node = fail_node
        self.n_succeed = 0
        self.n_failed = 0
        self.name = name

    def handle(self, task: Task):
        raise NotImplementedError

    def elapse(self, time):
        pass

    def next(self, task: Task):
        if self.next_node: self.next_node.handle(task)
        self.n_succeed += 1

    def fail(self, task: Task):
        task.add_log(self.name, self.timer, 'rejected')
        if self.fail_node: self.fail_node.handle(task)
        self.n_failed += 1

    def __str__(self):
        res = f'{self.name:11}:\tобработал {self.n_succeed:3d} запросов'
        if self.n_failed:
            res += f',\tотклонил {self.n_failed:3d} запросов'
        return res


class Endpoint(Node):
    def __init__(self, name=''):
        super().__init__()
        self.name = name
        self.count = 0

    def handle(self, task):
        if task.task_id % 100 == 0:
            task.add_log(self.name, Node.timer, '')
            print(task)
        self.count += 1


class GNode(Node):
    """
    Node whose processing time depends on generator
    """
    EPS = 10e-4

    def __init__(self, generator: IGenerator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._generator = generator
        self._remaining_time = 0
        self._is_ready = True

    def start_process(self):
        r = -1
        while r <= 0:
            r = self._generator.generate()
        self._remaining_time = r
        self._is_ready = False

    def is_ready(self) -> bool:
        return self._is_ready


def simulate(nodes: [Node], func_end_condition, dt=10e-2):
    Node.timer = 0
    while not func_end_condition():
        for node in nodes:
            node.elapse(dt)
        Node.timer += dt
