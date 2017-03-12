import sys
import cx_Oracle

def get_connection(filename=None, username=None, password=None):
    """
    Usage Example:
    from connect import get_connection
    conn = get_connection("sql_login.txt")
    """
    if filename is not None:
        file = open(filename)
        username = file.readline().rstrip('\n')
        password = file.readline().rstrip('\n')
        file.close()
    elif username is None or password is None:
        print("Username or password not entered.")
        return None

    try:
        return cx_Oracle.connect(username, password, "gwynne.cs.ualberta.ca:1521/CRS")
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
