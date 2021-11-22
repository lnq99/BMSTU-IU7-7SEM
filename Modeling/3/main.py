import itertools
import math

from PyQt6 import QtWidgets
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout,
    QPushButton, QTableWidget, QLabel, QLineEdit, QSpinBox
)

from qt_table import TableItem
from rand import RandomGenerator, RandomCriteria

STYLE_BTN_PRIMARY = 'background-color:#388e3c'
BOLD = QFont()
BOLD.setBold(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lab 3 - Random number generator')
        self.resize(480, 503)

        self.table = QTableWidget()
        self.model = None

        self.init_main_widget()
        self.generator = RandomGenerator()

    def init_main_widget(self):
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        header = QHBoxLayout()
        table_box = QVBoxLayout()
        footer = QHBoxLayout()
        layout.addLayout(header)
        layout.addLayout(table_box, 1)
        layout.addLayout(footer)

        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(10, 2000000)
        self.n_spinbox.setValue(100)

        generate_btn = QPushButton('Генерировать')
        generate_btn.clicked.connect(self.generate)
        generate_btn.setStyleSheet(STYLE_BTN_PRIMARY)

        header.addWidget(self.n_spinbox)
        header.addWidget(generate_btn)

        table = self.table
        row_count = 14
        col_count = 8
        table.setRowCount(row_count)
        table.setColumnCount(col_count)
        for r in range(1, row_count):
            for c in range(1, col_count):
                table.setItem(r, c, TableItem())

        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.resizeColumnsToContents()

        table.setSpan(0, 1, 1, 3)
        table.setSpan(0, 4, 1, 3)
        table.setItem(0, 1, TableItem('Программный метод:'))
        table.setItem(0, 4, TableItem('Табличный метод:'))
        table.setItem(12, 0, TableItem('m:'))
        table.setItem(13, 0, TableItem('p:'))

        self.set_table(1, 1, ['1р', '2р', '3р', '1р', '2р', '3р', '?р'], False)

        header = table.horizontalHeader()
        for i in range(1, 8):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        table_box.addWidget(table, 2)

        self.seqence_input = QLineEdit(self)
        add_sequence_btn = QPushButton('Добавить')
        add_sequence_btn.clicked.connect(self.add_sequence)
        add_sequence_btn.setStyleSheet(STYLE_BTN_PRIMARY)
        footer.addWidget(QLabel('Послед. чисел'))
        footer.addWidget(self.seqence_input)
        footer.addWidget(add_sequence_btn)

        self.set_cell_highlight((0, 1), (0, 4))
        self.set_cell_highlight(*itertools.product([1], range(1, 8)))
        self.set_cell_highlight(*itertools.product([12, 13], range(8)))

    def set_table(self, row, col, arr, vertical=True):
        for val in arr:
            self.table.item(row, col).setText(str(val))
            if vertical:
                row += 1
            else:
                col += 1

    def set_cell_highlight(self, *args):
        for row, col in args:
            item = self.table.item(row, col)
            item.setBackground(QColor(220, 250, 220, 100))
            item.setFont(BOLD)

    def generate(self):
        n = self.n_spinbox.value()
        for i in (1, 2, 3):
            l1 = self.generator.rand(RandomGenerator.Method.LinearCongruential, i, n)
            l2 = self.generator.rand(RandomGenerator.Method.Table, i, n)
            p1 = round(RandomCriteria.p_of_chi_square_test(l1, i), 3)
            p2 = round(RandomCriteria.p_of_chi_square_test(l2, i), 3)
            mean1 = round(sum(l1) / len(l1), 2)
            mean2 = round(sum(l2) / len(l2), 2)
            self.set_table(2, i, l1[:10] + [mean1, p1])
            self.set_table(2, i + 3, l2[:10] + [mean2, p2])

    def add_sequence(self):
        seq = self.seqence_input.text().strip().split()
        try:
            seq = [int(i) for i in seq]
        except ValueError:
            return

        i = math.floor(math.log10(max(seq))) + 1
        p = round(RandomCriteria.p_of_chi_square_test(seq, i), 3)
        n = len(seq)
        mean = round(sum(seq) / n, 3)
        pad = ['' for _ in range(n, 10)]
        self.set_table(2, 7, seq[:10] + pad)
        self.set_table(12, 7, [mean, p])


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

# https://www.rand.org/pubs/monograph_reports/MR1418.html
