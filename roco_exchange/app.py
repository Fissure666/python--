import json
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 数据存储文件路径
DATA_FILE = 'trades.json'

def load_data():
    """读取 JSON 文件"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

def save_data(data):
    """写入 JSON 文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 初始加载
trade_list = load_data()

@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    if search_query:
        # 过滤包含关键词的条目
        filtered = [
            t for t in trade_list 
            if search_query.lower() in t['have_pet'].lower() 
            or search_query.lower() in t['want_pet'].lower()
        ]
        return render_template('index.html', trades=filtered, search_query=search_query)
    return render_template('index.html', trades=trade_list)

@app.route('/post', methods=['POST'])
def post_info():
    uid = request.form.get('uid')
    have_pet = request.form.get('have_pet')
    want_pet = request.form.get('want_pet')
    
    if uid and have_pet and want_pet:
        trade_list.append({
            "uid": uid, 
            "have_pet": have_pet, 
            "want_pet": want_pet
        })
        save_data(trade_list) # 永久保存
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
import time

MESSAGES_FILE = 'messages.json'

# 加载留言
def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存留言
def save_messages(messages):
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

@app.route('/send_message', methods=['POST'])
def send_message():
    nickname = request.form.get('nickname', '匿名小洛克')
    content = request.form.get('content')
    
    if content:
        messages = load_messages()
        # 只保留最新的 50 条留言，防止文件过大
        messages.insert(0, {
            "nickname": nickname,
            "content": content,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })
        save_messages(messages[:50])
        
    return redirect(url_status='/')
@app.route('/send_message', methods=['POST'])
def send_message():
    nickname = request.form.get('nickname', '匿名小洛克')
    content = request.form.get('content')
    
    if content:
        messages = load_messages()
        # 插入新留言到列表最前端
        messages.insert(0, {
            "nickname": nickname,
            "content": content,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })
        # 修改这里：保留最新的 100 条留言
        save_messages(messages[:100])
        
    return redirect('/')

@app.route('/')
def index():
    trades = load_trades()
    messages = load_messages()  # 加载新留言
    return render_template('index.html', trades=trades, messages=messages)