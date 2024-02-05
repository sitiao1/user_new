from flask import Flask, request, jsonify
from database import Database

app = Flask(__name__)

# 数据库连接信息
DB_CONFIG = {
    'host': '60.205.59.6',
    'user': 'root',
    'password': 'uxin.com',
    'database': 'uxinlive'
}

# 数据落表
def insert_user(db, type, appid, introduce, requirement_name):
    db.insert_user(type, appid, introduce, requirement_name)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    def validate_type(value, accepted_values):
        if value not in accepted_values:
            return False
            # 如果类型为2，确保 introduce 字段存在且不为 None
        if value == 2 and 'introduce' not in data:
            return False
        return True

    def validate_appid(appid):
        allowed_appids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        if appid not in allowed_appids:
            return False
        return True

    def validate_introduce(introduce, type):
        if type == 2:
            allowed_introduces = [0, 1, 2, 3]
            if introduce not in allowed_introduces:
                return False
        return True

    def validate_requirement_name(requirement_name):
        if not requirement_name:
            return False
        if len(requirement_name) > 30:
            return False
        return True

    type = data.get('type')
    appid = data.get('appid')
    introduce = data.get('introduce')
    requirement_name = data.get('requirement_name')
    print(requirement_name)
    if not validate_type(type, [0, 1, 2]):
        return jsonify({'error': "type 只能输入 0、1 或 2，并且当type为 2 时必须传入 introduce 字段"}), 400
    if not validate_appid(appid):
        return jsonify({'error': "appid错误"}), 400
    if introduce is not None and not validate_introduce(introduce, type):
        return jsonify({'error': "type为2的时候必须传introduce字段，且取值只能为0、1、2、3"}), 400
    if not validate_requirement_name(requirement_name):
        return jsonify({'error': "requirement_name 必须为中文字符，且长度不能超过30个字符"}), 400

    # 如果参数验证通过，将数据写入数据库
    db = Database(**DB_CONFIG)
    if db.connect():
        insert_user(db, type, appid, introduce, requirement_name)
        db.close()
        return jsonify({'message': '新建成功'}), 200
    else:
        return jsonify({'error': '无法连接到数据库'}), 500

if __name__ == '__main__':
    app.run(debug=True)
