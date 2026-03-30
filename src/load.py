import sqlite3

# ------------------------------------------
# CREATE CONNECTION
# ------------------------------------------
def create_connection(db_name="data/bank.db"):
    conn = sqlite3.connect(db_name)
    return conn


# ------------------------------------------
# LOAD DATA TO DB
# ------------------------------------------
def load_to_db(df, conn, table_name="transactions"):
    df.to_sql(table_name, conn, if_exists="replace", index=False)


# ------------------------------------------
# RUN QUERY
# ------------------------------------------
def run_query(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)