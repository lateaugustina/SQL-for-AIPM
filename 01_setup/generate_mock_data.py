# generate_mock_data.py
# Claude生成的AIPM练习用虚拟数据集
# 运行后生成4个CSV文件：users.csv / ai_events.csv / orders.csv / llm_calls.csv
# 使用方法：python generate_mock_data.py
# 适合会python的人，运行后生成csv文件再用IMPORT导入

import random
from datetime import datetime, timedelta
import csv

random.seed(42)

# ── 1. users 表 ──────────────────────────────────────────────────────────────
cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "西安"]
devices = ["iOS", "Android", "Web"]
channels = ["小红书", "抖音", "朋友圈", "应用商店", "朋友推荐"]

start_date = datetime(2026, 1, 1)
n_users = 1000

users = []
for i in range(1, n_users + 1):
    reg_offset = random.randint(0, 180)
    reg_date = start_date + timedelta(days=reg_offset)
    is_paid = random.random() < 0.18
    users.append({
        "user_id": f"U{i:05d}",
        "register_date": reg_date.strftime("%Y-%m-%d"),
        "city": random.choice(cities),
        "device": random.choice(devices),
        "channel": random.choice(channels),
        "is_paid": 1 if is_paid else 0,
    })

with open("users.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=users[0].keys())
    w.writeheader()
    w.writerows(users)

print(f"users.csv 生成完成：{len(users)} 条记录")

# ── 2. ai_events 表 ──────────────────────────────────────────────────────────
features = ["写作助手", "图片生成", "聊天分析", "语音转写", "数据洞察"]

ai_events = []
event_id = 1
for u in users:
    reg_date = datetime.strptime(u["register_date"], "%Y-%m-%d")
    n_events = random.choices([0, 1, 3, 5, 10, 15], weights=[20, 15, 25, 20, 12, 8])[0]
    for _ in range(n_events):
        event_date = reg_date + timedelta(days=random.randint(0, 150))
        if event_date > datetime(2026, 6, 30):
            continue
        feature = random.choice(features)
        funnel_roll = random.random()
        if funnel_roll < 0.5:
            etype = "show"
        elif funnel_roll < 0.8:
            etype = "click"
        else:
            etype = "complete"
        ai_events.append({
            "event_id": event_id,
            "user_id": u["user_id"],
            "feature_name": feature,
            "event_type": etype,
            "event_time": event_date.strftime("%Y-%m-%d %H:%M:%S"),
        })
        event_id += 1

with open("ai_events.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=ai_events[0].keys())
    w.writeheader()
    w.writerows(ai_events)

print(f"ai_events.csv 生成完成：{len(ai_events)} 条记录")

# ── 3. orders 表 ─────────────────────────────────────────────────────────────
plans = ["月度会员", "年度会员", "单次购买"]
plan_price = {"月度会员": 38, "年度会员": 298, "单次购买": 9.9}

orders = []
order_id = 1
for u in users:
    if u["is_paid"] == 0:
        continue
    reg_date = datetime.strptime(u["register_date"], "%Y-%m-%d")
    n_orders = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
    for _ in range(n_orders):
        order_date = reg_date + timedelta(days=random.randint(0, 150))
        if order_date > datetime(2026, 6, 30):
            continue
        plan = random.choice(plans)
        orders.append({
            "order_id": f"O{order_id:06d}",
            "user_id": u["user_id"],
            "plan_type": plan,
            "amount": plan_price[plan],
            "order_time": order_date.strftime("%Y-%m-%d %H:%M:%S"),
        })
        order_id += 1

with open("orders.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=orders[0].keys())
    w.writeheader()
    w.writerows(orders)

print(f"orders.csv 生成完成：{len(orders)} 条记录")

# ── 4. llm_calls 表 ──────────────────────────────────────────────────────────
llm_calls = []
call_id = 1
for e in ai_events:
    if e["event_type"] != "complete":
        continue
    tokens = random.randint(300, 8000)
    resp_time = random.randint(800, 6000)
    llm_calls.append({
        "call_id": call_id,
        "user_id": e["user_id"],
        "feature_name": e["feature_name"],
        "token_count": tokens,
        "response_time_ms": resp_time,
        "call_time": e["event_time"],
    })
    call_id += 1

with open("llm_calls.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=llm_calls[0].keys())
    w.writeheader()
    w.writerows(llm_calls)

print(f"llm_calls.csv 生成完成：{len(llm_calls)} 条记录")
print("\n所有CSV文件生成完成！")
print("接下来将CSV文件导入SQLiteOnline，或使用mock_data_import.sql直接建表。")
