from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import certifi
import os

app = Flask(__name__)

# 🔒 请确保这里的密码已在 MongoDB "Database Access" 中重置并替换
MONGO_URI = "mongodb+srv://Fissure666:5vt4BtcxWcPyBAtB@fissure666.d9j3cva.mongodb.net/?retryWrites=true&w=majority&appName=Fissure666"

# 连接云端 MongoDB
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['rock_kingdom']
    trades_col = db['trades']
    messages_col = db['messages']
    print("✅ 云数据库连接成功！")
except Exception as e:
    print(f"❌ 连接失败: {e}")

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower().strip()
    
    # 获取数据（按 ID 倒序排列，确保最新消息在最上方）
    all_trades = list(trades_col.find().sort('_id', -1))
    messages = list(messages_col.find().sort('_id', -1))
    
    # 强化搜索：支持 UID、精灵名、性格、奖牌标签搜索
    if search_query:
        trades = [t for t in all_trades if 
                  search_query in str(t.get('uid', '')).lower() or 
                  search_query in str(t.get('have_pet', '')).lower() or 
                  search_query in str(t.get('want_pet', '')).lower()]
    else:
        trades = all_trades

    return render_template('index.html', messages=messages, trades=trades)

@app.route('/post', methods=['POST'])
def post_trade():
    uid = request.form.get('uid')
    have = request.form.get('have_pet')
    want = request.form.get('want_pet')
    if uid and have and want:
        # 存入 MongoDB
        trades_col.insert_one({'uid': uid, 'have_pet': have, 'want_pet': want})
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    nickname = request.form.get('nickname')
    content = request.form.get('content')
    if nickname and content:
        messages_col.insert_one({'nickname': nickname, 'content': content})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)