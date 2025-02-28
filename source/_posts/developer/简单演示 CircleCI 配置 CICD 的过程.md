---
title: 简单演示 CircleCI 配置 CICD 的过程
categories: developer
tags: [CICD,CircleCI]
keywords: CircleCI,CI,CD,CICD
cover: None
date: 2022-01-11 19:31:05
---

CircleCI （**下面简称 cc**） 是 GitHub 上一个免费的 CICD 平台。这篇文档简单介绍一下配置过程。

配置完成后的最终效果是：

> 在 master 分支 push 代码后，CircleCI 会使用我们自定义的 docker 镜像执行 cicd，并部署到自定义的 ecs 上。ecs 上也是基于 docker 运行的。

## Set Up

1. GitHub 账号
   - 一个 public ｜ private Repository，作为这次演示的 demo 项目。**下面简称 DemoRepo**。
2. 一台拥有公网 ip 的云服务器，**下面简称 ecs**。
   - 安装并启动 Docker
   - 安装 docker-compose
3. DockerHub 账号
   - 此为可选配置。
   - 如果开通了 DockerHub，则可以 push 自定义的镜像，cicd 中的 jobs 都可以基于这个自定义镜像来执行。否则只能基于公共镜像或 cc 的默认环境执行。
4. 一些基本的 linux 操作
   - ssh-keygen
   - ..

## 操作步骤

1. 授权 cc

   这一步主要是授权 cc 访问你的 github repo。授权成功后，在 cc 的主页应该能看到自己的 repo。

   [CircleCI · GitHub Marketplace](https://github.com/marketplace/circleci)

2. 在 DemoRepo 中配置 cc 规则

   这一步的作用是在 DepoRepo 中配置 cc 规则，比如有哪些 jobs、部署到哪儿等等。

   - 在 DemoRepo 根目录创建 `.circleci/config.yml`

     cc 在执行 cicd 时，会读取这个配置文件。

     以下是我实际使用的配置，我们在行内做一些注释。

     ```yaml
     # 指定 cc 的版本。
     # 2.1 支持参数引用，尽量使用 2.1 或之后的版本。
     version: 2.1
     
     # 定义一些参数，在下面会用到。
     # parameters 是固定前缀。
     parameters:
     
       # 定义了一个 runtime-image 的参数。
       # 后续 cicd 中的 test、build 等 job，都是在这个镜像中执行的。这是为了保证与最终部署的环境一致。
       # “ddyul/jdk17-gradle:v3”: 这个镜像是我 push 到 DockerHub 中的，也可以使用 DockerHub 中的公共镜像。
       runtime-image:
         type: string
         default: "ddyul/jdk17-gradle:v3"
     
       # 定义了 一个 depoly-ecs 参数，即最终部署的位置：上文的 ecs.
       # 部署时, 会通过 ssh 登录到这个服务器完成部署。
       deploy-ecs:
         type: string
         default: "47.99.xxx.xxx"
     
     # job 是 workflow 可执行的最小单元，一个完整的 workflow 由若干个 jobs 编排而成。
     jobs:
     
     	# 定义了一个名为 test 的job，运行环境是上文定义的 runtime-image。
       test:
         docker:
           - image: << pipeline.parameters.runtime-image >>
     
         working_directory: ~/repo
     
         environment:
           JVM_OPTS: -Xmx3200m
           TERM: dumb
     
         steps:
         	# git pull DemoRepo
         	# 后续我们会配置 deploy key，否则会提示没有 pull 权限。
         	# 注意：runtime-image 中要安装 git 和 openssh-client，否则无法 pull。
           - checkout
     
           - restore_cache:
               keys:
                 - v1-dependencies-{{ checksum "build.gradle" }}
                 - v1-dependencies-
     
           - run: gradle dependencies
     
           - save_cache:
               paths:
                 - ~/.gradle
               key: v1-dependencies-{{ checksum "build.gradle" }}
     			
     			# 运行 test case
           - run: gradle test
     
       build:
         docker:
           - image: << pipeline.parameters.runtime-image >>
     
         working_directory: ~/repo
     
         steps:
           - checkout
     
           - run: gradle dependencies
     
           - run: gradle build -x test
     
     	# 定义了名为 deploy 的 job。
       deploy:
         # 这个 job 的运行环境不是 docker image，而是一个 machine (machine: true)，因为我们只需要执行 ssh 就行了。
         machine: true
         steps:
         	# ssh 登录 ecs 之后，执行 "cd /opt/apps-run/demo;sh start.sh"
         	# start.sh 后续会补充。
           - run: ssh -o StrictHostKeyChecking=no root@<< pipeline.parameters.deploy-ecs >> "cd /opt/apps-run/demo;sh start.sh"
     
     workflows:
       version: 2.1
     
     	# 定义一个 workflow，由多个 jobs 编排而成。并且仅当 master 分支才执行。
       test-build-and-deploy:
         jobs:
           - test
           - build:
               requires:
                 - test
           - deploy:
               requires:
                 - test
                 - build
               filters:
                 branches:
                   only: master
     ```

     

3. 添加 GitHub Deploy Key

   这一步的作用是让 cc 能够 pull DemoRepo。

   在 cc 主页找到 DemoRepo，点击 Project Settings。

   ![image-20220111182212784](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20220111182213-image-20220111182212784.png)

   点击左侧 SSH Keys，点击添加 Deploy Key，结果如图即可。

   ![image-20220111182301051](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20220111182301-image-20220111182301051.png)

   注意：因为 step 1 已经完成了对 cc 的授权，点击添加 Deploy Key 后，cc 会创建一对 SHA256 key，并把公钥添加到 GitHub Repo 下。
   在 GitHub Repo Settings 中，能够看到 cc 添加的公钥。
   
   ![image-20220111183128195](https://bk-5lian.oss-cn-shanghai.aliyuncs.com/20220111183128-image-20220111183128195.png)
   
4. 添加 ecs ssh key

   这一步是为了让 cc 能够登录到 ecs，执行部署的命令。

   - 在本地使用 ssh-keygen 生成一对公密钥。

   - 将公钥添加到 ecs 的受信列表。即追加到 `~/.ssh/authorized_keys`末尾。

   - 将私钥添加到 cc 中。

     在 cc -> DemoRepo > Project Settings > SSH Keys > Additional SSH Keys 添加。

     注意 **Hostname** 填 ecs 的公网 ip。

5. 其他脚本补充

   *以下脚本仅作参考。*

   - ecs 中的部署脚本

     `/opt/apps-run/demo/start.sh`

     ```shell
     #!/bin/bash
     
     # DemoRepo 源代码路径
     demo_path="/opt/apps/demo"
     # DemoRepo 中的 Dockerfile 目录
     demo_docker_path="docker"
     
     this_path=$(pwd)
     
     cd $demo_path
     git pull
     commit=$(git log --pretty="%h" -n 1)
     cd $this_path
     
     docker build -t apps/demo:$commit -f $demo_path/$demo_docker_path/Dockerfile $demo_path
     
     docker-compose stop
     env IMG_TAG=$commit docker-compose up -d
     ```

     此脚本的主要作用：

     - pull 代码并构建 Docker 镜像，使用 docker-compose 启动镜像。

   - ecs 中的 docker-compose

     `/opt/apps-run/demo/docker-compose.yaml`

     ```yaml
     version: "3.5"
     services:
       yu:
         privileged: true
         image: apps/demo:${IMG_TAG}
         ports:
           - "8050:8080"
           - "8051:8081"
         volumes:
           - /var/log/demo:/workspace/logs
         environment:
           - LANG=en_US.UTF-8
           - ENVIRONMENT=prod
     ```

   - DemoRepo 中的 Dockerfile

     `DemoRepo/docker/Dockerfile`

     ```
     FROM ddyul/jdk17-gradle:v1
     RUN mkdir /workspace
     WORKDIR /workspace
     
     COPY . .
     
     RUN gradle build -x test
     
     ENTRYPOINT java -XX:+UseZGC -jar build/libs/yu.jar
     ```

## 演示

push 代码到 master，应该会触发 cc。

## 尾巴

本文算是 cc 的一个简单的 hello world，如有错误，欢迎指正。

