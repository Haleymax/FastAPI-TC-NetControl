# 基于 FastAPI 控制Linux tc实现弱网控制

## 1. 项目概述
通过 FastAPI 框架搭建一个web服务，通过提供接口实现对 Linux 系统
中 tc(traffic control) 工具对调用，实现对特定网卡进行弱网控制
## 2. 环境要求
1. **操作系统**：Linux（推荐Ubuntu 20.02 及以上版本 ）
2. **Python版本**：Python 3.8 以上

## 3. 安装与配置
1. 克隆仓库
```bash
git clone https://github.com/Haleymax/FastAPI-TC-NetControl.git
```
2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```
3. 安装依赖包
```bash
cd FastAPI-TC-NetControl
pip install -r requirements.txt 
```

4. 启动项目
```bash
python manage.py
```

## 4. API接口说明
