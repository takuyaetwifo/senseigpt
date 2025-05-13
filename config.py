import os
from dotenv import load_dotenv

# ローカル環境では .env を読み込む（Render では無視される）
load_dotenv()



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

    if os.getenv("RENDER") == "true":
        # Render 本番環境
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        # ローカル開発用
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            "LOCAL_DATABASE_URL",
            "postgresql://postgres:2933@localhost:5432/sensei_gpt"
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    
    
    
    
    
    
 #   SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
 #   SQLALCHEMY_DATABASE_URI = os.environ.get(
 #       "DATABASE_URL",
 #       "postgresql://postgres:2933@localhost:5432/sensei_gpt"
 #   )
 #   SQLALCHEMY_TRACK_MODIFICATIONS = False

    
#class Config:
#    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
#    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
#    SQLALCHEMY_TRACK_MODIFICATIONS = False

