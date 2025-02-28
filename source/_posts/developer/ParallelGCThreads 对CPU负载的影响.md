---
title: ParallelGCThreads 对CPU负载的影响
categories: developer
tags: [JVM,GC]
keywords: JVM,GC,ParallelGCThreads
cover: None
date: 2020-07-24 18:34:36
---

## 线上场景
在线上事故发生时，由于JVM一直在进行FGC，导致CPU占用100%，无法使用任何诊断工具进行诊断。

## 猜想
*是否可以通过限制GC的线程数量，达到降低GC时CPU负载的目的？*

## 调查`ParallelGCThreads`的默认值
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182000-image.png)
从官方文档可知，默认值和服务器核心数有关。
*https://www.oracle.com/java/technologies/javase/vmoptions-jsp.html*

#### 继续调查得到如下结论

① 如果用户显示指定了ParallelGCThreads，则使用用户指定的值。

② 否则，需要根据实际的CPU所能够支持的线程数来计算ParallelGCThreads的值，计算方法见步骤③和步骤④。

③ 如果物理CPU所能够支持线程数小于8，则ParallelGCThreads的值为CPU所支持的线程数。这里的阀值为8，是因为JVM中调用nof_parallel_worker_threads接口所传入的switch_pt的值均为8。

④ 如果物理CPU所能够支持线程数大于8，则ParallelGCThreads的值为8加上一个调整值，调整值的计算方式为：物理CPU所支持的线程数减去8所得值的5/8或者5/16，JVM会根据实际的情况来选择具体是乘以5/8还是5/16。

比如，在64线程的x86 CPU上，如果用户未指定ParallelGCThreads的值，则默认的计算方式为：ParallelGCThreads = 8 + (64 - 8) * (5/8) = 8 + 35 = 43。

#### SourceCode
```
unsigned int VM_Version::calc_parallel_worker_threads() {
  unsigned int result;
  if (is_M_series()) {
    // for now, use same gc thread calculation for M-series as for niagara-plus
    // in future, we may want to tweak parameters for nof_parallel_worker_thread
    result = nof_parallel_worker_threads(5, 16, 8);
  } else if (is_niagara_plus()) {
    result = nof_parallel_worker_threads(5, 16, 8);
  } else {
    result = nof_parallel_worker_threads(5, 8, 8);
  }
  return result;
}
unsigned int Abstract_VM_Version::parallel_worker_threads() {
  if (!_parallel_worker_threads_initialized) {
    if (FLAG_IS_DEFAULT(ParallelGCThreads)) {
      _parallel_worker_threads = VM_Version::calc_parallel_worker_threads();
    } else {
      _parallel_worker_threads = ParallelGCThreads;
    }
    _parallel_worker_threads_initialized = true;
  }
  return _parallel_worker_threads;
}
unsigned int Abstract_VM_Version::calc_parallel_worker_threads() {
  return nof_parallel_worker_threads(5, 8, 8);
}
unsigned int Abstract_VM_Version::nof_parallel_worker_threads(
  unsigned int num,
  unsigned int den,
  unsigned int switch_pt) {
  if (FLAG_IS_DEFAULT(ParallelGCThreads)) {
    assert(ParallelGCThreads == 0, "Default ParallelGCThreads is not 0");
    // For very large machines, there are diminishing returns
    // for large numbers of worker threads.  Instead of
    // hogging the whole system, use a fraction of the workers for every
    // processor after the first 8.  For example, on a 72 cpu machine
    // and a chosen fraction of 5/8
    // use 8 + (72 - 8) * (5/8) == 48 worker threads.
    unsigned int ncpus = (unsigned int) os::active_processor_count();
    return (ncpus <= switch_pt) ?
      ncpus : (switch_pt + ((ncpus - switch_pt) * num) / den);
  } else {
    return ParallelGCThreads;
  }
}
```

## 验证猜想
*是否可以通过限制GC的线程数量，达到降低GC时CPU负载的目的？*

#### 准备这些命令

```
# 指定GC线程数量，启动JVM
java -XX:ParallelGCThreads=3 -jar thirdparty.jar

# 查看JVM启动参数
jcmd <processId> VM.flags

# 查看所有GC线程
jstack <processId> | grep GC

# 实时查看GC情况 intervalMS: 采样间隔，毫秒
jstat -gc <processId> <intervalMS>
```

#### 验证方式
启动400个线程，持续3600s，不停地创建对象。
```
    public static void boostMem(int seconds, int threadCount) {
        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                List<Object> objects = new ArrayList<>();
                LocalDateTime endTime = LocalDateTime.now().plusSeconds(seconds);
                while (LocalDateTime.now().isBefore(endTime)) {
                    objects.add(new TestObject());
                }
            }).start();
        }
    }
```

####对照组A
1. `ParallelGCThreads=4`
2. 启动参数
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182226-image.png)
3. GC线程
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182246-image-1.png)
4. 初始状态
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182306-image-2.png)
5. 压测状态
压测约几秒后，开始FGC；
约20s左右，线程总数趋平，没有新的线程出现，CPU时间被GC线程全部占用，CPU负载87%；
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182324-image-3.png)

####对照组B
1. `ParallelGCThreads=3`
2. 启动参数
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182440-image.png)
3. GC线程
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182457-image-1.png)
4. 初始状态
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182511-image-2.png)
5. 压测状态
压测约几秒后，开始FGC；
约20s左右，线程总数趋平，没有新的线程出现，CPU时间被GC线程全部占用，CPU负载70%；
![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20200724182529-image-3.png)

## 结论
在相同负载且不会导致CPU爆满的情况下，更多的ParallelGCThreads会带来更大的CPU开销，推测相应的GC效率也必然更高。
我们可以配置更小的ParallelGCThreads，用GC效率换CPU空闲，让给诊断工具。

## 弊端
更小的ParallelGCThreads会导致正常情况下GC效率下降。并且服务器的核心数不固定，也需要更加灵活的配置方式。