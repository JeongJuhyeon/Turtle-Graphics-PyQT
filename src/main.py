import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout, QVBoxLayout, QColorDialog
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
        self.pen_down = False
        self.cur_color = Qt.black
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
        self.paint_current_square()

        # Grid layout
        grid = QGridLayout()

        grid.setColumnMinimumWidth(0, 25)
        for i in range(1, 10):
            grid.setColumnMinimumWidth(i, 40)
        for j in range(3):
            grid.setRowMinimumHeight(j, 40)


        # Coord label
        self.coord_label = QLabel(self)
        self.coord_label.setGeometry(230, 20, 60, 20)
        self.coord_label.setText("(0, 0)")

        # Pen status label
        self.pen_status_label = QLabel(self)
        self.pen_status_label.setText("Status: Up")
        self.pen_status_label.setMaximumSize(100, 20)
        grid.addWidget(self.pen_status_label, 2, 1, 1, 3)

        # Buttons
        self.button_pen = QPushButton("Pen")
        self.button_pen.setFixedSize(60, 40)
        self.button_pen.clicked.connect(self.on_pen)
        grid.addWidget(self.button_pen, 1, 1, 1, 3)


        self.button_left = QPushButton("<-")
        self.button_left.setFixedSize(40, 40)
        self.button_left.clicked.connect(self.on_left)
        self.button_left.setEnabled(False)
        grid.addWidget(self.button_left, 1, 4, 1, 1)

        self.button_up = QPushButton("^")
        self.button_up.setFixedSize(40, 40)
        self.button_up.clicked.connect(self.on_up)
        self.button_up.setEnabled(False)
        grid.addWidget(self.button_up, 0, 5, 1, 1)

        self.button_down = QPushButton("v")
        self.button_down.setFixedSize(40, 40)
        self.button_down.clicked.connect(self.on_down)
        grid.addWidget(self.button_down, 2, 5, 1, 1)

        self.button_right = QPushButton("->")
        self.button_right.setFixedSize(40, 40)
        self.button_right.clicked.connect(self.on_right)
        grid.addWidget(self.button_right, 1, 6, 1, 1)

        self.button_color = QPushButton("Color")
        self.button_color.setFixedSize(70, 40)
        self.button_color.clicked.connect(self.on_color)
        grid.addWidget(self.button_color, 1, 8, 1, 2)

        self.button_color = QPushButton("Eraser")
        self.button_color.setFixedSize(70, 40)
        self.button_color.clicked.connect(self.on_eraser)
        grid.addWidget(self.button_color, 2, 8, 1, 2)

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
        pixmap = self.labels[self.x + self.y * 20].pixmap()
        if self.pen_down:
            pixmap.fill(self.cur_color)

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

    def on_eraser(self):
        self.cur_color = QColor("transparent")

    def on_color(self):
        self.cur_color = QColorDialog.getColor(Qt.black, self, "Choose color")

    def on_pen(self):
        self.pen_down = not self.pen_down
        self.pen_status_label.setText("Status: Down") if self.pen_down else self.pen_status_label.setText("Status: Up")

    def on_left(self):
        self.button_right.setEnabled(True)

        self.un_red_previous_square()
        self.x -= 1
        self.paint_current_square()
        self.update_coord_label()
        if self.x == 0:
            self.button_left.setDisabled(True)

    def on_up(self):
        self.button_down.setEnabled(True)

        self.un_red_previous_square()
        self.y -= 1
        self.paint_current_square()
        self.update_coord_label()
        if self.y == 0:
            self.button_up.setDisabled(True)

    def on_down(self):
        self.button_up.setEnabled(True)

        self.un_red_previous_square()
        self.y += 1
        self.paint_current_square()
        self.update_coord_label()
        if self.y == 19:
            self.button_down.setDisabled(True)

    def on_right(self):
        self.button_left.setEnabled(True)

        self.un_red_previous_square()
        self.x += 1
        self.paint_current_square()
        self.update_coord_label()
        if self.x == 19:
            self.button_right.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TurtlePainter()
    sys.exit(app.exec_())
