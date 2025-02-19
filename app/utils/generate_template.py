from dominate import document
from dominate.tags import h1, h2, h3, table, tr, th, td, style

def generate_network_interface_html(data):
    # 创建文档
    doc = document(title='Network Interface Data')

    # 添加样式
    doc.head += style("""
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-family: Arial, sans-serif;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f4f4f4;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        h1, h2, h3 {
            font-family: Arial, sans-serif;
            color: #333;
        }
        h1 {
            font-size: 24px;
        }
        h2 {
            font-size: 20px;
        }
        h3 {
            font-size: 18px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
    """)

    for interface, traffic_data in data.items():
        # 添加主标题
        doc += h1(f"Network Interface: {interface}")

        # 生成表格的函数
        def generate_table(title, data):
            nonlocal doc
            with doc:
                h2(title)
                if data:  # 如果数据不为空
                    for key, value in data.items():
                        # 提取 IP 地址作为标题
                        if "dst_network=" in key:
                            ip_address = key.split("dst_network=")[1].split(",")[0]
                            doc += h3(f"Destination IP: {ip_address}")
                        # 生成表格
                        with table():
                            with tr():
                                th("Key")
                                th("Value")
                            if isinstance(value, dict):  # 如果是嵌套字典
                                for sub_key, sub_value in value.items():
                                    with tr():
                                        td(sub_key)
                                        td(sub_value)
                            else:
                                with tr():
                                    td(key)
                                    td(value)
                else:  # 如果数据为空
                    with table():
                        with tr():
                            td(colspan=2, style="text-align: center;")("No data available")

        # 生成 outgoing 表格
        generate_table("Outgoing Traffic", traffic_data["outgoing"])

        # 生成 incoming 表格
        generate_table("Incoming Traffic", traffic_data["incoming"])

    return str(doc)

# 给定的数据结构
data = {
    "wlo1": {
        "outgoing": {
            "dst_network=192.168.12.243/32, protocol=ip": {
                "filter_id": "800::800",
                "limit": 1000,
                "rate": "1Mbps"
            }
        },
        "incoming": {}
    }
}

# 调用函数生成 HTML 文档
html_output = generate_network_interface_html(data)
print(html_output)