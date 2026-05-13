from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import certifi
import os

app = Flask(__name__)

# ✨ 核心：把你在 image_746e3a.png 看到的那串链接贴在这里
# 记得把 <db_password> 换成你设定的数据库密码！
MONGO_URI = "mongodb+srv://Fissure666:5vt4BtcxWcPyBAtB@fissure666.d9j3cva.mongodb.net/?retryWrites=true&w=majority&appName=Fissure666"

# 连接云端
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['rock_kingdom']
    trades_col = db['trades']
    messages_col = db['messages']
    print("✅ 成功连接到云数据库！")
except Exception as e:
    print(f"❌ 连接失败: {e}")

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    
    # 从云端抓取最新的互换和留言（按 ID 倒序排列，最新的在上面）
    all_trades = list(trades_col.find().sort('_id', -1))
    messages = list(messages_col.find().sort('_id', -1))
    
    # 搜索过滤
    if search_query:
        trades = [t for t in all_trades if 
                  search_query in str(t.get('have_pet', '')).lower() or 
                  search_query in str(t.get('want_pet', '')).lower() or 
                  search_query in str(t.get('uid', '')).lower()]
    else:
        trades = all_trades

    return render_template('index.html', messages=messages, trades=trades)

@app.route('/post', methods=['POST'])
def post_trade():
    uid = request.form.get('uid')
    have = request.form.get('have_pet')
    want = request.form.get('want_pet')
    if uid and have and want:
        # 直接存入云端
        trades_col.insert_one({'uid': uid, 'have_pet': have, 'want_pet': want})
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    nickname = request.form.get('nickname')
    content = request.form.get('content')
    if nickname and content:
        # 存入云端留言板
        messages_col.insert_one({'nickname': nickname, 'content': content})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)