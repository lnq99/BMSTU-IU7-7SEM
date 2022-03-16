from .generator import RequestGenerator
from .queue import Queue
from .service import Service


LOG_FREQ = 5


class Model:
    def __init__(self, generator: RequestGenerator, queue: Queue, service: Service):
        self._generator = generator
        self._queue = queue
        self._service = service

    def time_based(self, n_tasks, dt=10e-3):
        generator, queue, service = self._generator, self._queue, self._service
        t_current = 0
        n_tasks_for_logging = n_tasks // LOG_FREQ

        while generator.generated_tasks < n_tasks \
                or not queue.is_empty or not service.is_ready:
            generator.elapse(dt)
            _, return_task = service.elapse(dt)

            if return_task:
                queue.enqueue(return_task)

            if generator.is_ready:
                task = generator.pop()
                queue.enqueue(task)

            if service.is_ready and not queue.is_empty:
                if service.completed_tasks % n_tasks_for_logging == 0:
                    print(f'Processed {service.completed_tasks:3d} tasks, t = {t_current:.4f}')
                task = queue.dequeue()
                service.process(task)

            t_current += dt

        return t_current, service.completed_tasks, queue.len_max

    def event_based(self, n_tasks):
        """
        events: task_generated, task_completed
        """
        generator, queue, service = self._generator, self._queue, self._service
        t_current = 0
        n_tasks_for_logging = n_tasks // LOG_FREQ
        dt = 0

        while generator.generated_tasks < n_tasks \
                or not queue.is_empty or not service.is_ready:
            t_current += dt
            t_remain_task_generated = generator.elapse(dt)
            t_remain_task_completed, return_task = service.elapse(dt)

            if return_task:
                queue.enqueue(return_task)

            if generator.is_ready:
                task = generator.pop()
                queue.enqueue(task)

            if service.is_ready and not queue.is_empty:
                if service.completed_tasks % n_tasks_for_logging == 0:
                    print(f'Processed {service.completed_tasks:4d} tasks, t = {t_current:.4f}')

                task = queue.dequeue()
                t_remain_task_completed = service.process(task)

            t_list = [t_remain_task_generated, t_remain_task_completed]
            t_list = list(filter(lambda x: x > 0, t_list))
            dt = min(t_list) if t_list else 0

        return t_current, service.completed_tasks, queue.len_max
