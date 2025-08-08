import subprocess

class Shutdown:

    def __init__(self,target_ip:str ,username:str, password:str):
        self.target_ip = target_ip
        self.username = username
        self.password = password

    def shutdown(self):
        # 构建通过net命令发送关机指令的命令
        cmd = [
            "net",
            "rpc",
            "shutdown",
            f"--ipaddress={self.target_ip}",
            f"--user={self.username}",
            f"--timeout=0",
            "--force"  # 强制关闭所有程序
        ]
        
        # 执行命令
        result = subprocess.Popen(
            f"net rpc shutdown --ipaddress={self.target_ip} --user={self.username}%{self.password}",
            shell=True,
        )
# if __name__ == "__main__":
#     # 配置Windows电脑信息
#     WINDOWS_IP = "192.168.0.2"  # Windows电脑IP
#     WINDOWS_USER = "test"       # Windows管理员用户名
#     WINDOWS_PASSWORD = "test"   # Windows管理员密码
    
#     shutdown(WINDOWS_IP, WINDOWS_USER, WINDOWS_PASSWORD)
