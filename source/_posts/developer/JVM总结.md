---
title: JVM总结
categories: developer
tags: [JVM]
keywords: JVM,java堆,java内存
cover: None
date: 2020-04-07 00:33:39
---

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200407003701-runtime_data_area.png)

## 类加载器子系统 Class Loader Sub System

### 加载阶段

   `引导类加载器 Bootstrap Class Loader` `扩展类加载器 Extension Class Loader` `系统类加载器 Application Class Loader`

   根据类的全限定名获取二进制字节流；

   将字节流所代表的静态存储结构转换为方法区的运行时数据结构；

   在内存中生成一个代表这个类的`java.lang.Class`对象，作为方法区这个类的各种数据的访问入口；

   ` 双亲委派机制`

   - 优势
     - 避免类的重复加载
     - 保证程序安全，防止核心api被篡改

### 链接阶段

#### 验证

#### 准备

#### 解析

### 初始化阶段

   `初始化`

## 运行时数据区 Runtime Data Areas

#### 方法区 (method area) | 元数据区 (meta space)

加载的类信息、运行时常量。

#### 堆 (heap)

#### PC寄存器 | 程序计数器 (program counter register)

#### 本地方法栈 (native method stack)

#### 虚拟机栈 (jvm stack)
