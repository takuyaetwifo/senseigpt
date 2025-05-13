from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    theme_color = db.Column(db.String(20), default="lightblue")  # ← ここを追加
    character_icon = db.Column(db.String(100), default="bear.png")  # ← 追加


class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_input = db.Column(db.Text, nullable=False)
    gpt_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime)
