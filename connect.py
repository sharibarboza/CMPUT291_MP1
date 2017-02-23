import sys
import cx_Oracle

def get_connection(filename):
    """
    Usage Example:
    from connect import get_connection

    conn = get_connection("sql_login.txt")
    curs = conn.cursor()
    ....
    ....
    ....
    curs.close()
    conn.close()

    """
    file = open(filename)
    username = file.readline()
    password = file.readline()
    file.close()

    connStr = "%s/%s@gwynne.cs.ualberta.ca:1521:CRS"

    try:
        return cx_Oracle.connect(connStr % (username, password))
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)


    

