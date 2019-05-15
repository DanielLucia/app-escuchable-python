from PyQt5 import QtWidgets

class episodesWidget (QtWidgets.QWidget):
    id = 0

    def __init__(self, parent = None):

        super(episodesWidget, self).__init__(parent)

        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        #self.textUpQLabel.setWordWrap(True)
        self.textDownQLabel = QtWidgets.QLabel()
        self.textDownQLabel.setWordWrap(True)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

        self.textUpQLabel.setStyleSheet('''
            font-weight: bold;
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
        self.iconQLabel.setPixmap(QtWidgets.QPixmap(imagePath))

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id