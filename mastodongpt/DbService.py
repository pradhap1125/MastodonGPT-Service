from flask import jsonify
from psycopg_pool import ConnectionPool


DB_CONFIG = "dbname=postgres user=postgres password=Chottu@1125 host=localhost port=5432"
pool = ConnectionPool(conninfo=DB_CONFIG, min_size=1, max_size=10)

def save_link(value, type):
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO Link_t (value, type) VALUES (%s, %s)", (value, type))
    conn.commit()
    pool.putconn(conn)

def get_links():

    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Link_t")
    rows = cur.fetchall()
    pool.putconn(conn)
    json_list = []
    for a in rows:
        json_list.append(

            {"id": a[0], "value": a[1], "type": a[2]
             }
        )
    return json_list

def delete_link(id):
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute("DELETE FROM Link_t WHERE id=%s", (id,))
    conn.commit()
    pool.putconn(conn)
    return jsonify(message="Link deleted!")
