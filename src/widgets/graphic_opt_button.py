from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class GraphicOptions(QPushButton):
    def __init__(self, parent=None):
        super(GraphicOptions, self).__init__(parent)
        
        # Setting the icon for the button
        self.setIcon(QIcon("assets/buttons/GRAPHICSOPTIONS1G.png"))
        self.setIconSize(QSize(122, 38))  # Setting the size of the icon
        
        # Setting the size of the button
        self.setFixedSize(122, 38)
        
        # Positioning the button
        self.move(499, 460)
        
        # Connecting the button click to the graphic_options method
        self.clicked.connect(self.graphic_options)
        
    def graphic_options(self):
        print("TODO: Graphics Option Menu")
