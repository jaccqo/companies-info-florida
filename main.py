import sys
from PyQt5.QtCore import Qt, QPoint,QBuffer
from PyQt5.QtGui import QIcon, QMouseEvent, QCursor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QScrollArea, QToolButton, QSizeGrip

from scraperthread import ScraperThread
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None

        # Set window properties
        self.setWindowTitle("Scraper")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMinimumSize(800, 600)

         # Load the previously browsed file path from settings
        self.settings = QSettings("Company scraper", "Scraper")
        self.file_path = self.settings.value("FilePath")

       
        # Initialize variables for window dragging and resizing
        self.draggable = False
        self.drag_position = QPoint()
        self.resizable = False
        self.resize_position = ""

        # Set window icon
        icon = QIcon("icons/buildings.png")
        self.setWindowIcon(icon)

        # Create title bar widget
        self.title_bar = QWidget(self)
        self.title_bar.setObjectName("TitleBar")
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar_layout.setSpacing(0)

        # Window title label with icon
        icon_pixmap = icon.pixmap(20, 20)
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        icon_pixmap.save(buffer, "PNG")
        icon_data = buffer.data().toBase64().data().decode()
        # title_text = f"<img src='data:image/png;base64,{icon_data}' align='left'> Company Scraper"
        title_text ="Company Info Scraper"
        self.title_label = QLabel(title_text)

        font = QFont("Arial")  # Replace "Cool Font" with the actual font name
        self.title_label.setFont(font)
        
        self.title_label.setObjectName("TitleLabel")
        self.title_bar_layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QToolButton()
        self.minimize_button.setObjectName("TitleBarButton")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setIcon(QIcon("icons/minus.png"))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.title_bar_layout.addWidget(self.minimize_button)

        # Maximize button
        self.maximize_button = QToolButton()
        self.maximize_button.setObjectName("TitleBarButton")
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.setIcon(QIcon("icons/maximize.png"))
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.title_bar_layout.addWidget(self.maximize_button)

        # Close button
        self.close_button = QToolButton()
        self.close_button.setObjectName("TitleBarButton")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setIcon(QIcon("icons/cross.png"))
        self.close_button.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_button)

        # Set the title bar widget as the window title bar
        self.set_title_bar_widget(self.title_bar)

         # Add resizable grips to all four corners
        top_left_grip = QSizeGrip(self)
        top_left_grip.setCursor(Qt.SizeFDiagCursor)
        top_right_grip = QSizeGrip(self)
        top_right_grip.setCursor(Qt.SizeBDiagCursor)
        
    

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Left widget
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_widget.setStyleSheet("background-color:rgba(34, 35, 36,0);")
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        # Select keywords file
        self.keywords_label = QLabel("Instructions:\n"
                                      "1. Click on the 'Browse' button to select a file containing keywords.\n"
                                      "2. Once the file is selected, click on the 'Start Scraping' button to begin the scraping process.")
        font = QFont("Arial")  # Replace "Cool Font" with the actual font name
        self.keywords_label.setFont(font)
        self.keywords_label.setStyleSheet("color: gray;")
        left_layout.addWidget(self.keywords_label)

        left_layout.addWidget(top_left_grip, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        
        self.keywords_input = QLineEdit()
        left_layout.addWidget(self.keywords_input)
        # Style self.keywords_input
        self.keywords_input.setStyleSheet("border: 2px solid gray; border-radius: 5px;color:white;")

        # Browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.setStyleSheet("background-color: #0f88fa;")
        self.browse_button.setObjectName("BrowseButton")
        self.browse_button.setCursor(QCursor(Qt.PointingHandCursor))  # Set cursor shape
        self.browse_button.clicked.connect(self.select_file)
        self.browse_button.setFixedWidth(200)
        left_layout.addWidget(self.browse_button, alignment=Qt.AlignCenter)  # Align the button to the center

        # Start Scraping button
        self.start_button = QPushButton("Start Scraping")
        self.start_button.setStyleSheet("background-color: #0f88fa;")
        self.start_button.setObjectName("StartButton")
        self.start_button.setCursor(QCursor(Qt.PointingHandCursor))  # Set cursor shape
        self.start_button.clicked.connect(self.start_scraping)
        self.start_button.setFixedWidth(200)
        left_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)  # Align the button to the center

                # Create the start button label
        self.credits = QLabel("Crafted by Jacko \n\nversion 0.01")
        self.credits.setObjectName("credits")

        

        # Set the font for the label
        font = QFont("fantasy",8)  # Replace "Cool Font" with the actual font name
        self.credits.setFont(font)
        self.credits.setStyleSheet("color:gray")

        # Set the fixed width for the label
        self.credits.setFixedWidth(200)

        left_layout.addWidget(self.credits, alignment=Qt.AlignLeft)
      

       
       

        # Right widget
        right_widget = QWidget()
        right_widget.setStyleSheet("border: none;background-color:rgb(54, 55, 56);")  # Remove border color
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(1)


        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setStyleSheet("border-radius: 1px;color:gray;background-color:#1b1c1c")
        self.output_text.setReadOnly(True)  # Set read-only property
        right_layout.addWidget(self.output_text)

        # Scroll area for output text area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(right_widget)

        # Add left and right widgets to the layout
        layout.addWidget(left_widget)
        layout.addWidget(scroll_area)

        # Apply custom style sheet
        style_sheet = """
        QMainWindow {
            background-color: rgba(54, 55, 56,100);
            color:white;
        }
        QWidget#TitleBar {
            background-color: rgba(54, 55, 56,100);
            border-bottom: 1px solid #252626;
            padding: 5px;
        }
        QLabel#TitleLabel {
            font-size: 14px;
            font-weight: bold;
            color:gray;
        }
        QToolButton#TitleBarButton {
            background-color: transparent;
            border: none;
        }
        QPushButton#BrowseButton,
        QPushButton#StartButton {
            background-color: #4287f5;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QTextEdit {
            background-color: #333333;
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
        QScrollBar:vertical {
            background: transparent;
            width: 8px;
        }
        QScrollBar::handle:vertical {
            background: #888888;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:hover {
            background: #aaaaaa;
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            background: none;
        }
        """
        self.setStyleSheet(style_sheet)

        

       


    
    def set_title_bar_widget(self, widget):
        self.setMenuWidget(widget)

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", self.file_path)
        if file_path:
            self.keywords_input.setText(file_path)
            self.file_path = file_path
            self.settings.setValue("FilePath", file_path)

    

    def start_scraping(self):
        if self.thread and self.thread.isRunning():
            # Thread is running, terminate it
            self.thread.terminate()
            self.thread.wait()
            self.thread = None
            self.start_button.setText("Start Scraping")
            self.start_button.setStyleSheet("background-color: #0f88fa;")
        else:
            file_path = self.keywords_input.text().strip()
            if not file_path:
                # File path is empty, show dialog
                warning_dialog = QMessageBox(self)
                warning_dialog.setIcon(QMessageBox.Warning)
                warning_dialog.setWindowTitle("File Not Specified")
                warning_dialog.setText("Please select a keywords file first.")
                
                warning_dialog.exec_()
                return

            with open(file_path, 'r') as file:
                keywords = file.read().splitlines()

            self.output_text.clear()

            # Create a new scrape thread for each keyword
            self.thread = ScraperThread(keywords)
            self.thread.start()
            self.thread.worker_signal.connect(self.append_scraped_data)
            self.start_button.setText("Running...")
            self.start_button.setStyleSheet("background-color: #07db74;")


           

    def append_scraped_data(self, data):
        
        if "Scraping completed!" in data:
            self.start_button.setText("Start Scraping")
            self.start_button.setStyleSheet("background-color: #0f88fa;")
 

        self.output_text.append("Scraping keyword: " + data)
        self.output_text.repaint()


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.draggable:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.draggable = False
            event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()


            

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


# to compile run the code below include icons folder though

# pyinstaller --onefile --add-data "icons/*.png;icons/" --add-data "scraperthread.py;." --add-data "bot.py;." main.py
