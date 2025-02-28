---
title: 推荐几个常用的 zsh 插件
categories: developer
tags: [zsh,on-my-zsh]
keywords: zsh,on-my-zsh
cover: None
date: 2022-11-03 07:17:47
---

推荐几个好用的 zsh 插件，安装以 [Oh My Zsh](https://ohmyz.sh/) 为例。

#### zsh-autosuggestions

自动补全插件，必备单品。

<img src="https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20221103061000.png" alt="image-20221103060959846" style="zoom:50%;" />

输入部分命令，按方向键右➡️。

###### 安装

```shell
omz plugin enable zsh-autosuggestions
```

#### zsh-syntax-highlighting

高亮插件，必备单品。

###### 安装

```shell
omz plugin enable zsh-syntax-highlighting
```

#### gitignore

一行命令自动下载 gitignore 模板，简化了新建项目时配置 gitignore 的麻烦。

###### 使用

```shell
gi python > python.ignore
gi java > java.ignore
```

插件会自动下载对应的模板文件到指定文件。

###### 安装

```
omz plugin enable gitignore
```

#### git-open

通过命令打开 git repository 的 web 页面，目前支持以下 hosts。

- github.com
- gist.github.com
- gitlab.com
- GitLab custom hosted (see below)
- bitbucket.org
- Atlassian Bitbucket Server (formerly _Atlassian Stash_)
- Visual Studio Team Services
- Team Foundation Server (on-premises)
- AWS Code Commit

###### 使用

```shell
# cd 到某个 git 项目下
git open
# 会调用浏览器打开对应的 web 页面
```

###### 安装

```shell
git clone https://github.com/paulirish/git-open.git $ZSH_CUSTOM/plugins/git-open
# e.g. git clone https://github.com/paulirish/git-open.git ~/.oh-my-zsh/plugins/git-open
omz plugin enable git-open
```

#### hitokoto/rand-quote

从 [hitokoto.cn](https://hitokoto.cn/) 或 [Random Quotes](http://www.quotationspage.com/random.php) 随机获取一句话，配合 cowsay 使用，可在每次启动 zsh 时让小牛对你打招呼~~

<img src="https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20221103070404.png" alt="image-20221103070404304" style="zoom:50%;" />

###### 安装及配置

1. 安装 hitokoto 或 rand-quote

   ```shell
   omz plugin enable hitokoto
   # or
   omz plugin enable rand-quote
   ```

​	注意：*这两个插件装一个即可。hitokoto 提供的是中文社区的句子，rand-quote 提供的是英文社区的句子。*

2. 安装 cowsay

   ```shell
   brew install cowsay
   # or
   npm install -g cowsay
   ```

3. 在 .zshrc 最后一行添加

   ```shell
   quote | cowsay
   # or 
   hitokoto | cowsay
   ```

#### web-search

使用命令直接搜索 google/baidu/github 等网站。

###### 使用

```shell
github web-search
google hello
baidu 你好
...
```

具体支持的网站可使用 `omz plugin info web-search` 查询。

###### 安装

```shell
omz plugin enable web-search
```

#### z

快速跳转到常用的目录。

<img src="https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20221103071137.png" alt="image-20221103071137053" style="zoom:50%;" />



###### 安装

```shell
omz plugin enable z
```
