import os
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(900, 600)

workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def showFilenameList():
    chooseWorkdir()
    listd = os.listdir(workdir)
    extentio = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    result = filter(listd, extentio)
    file_spisok.clear()
    file_spisok.addItems(result)

class ImageProcessor():
    def __init__(self):
        self.filename = ''
        self.image = ''
        self.savedir = 'savepapka/'

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        big_photo_pole.hide()
        pixmapimage = QPixmap(path)
        w, h = big_photo_pole.width(), big_photo_pole.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        big_photo_pole.setPixmap(pixmapimage) 
        big_photo_pole.show()   

    def do_bw(self):
            self.image = self.image.convert('L')
            self.saveImage()
            image_path = os.path.join(workdir, self.savedir, self.filename)
            self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.savedir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_counter(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.UnsharpMask)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if file_spisok.currentRow() >= 0:
        filename = file_spisok.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)





big_photo_pole = QLabel('Картинка')
file_spisok = QListWidget()
file_button = QPushButton('Папка')
left_button = QPushButton('Лево')
right_button = QPushButton('Право')
counter_button = QPushButton('Зеркало')
blur_button = QPushButton('Блюр')
sharp_button = QPushButton('Резкость')
bw_button = QPushButton('Чёрно-белый')

smal_H_list = QHBoxLayout()
smal_V_list = QVBoxLayout()
big_H_list = QHBoxLayout()
big_V_list = QVBoxLayout()

smal_H_list.addWidget(left_button)
smal_H_list.addWidget(right_button)
smal_H_list.addWidget(counter_button)
smal_H_list.addWidget(blur_button)
smal_H_list.addWidget(sharp_button)
smal_H_list.addWidget(bw_button)
smal_V_list.addWidget(file_button)
smal_V_list.addWidget(file_spisok)
big_V_list.addWidget(big_photo_pole)
big_V_list.addLayout(smal_H_list)
big_H_list.addLayout(smal_V_list, 20)
big_H_list.addLayout(big_V_list, 80)
















file_spisok.currentRowChanged.connect(showChosenImage)
bw_button.clicked.connect(workimage.do_bw)
left_button.clicked.connect(workimage.do_left)
blur_button.clicked.connect(workimage.do_blur)
sharp_button.clicked.connect(workimage.do_sharp)
right_button.clicked.connect(workimage.do_right)
counter_button.clicked.connect(workimage.do_counter)
file_button.clicked.connect(showFilenameList)
main_win.setLayout(big_H_list)
main_win.show()
app.exec()