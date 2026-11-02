# 环境搭建

## 练习工具
https://sqliteonline.com/
![SQLiteOnline界面说明](images/sqliteonline_interface.png)
在中间代码框输入SQL，点击左上角绿色Run按钮执行。

## 数据集说明

**1/ 虚拟数据集 generate_mock_data.py**

数据说明：这是一个虚构的AI产品模拟数据库，涵盖写作助手、图片生成、聊天分析、语音转写、数据洞察五个AI功能，用于AIPM数据分析练习。共4张表，1000名用户，时间范围2026年1月-6月。

数据来源：Claude生成

练习语法：SELECT/FROM/GROUP BY/ORDER BY/ROUND/COUNT/CASE WHEN/JOIN

业务练习：回答「用户从哪里来」的问题

阶段目标：熟悉界面功能、基础语法、建立数据直觉

**2/ 真实样本数据集 telco_import.sql**

数据说明：一份Telco电信公司的客户流失数据集，来自IBM的样本数据。目标是通过分析客户数据，预测哪些客户会流失，从而制定留存策略。

和AIPM场景的对应关系：虽然是电信数据，但其订阅制商业模式与AI SaaS产品高度相似，分析逻辑可直接迁移到AIPM场景。

数据来源：https://www.kaggle.com/datasets/blastchar/telco-customer-churn

涉及语法：LIMIT/GROUP BY + COUNT/CASE WHEN/ROUND/WHERE/GROUP BY + AVG/ORDER BY/多维度GROUP BY/WHERE + 条件筛选/AVG()

阶段目标：学习主要语法、完成业务问题、生成可视化报告

## 导入步骤

首先检测环境是否干净可用

```sql
SELECT 1+1;
```

**方式一：粘贴源码建表**

-> mock_data_import.sql 和 telco_import.sql
适合不会Python、想直接开始练SQL的人，复制粘贴即可运行

1/ 建表

```sql
CREATE TABLE 表名 (
  字段名1 数据类型,
  字段名2 数据类型,
  ...
);
```

2/ 插入数据

```sql
INSERT INTO 表名 (字段1, 字段2, ...) VALUES
(值1, 值2, ...),
(值1, 值2, ...);
```

3/ 验证所有表格都有数据

单张表查询行数：

```sql
SELECT COUNT(*) FROM 表名;
```

多张表同时查：

```sql
SELECT '表A的标签' AS 表名, COUNT(*) AS 数据条数 FROM 表A
UNION ALL
SELECT '表B的标签', COUNT(*) FROM 表B
UNION ALL
SELECT '表C的标签', COUNT(*) FROM 表C;
```

4/ 查出表结构

```sql
PRAGMA table_info(表名);
```

**方式二：使用界面按钮「IMPORT」导入CSV表格**

-> 适合会Python的人，先运行 generate_mock_data.py 生成CSV文件，再用IMPORT按钮导入

-> Telco数据集CSV文件请从Kaggle自行下载：
https://www.kaggle.com/datasets/blastchar/telco-customer-churn

虚拟数据集CSV文件可通过运行 generate_mock_data.py 自动生成