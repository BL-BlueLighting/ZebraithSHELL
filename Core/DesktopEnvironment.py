
import sys
from typing import Dict, Any, Optional
from dataclasses import dataclass
from Framework import *
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QFrame, QMenu, QGridLayout, QStyle
)
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtGui import QFont, QColor, QPalette


class DesktopIcon(QWidget):
    """DesktopIcon Base Class"""
    def __init__(self, icon_enum, text, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        layout.setSpacing(5)

        # icon label
        self.icon_label = QLabel()
        try:
            pixmap = QApplication.style().standardIcon(icon_enum).pixmap(48, 48)#type:ignore
        except Exception as e:
            print(f"[ FAILED ] Failed to initalize icon: {e}")
            pixmap = None
        if pixmap:
            self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  

        # text label
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        self.text_label.setFont(QFont("Sans", 10))
        self.text_label.setStyleSheet("color: white;")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)
        self.setFixedSize(80, 80)

    def mousePressEvent(self, event):#type:ignore
        # press event base
        print(f"[ DEBUG ] {self.text_label.text()} clicked")


class MainWindow(QMainWindow):
    def __init__(self):
        print("Zebraith Desktop Environment v0.0.1")
        print("By BL.BlueLighting")

        print("\nInitializing...")
        super().__init__()
        self.setWindowTitle("THE ZEBRAITH DESKTOP")
        self.setGeometry(100, 100, 800, 600)

        # cetral widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        print("\n[ INFO ] Central Widget Initialized.")
        

        # ---------- Desktop Area ----------
        self.desktop_area = QWidget()
        self.desktop_area.setAutoFillBackground(True)
        palette = self.desktop_area.palette()
        palette.setColor(self.desktop_area.backgroundRole(), QColor(30, 30, 30))  # Gray background
        self.desktop_area.setPalette(palette)

        # Grid icon
        desktop_layout = QGridLayout(self.desktop_area)
        desktop_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        desktop_layout.setHorizontalSpacing(20)
        desktop_layout.setVerticalSpacing(20)

        # Testing Icons
        icons = [
            (QStyle.SP_ComputerIcon, "计算机"),#type:ignore
            (QStyle.SP_DirIcon, "文件夹"),#type:ignore
            (QStyle.SP_FileIcon, "文件"),#type:ignore
            (QStyle.SP_TrashIcon, "回收站"),#type:ignore
        ]
        for i, (icon_enum, text) in enumerate(icons):
            di = DesktopIcon(icon_enum, text)
            desktop_layout.addWidget(di, i // 3, i % 3)  # 3 columns

        main_layout.addWidget(self.desktop_area, 1)  # Desktop area use more space

        print("\n[ INFO ] Desktop area initialized.")

        # ---------- Taskbar ----------
        self.taskbar = QFrame()
        self.taskbar.setFixedHeight(50)
        self.taskbar.setFrameShape(QFrame.StyledPanel)
        self.taskbar.setAutoFillBackground(True)
        taskbar_palette = self.taskbar.palette()
        taskbar_palette.setColor(self.taskbar.backgroundRole(), QColor(45, 45, 45))
        self.taskbar.setPalette(taskbar_palette)

        taskbar_layout = QHBoxLayout(self.taskbar)
        taskbar_layout.setContentsMargins(10, 5, 10, 5)

        # Start menu
        self.start_button = QPushButton()
        self.start_button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))#type:ignore
        self.start_button.setText(" 开始")
        self.start_button.setFont(QFont("Sans", 12))
        self.start_button.setFlat(True)
        self.start_button.setStyleSheet("color: white;")
        self.start_button.clicked.connect(self.on_start_button_clicked)
        self.start_menu = QMenu()
        self.start_menu.addAction("应用程序")
        self.start_menu.addAction("文件")
        self.start_menu.addSeparator()
        self.start_menu.addAction("设置")
        self.start_menu.addAction("关机")
        self.start_button.setMenu(self.start_menu)

        taskbar_layout.addWidget(self.start_button)
        taskbar_layout.addStretch()

        # Tray widget
        self.tray_widget = QWidget()
        tray_layout = QHBoxLayout(self.tray_widget)
        tray_layout.setContentsMargins(0, 0, 0, 0)
        tray_layout.setSpacing(10)

        # Internet icon
        self.network_icon = QLabel()
        network_pixmap = self.style().standardIcon(QStyle.SP_ComputerIcon).pixmap(24, 24)#type:ignore
        self.network_icon.setPixmap(network_pixmap)

        # Volume icon
        self.volume_icon = QLabel()
        volume_pixmap = self.style().standardIcon(QStyle.SP_MediaVolume).pixmap(24, 24)#type:ignore
        self.volume_icon.setPixmap(volume_pixmap)

        # Time
        self.clock_label = QLabel()
        self.clock_label.setFont(QFont("Sans", 12))
        self.clock_label.setStyleSheet("color: white;")
        self.update_time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)  # Update time every minute

        tray_layout.addWidget(self.network_icon)
        tray_layout.addWidget(self.volume_icon)
        tray_layout.addWidget(self.clock_label)

        taskbar_layout.addWidget(self.tray_widget)

        main_layout.addWidget(self.taskbar)

        print("[ INFO ] All widgets loaded.")

    def update_time(self):
        """Update clock viewing"""
        current = QTime.currentTime()
        self.clock_label.setText(current.toString("hh:mm"))

    def on_start_button_clicked(self):
        """Start button clicked"""
        ...
        #TODO: Finish this

@RegisterCommand("startd", ["cmd"])
def _ (args):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()