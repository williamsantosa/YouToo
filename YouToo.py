import pytube as pt, sys
import logging
from pytube import YouTube
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton

class YouToo(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("YouToo")
    self.setFixedSize(QSize(400, 300))

    button = QPushButton(text = "Download!")
    button.clicked.connect(self.on_button_download)

    self.setCentralWidget(button)
    
  def on_button_download(self):
    logging.info("on_button_download pressed")

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
  yt = YouTube('https://www.youtube.com/watch?v=8V4bPy4w3Hc&ab_channel=Avatar%3ATheLastAirbender')
  
  app = QApplication([])
  
  window = YouToo()
  window.show()

  app.exec()