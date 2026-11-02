# Telco Customer Churn \- Schema说明文档

> 这是一份Telco电信公司的客户流失数据集，来自IBM的样本数据。目标是通过分析客户数据，预测哪些客户会流失，从而制定留存策略。虽然是电信数据，但其订阅制商业模式与AI SaaS产品高度相似，分析逻辑可直接迁移到AIPM场景。

# 字段说明

|字段名|类型|业务含义|可能的值|
|---|---|---|---|
|customerid|TEXT|用户ID|7590\-VHVEG、5575\-GNVDE|
|gender|TEXT|用户性别|Male、Female|
|tenure|INTEGER|用户使用时长|1、2、34|
|contract|TEXT|用户套餐类型（单位/月）|Month\-to\-month、One year|
|monthlycharges|REAL|用户月消费金额|29\.85、56\.95|
|churn|TEXT|用户是否流失|Yes、No|
|phoneservice|TEXT|是否包含电话服务|Yes、No|
|internetservice|TEXT|是否包含网络服务|Yes、No|
|onlinesecurity|TEXT|是否包含在线安全服务|Yes、No|
|onlinebackup|TEXT|是否包含在线备份服务|Yes、No|
|techsupport|TEXT|是否包含技术支持服务|Yes、No|
|streamingtv|TEXT|是否包含直播电视服务|Yes、No|
|paymentmethod|TEXT|用户支付方式<br>|Electronic check、Mailed check、Credit card \(automatic\)、Bank transfer \(automatic\)|
|totalcharges|REAL|用户总花费|29\.85、1889\.5|
|seniorcitizen|INTERGER|是否为老年人|1=Yes、0=No|
|dependents|TEXT|是否有受抚养人|Yes、No|
|paperlessbilling|TEXT|是否使用无纸化支付方式|Yes、No|
|multiplelines|TEXT|是否有多条电话线路|Yes、No|
|streamingmovies|TEXT|是否包含直播电影服务|Yes、No|