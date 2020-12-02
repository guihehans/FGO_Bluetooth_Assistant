# FGO_Bluetooth_Helper

这是一个基于python的用于Jenkins CI/CD 流程的运维平台

## Getting Started

以下为部署和运行需求

### Prerequisites

1. window PC机 测试通过环境为win10.
2. 安装anaconda 64位windows运行环境.
3. 为了速度可添加国内源

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

```

### Installing

##### 安装步骤 
- 项目根目录下有conda 移植环境配置文件
environment.yml. 执行命令

```
conda env create -f environment.yml
```

此命令将会创建 conda环境,并安装所有需要的package.

项目路径为/leadbank/jenkins_tool
运行方法为：
```
cd /leadbank/jenkins_tool
/root/anaconda3/envs/jenkins/bin/python app.py [port_num>1024]
```
访问ip:port 可以看见index页面即运行成功。
日志路径在
```
/leadbank/jenkins_tool/log4py/jenkins.log
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Pandas](https://pandas.pydata.org/) - 数据访问以及处理
* [Python jenkins](https://python-jenkins.readthedocs.io/en/latest/index.html) - 用来访问jenkins服务接口
* [Crowd](https://python-crowd.readthedocs.io/en/latest/) - 集成访问现有crowd用户管理系统

## How to use
此平台方便运维简化build,deploy流程,可分为4个模块:

1. 测试环境-预发环境build
2. 预发环境-生产环境build
3. 预发环境deploy
4. 生产环境deploy


## Versioning

1.0.0
## Authors

* **桂鹤** 

## Acknowledgments

* Hat tip to anyone whose code was used
* Hat tip to anyone who is using the code
