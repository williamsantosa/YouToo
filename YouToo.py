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
    # Create Window
    self.setWindowTitle("YouToo")
    #self.setFixedSize(400, 300)

    # Set QMainWindow layout to vbox
    self.vbox = QVBoxLayout()
    self.widget = QWidget()
    self.widget.setLayout(self.vbox)
    self.setCentralWidget(self.widget)

    # YouTube Link Grid
    self.grid_yt_link = QGridLayout()

    self.label_yt_link = QLabel(text="YouTube Link")
    self.lineedit_yt_link = QLineEdit()

    self.grid_yt_link.addWidget(self.label_yt_link, 0, 0, 1, 1)
    self.grid_yt_link.addWidget(self.lineedit_yt_link, 1, 0, 1, 1)

    # Directory Grid
    self.grid_directory = QGridLayout()

    self.label_directory = QLabel(text="Output Directory")
    self.lineedit_directory = QLineEdit()
    self.button_directory = QPushButton(text='Select')

    self.button_directory.clicked.connect(self.on_button_directory)

    self.grid_directory.addWidget(self.label_directory, 0, 0, 1, 1)
    self.grid_directory.addWidget(self.lineedit_directory, 1, 0, 1, 2)
    self.grid_directory.addWidget(self.button_directory, 1, 2, 1, 1)

    # File Name & File Extension Grid
    self.grid_fnfe = QGridLayout()
    
    self.label_fnfe = QLabel(text="File Name & Extension")
    self.lineedit_filename = QLineEdit()
    self.combobox_file_extension = QComboBox()

    self.combobox_file_extension.addItems(["Any", "mp3", "mp4", "webm"])

    self.grid_fnfe.addWidget(self.label_fnfe, 0, 0, 1, 1)
    self.grid_fnfe.addWidget(self.lineedit_filename, 1, 0, 1, 2)
    self.grid_fnfe.addWidget(self.combobox_file_extension, 1, 2, 1, 1)

    # Audio & Video Grid
    self.grid_av = QGridLayout()

    self.label_av = QLabel(text="Audio & Video")
    self.combobox_av = QComboBox()

    self.combobox_av.addItems(["Both", "Audio Only", "Video Only"])

    self.grid_av.addWidget(self.label_av, 0, 0, 1, 1)
    self.grid_av.addWidget(self.combobox_av, 1, 0, 1, 1)

    # Download
    self.button_download = QPushButton(text = "Download!")

    # Add boxes to Window
    self.vbox.addLayout(self.grid_yt_link)
    self.vbox.addLayout(self.grid_directory)
    self.vbox.addLayout(self.grid_fnfe)
    self.vbox.addLayout(self.grid_av)
    self.vbox.addWidget(self.button_download)

  def on_button_directory(self):
    logging.info("on_button_directory pressed")
    directory = QFileDialog.getExistingDirectory(self, 'Select Directory')

    self.lineedit_directory.setText(directory)

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
    logging.error('No streams found with given inputs.')
    raise RuntimeError
  elif only_audio and only_video:
    logging.error('Invalid inputs. Cannot set both only_audio and only_video to True.')
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