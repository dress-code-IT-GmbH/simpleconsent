# Using Django with MSSQL

The general approach ist to install UnixODBC as ODBC Driver Manager and a particular driver (FreeTDS, Microsoft ODBC Driver 13/17).

Before using pyodbc the connection has to work on UnixODBC level, to be tested with isql.
Before using django-maysl-backend, pyodbc needs to be working. 

## MacOS - install pyodbc

Microsoft Dirvers (instruction for V13 and V17 fails, brew does not find recipe)
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15

    brew install unixodbc msodbcsql13 mssql-tools
    

Alternative with FreeTDS driver (did work)
https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Mac-OSX

    brew install unixodbc freetds

    /usr/local/etc/odbcinst.ini
    [FreeTDS]
    Description  = FreeTDS unixODBC Driver
    Driver       = /usr/local/Cellar/freetds/1.1.15_1/lib/libtdsodbc.0.so

## MacOS - install django-mssql-backend


## Example config MacOS + FreeTDS Driver

/etc/odbc.ini

    [WinIstAnders]  
    Driver = freeTDS  
    Server = 192.168.0.37,1433
    UID = SA
    PWD = scott

/etc/odbcinst.ini 

    [FreeTDS]
    Description  = FreeTDS unixODBC Driver
    Driver       = /usr/local/Cellar/freetds/1.1.15_1/lib/libtdsodbc.0.so
    
When the files are in place run this command

    odbcinst -i -s -f /usr/local/etc/odbc.ini    

## Example config Linux + MD Driver

/etc/odbc.ini

    [WinIstAnders]  
    Driver = ODBC Driver 13 for SQL Server  
    Server = 192.168.0.37,1433
    UID = SA
    PWD = scott

/etc/odbcinst.ini  (set by installation procedure)

    [ODBC Driver 17 for SQL Server]
    Description=Microsoft ODBC Driver 17 for SQL Server
    Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.4.so.2.1
    UsageCount=1

Test connection:

    isql -v WinIstAnders SA scott
    
    python
        import pyodbc
        connect_str = "DSN=WinIstAnders;UID=SA;PWD=scott"
        cnxn = pyodbc.connect(connect_str)


        
## Troubleshooting

UnixODBC configuration:
     
    odbcinst -j t
    isql -v -k "connectstring"

python project MSQL-CLI: https://github.com/dbcli/mssql-cli