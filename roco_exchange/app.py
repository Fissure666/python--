from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

MSG_FILE = 'messages.json'
TRADE_FILE = 'trades.json' # 假设你的互换数据存这里

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    messages = load_data(MSG_FILE)
    all_trades = load_data(TRADE_FILE)
    
    # 搜索过滤逻辑
    if search_query:
        trades = [t for t in all_trades if 
                  search_query in t.get('have_pet', '').lower() or 
                  search_query in t.get('want_pet', '').lower() or 
                  search_query in t.get('uid', '').lower()]
    else:
        trades = all_trades

    return render_template('index.html', messages=messages, trades=trades)

@app.route('/send_message', methods=['POST'])
def send_message():
    nickname = request.form.get('nickname')
    content = request.form.get('content')
    if nickname and content:
        messages = load_data(MSG_FILE)
        # 防重复：如果内容和第一条一样，不存
        if not (messages and messages[0]['content'] == content):
            messages.insert(0, {'nickname': nickname, 'content': content})
            save_data(MSG_FILE, messages)
    return redirect(url_for('index'))

@app.route('/post', methods=['POST'])
def post_trade():
    uid = request.form.get('uid')
    have = request.form.get('have_pet')
    want = request.form.get('want_pet')
    if uid and have and want:
        trades = load_data(TRADE_FILE)
        trades.insert(0, {'uid': uid, 'have_pet': have, 'want_pet': want})
        save_data(TRADE_FILE, trades)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)