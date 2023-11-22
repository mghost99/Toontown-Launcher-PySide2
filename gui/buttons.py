from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel
import base64
import gui.main_window as main_window
import os
import webbrowser

class ImageButton(QLabel):

    def __init__(self, parent, name, url="http://example.com"):
        QLabel.__init__(self, parent)
        self.parent = parent
        self.url = url
        self.setMouseTracking(True)
        self.count = 0
        self.old = self.parent.use_old
        if self.old:
            path = main_window.resource_path('resources/old/buttons/%s' % name)
            normal = QPixmap(path + '/normal.jpg')
            hover = QPixmap(path + '/hover.jpg')
            depressed = QPixmap(path + '/depressed.jpg')
            if os.path.exists(path + '/disabled.jpg'):
                disabled = QPixmap(path + '/disabled.jpg')
            else:
                disabled = QPixmap(path + '/depressed.jpg')
        else:
            path = main_window.resource_path('resources/buttons/%s' % name)
            normal = QPixmap(path + '/normal.png')
            hover = QPixmap(path + '/hover.png')
            depressed = QPixmap(path + '/depressed.png')
            if os.path.exists(path + '/disabled.png'):
                disabled = QPixmap(path + '/disabled.png')
            else:
                disabled = QPixmap(path + '/depressed.png')
        self.normal = normal
        self.hover = hover
        self.depressed = depressed
        self.disabled = disabled
        self.isHovering = False
        self.isDepressed = False
        self.enabled = True
        if self.enabled:
            self.setPixmap(self.normal)
        else:
            self.setPixmap(self.disabled)
        self.repaint()
        self.resize(self.normal.size())
        self.setStyleSheet('background:transparent;')

    def setImage(self, name, repaint=True):
        self.setPixmap(name)
        if repaint:
            self.repaint()

    def SetHoverBitmap(self, bitmap):
        self.hover = bitmap

    def SetDepressedBitmap(self, bitmap):
        self.depressed = bitmap

    def enterEvent(self, event):
        if not self.enabled:
            self.setImage(self.disabled)
            return

        self.isHovering = True
        if self.hover and not self.isDepressed:
            self.setImage(self.hover)

    def leaveEvent(self, event):
        if not self.enabled:
            self.setImage(self.disabled)
            return

        self.isHovering = False
        if not self.isDepressed:
            self.setImage(self.normal)

    def mousePressEvent(self, event):
        if not self.enabled:
            self.setImage(self.disabled)
            return

        self.isDepressed = True
        if self.depressed:
            self.setImage(self.depressed, repaint=False)

    def mouseReleaseEvent(self, event):
        if not self.enabled:
            self.setImage(self.disabled)
            return
        self.isDepressed = False
        if self.isHovering and self.hover:
            self.setImage(self.hover)
        else:
            self.setImage(self.normal)
        self.Clicked()

    def Clicked(self):
        pass

class CreateAccount(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'CreateAccount')
        self.setFixedSize(104, 13)
        if not self.old:
            self.move(628, 217)
        else:
            self.move(588, 218)

    def Clicked(self):
        webbrowser.open(self.url)

class ForgotPassword(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'ForgotPassword')
        self.setFixedSize(104, 13)
        if not self.old:
            self.move(508, 217)
        else:
            self.move(455, 218)

    def Clicked(self):
        webbrowser.open(self.url)

class GraphicOptions(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'GraphicOptions')
        self.setFixedSize(122, 38)
        self.move(499, 460)

        self.enabled = False
        self.setImage(self.disabled)

    def Clicked(self):
        pass

class Homepage(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'Homepage')
        self.setFixedSize(122, 38)
        if not self.old:
            self.move(253, 460)
        else:
            self.move(253, 461)

    def Clicked(self):
        webbrowser.open(self.url)

class ManageAccount(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'ManageAccount')
        if not self.old:
            self.setFixedSize(104, 13)
            self.move(400, 218)
        else:
            self.setFixedSize(122, 38)
            self.move(499, 461)

    def Clicked(self):
        webbrowser.open(self.url)

class Play(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'Play')
        self.setFixedSize(85, 36)
        self.move(653, 170)

    def Clicked(self):
        credentials = (
         self.parent.ubox.text(), self.parent.pbox.text())
        self.parent.credentials = credentials
        self.parent.on_play_button_clicked()

class PlayersGuide(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'PlayersGuide')
        self.setFixedSize(122, 38)
        if not self.old:
            self.move(132, 460)
        else:
            self.move(130, 461)

    def Clicked(self):
        webbrowser.open(self.url)

class Quit(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'Quit')
        self.setFixedSize(122, 38)
        if not self.old:
            self.move(620, 460)
        else:
            self.move(623, 461)

    def Clicked(self):
        self.parent.close()

class ReportBug(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'ReportBug')
        self.setFixedSize(122, 38)
        if not self.old:
            self.move(10, 460)
        else:
            self.move(4, 461)

    def Clicked(self):
        webbrowser.open(self.url)

class TMin(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'TMin')
        self.setFixedSize(19, 19)
        self.move(685, 1)

    def Clicked(self):
        self.parent.setWindowState(Qt.WindowMinimized)

class TopToons(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'TopToons')
        self.setFixedSize(122, 38)
        if not self.old:
            self.move(378, 460)
        else:
            self.move(377, 461)

    def Clicked(self):
        webbrowser.open(self.url)

class TQuit(ImageButton):

    def __init__(self, parent):
        ImageButton.__init__(self, parent, 'TQuit')
        self.setFixedSize(19, 19)
        self.move(710, 1)

    def Clicked(self):
        self.parent.close()
