from PyQt5.QtWidgets import *

class DlgDatabaseConfig(QDialog):
    '''
    this is a dialog using Qt, for client edit the database config, address username password...
    '''
    def __init__(self,HostName='localhost',Port=3306,UserName='root',Password=''):
        super().__init__()
        self.setWindowTitle('Database Configs')
        self.mHostName = HostName
        self.mPort = Port
        self.mUserName = UserName
        self.mPassword = Password

    def GetHostName():
        return self.mHostName
    def GetPort():
        return self.mPort
    def GetUserName():
        return mUserName
    def GetPassword():
        return mPassword

