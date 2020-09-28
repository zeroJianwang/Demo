import pymysql as sql
"""all the query result from pysql is tuple[][]"""
LocalDatabaseConfig = {
    'HostName' :'localhost',
    'HostPort' : 3306,
    'UserName' : 'Ada',
    'Password' : 'ljw123'
}

class TableData():
    ''' a data set of database table'''
    def __init__(self,Table,HeadList):
        self.mHeadList = HeadList
        self.mData = Table
        self.mRowCount = len(self.mData)
        self.mColumnCount = len(self.mData[0])
        pass

    def row(self,RowIdx):
        '''retutn a row of data'''
        if row > self.mRowCount:
            return None
        return self.mData[RowIdx]

    def at(self,row,col):
        if row > self.mRowCount or col > self.mColumnCount:
            return None
        return self.mData[row][col]

    def ToInsertSqlString(self,TargetDatabase,TargetTableName):
        if self.mHeadList == '*':
            pass
        InsertString = 'Insert into ' + TargetDatabase + '.' + TargetTableName + ' ('
        pass

class MysqlConnector():
    '''class for connect to mysql server'''
    def __init__(self,Host,User,Password,DatabaseName):
        self.mHost = Host
        self.mUser = User
        self.mPassword = Password
        self.mDatabaseName = DatabaseName

    def CheckTableExist(self,Table):
        '''Check a table if exist or not'''
        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()

        QueryString = 'show tables like ' + '\''+ Table + '\''

        affected = curser.execute(QueryString)
        if affected == 0:
            return False
        else:
            return True

    def GetCreateString(self, Table):
        '''return the string of table creation'''
        IsContain = MysqlConnector.CheckTableExist(self,Table)
        if False == IsContain:
            raise Exception('Table not found')

        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()

        QueryString = 'show create table ' + Table

        affected = curser.execute(QueryString)
        StringCreate = curser.fetchall()#Table creation string should be at row 1 column 2
        if affected > 0:
            return StringCreate[0][1]
        else:
            return 'Query error'
            
    def GetRowDataCount(self,Table):
        '''Get data row count of the the table'''
        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()

        QueryString = 'select count(*) from ' + self.mDatabaseName + '.' + Table

        affected = curser.execute(QueryString)
        if affected > 1 or affected == 0:
            raise Exception("affected row should be one")
        
        data = curser.fetchall()
        return data[0][0]
        
    def QueryTable(self,Table,Feilds,Condition = ''):
        '''Query a table of data, Feild can be '*', or list of feild
            Condition is start with 'where'
        '''
        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()
    
        Feild = ""
        if type(Feilds) == type(list()):
            for Fe in Feilds:
                Feild += Fe+','
            Feild = Feild[0:-1]
        else:
            Feild = Feilds
            
        QueryString = 'select '+ Feild +' from ' + self.mDatabaseName + '.' + Table + ' ' + Condition

        affected = curser.execute(QueryString)

        TmpTable = curser.fetchall()

        curser.close()
        database_conn.close()
        return TableData(TmpTable,Feilds)

    def QueryOneValue(self,Table,Feild,ConditionField,ConditionValue):
        '''Query one value, the sql query must return one value by the where condition'''
        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()

        QueryString = 'select '+ Feild +' from ' + self.mDatabaseName + '.' + Table + ' where '+ConditionField + '='+ ConditionValue

        affected = curser.execute(QueryString)
        if affected > 1 or affected == 0:
            raise Exception("affected row should be one")
        
        data = curser.fetchall()
        curser.close()
        database_conn.close()
        return data[0][0]

    def QueryOneRow(self,Table,Feilds,ConditionField,ConditionValue):
        ''' Query values of one row, the sql query must return one row by the where condition
            Feilds can be list of field and can be '*', means all the field
        '''
        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()
    
        Feild = ""
        if type(Feilds) == type(list()):
            for Fe in Feilds:
                Feild += Fe+','
            Feild = Feild[0:-1]
        else:
            Feild = Feilds
            
        QueryString = 'select '+ Feild +' from ' + self.mDatabaseName + '.' + Table + ' where ' + ConditionField + '='+ ConditionValue

        affected = curser.execute(QueryString)
        if affected > 1 or affected == 0:
            raise Exception("affected row should be one")

        '''this fecchall return a tupes of all rows'''
        DataQuery = curser.fetchall()
        
        values = list()
        for row in DataQuery:
            for col in row:
                if None == col:
                    values.append("")
                else:
                    values.append(str(col))

        curser.close()
        database_conn.close()
        return values

    def QuersyOneColumn(self,Table,Feild,Condition = ''):
        '''Query values of one column, the sql query must return one column result by the where coniftion'''
        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()

        QueryString = 'select '+ Feild + ' from ' + self.mDatabaseName + '.' + Table + ' ' + Condition

        curser.execute(QueryString)
        DataQuery = curser.fetchall()

        values = list()
        for row in DataQuery:
            for col in row:
                if None == col:
                    values.append("")
                else:
                    values.append(str(col))
                
        
        curser.close()
        database_conn.close()
        return values

    def Insert(self,Table,Keys,Values):
        '''insert one row of data into database'''
        database_conn = sql.connect(self.mHost,self.mUser,self.mPassword,self.mDatabaseName)
        curser = database_conn.cursor()

        QueryString = 'insert into ' + self.mDatabaseName + '.' + Table + ' ('
        for key in Keys:
            QueryString += key + ','
        QueryString = QueryString[0:-1]

        QueryString += ')values('
        for value in Values:
            QueryString += '\''+value + '\','
        QueryString = QueryString[0:-1]
        QueryString += ');'

        affected = curser.execute(QueryString)
        if affected != len(Keys):
            raise Exception("affected rows not match the requirment row")
        database_conn.commit()
        curser.close()
        database_conn.close()
        return True

    def Update(self,Feild,Value,Condition):
        pass
