# 環境変数の読み込み
import config
# 乱数用ライブラリ
import random
# MySQL用ライブラリ
import pymysql.cursors


def auto_lot(present_id, conn):  # 抽選するプレゼントID, 接続情報
    print("Lotterying present_id = " + str(present_id))
    # 受信処理記述（DB問い合わせ）
    with conn.cursor() as cursor:
        sql = "SELECT stock FROM presents WHERE id=%s"  # ストック数受信
        cursor.execute(sql, (present_id))
        result = cursor.fetchone()
        present_stock = result[0]
        print("Stock = " + str(present_stock))

        sql = "SELECT user_id, stamps FROM present_user WHERE present_id=%s"  # 応募した人のuser_idを受信
        cursor.execute(sql, (present_id))
        result = cursor.fetchall()
    # サーバに登録されているuser_idをリストに順に格納
    # 例 user_id = [1,1,1,1,2,2,2,4,4,12,13,13]
    # カラムstampsの個数分同じuser_idを入れると良い（事実上の抽選確率となる）
    user_id = []
    for i in range(len(result)):
        for j in range(0, result[i][1]):
            user_id.append(result[i][0])

    # print(user_id)

    remained_stock = manual_lot(present_stock, user_id)

    print("Remained stock = " + str(remained_stock))  # 残数表示
    print("")
    return
# end of auto_lot


def manual_lot(stock, appliciants):  # int, int[]
    winner = []
    for i in range(stock):
        if len(appliciants) == 0:
            break
        a = random.randrange(len(appliciants))
        winner.append(appliciants[a])
        b = appliciants[a]
    # randomライブラリを使って，配列からいくつかの要素を弾き出して新しいリストに格納する，ただし，一度出た人はリストから除外
    # 一度出た人を除外するというのは，その人のuser_idをappliciants上からすべて削除することを言う．
    # appliciantsの長さが0になったら強制的にbreak
        appliciants = [i for i in appliciants if i != b]
    print(winner)
    return stock - len(winner)
# end of auto_lot


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

for i in range(present_count):  # 抽選するプレゼントの種類分ループ
    auto_lot(i + 1, conn)

conn.close()  # DBから切断
