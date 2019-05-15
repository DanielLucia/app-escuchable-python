import sys
import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import config
import os
import urllib.request
import episodesWidget
import podcastWidget

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("main.ui", self)

        getCategories(self)
        self.categoriesList.itemClicked.connect(self.clickGetPodcasts)
        self.podcastsList.itemClicked.connect(self.clickGetEpisodios)
        self.episodiosList.itemClicked.connect(self.clickGetEpisodio)

        self.textDescriptionCategory.hide()
        self.textTitlePodcast.hide()
        self.textDescriptionPodcast.hide()

        #if (config.CATEGORY > 0):
        #   getPodcasts(self, config.CATEGORY)
        #if (config.PODCAST > 0):
        #    getEpisodios(self, config.PODCAST)

        qScroll = self.episodiosList



    def clickGetPodcasts(self, item):
        category = int(item.data(QtCore.Qt.UserRole))
        getPodcasts(self, category)

    def clickGetEpisodios(self, item):
        podcast = int(item.data(QtCore.Qt.UserRole))
        getEpisodios(self, podcast)

    def clickGetEpisodio(self, item):
        episode = int(item.data(QtCore.Qt.UserRole))
        getEpisodio(self, episode)

    def Cancel(self):
        self.close()



class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("login.ui", self)
        self.registrarButton.clicked.connect(self.clickRegisterUser)

    def Cancel(self):
        self.close()

    def clickRegisterUser(self):
        if (self.registerEmail.text() == ''):
            QMessageBox.critical(self, 'Escuchable', "El e-mail no puede estar vacio", QMessageBox.Ok)
            return

        if (self.registerPassword.text() == ''):
            QMessageBox.critical(self, 'Escuchable', "El password no puede estar vacio", QMessageBox.Ok)
            return

        payload = {'email': self.registerEmail.text(), 'password': self.registerPassword.text()}
        url = config.END_POINT + "register/"
        resp = requests.post(url=url, data=payload)
        data = resp.json()

        if ('token' in data):
            config.saveConfig('token', data["token"])
            _login.hide()
            _main.show()
        else:
            QMessageBox.critical(self, 'Escuchable', data['error'], QMessageBox.Ok)
            return


def getCategories(self):
    print('Inicio carga')
    self.statusBar().showMessage('Cargando categorias...')
    self.categoriesList.clear()

    url = config.END_POINT + "categories/"
    resp = requests.get(url=url)
    if (resp.status_code != 200):
        QMessageBox.critical(self, 'Escuchable', 'Ha ocurrido un error al recuperar los datos', QMessageBox.Ok)
        return

    datas = resp.json()
    for data in datas:
        item = QListWidgetItem(self.categoriesList)
        item.setText(data['nombre'])
        item.setData(QtCore.Qt.UserRole, data['id'])

    self.statusBar().showMessage('Estado')

    print('Fin carga')

def getPodcasts(self, category):
    print('Inicio carga')

    self.statusBar().showMessage('Cargando podcasts...')
    if (self.orderByUpdated.isChecked()):
        orderBy = 'fecha'
    else:
        orderBy = ''

    self.podcastsList.clear()

    payload = {'category': category, 'order-by': orderBy, 'token': config.TOKEN}
    url = config.END_POINT + "podcasts/"
    resp = requests.post(url=url, data=payload)
    if (resp.status_code != 200):
        QMessageBox.critical(self, 'Escuchable', 'Ha ocurrido un error al recuperar los datos', QMessageBox.Ok)
        return

    datas = resp.json()

    self.textDescriptionCategory.setText(datas["detail"]["meta_title"])
    self.textDescriptionCategory.show()

    for data in datas['podcasts']:
        #item = QListWidgetItem(self.podcastsList)
        #item.setText(data['nombre'])
        #item.setData(QtCore.Qt.UserRole, data['id'])

        widget = podcastWidget.podcastWidget()
        widget.setTextUp(data['nombre'])

        if (data["ultimopodcast"]):
            widget.setTextDown('Ultima actualizacion: ' + config.cleanhtml(data["ultimopodcast"]))

        widget.setID(data['id'])
        if (data['imagen'] != ''):
            widget.setIcon(data['imagen'])

        # Create QListWidgetItem
        myQListWidgetItem = QtWidgets.QListWidgetItem(self.podcastsList)
        myQListWidgetItem.setData(QtCore.Qt.UserRole, data['id'])

        # Set size hint
        myQListWidgetItem.setSizeHint(widget.sizeHint())

        # Add QListWidgetItem into QListWidget
        self.podcastsList.addItem(myQListWidgetItem)
        self.podcastsList.setItemWidget(myQListWidgetItem, widget)

    config.saveConfig('category', category)
    self.statusBar().showMessage('Estado')
    print('Fin carga')


def getEpisodios(self, podcast):
    print('Inicio carga')

    self.statusBar().showMessage('Cargando episodios...')
    self.episodiosList.clear()

    payload = {'podcast': podcast, 'token': config.TOKEN}
    url = config.END_POINT + "episodes/"
    resp = requests.post(url=url, data=payload)
    if (resp.status_code != 200):
        QMessageBox.critical(self, 'Escuchable', 'Ha ocurrido un error al recuperar los datos', QMessageBox.Ok)
        return

    datas = resp.json()

    if not datas['episodes']:
        QMessageBox.critical(self, 'Escuchable', 'Este podcast no tiene episodios', QMessageBox.Ok)
        return

    self.textTitlePodcast.setText(datas["detail"]["nombre"])
    self.textTitlePodcast.show()

    self.textDescriptionPodcast.setText(config.cleanhtml(datas["detail"]["descripcion"]))
    self.textDescriptionPodcast.show()

    for data in datas['episodes']:
        #item = QListWidgetItem(self.episodiosList)
        #item.setText(data['nombre'] + "\n" + data["fecha"])
        #item.setData(QtCore.Qt.UserRole, data['id'])

        widget = episodesWidget.episodesWidget()
        widget.setTextUp(data['nombre'])
        widget.setTextDown(data["fecha"])
        widget.setID(data['id'])
        #widget.setIcon(icon)

        # Create QListWidgetItem
        myQListWidgetItem = QtWidgets.QListWidgetItem(self.episodiosList)
        myQListWidgetItem.setData(QtCore.Qt.UserRole, data['id'])

        # Set size hint
        myQListWidgetItem.setSizeHint(widget.sizeHint())

        # Add QListWidgetItem into QListWidget
        self.episodiosList.addItem(myQListWidgetItem)
        self.episodiosList.setItemWidget(myQListWidgetItem, widget)



    config.saveConfig('podcast', podcast)
    self.statusBar().showMessage('Estado')
    print('Fin carga')

def getEpisodio(self, episode):


    buttonReply = QMessageBox.question(self, 'Escuchable', "¿Quieres descargar el episodio?", QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        print('Inicio carga')

        self.statusBar().showMessage('Descargando episodio...')

        payload = {'episode': episode, 'token': config.TOKEN}
        url = config.END_POINT + "episode/"
        resp = requests.post(url=url, data=payload)
        if (resp.status_code != 200):
            QMessageBox.critical(self, 'Escuchable', 'Ha ocurrido un error al recuperar los datos', QMessageBox.Ok)
            return

        data = resp.json()
        if not os.path.isdir("episodes/"):
            os.makedirs("episodes/")

        extension = os.path.splitext(data['episode']['url'])[1]
        urllib.request.urlretrieve(url, "episodes/" + str(episode) + '.' + extension)

        config.saveConfig('episode', episode)
        self.statusBar().showMessage('Estado')
        print('Fin carga')
    else:
        return


app = QApplication(sys.argv)
_main = Main()
_login = Login()

if (config.LOGGED):
    _main.show()
else:
    _login.show()
app.exec_()
