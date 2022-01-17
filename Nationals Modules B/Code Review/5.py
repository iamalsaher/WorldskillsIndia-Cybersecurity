import pickle
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("mysql://root@db/notes?")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/save", methods=["POST"])
def save_data():
    uf = request.files['note'].read()
    ds = pickle.loads(uf)
    db.execute(f"INSERT INTO notes (date, title, data) VALUES ('{ds[0].date}', '{ds[0].title}', '{ds[0].data}')")
    db.commit()
    return '', 204