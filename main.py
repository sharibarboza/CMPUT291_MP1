from connect import get_connection

# ----------------------------------- MAIN --------------------------------------

def main():
    # Connect to database
    conn = get_connection("sql_login.txt")
    curs = conn.cursor()

if __name__ == "__main__":
	main()
