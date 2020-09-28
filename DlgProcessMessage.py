from PyQt5.QtWidgets import *

class DlgProcessMessage(QDialog):
    '''this dialog is for showing all the message of a process'''
    def __init__(self):
        super().__init__()
        self.mMessageListView = QListView()
        self.mMessageList = []