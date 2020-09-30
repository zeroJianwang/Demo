import sys

from PyQt5.QtWidgets import *
from DatabaseStorage import MysqlConnector
from DatabaseStorage import LocalDatabaseConfig
from DatabaseStorage import CommandType

import time

if __name__ == '__main__':
     # app = QApplication(sys.argv)

     TargetTable = 'ag_vacuum_cali_2020'
     TargetDatabase = 'DMR_VacuumProbe'

     # 分别链接本地数据库和远程的服务端的数据库
     sqlRemote = MysqlConnector('10.253.102.35','readonly','read4tfg',TargetDatabase)
     sqlLocal = MysqlConnector(LocalDatabaseConfig['HostName'],LocalDatabaseConfig['UserName'],LocalDatabaseConfig['Password'],TargetDatabase)   
     
     # 检查本地是否已有这个表，如果没有生成
     LocalTableContain = sqlLocal.CheckTableExist(TargetTable)
     if False == LocalTableContain:
          CreateString = sqlRemote.GetCreateString(TargetTable)
          print('Create table:')
          print(CreateString)
          sqlLocal.Command(CreateString)
     else:
          print('Table exist')

     # 开始实时同步
     while True:
          LocalTableCount = sqlLocal.GetRowDataCount(TargetTable)
          RemoteTableCount = sqlRemote.GetRowDataCount(TargetTable)
          if LocalTableCount != RemoteTableCount:
               UpdatedRowCount = RemoteTableCount - LocalTableCount
               print('need to sysn :' + str(UpdatedRowCount) + 'rows of data'
               Table = sqlRemote.QueryTable(TargetTable,'*','order by da_zei desc limit '+str(RemoteTableCount-LocalTableCount))
               InsertString = Table.ToInsertSqlString('DMR_VacuumProbe',TargetTable)
               sqlLocal.Command(InsertString,CommandType.INSERT)
          else:
               print('No update data，Both data count:' + str(LocalTableCount))
          time.sleep(60)
     # app.exec_()

