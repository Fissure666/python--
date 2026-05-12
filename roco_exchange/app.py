from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# 数据存储路径
MSG_FILE = 'messages.json'

def load_messages():
    if os.path.exists(MSG_FILE):
        with open(MSG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_messages(messages):
    with open(MSG_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    messages = load_messages()
    # 这里假设你已经有了 trades 的逻辑，如果没有可以先给个空列表
    return render_template('index.html', messages=messages, trades=[])

@app.route('/send_message', methods=['POST'])
def send_message():
    nickname = request.form.get('nickname')
    content = request.form.get('content')
    
    if not nickname or not content:
        return redirect(url_for('index'))

    messages = load_messages()

    # ✨ 防重复逻辑：如果新内容和最上面一条完全一样，则不保存
    if messages and messages[0]['nickname'] == nickname and messages[0]['content'] == content:
        return redirect(url_for('index'))

    # 插入新留言并保存
    messages.insert(0, {'nickname': nickname, 'content': content})
    save_messages(messages)
    
    # ✨ 核心：必须重定向，防止刷新页面导致重复提交
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)