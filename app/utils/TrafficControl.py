import subprocess

class TrafficControl:
    def __init__(self, interface):
        self.interface = interface

    def execute_command(self, command):
        """执行 shell 命令并返回输出和错误信息"""
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode(), result.stderr.decode()
        except subprocess.CalledProcessError as e:
            return e.stdout.decode(), e.stderr.decode()

    def setup_tc(self, rate, delay, loss):
        """设置 tc 流量控制，包括带宽、延迟和丢包率"""
        # 清除现有的 tc 规则
        self.execute_command(f"tc qdisc del dev {self.interface} root 2>/dev/null")

        # 添加根排队规则
        command = f"tc qdisc add dev {self.interface} root handle 1: htb default 12"
        stdout, stderr = self.execute_command(command)
        print(stdout, stderr)

        # 添加带宽限制
        command = f"tc class add dev {self.interface} parent 1: classid 1:1 htb rate {rate} ceil {rate}"
        stdout, stderr = self.execute_command(command)
        print(stdout, stderr)

        # 添加默认类
        command = f"tc class add dev {self.interface} parent 1: classid 1:12 htb rate 1mbit"
        stdout, stderr = self.execute_command(command)
        print(stdout, stderr)

        # 添加延迟和丢包
        command = f"tc qdisc add dev {self.interface} parent 1:1 handle 10: netem delay {delay} loss {loss}%"
        stdout, stderr = self.execute_command(command)
        print(stdout, stderr)

        print(f"Traffic control set on {self.interface} with rate {rate}, delay {delay}, loss {loss}%")

if __name__ == "__main__":
    # 要设置的网络接口、带宽、延迟和丢包率
    network_interface = "eth0"  # 替换为你的网络接口
    bandwidth_rate = "1mbit"     # 替换为你想要的带宽限制
    delay_time = "100ms"         # 替换为你想要的延迟时间
    loss_rate = "5"              # 替换为你想要的丢包率（百分比）

    # 创建 TrafficControl 实例并设置流量控制
    tc = TrafficControl(network_interface)
    tc.setup_tc(bandwidth_rate, delay_time, loss_rate)
