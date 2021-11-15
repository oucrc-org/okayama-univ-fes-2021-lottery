# 環境変数の読み込み
import config
# 乱数用ライブラリ
import random
# MySQL用ライブラリ
import pymysql.cursors


def auto_lot():
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
        auto_lot_loop(i + 1, conn)

    conn.close()  # DBから切断


def auto_lot_loop(present_id, conn):  # 抽選するプレゼントID, 接続情報
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
    lot_array = make_lot_array(result)
    # print(lot_array)
    remained_stock = lot(present_stock, lot_array)

    print("Remained stock = " + str(remained_stock))  # 残数表示
    print("")
    return
# end of auto_lot


def lot(stock, appliciants):  # int, int[]
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


def make_lot_array(user_array):
    lot_array = []
    for i in range(len(user_array)):
        for j in range(0, user_array[i][1]):
            lot_array.append(user_array[i][0])
    return lot_array

# main


print("Select lottery mode(Auto:1, Manual:2).")
mode = int(input())
if mode < 0 or mode > 3:
    print("Illegal operation. Process cancelled.")
    exit
elif mode == 1:
    auto_lot()
elif mode == 2:
    print("Please input remained_stock.")
    stock = int(input())
    id_stamps = []
    while 1:
        print("Please input [user_id, stamps] 1set.")
        temp_str = input()
        if temp_str == '':
            break
        array = list(map(int, temp_str.split(",")))
        id_stamps.append(array)
    # endwhile

    if len(id_stamps) == 0:
        print("No [user_id, stamps] list created. Process cancelled.")
        exit(1)

    lot_array = make_lot_array(id_stamps)
    # print(id_stamps)
    remained_stock = lot(stock, lot_array)
    print("Remained stock = " + str(remained_stock))  # 残数表示
    print("")
