---
title: G1 VS ParallelGC 性能对比
categories: developer
tags: [JVM,GC]
keywords: G1,ParallelGC,GC,JVM
cover: None
date: 2020-08-21 14:49:41
---

## 准备这些命令

```
# 查看堆状态和选择的垃圾收集器
jmap -heap <pid>

# 手动执行FGC
jcmd <pid> GC.run

```

## 使用G1收集器

```
java -XX:+UseG1GC -jar demo.jar
```

#### 初始状态
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821143955-image-1.png)

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144008-image-2.png)

#### 压测场景A，单线程循环创建对象，持续600s
程序执行到43s时，抛出了`OutOfMemoryError: Java heap space`，过程终结。
此过程的CPU负载如下图。
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821143911-image.png)

#### 压测场景B，4线程循环创建对象，持续600s
约11min后，CPU负载稳定在0.1%，没有新的GC，4个线程都没有抛出OOM。
此过程的CPU负载如下图。
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144056-image-3.png)

#### 小结
单线程创建对象，一段时候后，会抛出OOM。
多线程创建对象，不会抛出OOM。
两种场景下，CPU负载都维持在比较低的水平。

## 使用ParallelGC收集器

#### 初始状态

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144529-image.png)

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144403-image-1.png)

####压测场景A，单线程循环创建对象，持续600s
约11min后，CPU负载稳定在0.1%，没有新的GC，没有抛出OOM。
此过程CPU负载几乎100%，没有采样。
此过程的GC采样。

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144548-image-2.png)

GC总消耗：
| YGC | YGCT | FGC | FGCT | GCT
| 26 | 3.797 | 156 | 649.261 | 653.058


##  相关代码

```
// seconds = 600, threadCount = 1
public static void boostMem(int seconds, int threadCount) {
    for (int i = 0; i < threadCount; i++) {
        new Thread(() -> {
            List<Object> objects = new ArrayList<>();
            LocalDateTime endTime = LocalDateTime.now().plusSeconds(seconds);
            while (LocalDateTime.now().isBefore(endTime)) {
                objects.add(new Object());
            }
        }).start();
    }
}
```

## 附件

[G1-4-threads.log](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144642-g1-4-threads.log)

[G1-1-thread.log](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144738-g1-1-thread.log)

[g1-cpu负载.numbers](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144806-g1-cpu负载.numbers)

[parallelgc-gc采样.numbers](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200821144829-parallelgc-gc采样.numbers)