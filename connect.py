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
    username = file.readline().rstrip('\n')
    password = file.readline().rstrip('\n')
    file.close()

    try:
        return cx_Oracle.connect(username, password, "gwynne.cs.ualberta.ca:1521/CRS")
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)


    

