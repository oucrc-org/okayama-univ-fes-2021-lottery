# 環境変数の読み込み
import config
# 乱数用ライブラリ
import random
# MySQL用ライブラリ
import pymysql.cursors

# DBに接続
conn = pymysql.connect(
    host=config.host,
    user=config.user,
    passwd=config.passwd,
    db=config.db,
    port=config.port,
    charset='utf8',
    cursorclass=pymysql.cursors.Cursor)

# 受信処理記述（DB問い合わせ）
# サーバに登録されている固有キーと名前をリストに順に格納
# 例 a = [[2417,岡大太郎],[13954, ことちゃん], ...]という形になるように

conn.close()  # DBから切断

# randomライブラリを使って，配列からいくつかの要素を弾き出せるようにする
