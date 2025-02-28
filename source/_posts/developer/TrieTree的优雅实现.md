---
title: TrieTree的优雅实现
categories: developer
tags: [数据结构]
keywords: TrieTree,搜索引擎,前缀匹配,字典树
cover: None
date: 2021-01-25 16:48:52
---


## 背景介绍

我们经常能在Baidu、Google中看到这样的功能。

![image-20210125113204642](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20210125113206-image-20210125113204642.png)

![image-20210125113219883](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20210125113220-image-20210125113219883.png)

用户输入关键字，badiu会根据关键字自动展开联想，给用户相关的搜索提示。

要实现这种功能，我们首先会想到数据库的模糊查询，比如下面这样一条语句。

```sql
select * from hot_indexes where name like '吵架%';
```

这种实现方式，无疑会给数据库造成巨大的查询压力，查询效率也非常低。

## TrieTree

Trie 树，又称前缀树、字典树或单词查找树，是一种树形结构，也是哈希表的变种。

TrieTree可用来解决`在一组字符串集合中快速查找某个字符串`的问题。

![trie_tree_array](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20210125113847-image-20210125113847258.png)

![](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20210125114108-trie_insert.gif)

从前面 Trie 树的图解可以看到， Trie 树的本质就是前缀树，通过提取出字符串的公共前缀（如果有的话），以达到快速匹配字符串的目的。

### TrieTree的特点

- 根节点不包含字符，除根节点外每个节点只包含一个字符。

- 从根节点到某一节点，路径上经过的字符连接起来，为该节点对应的字符串。

- 每个节点的所有子节点包含的字符都不相同，这一点也就保证了相同的前缀能够得到复用。

## TrieTree的数组实现

我们可以使用数组来实现TrieTree。代码如下。

```java
public final class Node {

    /**
     * 小写字母和空格
     */
    private static final int ALPHABET_SIZE = 27;

    private static final char SPACE = ' ';

    /**
     * 当前节点的27个子节点, 可能某些节点为null
     */
    final Node[] children;

    /**
     * 如果当前节点是句子的结尾, 保存这个句子
     */
    String sentence;

    Node() {
        children = new Node[ALPHABET_SIZE];
    }

    /**
     * 判断当前节点是不是一个句子
     */
    boolean isSentence() {
        return sentence != null;
    }

    /**
     * 判断当前节点的下一层中, 是否包含指定字符的节点
     */
    boolean contains(char ch) {
        return children[indexOf(ch)] != null;
    }

    void put(char ch) {
        if (!contains(ch)) {
            children[indexOf(ch)] = new Node();
        }
    }

    /**
     * 获取当前节点的下一层中, 指定字符的节点
     */
    Node next(char ch) {
        return children[indexOf(ch)];
    }

    void collect(Set<String> container) {
        if (sentence != null) {
            container.add(sentence);
        }
        for (int i = 0; i < ALPHABET_SIZE; i++) {
            if (children[i] != null) {
                children[i].collect(container);
            }
        }
    }

    public static int indexOf(char ch) {
        return ch == SPACE ? 26 : ch - 'a';
    }

}

public final class TrieTree {

    private static final Node ROOT = new Node();

    public static void put(String sentence) {
        Node cur = ROOT;
        for (int i = 0; i < sentence.length(); i++) {
            char ch = sentence.charAt(i);
            if (!cur.contains(ch)) {
                cur.put(ch);
            }
            cur = cur.children[Node.indexOf(ch)];
        }
        if (!cur.isSentence()) {
            cur.sentence = sentence;
        }
    }

    public static Set<String> collect(String prefix) {
        Node cur = ROOT;
        char ch;
        for (int i = 0; i < prefix.length(); i++) {
            ch = prefix.charAt(i);
            if (!cur.contains(ch)) {
                return Collections.emptySet();
            }
            cur = cur.next(ch);
        }
        HashSet<String> container = new HashSet<>();
        cur.collect(container);
        return container;
    }

}
```

这是我尝试的第一个版本。

### 优点

- 查询极快。

### 缺点

- 由于数据是一个固定的长度，不方便扩充字符集。一些特殊字符也要做单独的处理。
- 如果要扩展字符集，需要重写`Node.indexof()`和`Node.ALPHABET_SIZE`，违反开闭原则。

## TrieTree的Hash实现

```java
public final class Node {

    /**
     * 当前节点的所有子节点, 某些子节点可能为null
     */
    protected final Map<Character, Node> children;

    /**
     * 如果当前节点是句子的结尾, 保存这个句子
     */
    protected String sentence;

    protected Node() {
        children = new HashMap<>();
    }

    /**
     * 判断当前节点是不是一个句子
     */
    protected boolean isSentence() {
        return sentence != null;
    }

    /**
     * 将指定字符添加到当前节点的下一层(children)
     */
    protected void put(char ch) {
        if (!contains(ch)) {
            children.put(ch, new Node());
        }
    }

    /**
     * 判断当前节点的下一层中, 是否包含指定字符的节点
     */
    protected boolean contains(char ch) {
        return children.get(ch) != null;
    }

    /**
     * 获取当前节点的下一层中, 指定字符的节点
     */
    protected Node nextLevel(char ch) {
        return children.get(ch);
    }

    protected Set<String> collect() {
        HashSet<String> container = new HashSet<>();
        collect(container);
        return container;
    }

    private void collect(Set<String> container) {
        if (sentence != null) {
            container.add(sentence);
        }
        children.forEach((ch, node) -> children.get(ch).collect(container));
    }

}

public final class TrieTree {

    private static final Node ROOT = new Node();

    public static void put(String sentence) {
        sentence = format(sentence);
        if (!sentence.isBlank()) {
            Node cur = ROOT;
            for (int i = 0; i < sentence.length(); i++) {
                char ch = sentence.charAt(i);
                if (!cur.contains(ch)) {
                    cur.put(ch);
                }
                cur = cur.children.get(ch);
            }
            if (!cur.isSentence()) {
                cur.sentence = sentence;
            }
        }
    }

    public static Set<String> collect(String prefix) {
        prefix = format(prefix);
        Node cur = ROOT;
        char ch;
        for (int i = 0; i < prefix.length(); i++) {
            ch = prefix.charAt(i);
            if (!cur.contains(ch)) {
                return Collections.emptySet();
            }
            cur = cur.nextLevel(ch);
        }
        return cur.collect();
    }

    private static String format(String sentence) {
        return sentence.toLowerCase();
    }

}
```

使用HashMap代替数组，理论上能够支持所有字符集。

但是，这种实现方式耦合也非常严重，不方便进行扩展。因为Node中只有`sentence`这一个有效字段，如果我想在Node中承载别的信息，这种结构是不支持的。

### 反思现在的设计

1. Node本身是一个数据结构，就像数组、字典一样。在这里却和sentence绑定在一起了，耦合非常严重。
2. 无法在Node中承载更多信息(比如词频)，只能是一个字符串。
3. Node不能复用。而任何一个数据结构都应该是可以复用的。

回到一开始的问题，我们需要的是一种数据结构，这种数据结构能够根据前缀进行快速搜索。这个结构本身仅仅是一个容器，和数组、字典一样，没有任何业务含义。

## 更好的设计，结构和业务脱离

```java
/**
 * extends this class and then can be associated in TrieTree.
 * e.g:
 * ** [(value=x, frequency=0), (value=y, frequency=1), (value=z, frequency=2)]
 * ** sort:
 * ** [(value=z, frequency=2), (value=y, frequency=1), (value=x, frequency=0)]
 */
public abstract class Associable implements Comparable<Associable> {

    private static final int DEFAULT_FREQUENCY = 0;

    /**
     * value of this associable object. Can be a sentence, a word...
     */
    public final String value;

    /**
     * frequency of this associable object. The higher value has the higher priority.
     */
    public final int frequency;

    public Associable(String value, int frequency) {
        value = format(value);
        if (value.isBlank()) {
            throw new IllegalArgumentException("value can not be blank");
        }
        if (frequency < 0) {
            throw new IllegalArgumentException("frequency can not lt 0");
        }
        this.value = value;
        this.frequency = frequency;
    }

    public Associable(String value) {
        this(value, DEFAULT_FREQUENCY);
    }

    @Override
    public final int compareTo(Associable associable) {
        return associable.frequency - frequency;
    }

    public static String format(String value) {
        return value.toLowerCase();
    }

}


public class Prefix {

    public final String value;

    public Prefix(String value) {
        value = Associable.format(value);
        if (value.isBlank()) {
            throw new IllegalArgumentException("value can not be blank");
        }
        this.value = value;
    }

}


public final class Node<T extends Associable> {

    /**
     * 当前节点的所有子节点, 某些子节点可能为null
     */
    protected final Map<Character, Node<T>> children;

    /**
     * 如果当前节点是句子的结尾, 保存这个句子
     */
    protected T associable;

    protected Node() {
        children = new HashMap<>();
    }

    /**
     * 判断当前节点是不是一个句子
     */
    protected boolean isSentence() {
        return associable != null;
    }

    /**
     * 获取当前节点的句子
     */
    protected Optional<T> getSentence() {
        return Optional.ofNullable(associable);
    }

    /**
     * 将指定字符添加到当前节点的下一层(children)
     */
    protected void put(char ch) {
        if (!contains(ch)) {
            children.put(ch, new Node<>());
        }
    }

    /**
     * 判断当前节点的下一层中, 是否包含指定字符的节点
     */
    protected boolean contains(char ch) {
        return children.get(ch) != null;
    }

    /**
     * 获取当前节点的下一层中, 指定字符的节点
     */
    protected Node<T> nextLevel(char ch) {
        return children.get(ch);
    }

    /**
     * 收集当前节点下的所有句子, 如果当前节点也是句子, 加入
     * 如果container.size() = limit, 停止收集
     */
    protected List<T> collect(int limit) {
        PriorityQueue<T> priorityQueue = new PriorityQueue<>();
        collect(priorityQueue);
        int min = Math.min(priorityQueue.size(), limit);
        List<T> topSentences = new ArrayList<>(min);
        for (int i = 0; i < min; i++) topSentences.add(priorityQueue.poll());
        return topSentences;
    }

    private void collect(PriorityQueue<T> priorityQueue) {
        if (associable != null) {
            priorityQueue.add(associable);
        }
        children.forEach((ch, node) -> children.get(ch).collect(priorityQueue));
    }

}


public class TrieTree<T extends Associable> {

    private Node<T> root = new Node<>();

    private long size = 0;

    public void reset() {
        root = new Node<>();
        size = 0;
    }

    public void put(T t) {
        String value = t.value;
        Node<T> cur = root;
        for (int i = 0; i < value.length(); i++) {
            char ch = value.charAt(i);
            if (!cur.contains(ch)) {
                cur.put(ch);
            }
            cur = cur.children.get(ch);
        }
        if (!cur.isSentence()) {
            cur.associable = t;
            size++;
        }
    }

    /**
     * 获取所有符合指定前缀的句子
     */
    public List<T> collect(Prefix prefix) {
        return collect(prefix, Integer.MAX_VALUE);
    }

    public List<T> collect(Prefix prefix, int limit) {
        String value = prefix.value;
        Node<T> cur = root;
        char ch;
        for (int i = 0; i < value.length(); i++) {
            ch = value.charAt(i);
            if (!cur.contains(ch)) {
                return Collections.emptyList();
            }
            cur = cur.nextLevel(ch);
        }
        return cur.collect(limit);
    }

}


public final class Dataset extends Associable {

    public Dataset(String name, int frequency) {
        super(name, frequency);
    }

    @Override
    public String toString() {
        return "Dataset{" +
                "name='" + value + '\'' +
                ", frequency=" + frequency +
                '}';
    }

}
```

## Github源码
[cooocy/trie-tree-search](https://github.com/cooocy/trie-tree-search)