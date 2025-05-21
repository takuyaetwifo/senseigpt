from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(80))  # ←追加

    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    theme_color = db.Column(db.String(20), default="lightblue")  # ← ここを追加
    character_icon = db.Column(db.String(100), default="bear.png")  # ← 追加
    birthday = db.Column(db.Date)  # 誕生日
    hobbies = db.Column(db.String)  # 趣味（カンマ区切りなどでもOK）
    profile = db.Column(db.String)  # ひとことプロフィール
    background = db.Column(db.Text)         # 詳細な背景（管理者用）
    family_status = db.Column(db.Text)      # 家族全体の状況（管理者用）


class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_input = db.Column(db.Text, nullable=False)
    gpt_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime)
