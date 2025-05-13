
from flask import Flask, request, render_template, redirect, url_for, session
from models import db
from config import Config
from datetime import datetime
from functools import wraps
import openai
from datetime import datetime
import random
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from flask_migrate import upgrade
from models import User
from werkzeug.security import generate_password_hash
from models import ChatLog
import pytz

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


NG_WORDS = [
    # 暴力・差別
    "殺す", "死ぬ", "なぐる", "たたく", "暴力", "血", "グロ", "戦争", "自殺", "いじめ",
    "障害者", "バカ", "アホ", "差別", "死ね",

    # 性的
    "セックス", "えろ", "エロ", "ちんこ", "まんこ", "せい", "おっぱい", "裸", "変態",
    "オナニー", "AV", "性行為", "性交",

    # 個人情報・危険性
    "住所", "電話番号", "ライン", "LINE", "SNS", "連絡先", "会おう", "会いたい", "家来て",

    # 薬物・アルコール
    "ドラッグ", "薬物", "酒", "飲酒", "たばこ", "煙草", "大麻", "覚せい剤"
]





def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


#@app.before_first_request
#def create_tables():
#    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="ログイン失敗")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
from datetime import datetime

def get_japanese_season(month: int) -> str:
    if month in [3, 4, 5]:
        return "春"
    elif month in [6, 7, 8]:
        return "夏"
    elif month in [9, 10, 11]:
        return "秋"
    else:
        return "冬"

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    now = datetime.now()
    utc_now = datetime.utcnow()
    jst = pytz.timezone('Asia/Tokyo')
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(jst)
    
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H時%M分")
    season = get_japanese_season(now.month)

    lesson = random.choice(LESSONS)

    # 時間帯に応じたあいさつ
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "おはようございます"
    elif 12 <= hour < 18:
        greeting = "こんにちは"
    else:
        greeting = "こんばんは"

    username = session["username"]
    greeting_message = f"{greeting}、{username}さん！"

    messages = [{
        "role": "system",
        "content": f"{greeting_message} 今日は{date_str}、{season}です。現在の時刻は{time_str}です。あなたは子どもにやさしく教えるAI先生です。"
    }]

    #history = ChatLog.query.filter_by(user_id=session["user_id"]).order_by(ChatLog.id.asc()).limit(10).all()
    #for row in history:
    #    messages.append({"role": "user", "content": row.user_input})
    #    messages.append({"role": "assistant", "content": row.gpt_response})

    #if request.method == "POST":
    #    user_input = request.form["message"]
    #    messages.append({"role": "user", "content": user_input})
        
        
        
    # 過去の履歴（古い順）を追加
    history = ChatLog.query.filter_by(user_id=session["user_id"]).order_by(ChatLog.id.asc()).limit(5).all()
    for row in history:
        messages.append({"role": "user", "content": row.user_input})
        messages.append({"role": "assistant", "content": row.gpt_response})

        
    if request.method == "POST":
        user_input = request.form["message"]
        messages.append({"role": "user", "content": user_input})    
        

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            main_reply = response.choices[0].message.content

            # スタンプ処理
            STAMP_EMOJIS = ["🌟", "✨", "💯", "👏", "😊", "👍", "🎉", "🥳", "🤗", "🙌"]
            stamp_count = random.randint(2, 3)
            selected_stamps = random.sample(STAMP_EMOJIS, stamp_count)
            stamp_string = " ".join(selected_stamps)

            gpt_response = f"{main_reply}\n\n{stamp_string}"
            messages.append({"role": "assistant", "content": gpt_response})
        except Exception as e:
            gpt_response = f"エラー: {e}"

        log = ChatLog(
            user_id=session["user_id"],
            user_input=user_input,
            gpt_response=gpt_response,
            timestamp=now
        )
        db.session.add(log)
        db.session.commit()

    rows = ChatLog.query.filter_by(user_id=session["user_id"]).order_by(ChatLog.id.desc()).limit(5).all()
    user = User.query.get(session["user_id"])
    return render_template(
        "chat.html",
        username=username,
        rows=rows,
        lesson=lesson,
        messages=messages,
        theme_color=user.theme_color,
        user_icon=user.character_icon
    )




@app.route("/clear_chat", methods=["POST"])
@login_required
def clear_chat():
    ChatLog.query.filter_by(user_id=session["user_id"]).delete()
    db.session.commit()
    return redirect(url_for("chat"))



@app.route("/admin/delete-users-table")
def delete_users():
    from sqlalchemy import text
    db.session.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
    db.session.commit()
    return "users テーブルが存在していれば削除しました。"


#@app.route("/settings", methods=["GET", "POST"])
#@login_required
#def settings():
#    if request.method == "POST":
#        color = request.form["theme_color"]
#        user = User.query.get(session["user_id"])
#        user.theme_color = color
#        db.session.commit()
#        return redirect(url_for("chat"))
    
#    return render_template("settings.html", username=session["username"])

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.theme_color = request.form["theme_color"]

        if "icon_file" in request.files:
            file = request.files["icon_file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(f"user{user.id}_" + file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                user.character_icon = filename

        db.session.commit()
        return redirect(url_for("chat"))

    return render_template("settings.html",
                           username=user.username,
                           current_color=user.theme_color,
                           current_icon=user.character_icon)



LESSONS = [
    "今日の漢字：『海』 - 水がいっぱいの場所だね！",
    "今日の英単語：『sun』 - 太陽のことだよ！",
    "今日のことわざ：『石の上にも三年』 - がまんすれば結果が出るってこと！",
    "今日の算数：『2×3=6』 - 2を3回たすと6になるよ！",
    "今日の生き物：『カブトムシ』 - つのがかっこいい昆虫！"
    "今日の漢字：『空』 - そらのことだよ。雲や星が見えるね！",
    "今日の英単語：『book』 - 本のことだよ。たくさん読もう！",
    "今日のことわざ：『七転び八起き』 - 何度失敗してもがんばれば大丈夫！",
    "今日の算数：『10÷2=5』 - わり算も覚えよう！",
    "今日の理科：『水は100℃で沸騰する』 - お湯がぶくぶくする温度だね！",
    "今日の社会：『日本の首都は東京』 - 日本の中心だよ！",
    "今日の生き物：『コアラ』 - ユーカリの葉を食べているよ！",
    "今日のマナー：『ごはんの前には「いただきます」』 - 感謝の気持ちを忘れずに！",
    "今日の英単語：『dog』 - 犬のことだよ。かわいいね！",
    "今日の音楽：『ドレミファソラシド』 - 音のならびだよ。歌ってみよう！",
    "今日の体育：『なわとびはリズムが大切』 - うまく飛べるかな？",
    "今日の図工：『色をまぜると新しい色ができる』 - ためしてみよう！",
    "今日の道徳：『やさしい言葉をつかおう』 - みんながうれしくなるよ！",
    "今日の地理：『富士山は日本一高い山』 - 高さは約3776メートル！",
    "今日の天気：『雨の日はかさをわすれずに』 - ぬれないように気をつけよう！"
        # 国語
    "今日の漢字：『森』 - 木がたくさんあるところだよ！",
    "今日の漢字：『空』 - そらのことだね！",
    "今日のことわざ：『犬も歩けば棒にあたる』 - 思わぬことがおこるよ！",
    "今日のことわざ：『花より団子』 - 見た目より中身が大事！",
    "今日のことば：『うでがなる』 - やる気まんまん！",

    # 算数
    "今日の算数：『5×4=20』 - 5を4回たすと20！",
    "今日の算数：『1L = 1000mL』 - ジュースのりょうの勉強！",
    "今日の図形：『正三角形』 - ぜんぶの辺が同じ長さ！",
    "今日の単位：『1時間 = 60分』 - 時こくのきほん！",
    "今日の計算：『12÷3=4』 - わりざんの練習！",

    # 英語
    "今日の英単語：『apple』 - りんご 🍎",
    "今日の英単語：『dog』 - いぬ 🐶",
    "今日のフレーズ：『How are you?』 - 元気？",
    "今日の英単語：『blue』 - あおい色 💙",
    "今日の英語：『I like soccer.』 - サッカーが好き！",

    # 理科
    "今日の生き物：『アサガオ』 - 夏にさく花！",
    "今日の生き物：『カマキリ』 - 前足がかっこいい虫！",
    "今日の自然：『雲』 - 空にうかぶしろいもの！",
    "今日の実験：『水のあたたまり方』 - 下から上にあたたまるよ！",
    "今日の科学：『じしゃく』 - N極とS極があるよ！",

    # 社会
    "今日の地名：『東京』 - 日本の首都！",
    "今日の県：『北海道』 - 一番大きな都道府県！",
    "今日の昔話：『聖徳太子』 - 10人の話をきいた？",
    "今日の行事：『お正月』 - 1月の大切な日！",
    "今日の建物：『おしろ』 - むかしの大名が住んでたよ！",

    # 道徳・生活
    "今日のマナー：『あいさつをする』 - 笑顔で「おはよう！」",
    "今日の生活：『くつをそろえる』 - じぶんのことはじぶんで！",
    "今日の保健：『早寝早起き』 - 体にいい習慣！",
    "今日の気持ち：『ありがとうを言う』 - 感謝のこころ！",
    "今日の行動：『おてつだいしよう』 - 家族がよろこぶよ！"
]




UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







#local
#if __name__ == "__main__":
    #with app.app_context():
    #    db.create_all()
    #app.run(debug=True)  # パソコンでは host や port は指定不要

#render    
# ✅ appを定義した後に書く
#if __name__ == "__main__":
#    with app.app_context():
#        db.create_all()
  #      upgrade()  # ✅ Flask 3 ではここで直接呼び出す
#    port = int(os.environ.get("PORT", 10000))
#    app.run(host="0.0.0.0", port=port)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # FlaskMigrate を使っている場合：upgrade() をここで呼ぶ（任意）
        # from flask_migrate import upgrade
        # upgrade()

    is_render = os.getenv("RENDER") == "true"

    if is_render:
        # ✅ Render 環境
        port = int(os.environ.get("PORT", 10000))
        app.run(host="0.0.0.0", port=port)
    else:
        # ✅ ローカル開発環境
        app.run(debug=True)  # host/port 指定不要
