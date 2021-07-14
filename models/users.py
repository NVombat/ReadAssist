import sqlite3

#function for creating table to store user
def make_user():
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS user(Email TEXT, Name TEXT, Password TEXT)'
    cur.execute(sql)
    conn.commit()


#function to insert values into user table 
def insert(tablename : str, values: tuple):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    sql = f'INSERT INTO {tablename} VALUES{values}'    
    cur.execute(sql)
    conn.commit()


#function checks if email and password match
def checkpassword(password : str, email : str):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    sql = f"SELECT * FROM user WHERE Password='{password}' AND Email='{email}'"
    cur.execute(sql)
    results = cur.fetchall()
    if len(results) >0 :
        return True

    return False


#function to get user's email 
def getemail():
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    sql = 'SELECT Email FROM user'
    cur.execute(sql)
    emails = cur.fetchall()
    
    return emails


#function to get name from user table
def getname(email: tuple):
    email = email[0]
    conn = sqlite3.connect("app.db")

    cur = conn.cursor()
    sql = f"SELECT Name FROM user WHERE Email='{email}'"

    cur.execute(sql)
    result = cur.fetchall()
    return result[0][0]


if __name__ == '__main__':
    pass
    # insert("user", values=("at8029@srmist.edu.in", "Aradhya", "SOMEONE"))
    # print(checkpassword("SOMEONE", "at8029@srmist.edu.in"))