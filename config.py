# .env ファイルをロードして環境変数へ反映
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# 環境変数を参照
host = os.getenv('HOST')
user = os.getenv('USER')
passwd = os.getenv('PASSWD')
db = os.getenv('DB')
port = int(os.getenv('PORT'))
