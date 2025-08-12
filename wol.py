import socket

class Wake:
    def __init__(self, mac_address: str, broadcast_ip: str = "255.255.255.255"):
        self.mac_address = mac_address
        self.broadcast_ip = broadcast_ip  # 广播地址，而非目标设备IP

    def wake_on_lan(self, port: int = 9):
        """通过广播发送魔术包唤醒设备"""
        try:
            # 处理MAC地址：去除分隔符并转换为字节流
            mac_clean = self.mac_address.replace(':', '').replace('-', '')
            if len(mac_clean) != 12:
                raise ValueError(f"无效的MAC地址: {self.mac_address}，正确格式应为AA:BB:CC:DD:EE:FF")
            
            mac_bytes = bytes.fromhex(mac_clean)
            
            # 构建魔术包：6字节0xFF + 16次MAC地址字节流（共102字节）
            magic_packet = b'\xff' * 6 + mac_bytes * 16
            
            # 创建UDP套接字并发送广播
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(magic_packet, (self.broadcast_ip, port))
            
            print(f"已向广播地址 {self.broadcast_ip} 发送WOL魔术包（目标MAC: {self.mac_address}）")
            
        except Exception as e:
            raise RuntimeError(f"发送WOL魔术包失败: {str(e)}")