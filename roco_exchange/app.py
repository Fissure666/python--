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