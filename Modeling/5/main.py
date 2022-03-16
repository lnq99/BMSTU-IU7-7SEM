if __name__ == '__main__':
    from system.generator import *
    from system.model import Endpoint, simulate
    from system.service import Service, QueueService

    success = Endpoint('Succeed')
    fail = Endpoint('Failed')

    comp1 = QueueService(Const(15), success, name='Компьютер 1')
    comp2 = QueueService(Const(30), success, name='Компьютер 2')

    op3 = Service(Uniform(20, 60), comp2, fail, 'Оператор 3')
    op2 = Service(Uniform(30, 50), comp1, op3, 'Оператор 2')
    op1 = Service(Uniform(15, 25), comp1, op2, 'Оператор 1')

    n_tasks = 300
    requests = RequestGenerator(Uniform(8, 12), n_tasks, op1, name='Генератор')

    nodes = [requests, op1, op2, op3, comp1, comp2]
    end_condition = lambda: success.count + fail.count == n_tasks
    simulate(nodes, end_condition)

    for node in nodes:
        print(node)
    print('\nЧисло обслуженных клиентов:', success.count)
    print('Число клиентов получивших отказ:', fail.count)
    print(f'Вероятность отказа: {fail.count / n_tasks:.4f}')
