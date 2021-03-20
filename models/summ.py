import sqlite3

#function for creating summary_tbl
def summary_tbl(path : str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()


    sql = 'CREATE TABLE IF NOT EXISTS summary_tbl(Email TEXT, Summary TEXT)'
    cur.execute(sql)
    conn.commit()
    
#function for inserting values into the summary_tbl
def insert(user_email_id : str, summary_text: str):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    sql = f"INSERT INTO summary_tbl VALUES('{user_email_id}','{summary_text}')"   
    cur.execute(sql)
    conn.commit()

#function that returns the final summary from table where email = currently logged in user
def getq(user_email : str):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    sql = f"SELECT Summary FROM summary_tbl WHERE Email='{user_email}' "
    cur.execute(sql)
    fsummary = cur.fetchall()[-1]
    
    return fsummary
