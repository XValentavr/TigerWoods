# -*- coding: utf-8 -*-
import json
import mysql.connector


def database():
    conn = mysql.connector.connect(
        user="root", password="root", host="localhost", port="3306", database="golfbot"
    )
    return conn


def add_golf_user(chat_id, name, username):
    conn = database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO golf_users (chat_id, name, username) VALUES (%s,%s,%s)",
        (chat_id, name, username),
    )
    conn.commit()
    conn.close()
    return


def is_golf_user(chat_id):
    conn = database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM golf_users WHERE chat_id='{}'".format(chat_id))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


def add_golf_train(
        dates, date, time, type, place, latitude, longitude, price, quantity
):
    conn = database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO golf_train (datetime,date,time,type,place,latitude,longitude,price,quantity,users,users_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (
            dates,
            date,
            time,
            type,
            place,
            latitude,
            longitude,
            price,
            quantity,
            "[]",
            "[]",
        ),
    )
    conn.commit()
    conn.close()
    return


def golf_train():
    conn = database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM golf_train")
    result = cursor.fetchall()
    conn.close()
    return result


def golf_train_id(id):
    conn = database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM golf_train WHERE id='{}'".format(id))
    result = cursor.fetchone()
    conn.close()
    return result


def golf_sign(id, chat_id, name, username):
    conn = database()
    cursor = conn.cursor()
    data = {"id": str(chat_id), "name": name, "username": username}
    cursor.execute(
        """UPDATE golf_train SET users=JSON_ARRAY_APPEND(users, '$', '{}'),users_id=JSON_ARRAY_APPEND(users_id, '$', '{}') WHERE id={} """.format(
            json.dumps(data, ensure_ascii=False), chat_id, id
        )
    )
    conn.commit()
    conn.close()
    return


def delete_train(id):
    conn = database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM golf_train WHERE id='{}'".format(id))
    conn.commit()
    conn.close()
    return


def minus(id):
    conn = database()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM golf_train WHERE id='{}'".format(id))
    result = cursor.fetchone()
    cursor.execute(
        """UPDATE golf_train SET quantity='{}' WHERE id='{}'""".format(
            result[0] - 1, id
        )
    )
    conn.commit()
    conn.close()
    return result[0] - 1


def plus(id):
    conn = database()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM golf_train WHERE id='{}'".format(id))
    result = cursor.fetchone()
    cursor.execute(
        """UPDATE golf_train SET quantity='{}' WHERE id='{}'""".format(
            result[0] + 1, id
        )
    )
    conn.commit()
    conn.close()
    return result[0] + 1


def cancel_golf_sign(id, chat_id, name, username):
    conn = database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM golf_train WHERE id='{}'".format(id))
    result = cursor.fetchone()
    users = eval(result[10])
    for i in users:
        if str(chat_id) in i:
            users.remove(i)
    users_id = eval(result[11])
    users_id.remove(str(chat_id))
    cursor.execute(
        """UPDATE golf_train SET users="{}",users_id="{}" WHERE id='{}'""".format(
            users, users_id, id
        )
    )
    conn.commit()
    conn.close()
    return
