from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize

class LiPrompt(QLabel):
    def __init__(self, parent=None):
        super(LiPrompt, self).__init__(parent)
        
        # Setting the pixmap for the label
        self.setPixmap(QPixmap("assets/LIPROMPT.png"))
        # Setting the size of the label
        self.setFixedSize(QSize(98, 52))
        
        # Positioning the label
        self.move(400, 165)