import sqlite3

schema='''
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
	uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
, username TEXT, score INTEGER, created INTEGER, last_submitted INTEGER DEFAULT 0, password TEXT NOT NULL);
CREATE TABLE flags (
	fid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	fname TEXT NOT NULL,
	points INTEGER NOT NULL
);
CREATE TABLE submissions (
	sid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user" INTEGER NOT NULL,
	flag INTEGER NOT NULL,
	time INTEGER NOT NULL
);
DELETE FROM sqlite_sequence;
CREATE UNIQUE INDEX users_id_IDX ON users (uid);
COMMIT;
'''

con = sqlite3.connect('database.db')
# f = open('schema.sql', 'r')
# script = f.read()
cur = con.cursor()
cur.executescript(schema)