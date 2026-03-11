# --- 我的第一个收银程序 (Cashier System v1.0) ---

while True:
    # 1. 获取输入（模拟扫码）
    name = input("商品名称 (Item): ")
    price = int(input("商品原价 (Price): "))
    
    # 2. 逻辑处理（模拟会员折扣）
    if price > 100:
        price = price - 20
        print("恭喜！触发满100减20优惠！")
        
    # 3. 结果输出（模拟打印小票）
    print(">>> " + name + " 的最终应付金额为:", price)
    print("-" * 20)  # 打印一条分割线，看起来更像小票