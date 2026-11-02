# 5 个 AI SQL 错误的审查案例

本文通过 5 个典型案例，展示 AI 生成 SQL 时常见的业务理解、字段核对和逻辑设计问题。每个案例均包含业务问题、错误 SQL 或错误思路、错误原因、正确做法以及审查清单。

## 案例 1：分组方式缺乏依据

**错误类型：** 分析决策错误

### 业务问题

分析月消费金额与客户流失率之间的关系。

### 错误做法

直接使用等距区间对月消费金额进行分组：

```sql
CASE
  WHEN monthlycharges < 30 THEN '低消费'
  WHEN monthlycharges < 60 THEN '中消费'
  ELSE '高消费'
END
```

### 错误原因

分组边界仅依据 30 的等距区间设定，没有先检查数据分布，导致各组样本量严重不均（示例分组数量为 287、180、174、312、72）。样本量过少的分组会降低结论的稳定性和可信度。

### 正确做法

先查看数据的最小值、最大值、平均值和四分位数，再根据实际分布决定分组边界，使各组样本量尽量均衡。

```sql
-- 先查看数据分布和四分位数
SELECT
  MIN(monthlycharges) AS 最小值,
  MAX(monthlycharges) AS 最大值,
  AVG(monthlycharges) AS 平均值,
  (
    SELECT monthlycharges
    FROM telco
    ORDER BY monthlycharges
    LIMIT 1 OFFSET (SELECT COUNT(*) / 4 FROM telco)
  ) AS Q1,
  (
    SELECT monthlycharges
    FROM telco
    ORDER BY monthlycharges
    LIMIT 1 OFFSET (SELECT COUNT(*) * 3 / 4 FROM telco)
  ) AS Q3
FROM telco;

-- 再基于四分位数确定分组边界，使每组约占 25% 的样本
```

### 审查清单

- 分组前是否检查过数据分布？
- 各组样本量是否均衡，且是否达到最低分析要求（建议每组至少 30 人）？
- 分组边界是否具有业务或统计依据？

## 案例 2：使用了不存在的字段

**错误类型：** 字段审查遗漏

### 业务问题

分析各服务类型对客户流失率的影响。

### 错误 SQL

```sql
SELECT
  '设备保护 deviceprotection' AS 服务名称,
  COUNT(
    CASE
      WHEN deviceprotection = 'Yes' AND churn = 'Yes' THEN 1
    END
  ) AS 订阅且流失
FROM telco
WHERE contract = 'Month-to-month'
  AND tenure <= 3;
```

### 错误原因

生成查询时直接使用了未经 Schema 核对的字段名 `deviceprotection`。如果该字段在实际数据表中不存在，查询会直接报错；即使字段名称相近，也可能导致查询结果与业务含义不一致。

### 正确做法

写 SQL 之前，必须通过 Schema 文档或数据库命令核对字段名，不能仅凭记忆或常见数据集结构进行假设。

```sql
-- 先核对 telco 表的字段
PRAGMA table_info(telco);

-- 确认字段存在且含义正确后，再编写查询
```

### 审查清单

- 所有字段名是否已经通过 `PRAGMA` 或 Schema 文档核对？
- 字段名是否来自实际数据库，而不是来自训练数据或相似项目？
- 字段名称与业务含义是否一致？

## 案例 3：边界值遗漏导致 NULL

**错误类型：** `CASE WHEN` 逻辑漏洞

### 业务问题

按四分位数分组，分析月费与客户流失率之间的关系。

### 错误 SQL

```sql
CASE
  WHEN monthlycharges < 74.95 THEN '③ 53.85-74.95'
  WHEN monthlycharges > 74.95 THEN '④ >74.95'
END
```

### 错误原因

这里使用了 `<` 和 `>`，但没有处理 `monthlycharges = 74.95` 的情况。月费恰好等于 74.95 的用户无法匹配任何条件，最终会得到 `NULL`，造成数据遗漏。

### 正确做法

边界条件应使用 `>=` 或 `<=`，或者通过 `ELSE` 兜底，确保每条记录都能被归类。

```sql
CASE
  WHEN monthlycharges < 74.95 THEN '③ 53.85-74.95'
  ELSE '④ >=74.95'
END
```

### 审查清单

- `CASE WHEN` 是否覆盖了所有可能的值？
- 边界值是否被明确处理？
- 查询结果中是否出现了意外的 `NULL`？

## 案例 4：`UNION ALL` 列名含义混乱

**错误类型：** 多表拼接审查遗漏

### 业务问题

对比性别和家庭成员情况与客户流失率之间的关系。

### 错误 SQL

```sql
SELECT
  CASE
    WHEN gender = 'Female' THEN '女性用户'
    ELSE '男性用户'
  END AS 用户性别,
  ...
FROM telco
GROUP BY 用户性别

UNION ALL

SELECT
  CASE
    WHEN dependents = 'Yes' THEN '家庭用户'
    ELSE '非家庭用户'
  END AS 是否家庭用户,
  ...
FROM telco
GROUP BY 是否家庭用户;
```

### 错误原因

`UNION ALL` 的结果列名以第一段 `SELECT` 的列名为准。因此，第二段关于家庭用户的结果也会显示在“用户性别”列下，导致数据含义混乱，容易误导后续分析。

### 正确做法

统一结果列名，并增加“维度”列，用于区分不同的分析角度。

```sql
SELECT
  '性别' AS 维度,
  CASE
    WHEN gender = 'Female' THEN '女性用户'
    ELSE '男性用户'
  END AS 分类,
  ...
FROM telco

UNION ALL

SELECT
  '是否家庭用户' AS 维度,
  CASE
    WHEN dependents = 'Yes' THEN '家庭用户'
    ELSE '非家庭用户'
  END AS 分类,
  ...
FROM telco;
```

### 审查清单

- `UNION ALL` 的每段 `SELECT` 是否具有相同的列数？
- 第一段查询的列名是否能准确描述所有拼接结果？
- 是否需要增加“维度”列来区分不同分析角度？

## 案例 5：错误理解多值字段

**错误类型：** 字段理解偏差

### 业务问题

分析网络服务类型与客户流失率之间的关系。

### 错误思路

把 `internetservice` 当作普通的 Yes/No 服务字段，按照“已订阅”和“未订阅”进行分析：

```sql
-- 错误：把 internetservice 当作 Yes/No 字段处理
SELECT
  '网络服务 internetservice' AS 服务名称,
  COUNT(
    CASE
      WHEN internetservice = 'Yes' AND churn = 'Yes' THEN 1
    END
  ) AS 订阅且流失,
  COUNT(
    CASE
      WHEN internetservice = 'No' AND churn = 'Yes' THEN 1
    END
  ) AS 未订阅且流失
FROM telco;
```

由于 `internetservice` 中不存在 `Yes` 值，“订阅且流失”会全部返回 0，结果因此失真。

### 错误原因

写查询前没有检查字段的实际取值，想当然地认为该字段只有 Yes/No 两种值。实际上，`internetservice` 的取值为 `DSL`、`Fiber optic` 和 `No`。

### 正确做法

对于不熟悉的字段，先用 `SELECT DISTINCT` 查看实际取值，再根据字段类型设计分析逻辑。

```sql
-- 先查看字段的实际取值
SELECT DISTINCT internetservice
FROM telco;

-- 再根据实际取值进行分组分析
SELECT
  internetservice AS 网络类型,
  COUNT(customerid) AS 用户数,
  ROUND(
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0
    / COUNT(customerid),
    1
  ) AS 流失率
FROM telco
GROUP BY internetservice;
```

### 审查清单

- 是否检查过字段的实际可能值？
- 是否存在想当然假设字段格式的情况？
- 对多值分类字段，是否错误使用了 Yes/No 判断逻辑？

## 总结

以上 5 个案例分别覆盖以下常见问题：

1. 分析分组缺乏数据依据；
2. 使用了未经核对的字段；
3. `CASE WHEN` 边界条件遗漏；
4. `UNION ALL` 拼接后的列名和维度含义混乱；
5. 未验证字段取值，错误理解多值分类字段。

这些问题涵盖了 AIPM 在审查 AI 生成 SQL 时最常见的业务决策、字段核对和逻辑设计风险。
