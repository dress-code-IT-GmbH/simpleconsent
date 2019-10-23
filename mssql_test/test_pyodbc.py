import pyodbc

DSN = 'WinIstAnders'
USER = 'SA'
PASSWORD = 'scott'

def test_connect():
    connect_str = f"DSN={DSN};UID={USER};PWD={PASSWORD}"
    print('connecting to ' + connect_str)
    cnxn = pyodbc.connect(connect_str)
    #cnxn = pyodbc.connect(driver=driver, host=server, database=database,
    #                      user=username, password=password)
    cursor = cnxn.cursor()

    print ('Using the following SQL Server version:')
    tsql = "SELECT @@version;"
    with cursor.execute(tsql):
        row = cursor.fetchone()
        print (str(row[0]))
