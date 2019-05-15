from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import urllib.request
import ntpath

class podcastWidget (QtWidgets.QWidget):
    id = 0

    def __init__(self, parent = None):
        super(podcastWidget, self).__init__(parent)

        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        #self.textUpQLabel.setWordWrap(True)
        self.textDownQLabel = QtWidgets.QLabel()
        self.textDownQLabel.setWordWrap(True)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()

        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 1)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            font-size: 13px;
            padding: 0;
            margin: 0;
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: #b2b2b2;
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        filename = ntpath.basename(imagePath)
        if (os.path.isfile(filename)):
            urllib.request.urlretrieve(imagePath, filename)

        pixmap = QPixmap(imagePath).scaled(64, 64)
        self.iconQLabel.setPixmap(pixmap)

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id