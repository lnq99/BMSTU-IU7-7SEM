if __name__ == '__main__':
    from system.generator import *
    from system.model import Endpoint, simulate
    from system.service import Service, QueueService
    from system.queue import Queue

    success = Endpoint('обработан')
    failure = Endpoint('отклонен')

    q1 = Queue()
    q2 = Queue()
    q3 = Queue()

    comp1 = QueueService(Normal(20, 4), q1, success, name='Компьютер 1')
    comp2 = QueueService(Normal(30, 5), q1, success, name='Компьютер 2')
    comp3 = QueueService(Normal(20, 4), q2, success, name='Компьютер 3')
    comp4 = QueueService(Normal(30, 5), q3, success, name='Компьютер 4')

    op3 = Service(Uniform(15, 30), q3, failure, 'Оператор3 (v1)')
    op2 = Service(Uniform(20, 25), q2, op3, 'Оператор2 (v1)')
    op1 = Service(Uniform(10, 20), q1, op2, 'Оператор1 (v2)')

    n_tasks = 500
    anyApiRequests = RequestGenerator(Uniform(10, 15), n_tasks, op1, name='Генератор 1')
    oldApiRequests = RequestGenerator(Uniform(10, 18), n_tasks, op2, name='Генератор 2')

    nodes = [anyApiRequests, oldApiRequests, op1, op2, op3, comp1, comp2, comp3, comp4]
    end_condition = lambda: success.count + failure.count == n_tasks
    simulate(nodes, end_condition)

    for node in nodes:
        print(node)
    print('\nЧисло обслуженных клиентов:', success.count)
    print('Число клиентов получивших отказ:', failure.count)
    print(f'Вероятность отказа: {failure.count / n_tasks:.4f}')
