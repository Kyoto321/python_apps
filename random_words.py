# Ran dom words generator app with pyQt

# import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QPushButton, QVBoxLayout, QHBoxLayout

from random import choice

#  main windows objects and settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Random Word Generator")
main_window.resize(300, 200)


# create all app objects (instances)
title = QLabel("Random Keywords")

text1 = QLabel("?")
text2 = QLabel("?")
text3 = QLabel("?")

button1 = QPushButton("Click me")
button2 = QPushButton("Click me")
button3 = QPushButton("Click me")

words = ["apple", "banana", "mango", "orange", "potato"]


# create designs and layout
main_layout = QVBoxLayout()

row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

row1.addWidget(title, alignment=Qt.AlignCenter)

row2.addWidget(text1, alignment=Qt.AlignCenter)
row2.addWidget(text2, alignment=Qt.AlignCenter)
row2.addWidget(text3, alignment=Qt.AlignCenter)

row3.addWidget(button1)
row3.addWidget(button2)
row3.addWidget(button3)

main_layout.addLayout(row1)
main_layout.addLayout(row2)
main_layout.addLayout(row3)

main_window.setLayout(main_layout)


# functions
def random_word1():
    word = choice(words)
    text1.setText(word)

def random_word2():
    word = choice(words)
    text2.setText(word)
    
def random_word3():
    word = choice(words)
    text3.setText(word)
    

# events
button1.clicked.connect(random_word1)
button2.clicked.connect(random_word2)
button3.clicked.connect(random_word3)



# show/exec app
main_window.show()
app.exec_()