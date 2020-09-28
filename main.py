import sys

from PyQt5.QtWidgets import *
from DatabaseStorage import MysqlConnector
from DatabaseStorage import LocalDatabaseConfig
if __name__ == '__main__':
     app = QApplication(sys.argv)
    # parent = QWidget()
    # FilefName = QFileDialog.getOpenFileName(parent)

    sqlremote = MysqlConnector('10.253.102.35','readonly','read4tfg','DMR_VacuumProbe')
    TestString = sql.GetCreateString('ag_vacuum_cali_2020')

    sqllocal = MysqlConnector(LocalDatabaseConfig['HostName'],LocalDatabaseConfig['UserName'],LocalDatabaseConfig['Password'],'DMR_VacuumProbe')   
    # feilds = ['sn','da_zei','typ']
    # RowValues = sql.QueryOneRow('ag_vacuum_cali_2020',feilds,'sn','83160898')
    # print('test Query row data:')
    # print(RowValues)
    
    # RowValues = sql.QueryOneRow('ag_vacuum_cali_2020','*','sn','83160898')
    # print('test Query row data:')
    # print(RowValues)


    IsContain1 = sql.CheckTableExist('ag_vacuum_cali_2020')
    print('ag_vacuum_cali_2020:'+str(IsContain1))
    IsContain2 = sql.CheckTableExist('ag_vacuum_cali_2028')
    print('ag_vacuum_cali_2028:'+str(IsContain2))
    table = sql.QueryTable('ag_vacuum_cali_2020','*')
    # InsertString = table.ToInsertSqlString()
    print(table.at(3,1))
    DataCount = sql.GetRowDataCount('ag_vacuum_cali_2020')
    print(DataCount)

    app.exec_()
