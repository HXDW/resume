from flask import Flask, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_logged_in BOOLEAN DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# 注册用户
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"message": "注册成功"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"message": "用户名已存在"}), 400
    finally:
        conn.close()

# 登录
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            c.execute("UPDATE users SET is_logged_in = 1 WHERE username = ?", (username,))
            conn.commit()
            return jsonify({"message": "登录成功"}), 200
        else:
            return jsonify({"message": "用户名或密码错误"}), 401
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return jsonify({"message": "服务器内部错误"}), 500
    finally:
        conn.close()

# 检查登录状态
@app.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    username = request.args.get('username')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT is_logged_in FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user and user[0] == 1:
        return jsonify({"is_logged_in": True}), 200
    return jsonify({"is_logged_in": False}), 200

# 启动服务
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
