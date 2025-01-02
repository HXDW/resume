from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'resume_site',
    'charset': 'utf8mb4'
}


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        # 尝试连接数据库
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 插入用户数据
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return jsonify({"message": "注册成功"}), 200

    # 捕获用户名已存在的错误
    except pymysql.err.IntegrityError:
        return jsonify({"message": "用户名已存在"}), 400

    # 捕获数据库连接相关错误
    except pymysql.MySQLError as e:
        print(f"Database error during registration: {e}")
        return jsonify({"message": "数据库连接失败"}), 500

    # 确保连接始终关闭
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        # 尝试连接数据库
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 查询用户
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        # 登录逻辑
        if user:
            cursor.execute("UPDATE users SET is_logged_in = TRUE WHERE username = %s", (username,))
            conn.commit()
            return jsonify({"message": "登录成功"}), 200
        else:
            return jsonify({"message": "用户名或密码错误"}), 401

    # 捕获数据库连接相关错误
    except pymysql.MySQLError as e:
        print(f"Database error during login: {e}")
        return jsonify({"message": "数据库连接失败"}), 500

    # 确保连接始终关闭
    finally:
        if 'conn' in locals() and conn:
            conn.close()


# 检查用户登录状态
@app.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    username = request.args.get('username')

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT is_logged_in FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user[0]:
        return jsonify({"is_logged_in": True}), 200
    return jsonify({"is_logged_in": False}), 200

# 默认路由
@app.route('/')
def home():
    return "Welcome to the Flask App!"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
