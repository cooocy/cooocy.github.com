---
title: 使用profiles和explain查看并验证MySQL回表效率
categories: developer
tags: [MySQL]
keywords: MySQL,profiles,explain,回表
cover: None
date: 2020-10-11 12:46:41
---

#### 操作步骤

1. 打开profiling

   ```sql
   - 查看并打开profiling开关。会话关闭后，profiling会自动关闭。
   show variables like 'profiling';
   set profiling = 'ON';
   ```

2. 执行SQL

3. 查看执行效率

   ```sql
   show profiles;
   ```

#### 案例

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20201011122409-01.png)

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20201011122503-02.png)

## 使用`explain`，验证非覆盖索引下的回表性能

#### 数据库现场

`Innodb`引擎；一张370W数据的表，主键聚簇索引，ppid二级索引。

所有数据的ppid均相同，则非覆盖索引查询时，会最大化回表次数，放大性能差距。

对比以下两条SQL的执行效率。

```sql
select id from tbl where ppid = 'ppid-example';
select insert_time from tbl where ppid = 'ppid-example';
```

#### 结果

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20201011123510-企业微信截图_de3c929b-bedb-490f-be31-26197017977e.png)

对比2、4两条SQL，发现执行时间相差巨大。多余的时间是由逐次回表导致的。

使用`explain`查看执行计划，也可以从旁验证。

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20201011123747-企业微信截图_7af95faa-7fd9-4074-9dd7-6489fbdf0c60.png)