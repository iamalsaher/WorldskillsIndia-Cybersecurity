import sqlite3
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
conn = sqlite3.connect('database.db')
cur = conn.cursor()

usernames = ["apple","mango","guava","melon"]
passwords = ["8becM9eKnvYt4QZY","Lsbc5uMZ3suMAY89","5pyLvbFNnh4MVbpY","sM8QgHJecdrJE3Xf"]
ts = int(datetime.now().timestamp())

assert(len(usernames)==len(passwords))

for i in range (len(usernames)):
    hash = bcrypt.generate_password_hash(passwords[i]).decode()
    cur.execute(f"INSERT INTO `users` (`username`, `score`, `created`, `password`) VALUES ('{usernames[i]}', 0, {ts}, '{hash}')")

conn.commit()
