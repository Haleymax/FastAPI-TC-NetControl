from dominate import document
from dominate.tags import style, div, h1, h2, h3, table, th, tr, td, br, hr

css_style = """
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
    """

class Template:
    def __init__(self, data, title="Network Data"):
        self.data = data
        self.doc = document(title=title)

    def generate(self):
        self.doc.head += style(css_style)
        with self.doc.body:
            if not self.data:
                h1("No Data Available")
                return str(self.doc)

            for interface, traffic in self.data.items():
                with div():
                    h1(f"Network Interface: {interface}")
                    if isinstance(traffic, dict):
                        if 'outgoing' in traffic and isinstance(traffic['outgoing'], dict):
                            h2("Outgoing")
                            self.generate_data_table(traffic['outgoing'])

                        br()
                        br()
                        hr()
                        if 'incoming' in traffic and isinstance(traffic['incoming'], dict):
                            h2("Incoming")
                            self.generate_data_table(traffic['incoming'])
        return str(self.doc)

    def generate_data_table(self, table_data):
        if not table_data:
            h3("No Data Available")
            return

        for device, data in table_data.items():
            if "dst_network" in device:
                try:
                    device_ip = device.split("dst_network=")[1].split(",")[0]
                    h3(device_ip)
                    with table():
                        with tr():
                            th("Parameter")
                            th("Value")
                        if isinstance(data, dict):
                            for sub_key, sub_value in data.items():
                                with tr():
                                    td(sub_key)
                                    td(sub_value)
                        else:
                            with tr():
                                td("No Data Available")
                                td("")
                except Exception as e:
                    h3(f"Error parsing device: {e}")
                    continue
            br()