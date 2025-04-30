import sys
import os
import vlc
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QFrame, QSlider, QLabel, QHBoxLayout, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon


class VideoWindow(QMainWindow):
    def __init__(self, media_path):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        # Create VLC instance
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Video frame
        self.video_frame = QFrame(self)
        self.video_frame.setStyleSheet("background-color: black;")
        self.media_player.set_nsobject(int(self.video_frame.winId()))

        # Controls
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("icons/play.png"))
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon("icons/pause.png"))
        self.pause_button.clicked.connect(self.pause_video)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 1000)
        self.position_slider.sliderReleased.connect(self.seek_video)

        # Timer for updating slider position
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_ui)

        # Layouts
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(QLabel("Volume"))
        control_layout.addWidget(self.volume_slider)

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.addWidget(self.position_slider)
        layout.addLayout(control_layout)

        self.central_widget.setLayout(layout)

        # Load media
        self.media_player.set_media(self.instance.media_new(media_path))
        self.media_player.play()
        self.timer.start()

    def play_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def set_volume(self, value):
        self.media_player.audio_set_volume(value)

    def seek_video(self):
        position = self.position_slider.value() / 1000.0
        self.media_player.set_position(position)

    def update_ui(self):
        if self.media_player.is_playing():
            position = self.media_player.get_position() * 1000
            self.position_slider.setValue(int(position))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Player")
        self.setGeometry(100, 100, 300, 200)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Open file button
        self.open_file_button = QPushButton("Open File")
        self.open_file_button.clicked.connect(self.open_file)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.open_file_button)
        self.central_widget.setLayout(layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv)"
        )
        if file_name:  # Если файл выбран
            self.close()  # Закрыть основное окно
            self.video_window = VideoWindow(file_name)  # Создать новое окно для видео
            self.video_window.show()  # Отобразить окно


if __name__ == "__main__":
    os.environ["QT_MAC_WANTS_LAYER"] = "1"  # Fix for macOS rendering issues
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())