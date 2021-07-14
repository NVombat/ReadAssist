import sqlite3

#Creates a table Text to store the users complete uploaded text
def text_tbl(path :str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cmd = 'CREATE TABLE IF NOT EXISTS Text(Email TEXT, Text TEXT)'
    cur.execute(cmd)
    conn.commit()


#insert commands for adding TEXT 
def insert_text(tablename : str, email : str, text : str, path :str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    values = (email, text)
    cmd =f'INSERT INTO {tablename} VALUES{values}' 
    print(cmd)

    cur.execute(cmd)
    conn.commit()


#commands to get fetch complete TEXT from table where email = currently logged in user    
def get_text(email : str, path : str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    sql = f"SELECT Summary FROM Text WHERE Email = '{email}' "
    cur.execute(sql)
    complete_summary = cur.fetchall()

    return complete_summary


if __name__ == '__main__':
    text_tbl()
    insert_text('Text', 'at8029srmist', 'SOMEONE', path='../app.db')