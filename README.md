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
> 以下均以 python 代码为例
1. 清除全局（所有设备弱网参数信息）
```python
import requests

remove_api = "http://host:port/tc/remove"

try:
    response = requests.get(remove_api)

    if response.status_code == 200:
        print("请求成功")
        try:
            print("响应内容:", response.json())
        except ValueError:
            print("响应内容:", response.text)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)
except requests.RequestException as e:
    print(f"请求发生错误: {e}")
```
> 通过发送get请求不指定参数实现删除全局的配置信息

2. 清除指定设备弱网配置信息
```python
import requests

remove_api = "http://host:port/tc/remove?device=device_ip_address"

try:
    response = requests.get(remove_api)

    if response.status_code == 200:
        print("请求成功")
        try:
            print("响应内容:", response.json())
        except ValueError:
            print("响应内容:", response.text)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)
except requests.RequestException as e:
    print(f"请求发生错误: {e}")

```
> 删除指定设备同样是通过刚刚get请求去实现，不过需要在后面添加上需要删除设备的ip地址

3. 添加弱网参数
```python
import requests

url = "http://host:port/tc"
# 定义 TC 数据，根据实际的 TC 类的字段进行填写
tc_data = {
    "rate": "1Mbps",  # 带宽，根据实际情况修改\
    "loss": 0,
    "ipaddr": "device_ip_address"
}

try:
    # 发送 POST 请求
    response = requests.post(url, json=tc_data)
    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功")
        print("响应内容:", response.json())
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)
except requests.RequestException as e:
    print(f"请求发生错误: {e}")
```
> 通过发送 post 请求将将弱网参数的数据发送过去

4. 所有接口的返回数据类型一致，均为现网卡的配置信息
```json
{
  "success": true,
  "interface": "wlo1",
  "message": {
    "wlo1": {
      "outgoing": {
      },
      "incoming": {
      }
    }
  }
}
```