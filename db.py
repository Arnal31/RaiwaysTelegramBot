import sqlite3
import exceptions

conn = sqlite3.connect("city.db", check_same_thread=False)  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


def select_city_id(city):
    sql = "SELECT ID FROM City WHERE name=?"
    cursor.execute(sql, [(city)])
    city_id = cursor.fetchall()
    if not city_id:
        raise exceptions.RouteError
    else:
        return str(city_id[0]).rstrip(",')").lstrip("('")
