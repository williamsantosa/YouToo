import time, logging, os
import pytube as pt, sys
from pytube import YouTube
from pytube.contrib.playlist import Playlist
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
    self.setFixedSize(230, 250)

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
    self.button_download = QPushButton(text = "Download")
    self.button_download.clicked.connect(self.on_button_download)

    # Add boxes to Window
    self.vbox.addLayout(self.grid_yt_link)
    self.vbox.addLayout(self.grid_directory)
    self.vbox.addLayout(self.grid_fnfe)
    self.vbox.addLayout(self.grid_av)
    self.vbox.addWidget(self.button_download)

  def on_button_download(self):
    # Generate Window
    self.win = QMainWindow()
    self.win.setWindowTitle("Download Window")
    self.win.setFixedSize(700, 150)
    self.vbox_download = QVBoxLayout()
    self.widget_download = QWidget()
    self.widget_download.setLayout(self.vbox_download)
    self.win.setCentralWidget(self.widget_download)

    # Progress Bars
    self.label_individual = QLabel(text="")
    self.label_total = QLabel(text="")
    self.progressbar_individual = QProgressBar()
    self.progressbar_individual.setRange(0, 3)
    self.progressbar_total = QProgressBar()

    # Done Button
    self.button_done_download = QPushButton(text="Done")
    self.button_done_download.clicked.connect(lambda x : self.win.close())

    # Add widgets
    self.vbox_download.addWidget(self.label_individual)
    self.vbox_download.addWidget(self.progressbar_individual)
    self.vbox_download.addWidget(self.label_total)
    self.vbox_download.addWidget(self.progressbar_total)
    self.vbox_download.addWidget(self.button_done_download)
    self.win.show()

    # Display updated window
    app.processEvents()

    # Set variables for download
    yt_link = self.lineedit_yt_link.text().strip()
    if "https://www.youtube.com/playlist?list=" in yt_link:
      download_list = Playlist(yt_link).video_urls
    elif "https://www.youtube.com/watch?v=" in yt_link:
      download_list = [yt_link]
    else:
      self.error = ErrorDialog("YouTube Link Error", f"Invalid YouTube link: {yt_link}")
      return

    output_path = self.lineedit_directory.text().strip()
    if len(output_path) == 0 or not os.path.isdir(output_path):
      self.error = ErrorDialog("Output Path Error", f"Invalid output path: {output_path}")
      return
    
    if self.combobox_av.currentText() == "Both":
      only_audio = False
      only_video = False
    elif self.combobox_av.currentText() == "Audio Only":
      only_audio = True
      only_video = False
    elif self.combobox_av.currentText() == "Video Only":
      only_audio = False
      only_video = True

    filename = None if len(self.lineedit_filename.text()) == 0 or len(download_list) > 1 else self.lineedit_filename.text()
    file_extension = None if self.combobox_file_extension.currentText() == "Any" else self.combobox_file_extension.currentText()

    # Create progres bar
    self.progressbar_total.setRange(0, len(download_list))
    val_total = 0

    # Download each link in the list
    for link in download_list:
      app.processEvents()
      self.label_total.setText(f"Beginning download for {link}...")
      download_youtube(
        output_path=output_path,
        link=link,
        filename=filename,
        file_extension=file_extension,
        only_audio=only_audio,
        only_video=only_video,
        var_progress=self.progressbar_individual,
        var_label=self.label_individual
      )
      self.label_total.setText(f"Finished download for {link}.")
      val_total += 1
      self.progressbar_total.setValue(val_total)

  def on_button_directory(self):
    directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
    self.lineedit_directory.setText(directory)

## Custom Dialog Functions

class ErrorDialog(QDialog):
  def __init__(self, title, errmsg1=None, errmsg2=None):
    super().__init__()

    self.setWindowTitle(title)

    QBtn = QDialogButtonBox.StandardButton.Ok
    self.buttonBox = QDialogButtonBox(QBtn)
    self.buttonBox.clicked.connect(lambda x : self.close())

    self.layout = QVBoxLayout()
    if errmsg1:
      label = QLabel(text=errmsg1)
      label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
      self.layout.addWidget(label)
    if errmsg2:
      label = QLabel(text=errmsg2)
      label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
      self.layout.addWidget(label)

    self.layout.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    self.setLayout(self.layout)
    self.show()

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

def download_youtube(output_path, link, yt=None, filename=None, file_extension=None, abr=None, resolution=None, only_audio=False, only_video=False, var_progress=None, var_label=None):
  """
  Downloads YouTube video from link into the output_path specified.

  :param output_path (str): path where the file will be outputted
  :param link (str): YouTube video link
  :param yt (YouTube): YouTube object to download in place of link
  :param filename (str): name of the file to download
  :param file_extension (str): extension of the file to search for and download
  :param abr (str): average bit rate, e.g 140kbs
  :param resolution (str): resolution of the video, e.g 144p
  :param only_audio (bool): searches only for audio
  :param only_video (bool): searches only for videos
  :param var_progress (QProgressBar): Progress bar to update 
  :param var_label (QLabel): Label to update
  :return: none
  """
  if var_progress and var_label:
    var_label.setText(f'Beginning download...')
    var_progress.reset()

  if not yt:
    try:
      yt = YouTube(link)
    except:
      logging.error(f'Could not create YouTube object with link: {link}. Check internet connection.')
      self.error = ErrorDialog("YouTube Error", f"YouTube object not created with {link}.")
      app.processEvents()
      return

  if var_progress and var_label:
    var_label.setText(f'Created YouTube object with {yt.title}...')
    var_progress.setValue(1)

  streams = yt.streams.filter(
    file_extension=file_extension,
    abr=abr,
    resolution=resolution,
    only_audio=only_audio,
    only_video=only_video
  )

  if len(streams) == 0:
    logging.error('No streams found with given inputs.')
    self.error = ErrorDialog("Stream Error", f"No streams found with file extension \"{file_extension}\" for {link}.")
    app.processEvents()
    return
  elif only_audio and only_video:
    logging.error('Invalid inputs. Cannot set both only_audio and only_video to True.')
    self.error = ErrorDialog("Input Error", "Please fix. Cannot set both only_audio and only_video to True.")
    app.processEvents()
    return
  elif only_audio or file_extension == "mp3":
    streams = streams.order_by('abr')
  elif only_video:
    streams = streams.order_by('resolution')
  else:
    streams = streams.order_by('abr')
    streams = streams.order_by('resolution')

  # Increment progress bar
  if var_progress and var_label:
    var_label.setText(f'Finished checking for streams...')
    var_progress.setValue(2)

  # Get stream and file extension
  stream = yt.streams.get_by_itag(int(streams[-1].itag))
  mime = stream.mime_type
  file_extension = mime[mime.find('/')+1:]

  # Download file
  try:
    if filename and file_extension:
      stream.download(output_path, f"{filename}.{file_extension}")
    else:
      stream.download(output_path)
  except:
    logging.error(f'Error occurred when downloading {link} with itag {itag}.')
    self.error = ErrorDialog("Stream Download Error", f"Error occurred when downloading {link} with {itag}.")
    return

  # Increment progress bar
  if var_progress and var_label:
    var_label.setText(f'Finished downloading video.')
    var_progress.setValue(3)

## Main Function

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

  app = QApplication(sys.argv)
  
  window = YouToo()
  window.show()

  app.exec()