import sqlite3

#creates a table Text
def summarydb(path :str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cmd = 'CREATE TABLE IF NOT EXISTS Text(Email TEXT, Summary TEXT)'
    cur.execute(cmd)
    conn.commit()

#insert commands for adding summary 
def insertsummary(tablename : str, email : str, summary : str, path :str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    values = (email, summary)
    cmd =f'INSERT INTO {tablename} VALUES{values}' 
    print(cmd)

    cur.execute(cmd)
    conn.commit()

#commands to get fetch complete summary from table where email = currently logged in user    
def getsummary(email : str, path : str):
    
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    sql = f"SELECT Summary FROM Text WHERE Email = '{email}' "
    cur.execute(sql)
    complete_summary = cur.fetchall()

    return complete_summary


    
if __name__ == '__main__':
    summarydb()
    insertsummary('Text', 'at8029srmist', 'SOMEONE', path='../app.db')
    
