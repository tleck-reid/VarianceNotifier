import pyodbc
from getpass import getpass
import mysql.connector 
from mysql.connector import Error
import os

#
#Todo: Need to move this somewhere more secure 
#
#---------------------------------------------##
class Connection_Establisher:
    def __Vault(self,key):
    
        __t = {
            "PDI_ADDRESS": os.getenv['PDI_IP'],
            "PDI_USERNAME": os.getenv['PDI_USER'],
            "PDI_PASSWORD": os.getenv['PDI_PASSWORD']
            }
        return __t[key]
    #------------------------------------------------#

    """
        Establish_PDI_Connection
        Parameters:
            * Database: Database to connect to
            * Username: PDI Username
            * Password: PDI Password
        Summary: Establishes connection with a PDI database
        returns: pyodbc connection
    """
    def Establish_PDI_Connection(self,Database):
        Driver = "{ODBC Driver 18 for SQL Server}"
        Server = self.__Vault("PDI_ADDRESS")
        Connection =(
                f'DRIVER={Driver};'
                f'SERVER={Server};'
                f'DATABASE={Database};'
                f'UID={self.__Vault("PDI_USERNAME")};' 
                f'PWD={self.__Vault("PDI_PASSWORD")};'
                f'TrustServerCertificate=yes;'
        )
        return pyodbc.connect(Connection)
