# 環境変数の読み込み
import config
# 乱数用ライブラリ
import random
# MySQL用ライブラリ
import pymysql.cursors


def lot(present_id, conn):  # 抽選するプレゼントID, 接続情報
    print("Lotterying present_id = " + str(present_id))
    # 受信処理記述（DB問い合わせ）
    with conn.cursor() as cursor:
        sql = "SELECT stock FROM presents WHERE id=%s"  # ストック数受信
        cursor.execute(sql, (present_id))
        result = cursor.fetchone()
        present_stock = result[0]
        print("Stock = "+str(present_stock))

        sql = "SELECT user_id FROM present_user WHERE present_id=%s"  # 応募した人のuser_idを受信
        cursor.execute(sql, (present_id))
        result = cursor.fetchall()
    # サーバに登録されているuser_idをリストに順に格納
    # 例 user_id = [1,2,12]
    user_id = []
    for i in range(len(result)):
        user_id.append(result[i][0])
    print("Applicants_id = " + str(user_id))

    # カラムstampsの個数分同じuser_idを入れると良い（事実上の抽選確率となる）
    # randomライブラリを使って，配列からいくつかの要素を弾き出せるようにする，ただし，一度出た人はリストから除外

    # print("Remained stock = ...") # 残数表示

    print("")
    return
# end of lot


# main
# DBに接続
conn = pymysql.connect(
    host=config.host,
    user=config.user,
    passwd=config.passwd,
    db=config.db,
    port=config.port,
    charset='utf8',
    cursorclass=pymysql.cursors.Cursor)

with conn.cursor() as cursor:  # 抽選するプレゼントの種類数を自動取得
    sql = "SELECT COUNT(*) FROM presents"
    cursor.execute(sql)
    result = cursor.fetchone()
present_count = result[0]

for i in range(1, present_count):  # 抽選するプレゼントの種類分ループ
    lot(i, conn)

conn.close()  # DBから切断
