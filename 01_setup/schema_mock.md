# 什么是 Schema 说明文档

> 数据库的【目录说明书】，说明该数据库里有哪些表、每张表有哪些字段、每个字段存的是什么意思
# 数据库 Schema 说明文档

> 这是一个虚构的AI产品模拟数据库，涵盖写作助手、图片生成、聊天分析、语音转写、数据洞察五个AI功能，用于AIPM数据分析练习。共4张表，1000名用户，时间范围2026年1月-6月。


---

## 数据类型说明

| 类型 | 含义 | 举例 |
|------|------|------|
| TEXT | 文字/字符串 | "北京"、"U00001"、"2026-01-15" |
| INTEGER | 整数 | 0、1、495 |
| REAL | 小数 | 9.9、38.0、298.0 |

---

## 表1：users（用户基础信息）

**业务含义：** 每一行代表一个注册用户，记录用户的基本属性信息。

| cid | 字段名 | 类型 | 业务含义 | 可能的值 |
|-----|--------|------|----------|----------|
| 0 | user_id | TEXT | 用户唯一识别码 | U00001 ~ U01000 |
| 1 | register_date | TEXT | 注册日期，格式YYYY-MM-DD | 2026-01-01 ~ 2026-06-30 |
| 2 | city | TEXT | 注册时所在城市 | 北京/上海/广州/深圳/杭州/成都/武汉/西安 |
| 3 | device | TEXT | 使用设备类型 | iOS / Android / Web |
| 4 | channel | TEXT | 用户从哪个渠道注册的 | 小红书/抖音/朋友圈/应用商店/朋友推荐 |
| 5 | is_paid | INTEGER | 是否付费用户 | 1=付费用户，0=免费用户 |

**注意事项：**
- `is_paid` 是静态标签，只代表"曾经付费过"，不代表"当前订阅有效"
- 如果要查"当前有效付费用户"，需要关联 orders 表看最近订单时间

---

## 表2：ai_events（AI功能使用日志）

**业务含义：** 每一行代表一次用户与AI功能的交互行为，记录了完整的功能使用漏斗（曝光→点击→完成）。

| cid | 字段名 | 类型 | 业务含义 | 可能的值 |
|-----|--------|------|----------|----------|
| 0 | event_id | INTEGER | 事件唯一ID | 自增整数 |
| 1 | user_id | TEXT | 触发该事件的用户 | 关联 users.user_id |
| 2 | feature_name | TEXT | 使用的AI功能名称 | 写作助手/图片生成/聊天分析/语音转写/数据洞察 |
| 3 | event_type | TEXT | 用户行为类型（漏斗步骤） | show=曝光，click=点击，complete=完成 |
| 4 | event_time | TEXT | 事件发生时间，格式YYYY-MM-DD HH:MM:SS | 2026-01-01 00:00:00 起 |

**注意事项：**
- 漏斗逻辑：show → click → complete，转化率依次递减
- 同一个用户对同一个功能可能有多条记录（多次使用）
- 做DAU分析时需要用 `COUNT(DISTINCT user_id)` 去重，不能直接 `COUNT(*)`

---

## 表3：orders（付费订单）

**业务含义：** 每一行代表一笔付费订单，只有 is_paid=1 的用户会有对应订单记录。

| cid | 字段名 | 类型 | 业务含义 | 可能的值 |
|-----|--------|------|----------|----------|
| 0 | order_id | TEXT | 订单唯一ID | O000001 起 |
| 1 | user_id | TEXT | 下单用户 | 关联 users.user_id |
| 2 | plan_type | TEXT | 购买的套餐类型 | 月度会员/年度会员/单次购买 |
| 3 | amount | REAL | 订单金额（元） | 9.9=单次，38.0=月度，298.0=年度 |
| 4 | order_time | TEXT | 下单时间，格式YYYY-MM-DD HH:MM:SS | 2026-01-01 00:00:00 起 |

**注意事项：**
- 一个用户可能有多笔订单（复购）
- `amount` 是 REAL 类型，计算收入时用 `SUM(amount)`
- 和 users 表通过 `user_id` 关联

---

## 表4：llm_calls（大模型调用记录）

**业务含义：** 每一行代表一次大模型API调用，只有用户完成（complete）AI功能使用时才会产生调用记录，用于分析AI功能的成本和性能。

| cid | 字段名 | 类型 | 业务含义 | 可能的值 |
|-----|--------|------|----------|----------|
| 0 | call_id | INTEGER | 调用唯一ID | 自增整数 |
| 1 | user_id | TEXT | 触发调用的用户 | 关联 users.user_id |
| 2 | feature_name | TEXT | 哪个AI功能触发的调用 | 写作助手/图片生成/聊天分析/语音转写/数据洞察 |
| 3 | token_count | INTEGER | 本次调用消耗的token数 | 300 ~ 8000 |
| 4 | response_time_ms | INTEGER | 模型响应时间（毫秒） | 800 ~ 6000 |
| 5 | call_time | TEXT | 调用时间，格式YYYY-MM-DD HH:MM:SS | 2026-01-01 00:00:00 起 |

**注意事项：**
- token_count 用于计算API成本：成本（美元）= token_count × 0.002 / 1000
- response_time_ms 越大说明响应越慢，用户体验越差
- 和 ai_events 表的关系：ai_events.event_type = 'complete' 时才产生 llm_calls 记录

---

## 表关系总览

```
users（主表）
  ├── ai_events（通过 user_id 关联）
  │     └── llm_calls（通过 user_id + feature_name 关联）
  └── orders（通过 user_id 关联）
```

**核心关联字段：**
- `users.user_id` = `ai_events.user_id` = `orders.user_id` = `llm_calls.user_id`
- 做跨表分析时，user_id 是所有表之间的桥梁

---

## 常见分析场景 × 需要用到的字段

| 业务问题 | 需要的表 | 关键字段 |
|----------|----------|----------|
| 各渠道用户数和付费率 | users | channel, is_paid |
| AI功能使用漏斗 | ai_events | feature_name, event_type |
| 各功能日活用户数 | ai_events | feature_name, event_time, user_id |
| 总收入和客单价 | orders | amount |
| 付费用户的功能使用偏好 | users + ai_events | is_paid, feature_name |
| 各功能API调用成本 | llm_calls | feature_name, token_count |
| 用户从注册到首次付费的时间 | users + orders | register_date, order_time |
