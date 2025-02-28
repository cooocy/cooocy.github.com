---
title: Arthas实战教程
categories: developer
tags: [JVM,Java]
keywords: arthas,JVM内存,JVM诊断,JVM调优
cover: None
date: 2020-07-18 10:49:30
---

## 启动
使用以下命令启动，在提示下输入要诊断的目标服务。
```
java -jar arthas-boot.jar
```
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718102718-image.png)

## dashboard
```
dashboard
```
可以直观地看到服务的各种监控数据。
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718102822-image-1.png)

## thread

#### 查看各状态的线程
```
thread --state <threadState>
```
- Example
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718102902-image-2.png)

###### 查看`CPU`占用最高的n个线程及其`stack`信息
```
thread -n <count>
```
- Example
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718102939-image-3.png)
从调用栈可以看到，该服务执行了`BoostUtil.boostCPU2`导致CPU暴增，通过查询code发现，该方法是一个耗时的循环。
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718103411-image-7.png)

## trace
以下主要展示调用链。

###### 跟踪方法的调用链
```
track <class> <method>
```
- Example
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718104020-image.png)
输入命令后，`terminal`会一直处于挂起状态，需要手动退出。
在行首，可以直观地看到每个方法的调用时长。在当前案例中，`BoostUtil.trace()`耗时6015ms。

###### 根据调用耗时过滤
```
track <class> <method> '#cost > <ms>'
```
- Example
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718103109-image-6.png)
两次trace后，调用了同样的api，但由于第二次trace的过滤条件是『耗时大于7000ms』，所以没有输出。

###### trace到若干次后就退出
```
track <class> <method> -n <times>
```
被官方文档骗了，并没有自动退出。

## watch

###### 观测方法的入参和返回值
```
watch <class> <method> "{params,returnObj}" -x <depthOfReadResult>
```
depthOfReadResult: 表示读返回值的递归深度。
- Example
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718104325-image.png)
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718104350-image-1.png)

## monitor
方法执行监控。

###### 监控一定周期内，方法的调用情况
```
monitor -c <cycleSeconds> ink.wulian.demo.micronaut.controller.AgentController trace
```
cycleSeconds: 表示一个统计周期的秒值。
- Example
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718104407-image-2.png)
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718104429-image-3.png)
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718104445-image-4.png)
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200718104554-image-5.png)

## dump
- Example
```
heapdump /tmp/dump.hprof
```
创建dump文件，可以使用`VisualVM`对运行时内存做进一步分析。