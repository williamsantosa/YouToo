import time, logging, os, sys
import pytube as pt
from pytube import YouTube
from pytube.contrib.playlist import Playlist
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
## User Interface Functions

class YouToo(QMainWindow):
  def __init__(self):
    super().__init__()

    self.init_ui()

  def init_ui(self):
    # Create Window
    self.setWindowTitle("YouToo")
    self.setFixedSize(230, 270)
    self.setWindowIcon(QIcon('assets/icon.png'))

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
    self.lineedit_directory.setFixedWidth(145)
    self.button_directory.setFixedWidth(60)

    self.button_directory.clicked.connect(self.on_button_directory)

    self.grid_directory.addWidget(self.label_directory, 0, 0, 1, 1)
    self.grid_directory.addWidget(self.lineedit_directory, 1, 0, 1, 2)
    self.grid_directory.addWidget(self.button_directory, 1, 2, 1, 1)

    # File Name & File Extension Grid
    self.grid_fnfe = QGridLayout()
    
    self.label_fnfe = QLabel(text="File Name & Extension")
    self.lineedit_filename = QLineEdit()
    self.combobox_file_extension = QComboBox()
    self.lineedit_filename.setFixedWidth(145)
    self.combobox_file_extension.setFixedWidth(60)

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

    # Menu bar
    self.menu = self.menuBar()

    # Create menu bar categories
    self.menu_file = self.menu.addMenu("File")
    self.menu_help = self.menu.addMenu("Help")

    # Create actions
    self.button_mexit = QAction("Exit", self)
    self.button_mexit.setIcon(QIcon("assets/exit.png"))
    self.button_mhelp = QAction("Help", self)
    self.button_mhelp.setIcon(QIcon("assets/help.png"))

    # Add actions
    self.menu_file.addAction(self.button_mexit)
    self.menu_file.triggered.connect(self.close)
    self.menu_help.addAction(self.button_mhelp)
    self.menu_help.triggered.connect(self.on_menu_help)

    # Add widgets to Window
    self.vbox.addLayout(self.grid_yt_link)
    self.vbox.addLayout(self.grid_directory)
    self.vbox.addLayout(self.grid_fnfe)
    self.vbox.addLayout(self.grid_av)
    self.vbox.addWidget(self.button_download)

  def on_menu_help(self):
    # Generate Window
    self.win = QMainWindow()
    self.win.setWindowTitle("Help Window")
    self.win.setFixedSize(400, 340)
    self.win.setWindowIcon(QIcon("assets/help.png"))
    self.vbox_help = QVBoxLayout()
    self.widget_help = QWidget()
    self.widget_help.setLayout(self.vbox_help)
    self.win.setCentralWidget(self.widget_help)

    # Place content into help
    help_text = (
    """    Description
    YouToo is a program that downloads YouTube videos to your 
    computer for the purpose of quick and easy media acquisition.

    Usage
    1. Enter a valid YouTube link containing a public video/playlist.
    2. Select an output directory for the files to be downloaded to.
    3. Enter the file name and the downloaded video's extension.
    4. Select both, audio only, or video only, depending on your
        preference.

    Notes
    1. If a playlist is provided the file name entered will be ignored.
        Download videos sequentially to name each one, or download all
        then rename them.
    2. If no streams with the extension is found, an error message will
        appear. Select another extension and try again.
    """
    )
    self.label_help = QLabel(text=help_text)
    self.button_done_help = QPushButton(text="Done")
    self.button_done_help.clicked.connect(self.win.close)

    # Add to vbox
    self.vbox_help.addWidget(self.label_help)
    self.vbox_help.addWidget(self.button_done_help)

    # Show menu
    self.win.show()
    app.processEvents()

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
    self.button_done_download.setDisabled(True)

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
    elif "https://www.youtube.com/watch?v=" in yt_link or "https://youtu.be/" in yt_link:
      download_list = [yt_link]
    else:
      error = ErrorDialog("YouTube Link Error", f"Invalid YouTube link: {yt_link}")
      return

    output_path = self.lineedit_directory.text().strip()
    if len(output_path) == 0 or not os.path.isdir(output_path):
      error = ErrorDialog("Output Path Error", f"Invalid output path: {output_path}")
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
    self.button_done_download.setDisabled(False)

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
  def update(var_progress, var_label, text, value):
    """
    Update the progress bar and text

    :param var_progress (QProgressBar): Progress bar to update 
    :param var_label (QLabel): Label to update
    :param text: text to set var_label to
    :param value: value of the progress bar
    :return: none
    """
    if var_progress and var_label:
      var_label.setText(text)
      var_progress.setValue(value)
      app.processEvents()

  # Update progress bar
  var_progress.reset()
  update(var_progress, var_label, 'Beginning download...', 0)

  # Create YouTube object
  if not yt:
    try:
      yt = YouTube(link)
    except:
      logging.error(f'Could not create YouTube object with link: {link}. Check internet connection.')
      error = ErrorDialog("YouTube Error", f"YouTube object not created with {link}.")
      app.processEvents()
      return

  # Update progress bar
  update(var_progress, var_label, f'Created YouTube object with {yt.title}...', 1)

  # Filter streams
  streams = yt.streams.filter(
    file_extension=file_extension,
    abr=abr,
    resolution=resolution,
    only_audio=only_audio,
    only_video=only_video
  )

  if len(streams) == 0:
    logging.error('No streams found with given inputs.')
    error = ErrorDialog("Stream Error", f"No streams found with file extension \"{file_extension}\" for {link}.")
    app.processEvents()
    return
  elif only_audio and only_video:
    logging.error('Invalid inputs. Cannot set both only_audio and only_video to True.')
    error = ErrorDialog("Input Error", "Please fix. Cannot set both only_audio and only_video to True.")
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
  update(var_progress, var_label, 'Finished checking for streams...', 2)

  # Get stream and file extension
  stream = yt.streams.get_by_itag(int(streams[-1].itag))
  mime = stream.mime_type
  file_extension = mime[mime.find('/')+1:]

  # Update progress bar
  update(var_progress, var_label, 'Obtained stream and file extension...', 2)
  
  # Download file
  try:
    # Update progress bar
    update(var_progress, var_label, 'Attempting to download...', 2)
    if filename and file_extension:
      stream.download(output_path, f"{filename}.{file_extension}")
    else:
      stream.download(output_path)
  except:
    logging.error(f'Error occurred when downloading {link} with itag {itag}.')
    error = ErrorDialog("Stream Download Error", f"Error occurred when downloading {link} with {itag}.")
    return

  # Increment progress bar
  update(var_progress, var_label, 'Finished downloading video.', 3)

## Main Function

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

  app = QApplication(sys.argv)
  
  window = YouToo()
  window.show()

  app.exec()