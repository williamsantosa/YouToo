import pytube as pt, sys
import logging
from pytube import YouTube
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

class YouToo(QMainWindow):
  def __init__(self):
    super().__init__()

    self.init_ui()
    
  def init_ui(self):
    # YouTube Link
    self.yt_link = ""

    # Create Window
    self.setWindowTitle("YouToo")
    #self.setFixedSize(400, 300)

    # Set QMainWindow layout to grid
    self.grid = QGridLayout()
    self.widget = QWidget()
    self.widget.setLayout(self.grid)
    self.setCentralWidget(self.widget)

    # Create widgets
    self.button_download = QPushButton(text = "Download!")
    self.button_file_name = QPushButton(text = 'File Name')
    self.le = QLabel(text = '')

    # Connect events
    self.button_download.clicked.connect(self.on_button_download)
    self.button_file_name.clicked.connect(self.on_button_file_name)
    
    # Add widgets to the screen
    self.grid.addWidget(self.button_file_name, 0, 0, 1, 1)
    self.grid.addWidget(self.le, 1, 0, 1, 1)
    self.grid.addWidget(self.button_download, 2, 0, 1, 1)

  def on_button_download(self):
    logging.info("on_button_download pressed")
    fname = QFileDialog.getExistingDirectory(self, 'Open Directory')
    
    if fname:
      self.le.setText(str(fname))

  def on_button_file_name(self):
    text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

    if ok:
      self.le.setText(str(text))

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

  app = QApplication(sys.argv)
  
  window = YouToo()
  window.show()

  app.exec()