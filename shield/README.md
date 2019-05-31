# Shield

其前身战略科学军团（Strategic Scientific Reserve，简称S.S.R. ，二战时期的组织（详见美国队长和特工卡特）)。  

![神盾局](https://vignette.wikia.nocookie.net/marvelcinematicuniverse/images/5/51/SHIELD_Profile.png/revision/latest/scale-to-width-down/310?cb=20160424134326)

1991年改为战略危险干预与谍报后勤处（Strategic, Hazard Intervention, Espionage Logistics Directorate）  
在2008年上映的《钢铁侠》电影里为国土战略防御攻击与后勤保障局（Strategic Homeland Intervention, Enforcement and Logistics Division），缩写为S.H.I.E.L.D.，由于Shield英文意为盾牌，故翻译为神盾局。  

# usage
将之前写的后端部分专门提出来了一个基础框架部分。单独作为一个项目来存储。  
以后启新项目的时候，直接使用下面的命令就可以开始一个新项目了：
```
git clone git@github.com:forminute/shield.git preview-server
cd preview-server
git remote rename origin base 
git remote add origin git@github.com:forminute/preview-server.git
git push origin master
```
另一种使用方式(已经创建好了项目的情况):
```
git remote add base git@github.com:forminute/shield.git
git fetch base
git merge base/master --allow-unrelated-histories
```
# docker-compose部署
这里推荐一种基于`docker-compose`部署的方式。部署简单方便，特别适合项目初期，等项目做到稳定了之后可以很简单的迁移到`k8s`集群.
1. 增加默认的运行tornado的镜像以及一个运行定时任务`crontab`的镜像（Dockerfile在docker文件夹里面）
2. Makefile增加打包镜像以及fetch-code等常用命令
3. 编辑`docker-compose.yml`配置依赖的服务。包括自带的rabbitmq，mysql, redis(非必须)，以及负载均衡器`jwilder/nginx-proxy:alpine`，还有定时任务
4. 使用`docker-compose up -d --scale shield=2`部署服务
5. 平时使用`make fetch-code`和`make restart-shield`重启服务
6. 往`k8s`迁移的时候，增加一个`Dockerfile`将代码打包到镜像，同时增加打包镜像和推送到`registry`的命令


