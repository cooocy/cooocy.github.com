---
title: git 多账号配置
categories: developer
tags: [git]
keywords: git,git多帐号
cover: https://bk-5lian.oss-cn-shanghai.aliyuncs.com/logo%402x-1569127072212.png
date: 2019-09-22 12:38:04
---

### 不同的公钥对应不同的网站
```ssh
# 使用 ssh-kengen 生成多个密钥，添加进gitee或者github。
# cd ~/.ssh
# touch config 文件，内容如下.
- gitee
Host            gitee.com
Hostname        gitee.com
PreferredAuthentications    publickey
IdentityFile    ~/.ssh/id_rsa_gitee

- github
Host            github.com
Hostname        github.com
PreferredAuthentications    publickey
IdentityFile    ~/.ssh/id_rsa_github
```

### 设置```user.name```和```user.email```
```ssh
# 将gitee的仓库设置为public，clone代码。
# 进入代码目录。
git config user.name demo
git confgi user.email demo@foxmai.com
# 将gitee仓库设置为private。
```