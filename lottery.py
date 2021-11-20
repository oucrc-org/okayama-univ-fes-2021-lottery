# 環境変数の読み込み
import config
# 時刻用ライブラリ
import datetime
# 乱数用ライブラリ
import random
# 環境変数用ライブラリ
import os
# MySQL用ライブラリ
import pymysql.cursors


def db_connect():
    # DBに接続
    conn = pymysql.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        db=config.db,
        port=config.port,
        charset='utf8',
        cursorclass=pymysql.cursors.Cursor)

    return conn
# end of db_connect


def auto_lot():
    # DBに接続
    conn = db_connect()

    with conn.cursor() as cursor:  # 抽選するプレゼントの種類数を自動取得
        sql = "SELECT COUNT(*) FROM presents"
        cursor.execute(sql)
        result = cursor.fetchone()
    present_count = result[0]

    for i in range(present_count):  # 抽選するプレゼントの種類分ループ
        auto_lot_loop(i + 1, conn)

    conn.close()  # DBから切断
    return
# end of auto_lot


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
# end of auto_lot_loop


def auto_lot8(stock):  # スタンプ8つ集めた人で景品を分配
    # DBに接続
    conn = db_connect()

    with conn.cursor() as cursor:  # 抽選するユーザをDBから取得
        sql = "SELECT user_id, stamps FROM present_user where stamps=%s"
        cursor.execute(sql, (8))
        result = cursor.fetchall()

    lot_base = []

    for i in range(len(result)):
        a = [result[i][0], 1]  # 計算コストの削減
        lot_base.append(a)

    lot_array = make_lot_array(lot_base)
    # print(lot_array)
    remained_stock = lot(stock, lot_array)

    print("Remained stock = " + str(remained_stock))  # 残数表示
    print("")

    conn.close()
    return
# end of auto_lot8


def lot(stock, appliciants):  # int, int[]
    set_seed()
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
# end of lot


def make_lot_array(user_array):  # user_arrayが2次元配列でない場合，型エラー
    lot_array = []
    for i in range(len(user_array)):
        for j in range(0, user_array[i][1]):
            lot_array.append(user_array[i][0])
    return lot_array
# end of make_lot_array


def null_blocker(user_input, value_name):
    if user_input == '':
        print("You must input " + str(value_name) + ". Process cancelled.")
        exit(1)
    return
# end of null_blocker


def set_seed():
    pid = os.getpid()
    dt = datetime.datetime.now()
    da = dt.date()
    random.seed(pid + dt.hour + dt.minute + dt.second +
                dt.microsecond + da.year + da.month + da.day)
    return
# end of set_seed

# main


print("Select lottery mode(Auto:1, Manual:2, Auto8:3).")
mode = input()
null_blocker(mode, "mode")
mode = int(mode)
if mode < 0 or mode > 4:
    print("Illegal operation. Process cancelled.")
    exit(1)
elif mode == 1:
    auto_lot()
elif mode == 2:
    print("Please input remained_stock.")
    stock = input()
    null_blocker(stock, "remained_stock")
    stock = int(stock)
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
elif mode == 3:
    print("Please input remained_stock.")
    stock = input()
    null_blocker(stock, "remained_stock")
    stock = int(stock)
    auto_lot8(stock)
