import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPixmap
from PyQt5.QtCore import Qt, QRect, QSize


class TurtlePainter(QWidget):

    def __init__(self):
        super(TurtlePainter, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 620)  # x, y, w, h
        self.setWindowTitle("Brushes")

        self.x = 0
        self.y = 0
        self.pen_down = True
        self.labels = []

        # Drawing all the squares. From (50, 50) to (450, 450)

        pixmap = QPixmap(20, 20)
        pixmap.fill(QColor("transparent"))
        for j in range(20):
            for i in range(20):
                painter = QPainter(pixmap)
                painter.drawRect(0, 0, 19, 19)
                painter.end()
                self.labels.append(QLabel(self))
                self.labels[-1].setPixmap(pixmap)
                self.labels[-1].setGeometry(50 + 20 * i, 50 + 20 * j, 20, 20)  # x, y, w, h

        # Grid layout
        grid = QGridLayout()

        grid.setColumnMinimumWidth(0, 25)
        for i in range(1, 10):
            grid.setColumnMinimumWidth(i, 40)
        for j in range(3):
            grid.setRowMinimumHeight(j, 40)

        self.coord_label = QLabel(self)
        self.coord_label.setGeometry(230, 20, 50, 20)
        self.coord_label.setText("(0, 0)")

        # Buttons
        self.button_pendown = QPushButton("Down")
        self.button_pendown.setFixedSize(60, 40)
        self.button_pendown.clicked.connect(self.on_pen)
        grid.addWidget(self.button_pendown, 1, 1, 1, 2)

        self.button_left = QPushButton("<-")
        self.button_left.setFixedSize(40, 40)
        self.button_left.clicked.connect(self.on_left)
        grid.addWidget(self.button_left, 1, 4, 1, 1)

        self.button_up = QPushButton("^")
        self.button_up.setFixedSize(40, 40)
        self.button_up.clicked.connect(self.on_up)
        grid.addWidget(self.button_up, 0, 5, 1, 1)

        self.button_down = QPushButton("v")
        self.button_down.setFixedSize(40, 40)
        self.button_down.clicked.connect(self.on_down)
        grid.addWidget(self.button_down, 2, 5, 1, 1)

        self.button_right = QPushButton("->")
        self.button_right.setFixedSize(40, 40)
        self.button_right.clicked.connect(self.on_right)
        grid.addWidget(self.button_right, 1, 6, 1, 1)

        self.button_penup = QPushButton("Up")
        self.button_penup.setFixedSize(70, 40)
        grid.addWidget(self.button_penup, 1, 8, 1, 2)

        # Vertical layout
        vert_layout = QVBoxLayout(self)

        hidden_label = QLabel()
        hidden_label.setGeometry(0, 0, 500, 100)
        vert_layout.addWidget(hidden_label)
        vert_layout.addLayout(grid)

        self.show()

    def update_coord_label(self):
        self.coord_label.setText("({}, {})".format(self.x, self.y))

    def paint_current_square(self):

        pixmap = QPixmap(20, 20)
        if self.pen_down:
            pixmap.fill(QColor("black"))

        painter = QPainter(pixmap)
        painter.setPen(Qt.red)
        painter.drawRect(0, 0, 19, 19)
        painter.end()

        self.labels[self.x + self.y * 20].setPixmap(pixmap)

    def un_red_previous_square(self):
        pixmap = self.labels[self.x + self.y * 20].pixmap()
        painter = QPainter(pixmap)
        painter.setPen(Qt.black)
        painter.drawRect(0, 0, 19, 19)
        painter.end()
        self.labels[self.x + self.y * 20].setPixmap(pixmap)

    def on_pen(self):
        self.pen_down = not self.pen_down

    def on_left(self):
        if self.x == 0:
            return

        self.un_red_previous_square()
        self.x -= 1
        self.paint_current_square()
        self.update_coord_label()

    def on_up(self):
        if self.y == 0:
            return

        self.un_red_previous_square()
        self.y -= 1
        self.paint_current_square()
        self.update_coord_label()

    def on_down(self):
        if self.y == 19:
            return

        self.un_red_previous_square()
        self.y += 1
        self.paint_current_square()
        self.update_coord_label()

    def on_right(self):
        if self.x == 19:
            return

        self.un_red_previous_square()
        self.x += 1
        self.paint_current_square()
        self.update_coord_label()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TurtlePainter()
    sys.exit(app.exec_())
