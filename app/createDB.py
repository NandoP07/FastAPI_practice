import sqlite3 as sql



def create_db():
    conn = sql.connect("comercio.db")
    conn.commit()
    conn.close()

def create_table(table_name):
    conn = sql.connect(f"{table_name}.db")
    cursor = conn.cursor()



if __name__ == "__main__":
    create_db()