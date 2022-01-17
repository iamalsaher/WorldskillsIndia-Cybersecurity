from datetime import datetime

from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import sqlite3
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = "MKfYBu3m324dfWNbk2qn9pp2SASPh2FM"
jwt = JWTManager(app)

create = False
if not os.path.exists('database.db'):
    create = True

conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()

if create is True:
    f = open('schema.sql', 'r')
    script = f.read()
    cur.executescript(script)


@app.route('/login', methods=["POST"])
def login():
    try:
        data = request.get_json()
        expires = timedelta(days=365)
        uname = data.get('username')
        if uname is not None:
            cur.execute(f"SELECT * FROM `users` WHERE `username` = '{uname}'")
            row = cur.fetchone()
        else:
            raise ValueError

        if row is None:
            raise ModuleNotFoundError

        password = data.get("password")
        if password is not None:
            auth = bcrypt.check_password_hash(row[5], password)
        else:
            raise ValueError

        if auth is True:
            access_token = create_access_token(identity=row[0], expires_delta=expires)
            return jsonify(ok=True, status="Logged in", token=access_token), 200
        else:
            raise AttributeError

    except AttributeError:
        return jsonify(ok=False, status="wrong pw"), 401

    except ModuleNotFoundError:
        return jsonify(ok=False, status="Not Found"), 400

    except ValueError:
        return jsonify(ok=False, status="huh?"), 422


def check_exisiting(user, flag):
    print(user, flag)
    cur.execute(f"SELECT sid FROM `submissions` WHERE `user` = {user} AND `flag` = {flag}")
    res = cur.fetchone()
    print(res)
    return res is not None


@app.route('/submit', methods=['POST'])
@jwt_required()
def submit():
    try:
        user = get_jwt_identity()
        data = request.get_json()
        print(data)
        flag = data.get('flag')
        print(flag)
        if flag is not None:
            print('here')
            cur.execute(f"SELECT * FROM `flags` WHERE fname = '{flag}'")
            dbflag = cur.fetchone()
            print(dbflag)
        else:
            raise ValueError

        print(dbflag)
        if (dbflag is not None) and check_exisiting(user, dbflag[0]) is False:
            now = int(datetime.now().timestamp())
            cur.execute(f"INSERT INTO `submissions` (`user`, `flag`, `time`) VALUES ({user}, {dbflag[0]}, {now})")
            cur.execute(f"UPDATE `users` SET score = score + {dbflag[2]}, last_submitted = {now} WHERE uid = {user}")
            conn.commit()
            return jsonify(ok=True, status="recorded"), 200
        else:
            raise NotImplementedError

    except NotImplementedError:
        return jsonify(ok=False, status="Invalid entry"), 400

    except ValueError:
        return jsonify(ok=False, status="huh?"), 422


def convert(row):
    temp = {
        "time": datetime.fromtimestamp(row[2]).strftime("%Y-%m-%d %H:%M:%S"),  # IST
        "username": row[1],
        "uid": row[0],
        "score": row[2]
    }
    return temp


@app.route('/leaderboard')
def results():
    print("here")
    cur.execute("SELECT uid, username, score, last_submitted FROM users ORDER BY last_submitted DESC")
    results = cur.fetchall()
    final = list(map(convert, results))
    # print(results)
    return jsonify(final)


if __name__ == '__main__':
    app.run(debug=True)
