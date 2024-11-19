# Calculator app with pyQt

# import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel,QPushButton, QVBoxLayout, QHBoxLayout,QGridLayout
from PyQt5.QtGui import QFont

from random import choice
import sys

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # main windows objects and settings
        self.setWindowTitle("Calculator")
        self.resize(300, 200)


        # create all app objects (instances)
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("Helvetica", 32))
        
        self.grid = QGridLayout()

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", ".",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        # loop for creating buttons
        row = 0
        col = 0
        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.input_button)
            button.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding: 10px;}")
            self.grid.addWidget(button, row, col)
            col += 1
            
            if col > 3:
                col = 0
                row+= 1
                
        self.clear = QPushButton("clear")
        self.delete = QPushButton("<")
        self.clear.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding: 10px;}")
        self.delete.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding: 10px;}")
        # create designs and layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_box)
        main_layout.addLayout(self.grid)

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear)
        button_row.addWidget(self.delete)

        main_layout.addLayout(button_row)
        main_layout.setContentsMargins(25,25,25,25)

        self.setLayout(main_layout)

        self.clear.clicked.connect(self.input_button)
        self.delete.clicked.connect(self.input_button)


    #functionalty method
    def input_button(self):
        button = app.sender()
        text = button.text()
        
        if text == "=":
            symbol = self.text_box.text()
            try:
                res = eval(symbol)
                self.text_box.setText(str(res))
            except Exception as e:
                print("Errors:", e)
        
        elif text == "clear":
            self.text_box.clear()
            
        elif text == "<":
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
            
        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CalculatorApp()
    main_window.setStyleSheet("QWidget: { background-color:#f0f0f0 }")
    main_window.show()
    sys.exit(app.exec_())