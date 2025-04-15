from flask import jsonify
from psycopg_pool import ConnectionPool

from mastodongpt.JwtService import create_unsigned_jwt
from mastodongpt.HashService import hash_password

DB_CONFIG = "dbname=postgres user=postgres password=250620 host=localhost port=5432"
pool = ConnectionPool(conninfo=DB_CONFIG, min_size=1, max_size=10)

def save_link(value, type):
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO Link_t (value, type) VALUES (%s, %s)", (value, type))
    conn.commit()
    cur.execute(("SELECT id FROM Link_t WHERE value = %s AND type = %s"), (value, type))
    unique_id = cur.fetchone()[0]
    pool.putconn(conn)
    return unique_id

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

def update_audit_query(query):
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO Chat_Audit (query) VALUES (%s)", (query,))
    conn.commit()
    pool.putconn(conn)

def login_dashboard(data):
    with pool.connection()  as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email_id, password, user_name FROM admin_data WHERE email_id = %s and password=%s", (data['email_id'],hash_password(data['password'],'acs57501')))
            user = cur.fetchone()
            if user:
                payload = {
                    "sub": "masatdongpt-admin",
                    "name": user[2],
                    "admin": True
                }
                token =create_unsigned_jwt(payload)
                return jsonify({"access_token": token})
            else:
                raise Exception("Invalid credentials")

def validate_userName(userName):
    with pool.connection()  as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email_id FROM admin_data WHERE user_name = %s", (userName,))
            user = cur.fetchone()
            if user:
                return True
            else:
                return False