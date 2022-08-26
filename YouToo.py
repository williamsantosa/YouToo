import pytube as pt, sys
import logging
from pytube import YouTube
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

class YouToo(QMainWindow):
  def __init__(self):
    super().__init__()

    self.yt_link = ""

    self.setWindowTitle("YouToo")
    self.setFixedSize(400, 300)

    self.grid = QGridLayout()

    button_download = QPushButton(text = "Download!")
    button_download.clicked.connect(self.on_button_download)
    
    self.setCentralWidget(button)

  def on_button_download(self):
    logging.info("on_button_download pressed")

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

  app = QApplication([])
  
  window = YouToo()
  window.show()

  app.exec()