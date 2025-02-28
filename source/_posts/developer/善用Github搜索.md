---
title: 善用Github搜索
categories: developer
tags: [Github]
keywords: github搜索
cover: https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200819172745-snipaste_2020-08-19_17-27-26.png
date: 2020-08-19 17:28:40
---

## 常用搜索条件

### 根据repo名称、描述文件、readme搜索

如果省略此限定符，则只搜索`repository name` 和 `description`。

| Qualifier        | Example                              |
| `in:name`        | micronaut in:name                    |
| `in:description` | micronaut in:description             |
| `in:readme`      | micronaut in:readme,name,description |

### 根据repo的owner搜索

| Qualifier         | Example     |
| `user:{userName}` | user:cooocy |
| `org:{orgName}`   | org:graviti |

### 根据编程语言搜索

| Qualifier             | Example |      
| `language:{language}` | language:java |

### 根据Stars数量搜索

| Qualifier   | Example      |
| `stars:{n}` | stars:500    |
|             | stars:0..20  |
|             | stars:>=1000 |

### 根据源代码搜索 (需要登录)

| Qualifier | Example                  |
| `in:file` | requestlogfilter in:file |

## Super Example

```
micronaut in:name,readme,description language:java user:cooocy stars:>=0 requestlogfilter in:file
```

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200819171611-snipaste_2020-08-19_17-15-51.png)

如果实在不知道怎么搜，可以使用 [Github懒人搜索](https://github.com/search/advanced)

## 参考文档

[Searching for repositories](https://docs.github.com/en/github/searching-for-information-on-github/searching-for-repositories)