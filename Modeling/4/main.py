from system.model import Model
from system.generator import *
from system.queue import Queue
from system.service import Service

from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)
        self.init_ui()

    def init_ui(self):
        ui = self.ui
        ui.a.setValue(2)
        ui.b.setValue(8)
        ui.m.setValue(5)
        ui.sigma.setValue(1)
        ui.return_factor.setValue(0.1)
        ui.dt.setValue(10e-3)

        ui.n_tasks.setRange(5, 5000)
        ui.n_tasks.setValue(100)
        ui.run.setStyleSheet('background-color:#388e3c')

    @pyqtSlot(name='on_run_clicked')
    def on_run(self):
        ui = self.ui
        try:
            a = ui.a.value()
            b = ui.b.value()
            m = ui.m.value()
            sigma = ui.sigma.value()
            n_tasks = ui.n_tasks.value()
            return_factor = ui.return_factor.value()
            dt = ui.dt.value()

            g_uniform = UniformGenerator(a, b)
            g_normal = NormalGenerator(m, sigma)
            queue = Queue()

            print('Принцип Δt')
            generator = RequestGenerator(g_uniform, n_tasks)
            service = Service(g_normal, return_factor)
            model = Model(generator, queue, service)
            t, completed_tasks, queue_len_max = model.time_based(n_tasks, dt)
            self.show_result(self.ui.result_time, t, completed_tasks, completed_tasks-n_tasks, queue_len_max)

            print()

            print('Событийный принцип')
            generator = RequestGenerator(g_uniform, n_tasks)
            service = Service(g_normal, return_factor)
            model = Model(generator, queue, service)
            t, completed_tasks, queue_len_max = model.event_based(n_tasks)
            self.show_result(self.ui.result_event, t, completed_tasks, completed_tasks-n_tasks, queue_len_max)

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    @staticmethod
    def show_result(text_edit, t, completed_tasks, returned_tasks, queue_len_max):
        result_str = f'Обработанные заявки: {completed_tasks}\n\n'\
            f'Повторно обработанные заявки: {returned_tasks}\n\n'\
            f'Максимальная длина очереди: {queue_len_max}\n\n'\
            f'Время работы: {t:.2f}'

        text_edit.setPlainText(result_str)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
