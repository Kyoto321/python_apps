# Image editor app

# import modules
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QListWidget, QLabel,QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap

from PIL import Image, ImageFilter, ImageEnhance

#  main windows objects and settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Image Editor App")
main_window.resize(900, 700)


# create all app objects (instances)
btn_folder = QPushButton("folder")
file_list = QListWidget()
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpness")
gray = QPushButton("Brightness")
saturation = QPushButton("Saturation")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")


# dropdown box
filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Left")
filter_box.addItem("Right")
filter_box.addItem("Mirror")
filter_box.addItem("Sharpness")
filter_box.addItem("Brightness")
filter_box.addItem("Saturation")
filter_box.addItem("Contrast")
filter_box.addItem("Blur")

picture_box = QLabel("Image will appear here")


# app design
main_layout = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(file_list)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(gray)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)

col2.addWidget(picture_box)

main_layout.addLayout(col1,20)
main_layout.addLayout(col2,80)

main_window.setLayout(main_layout)


# app fuctionality
 
working_dir = ""

# filter files and extensions
def filter(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results
            

# choose correct working directory 
def getWorkingDir():
    global working_dir
    working_dir = QFileDialog.getExistingDirectory()
    extensions = ['.jpg', '.jpeg', '.webp', '.svg', 'png']
    filenames = filter(os.listdir(working_dir), extensions)
    file_list.clear()

    for filename in filenames:
        file_list.addItem(filename)


# edit image
class Editor():
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = "edits/"
        
    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_dir, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()
        
    def save_image(self):
        path = os.path.join(working_dir, self.save_folder)
        if not(os.path.isdir(path) or os.path.exists(path)):
            os.mkdir(path)
            
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
        
    def show_image(self, path):
        picture_box.hide()
        # load image
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w,h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()
        
    def gray(self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)
        
    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)
        
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)
        
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)
        
    def color(self):
        self.image = ImageEnhance.Color(self.image).enhance(1.2)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)
        
    def contrast(self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.2)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)
        
    def apply_filter(self, filter_name):
        if filter_name == "Original":
            self.image == self.original.copy()
        else:
            mapping = {
                "Left": lambda image : image.transpose(Image.ROTATE_90),
                "Right": lambda image : image.transpose(Image.ROTATE_270),
                "Mirror": lambda image : image.transpose(Image.FLIP_LEFT_RIGHT),
                "Sharpness": lambda image : image.filter(ImageFilter.SHARPEN),
                "Brightness": lambda image : image.convert("L"),
                "Saturation": lambda image : ImageEnhance.Color(image).enhance(1.2),
                "Contrast": lambda image : ImageEnhance.Contrast(image).enhance(1.2),
                "Blur": lambda image : image.filter(ImageFilter.BLUR)
            }
            filter_func = mapping.get(filter_name)
            if filter_func:
                self.image = filter_func(self.image)
                self.save_image()
                image_path = os.path.join(working_dir, self.save_folder, self.filename)
                self.show_image(image_path) 
            pass      
        
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)
 
        
main = Editor()       


def handle_filter():
    if file_list.currentRow() >= 0:
        select_filter = filter_box.currentText()
        main.appy_filter(select_filter)
   

def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text() 
        main.load_image(filename)
        main.show_image(os.path.join(working_dir, main.filename))
        

btn_folder.clicked.connect(getWorkingDir)
file_list.currentRowChanged.connect(displayImage)
filter_box.currentTextChanged.connect(handle_filter) #3:30

gray.clicked.connect(main.gray)
btn_left.clicked.connect(main.left)
btn_right.clicked.connect(main.right)
sharpness.clicked.connect(main.sharpen)
saturation.clicked.connect(main.color)
blur.clicked.connect(main.blur)
mirror.clicked.connect(main.mirror)


# show/exec app
main_window.show()
app.exec_()




