import pyodbc
import cx_Oracle

class SQLLogin:
    def __init__(self):
        self.connection = None

    def connect_mssql(self, server, database, username, password, trust_server_certificate):
        try:
            trust_certificate = 'yes' if trust_server_certificate else 'no'
            self.connection = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate={trust_certificate}'
            )
            print("Connected to MS SQL Server")
            cursor = self.connection.cursor()
            cursor.execute("SELECT @@VERSION")
            row = cursor.fetchone()
            while row:
                print(row[0])
                row = cursor.fetchone()
        except Exception as e:
            print(f"Error connecting to MS SQL Server: {e}")
            raise

    def connect_oracle(self, host, port, service_name, username, password,use_sid=False):
        try:
            if use_sid:
                dsn_tns = cx_Oracle.makedsn(host, port, sid=service_name)
            else:
                dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
            self.connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            print("Connected to Oracle Database")
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM v$version")
            row = cursor.fetchone()
            while row:
                print(row[0])
                row = cursor.fetchone()
        except cx_Oracle.DatabaseError as e:
            print(f"Error connecting to Oracle Database: {e}")
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

# Example usage
if __name__ == "__main__":
    sql_login = SQLLogin()
    try:
        sql_login.connect_mssql('server', 'database', 'username', 'password', True)
    except Exception as e:
        print("Failed to connect to MS SQL Server")

    try:
        sql_login.connect_oracle('host', '1521', 'service_name', 'username', 'password')
    except Exception as e:
        print("Failed to connect to Oracle Database")

    sql_login.close_connection()
