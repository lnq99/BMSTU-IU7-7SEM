from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout,
    QPushButton, QTableView,
    QLabel, QSpinBox,
)

from graph import draw_graph, adjacency_matrix_to_edges
from table import NumpyModel
from markov import Markov


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lab 2 - Markov process')
        self.resize(820, 860)

        self.markov = Markov()
        self.n_state = QSpinBox()
        self.graph = QTableView()
        self.result = QTableView()
        self.model = None

        self.fig = plt.figure()
        self.axs = [plt.subplot(1, 3, (1, 2)), plt.subplot(2, 3, 3), plt.subplot(2, 3, 6)]

        self.init_main_widget()
        self.generate()
        self.solve()

    def init_main_widget(self):
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        input_box = QHBoxLayout()
        table_box = QHBoxLayout()
        graph_box = QVBoxLayout()
        layout.addLayout(input_box)
        layout.addLayout(table_box, 1)
        layout.addLayout(graph_box, 2)

        self.n_state.setValue(4)
        self.n_state.setRange(3, 10)

        generate_btn = QPushButton('Генерировать')
        generate_btn.clicked.connect(self.generate)
        generate_btn.setStyleSheet('background-color:#388e3c')
        solve_btn = QPushButton('Рассчитать')
        solve_btn.clicked.connect(self.solve)
        solve_btn.setStyleSheet('background-color:#388e3c')

        input_box.addWidget(QLabel('Количество состояний'))
        input_box.addWidget(self.n_state)
        input_box.addWidget(generate_btn)
        input_box.addWidget(solve_btn, 1, Qt.AlignmentFlag.AlignRight)

        table_box.addWidget(self.graph, 2)
        table_box.addWidget(self.result, 1)

        self.fig.set_tight_layout(True)
        plt.tight_layout()
        canvas = FigureCanvas(self.fig)
        toolbar = NavigationToolbar(canvas, self, coordinates=False)
        graph_box.addWidget(canvas)
        graph_box.addWidget(toolbar)

    def update_graph(self):
        self.axs[0].clear()
        draw_graph(adjacency_matrix_to_edges(self.markov.graph), self.axs[0])
        self.fig.canvas.flush_events()

    def generate(self):
        size = int(self.n_state.value())
        self.markov.gen_state_graph(size)
        self.model = NumpyModel(self.markov.graph)
        self.model.dataChanged.connect(self.update_graph)
        self.graph.setModel(self.model)
        self.graph.resizeColumnsToContents()

        self.update_graph()

    def solve(self):
        for axs in self.axs[1:]:
            axs.clear()
        self.markov.solve(self.axs[1:])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.result.setModel(NumpyModel(self.markov.result, ['p', 't (p0=1)', 't (pi=1/n)']))
        self.result.resizeColumnsToContents()
        header = self.result.horizontalHeader()
        for i in (0, 1, 2):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
