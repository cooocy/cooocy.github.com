---
title: 基于 SpringAOP，解析对象中的引用字段，还原原始对象
categories: developer
tags: [Spring]
keywords: SpringAOP,对象引用解析
cover: None
date: 2025-01-07 17:14:20
---

项目中经常会写一种数据组装逻辑：根据 ID 或 Name 查询引用数据，并组装到原数据行。比如，这里有一个书籍列表。

```json
[
  {
    "name": "红楼梦",
    "authorId": 12
  },
  {
    "name": "Why Github?",
    "authorId": 13
  }
]
```

我们需要提取列表中的 authorId，并调用某个 RPC 接口或本地接口，查询到对应的用户列表，然后逐一合并，形成最终的数据结构，如

```json
[
  {
    "name": "红楼梦",
    "author": {
      "id": 12,
      "name": "曹雪芹"
    }
  },
  {
    "name": "Why Github?",
    "author": {
      "id": 13,
      "name": "cooocy"
    }
  }
]
```

这种代码既没什么技术含量，又大量重复，并且写多了会污染我们的核心代码。这里提供一个基于 `Spring AOP` 实现的通用处理框架。

## 使用

在基础对象类 `Book` 和 `BookRepository` 中的查询方法中增加如下注解。

```java
class Book {
    String name;
    // 使用 @Ref 表达引用关系
    @Ref(analyzer = UserRepository.class, refField = "id", analysisTo = "author")
    Long authorId;
    @Transient // 不进行持久化, 非必要注解
    UserShadow author;
}

class BookRepository {
    // 使用 @RefAnalysis 对原方法增强, 会被 AOP 拦截
    @RefAnalysis
    List<Book> findAll();
}
```

新增或修改原有的用户查询接口，使之实现 `RefAnalyzer`。

```java
class UserRepository implements RefAnalyzer<UserShadow, User, Long> {

    // 单个查询, 这里使用的 User.id 作为引用关系, 根据实际情况
    Publisher findOne(Long id) {  
    }

    // 批量查询
    List<Publisher> findMany(List<Long> ids) {
    }
    
    // 查询不到用户时, 可以返回 null 或者兜底对象
    User fallback(Long id) {
        return new User(id, "Unknown");
    }
    
    // 有些时候需要做对象转换, 查询到的是 A 对象, 转成 B 对象, 比如一些脱敏场景
    // 如果不需要转换, 可以返回原对象, 记得修改 implements 后的范型参数为 <User, User, Long>
    UserShadow convert(User user) {
        return new UserShadow();
    }

}
```

另外考虑的一些深层引用，还可以使用 `@DeepRef` 进行深层引用，可以参考 github 源码，在最下方提供了链接。

## 源代码

[Rennala](https://github.com/cooocy/rennala)


