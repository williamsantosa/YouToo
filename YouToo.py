import pytube as pt, sys
import logging
from pytube import YouTube
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

## User Interface Functions

class YouToo(QMainWindow):
  def __init__(self):
    super().__init__()

    self.init_ui()

  def init_ui(self):
    # Variables
    self.output_path = ""
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
    directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
    
    if directory:
      self.output_path = str(directory)
      self.le.setText(str(directory))

  def on_button_file_name(self):
    text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

    if ok:
      self.le.setText(str(text))

## Helper Functions

def list_res(streams):
  """
  Returns a list of the streams' resolution (res) in ascending order 

  :param streams (StreamQuery): Object to query the res
  :return (list[str]): list of res in ascending order
  """
  return [stream.resolution for stream in streams.order_by('resolution')]
  
def list_abr(streams):
  """
  Returns a list of the streams' average bit rate (abr) in ascending order 

  :param streams (StreamQuery): Object to query the abrs
  :return (list[str]): list of abrs in ascending order
  """
  return [stream.abr for stream in streams.order_by("abr")]

## Core Functions

def download_youtube(output_path, link, itag=None, filename=None, file_extension=None, abr=None, resolution=None, only_audio=False, only_video=False):
  """
  Downloads YouTube video from link into the output_path specified.

  :param output_path (str): path where the file will be outputted
  :param link (str): YouTube video link
  :param itag (int): stream itag to download, optional
  :param filename (str): name of the file to download
  :param file_extension (str): extension of the file to search for and download
  :param abr (str): average bit rate, e.g 140kbs
  :param resolution (str): resolution of the video, e.g 144p
  :param only_audio (bool): searches only for audio
  :param only_video (bool): searches only for videos
  :return: none
  """
  try:
    yt = YouTube(link)
  except:
    logging.error(f'Could not create YouTube object with link: {link}. Check internet connection.')
    raise RuntimeError
  
  if itag:
    try:
      stream = yt.streams.get_by_itag(itag)
      if filename and file_extension:
        stream.download(output_path, f"{filename}.{file_extension}")
      else:
        stream.download(output_path)
    except:
      logging.error(f'Error occurred when downloading {link} with itag {itag}.')
      raise RuntimeError
    return

  streams = yt.streams.filter(
    file_extension=file_extension,
    abr=abr,
    resolution=resolution,
    only_audio=only_audio,
    only_video=only_video
  )

  if len(streams) == 0:
    logging.error('No streams found with given input.')
    raise RuntimeError
  elif only_audio and only_video:
    logging.error('Invalid inputs. Cannot input both only_audio and only_video.')
    raise ValueError
  elif only_audio or file_extension == "mp3":
    streams = streams.order_by('abr')
  elif only_video:
    streams = streams.order_by('resolution')
  else:
    streams = streams.order_by('resolution')

  stream = yt.streams.get_by_itag(int(streams[-1].itag))
  try:
    if filename and file_extension:
      stream.download(output_path, f"{filename}.{file_extension}")
    else:
      stream.download(output_path)
  except:
    logging.error(f'Error occurred when downloading {link} with itag {itag}.')
    raise RuntimeError

## Main Function

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

  app = QApplication(sys.argv)
  
  window = YouToo()
  window.show()

  app.exec()